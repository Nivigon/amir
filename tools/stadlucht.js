#!/usr/bin/env node
// stadlucht.js: lucht tussen de huizen van de stad nameten.
//
// Met achterTot houden de rijen huizen in de verte op een grens op, en links daarvan is lucht boven de savanne
// (Ishmul). Die rand mag op het scherm nooit rechts van de linkermuur van het meest linkse huis aan de straat liggen:
// dan zie je boven een laag huis blauwe lucht waar de stad hoort (zo stond het in Ishmul, op de brug). Dit script laadt
// elk level met stad.achterTot (en de Co-op maps) in Chromium, loopt de camera over de hele straat en meldt FOUT op elke
// plek waar de verte te vroeg ophoudt. En FOUT als een huis in de verte in een keer verdwijnt of verschijnt: de rand van
// een rij mag per stap niet verder springen dan de camera schuift (elke rij houdt op bij een vast huis, stadAchterRanden).
//
//   node tools/stadlucht.js                 alle levels met achterTot, op 1280x720, 852x393, 1440x620 en 1920x1080
//   node tools/stadlucht.js Ishmul          alleen de levels waarvan de naam dit bevat
//   node tools/stadlucht.js level.json      een level uit de Maker (Spel-JSON)
//   node tools/stadlucht.js --schermen 1280x720
//
// Draai hem na een wijziging aan stadAchter, aan de achterrijen (STAD.rijen) of aan een level met achterTot.
// Nodig: Node en Playwright (npm i -g playwright) met Chromium. Het script start zelf een webserver.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('stadlucht: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const losse = [];
for (let i = 0; i < args.length; i++){
  if (args[i] === '--schermen'){ i++; continue; }
  if (!args[i].startsWith('--')) losse.push(args[i]);
}
const doel = losse[0] || '';
const def = doel.endsWith('.json') ? JSON.parse(fs.readFileSync(doel, 'utf8')) : null;
const schermen = opt('--schermen', '1280x720,852x393,1440x620,1920x1080').split(',').map(s => s.split('x').map(Number));

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp3': 'audio/mpeg', '.css': 'text/css' };
function server(){
  return new Promise(res => {
    const srv = http.createServer((req, rep) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      fs.readFile(p, (e, d) => {
        if (e){ rep.statusCode = 404; rep.end('nee'); return; }
        rep.setHeader('Content-Type', TYPES[path.extname(p).toLowerCase()] || 'application/octet-stream');
        rep.end(d);
      });
    }).listen(0, '127.0.0.1', () => res(srv));
  });
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await chromium.launch();
  let fouten = 0, gemeten = 0;
  for (const [w, h] of schermen){
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    page.on('pageerror', e => console.log('  fout in de pagina: ' + e.message));
    await page.goto(url);
    await page.waitForFunction(() => typeof setLevel === 'function' && typeof MP_ISHMUL_LEVEL !== 'undefined');
    // welke levels: alles met stad.achterTot (in een episode, een testreeks of een Co-op map)
    const namen = await page.evaluate(([doel, def]) => {
      if (def) return [def.name || 'level.json'];
      const lijsten = [KUM_LEVELS, TEST_LEVELS, STOK_LEVELS, RW_LEVELS, TUT_LEVELS, BAB_LEVELS, MUR_LEVELS, STAD_LEVELS, OAK_LEVELS,
                       BEL_LEVELS, GP_LEVELS, RIV_LEVELS, COOPEP_LEVELS, COOPEP2_LEVELS, [MP_COOP_LEVEL, MP_ISHMUL_LEVEL]];
      const uit = [];
      for (const l of lijsten) for (const d of l)
        if (d.stad && d.stad.achterTot != null && (!doel || d.name.toLowerCase().includes(doel.toLowerCase())) && !uit.includes(d.name)) uit.push(d.name);
      return uit;
    }, [doel, def]);
    if (!namen.length){ console.log('geen level met achterTot gevonden' + (doel ? ': ' + doel : '')); break; }
    for (const naam of namen){
      const span = await page.evaluate(([naam, def]) => {
        let d = def;
        if (!d){
          const lijsten = [KUM_LEVELS, TEST_LEVELS, STOK_LEVELS, RW_LEVELS, TUT_LEVELS, BAB_LEVELS, MUR_LEVELS, STAD_LEVELS, OAK_LEVELS,
                           BEL_LEVELS, GP_LEVELS, RIV_LEVELS, COOPEP_LEVELS, COOPEP2_LEVELS, [MP_COOP_LEVEL, MP_ISHMUL_LEVEL]];
          for (const l of lijsten) for (const q of l) if (!d && q.name === naam) d = q;
        }
        setLevel(0, [d]); beginPlay('medium');
        const sc = nowScale(); let l = 1e9, r = -1e9;
        for (const g of level.stad.gevels || []){ const m = stadGevelMaat(g, sc); l = Math.min(l, m.left); r = Math.max(r, m.right); }
        return [l, r];
      }, [naam, def]);
      await page.waitForFunction(() => !laadWacht && stadKlaar('gevel'), null, { timeout: 90000 });
      // de camera van rechts van de huizen tot ver links ervan; per plek een paar beelden laten tekenen
      const slecht = [], sprong = []; let vorig = null;
      for (let x = span[1] + w; x >= span[0] - w; x -= 40){
        const r = await page.evaluate(async x => {
          world = x;
          await new Promise(k => requestAnimationFrame(() => requestAnimationFrame(k)));
          world = x;
          await new Promise(k => requestAnimationFrame(() => requestAnimationFrame(k)));
          // de huizen aan de straat op het scherm, met de camera van dat beeld (niet Amir: de camera kijkt vooruit) en de zoom:
          // de verte staat buiten de zoom, de huizen aan de straat erin
          const sc = nowScale(), huizen = (level.stad.gevels || []).map(g => { const m = stadGevelMaat(g, sc); const z = stadAchterZoom; return [W / 2 + (m.left - stadAchterCam) * z, W / 2 + (m.right - stadAchterCam) * z]; });
          const links = Math.min(...huizen.map(h => h[0])), rand = stadAchterRand;
          // tussen de linkermuur van de stad en de rand van de verte: elk stuk in beeld dat geen huis aan de straat dekt is lucht
          let lucht = 0;
          if (rand != null) for (let px = Math.max(0, Math.ceil(links)); px < Math.min(W, rand - 1); px++)
            if (!huizen.some(h => px >= h[0] && px <= h[1])) lucht++;
          // per rij de linkerrand: de linkerkant van het eerste huis (gx), dat met zijn rij meeschuift (stadAchterRanden)
          const randen = stadAchterRijen.map(q => q.gx);
          return { rand, links, lucht, x: Math.round(stadAchterCam), cam: stadAchterCam, z: stadAchterZoom, randen };
        }, x);
        gemeten++;
        if (r.lucht > 1) slecht.push(r);
        // een huis in de verte dat in een keer verdwijnt of verschijnt: de rand van een rij springt verder dan de camera
        // en de huizen aan de straat in die stap konden schuiven
        if (vorig && vorig.randen.length === r.randen.length){
          const mag = Math.abs(r.cam - vorig.cam) * Math.max(1, r.z) + 24;
          r.randen.forEach((e, i) => { if (Math.abs(e - vorig.randen[i]) > mag) sprong.push({ x: r.x, rij: i, van: vorig.randen[i], naar: e }); });
        }
        vorig = r;
      }
      if (sprong.length){
        fouten += sprong.length;
        const s = sprong[0];
        console.log('FOUT  ' + naam + ' (' + w + 'x' + h + '): op ' + sprong.length + ' plekken springt een huis in de verte, bv. camera op ' +
                    s.x + ', rij ' + s.rij + ': de rand van ' + Math.round(s.van) + ' naar ' + Math.round(s.naar));
      }
      if (slecht.length){
        fouten += slecht.length;
        const s = slecht[0];
        console.log('FOUT  ' + naam + ' (' + w + 'x' + h + '): op ' + slecht.length + ' plekken lucht tussen de huizen, bv. camera op ' +
                    s.x + ': ' + s.lucht + ' px lucht, de verte houdt op ' + Math.round(s.rand) + ', het meest linkse huis begint op ' + Math.round(s.links));
      } else if (!sprong.length) console.log('OK    ' + naam + ' (' + w + 'x' + h + ')');
    }
    await page.close();
  }
  await browser.close(); srv.close();
  console.log(gemeten + ' plekken gemeten, ' + (fouten ? fouten + ' fouten' : 'nergens lucht tussen de huizen en geen huis dat verspringt'));
  process.exit(fouten ? 1 : 0);
})();
