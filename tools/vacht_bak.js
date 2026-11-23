#!/usr/bin/env node
'use strict';
// Bakt de maskers voor de outfits van de stoktribe (VACHT, VACHT_BAK): per frame van Amir dat een stokspeler kan tonen een
// plaatje met dezelfde naam in karakters/amir_vacht/, rood de broek (0 tot 255) en groen de vacht, zwart en ondoorzichtig.
// Het rekenwerk is precies dat van het spel: het script laadt de HTML in Chromium en roept broekMaskers aan (met een outfit
// met broek en vacht; de maskers hangen niet van de outfit af). Een masker is alleen de rechthoek om broek en vacht;
// lijst.json geeft per frame waar die zit: [x, y, breedte, hoogte, de breedte van het hele frame].
//
//   node tools/vacht_bak.js                 alle mappen (zie MAPPEN)
//   node tools/vacht_bak.js --alleen rol    alleen de frames waarvan het pad dit bevat (de lijst blijft compleet)
//
// Aan het eind pakt tools/vacht_bak_pak.py de maskers in (een palet, exact); daarvoor zijn Python, numpy en Pillow nodig.
// Draai het opnieuw na nieuwe of andere frames in die mappen, of na een wijziging aan vachtMasker, broekMaskers, BROEK of
// VACHT (zaad, groei, eiland), en daarna tools/gen-offline-manifest.py.
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('vacht_bak: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();
const ROOT = path.dirname(__dirname);
const BRON = path.join(ROOT, 'karakters/amir');
const DOEL = path.join(ROOT, 'karakters/amir_vacht');
// wat een speler met de stokken kan tonen: zijn stokken (ook de stokken uit de winkel), de lage zwaai, de
// bewegingen (springen, rollen, bukken, sluipen, rennen, de trap) en de idle. De speeraanvallen en de skins niet.
const MAPPEN = ['stokken', 'stokken_goud', 'stokken_klauw', 'aanval/lowsweep', 'beweging', 'idle'];
const args = process.argv.slice(2);
const alleen = (() => { const i = args.indexOf('--alleen'); return i >= 0 ? args[i + 1] : null; })();

function frames(){
  const uit = [];
  const loop = d => {
    for (const e of fs.readdirSync(path.join(BRON, d), { withFileTypes: true })){
      const r = d + '/' + e.name;
      if (e.isDirectory()){ if (e.name !== 'bron') loop(r); }
      else if (e.name.endsWith('.png')) uit.push(r);
    }
  };
  for (const m of MAPPEN) loop(m);
  return uit.sort();
}

function server(){
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT)){ res.writeHead(403); res.end(); return; }
      fs.readFile(p, (err, data) => {
        if (err){ res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': p.endsWith('.html') ? 'text/html' : p.endsWith('.png') ? 'image/png' : 'application/octet-stream' });
        res.end(data);
      });
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}

(async () => {
  const lijst = frames();
  const s = await server();
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('pageerror', e => console.log('fout in de pagina: ' + e.message));
  await page.goto('http://127.0.0.1:' + s.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof broekMaskers === 'function' && typeof vachtKl === 'function');
  // het opstartlevel kan een skin hebben (SKIN): dan zou src van een Amir-frame naar die skin gaan, en bakten we het verkeerde frame
  await page.evaluate(() => skinZet(null));
  const oud = fs.existsSync(path.join(DOEL, 'lijst.json')) ? JSON.parse(fs.readFileSync(path.join(DOEL, 'lijst.json'), 'utf8')) : {};
  const nieuw = {};
  if (alleen) for (const r in oud) if (!r.includes(alleen)) nieuw[r] = oud[r];
  let n = 0, leeg = 0, bytes = 0;
  const geschreven = [];
  for (const rel of lijst){
    if (alleen && !rel.includes(alleen)) continue;
    const uitk = await page.evaluate(async src => {
      const im = new Image(); im.src = src;
      await im.decode();
      const w = im.naturalWidth, h = im.naturalHeight;
      const c = document.createElement('canvas'); c.width = w; c.height = h;
      const g = c.getContext('2d', { willReadFrequently: true });
      g.drawImage(im, 0, 0);
      const p = g.getImageData(0, 0, w, h).data;
      const { mk, vm } = broekMaskers(p, w, h, vachtKl('firedancer'));
      const d = g.createImageData(w, h), q = d.data;
      let x0 = w, y0 = h, x1 = -1, y1 = -1;
      for (let j = 0, i = 0; j < w * h; j++, i += 4){
        const r = Math.round(mk[j] * 255), gr = vm && vm[j] ? 255 : 0;
        q[i] = r; q[i + 1] = gr; q[i + 2] = 0; q[i + 3] = 255;
        if (r || gr){ const x = j % w, y = (j - x) / w; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      }
      if (x1 < 0) return null;
      // alleen de rechthoek om broek en vacht: kleiner, en het spel kleurt dan ook alleen dat stuk
      g.putImageData(d, 0, 0);
      const k = document.createElement('canvas'); k.width = x1 - x0 + 1; k.height = y1 - y0 + 1;
      k.getContext('2d').drawImage(c, x0, y0, k.width, k.height, 0, 0, k.width, k.height);
      return { url: k.toDataURL('image/png'), vak: [x0, y0, k.width, k.height, w] };
    }, 'karakters/amir/' + rel);
    const uit = path.join(DOEL, rel);
    if (!uitk){ leeg++; if (fs.existsSync(uit)) fs.unlinkSync(uit); continue; }
    const buf = Buffer.from(uitk.url.split(',')[1], 'base64');
    fs.mkdirSync(path.dirname(uit), { recursive: true });
    fs.writeFileSync(uit, buf);
    nieuw[rel] = uitk.vak; n++; geschreven.push(uit);
  }
  fs.mkdirSync(DOEL, { recursive: true });
  const gesorteerd = {};
  for (const r of Object.keys(nieuw).sort()) gesorteerd[r] = nieuw[r];
  fs.writeFileSync(path.join(DOEL, 'lijst.json'), JSON.stringify(gesorteerd).replace(/\],"/g, '],\n"') + '\n');
  // kleiner inpakken: een palet in plaats van RGBA (exact, tools/vacht_bak_pak.py)
  if (geschreven.length) require('child_process').execFileSync('python3', [path.join(__dirname, 'vacht_bak_pak.py'), ...geschreven], { stdio: 'inherit' });
  bytes = geschreven.reduce((s, f) => s + fs.statSync(f).size, 0);
  console.log(n + ' maskers gebakken (' + Math.round(bytes / 1024) + ' kB), ' + leeg + ' frames zonder broek of vacht; lijst.json: ' + Object.keys(nieuw).length + ' frames');
  await browser.close();
  s.close();
})();
