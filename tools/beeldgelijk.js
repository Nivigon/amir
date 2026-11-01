#!/usr/bin/env node
// Beeldgelijk: kijkt na of een wijziging aan de tekencode het beeld echt niet verandert.
//
// Twee potjes lopen nooit gelijk (het spel ademt op de echte klok en trekt toeval), dus twee
// runs vergelijken heeft geen zin. Daarom zet dit script een vlag in het spel waarmee de oude
// en de nieuwe tekenweg naast elkaar staan, en tekent het hetzelfde beeld twee keer in
// hetzelfde potje: een keer met de vlag uit, een keer met de vlag aan. Daartussen verandert
// niets (de klok staat stil, het spel staat op pauze, en de toevalsreeks begint weer vooraan),
// dus elk pixelverschil komt van de wijziging zelf.
//
//   node tools/beeldgelijk.js --vlag LAGFIX            de vaste reeks levels
//   node tools/beeldgelijk.js --vlag LAGFIX "Test 27"  alleen dit level
//   node tools/beeldgelijk.js --vlag LAGFIX --plekken -300,-2000
//   node tools/beeldgelijk.js --vlag LAGFIX --breed 852 --hoog 393
//
// 'gelijk' op elke plek betekent: de wijziging verandert geen enkele pixel. Nodig: Node en
// Playwright met Chromium.
'use strict';
const fs = require('fs'), path = require('path'), http = require('http');
function laadPlaywright(){
  const plekken = ['playwright', '/opt/node-tools/node_modules/playwright',
                   path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) {} }
  console.error('beeldgelijk: Playwright ontbreekt (npm i -g playwright)'); process.exit(2);
}
const { chromium } = laadPlaywright();
const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const breed = Number(opt('--breed', 1280)), hoog = Number(opt('--hoog', 720));
const plekken = (opt('--plekken', '-300,-1800,-3600,-6000')).split(',').map(Number);
const vlag = opt('--vlag', null);
if (!vlag){ console.error('beeldgelijk: geef de vlag mee, bijvoorbeeld --vlag LAGFIX'); process.exit(2); }
const SCHAKELS = ['--breed', '--hoog', '--plekken', '--vlag'];
const namen = args.filter(a => !a.startsWith('--') && !SCHAKELS.includes(args[args.indexOf(a) - 1]));
const STANDAARD = ['Valse Koning 1', 'Valse Koning 3', 'Valse Koning 4', 'Valse Koning 5', 'Valse Koning 6',
                   'Valse Koning 8', 'Test 1', 'Test 10', 'Test 27', 'Test 45', 'Baboon 1', 'Baboon 4'];
const LEVELS = namen.length ? namen : STANDAARD;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg',
  '.webmanifest': 'application/manifest+json', '.css': 'text/css' };
function server(){
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT)){ res.writeHead(403); res.end(); return; }
      fs.readFile(p, (e, d) => {
        if (e){ res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
        res.end(d);
      });
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}
async function start(){
  try { return await chromium.launch(); } catch (e){
    const map = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
    const k = fs.existsSync(map) ? fs.readdirSync(map).filter(d => /^chromium-\d+$/.test(d)).sort().reverse() : [];
    for (const d of k){ const exe = path.join(map, d, 'chrome-linux', 'chrome'); if (fs.existsSync(exe)) return chromium.launch({ executablePath: exe }); }
    throw e;
  }
}
// Dit draait in de pagina, voor het spel: de beeldlus komt in onze hand.
function neemLusOver(){
  let z = 123456789;
  Math.random = () => { z ^= z << 13; z ^= z >>> 17; z ^= z << 5; z |= 0; return ((z >>> 0) % 1000000) / 1000000; };
  window.__zaai = () => { z = 123456789; };
  window.__n = 0; window.__wacht = null; window.__eigen = false;
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => {
    if (window.__eigen){ window.__wacht = cb; return 0; }         // wij stappen zelf
    return raf(t => { window.__n++; cb(t); });
  };
  // zelf een beeld verder: altijd met dezelfde tijdstempel, dus dt blijft 0
  window.__stap = k => {
    for (let i = 0; i < k; i++){
      const cb = window.__wacht; if (!cb) return i;
      window.__wacht = null; window.__n++; cb(window.__klok);
    }
    return k;
  };
  // De ring om de zon, het gras in de voorgrond en de puls op een zegel ademen op de echte
  // klok. Die zetten we stil zodra het level loopt, niet eerder: de laadpoort en de lichtkaart
  // rekenen met een tijdbudget en zouden met een stilstaande klok al hun werk in een beeld doen.
  window.__bevries = () => {
    window.__klok = performance.now();
    performance.now = () => window.__klok;
    window.__eigen = true;
  };
}
// Een kopie van het canvas, zodat twee beelden naast elkaar te leggen zijn.
function beeldPak(){
  const c = document.getElementById('c');
  return c.getContext('2d').getImageData(0, 0, c.width, c.height);
}
(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await start();
  console.log('beeldgelijk  ' + breed + 'x' + hoog + '  vlag ' + vlag
              + '  bevroren op x = ' + plekken.join(', '));
  let stuk = 0;
  for (const naam of LEVELS){
    const page = await browser.newPage({ viewport: { width: breed, height: hoog } });
    const fouten = [];
    page.on('pageerror', e => fouten.push(e.message));
    await page.addInitScript(neemLusOver);
    await page.goto(url);
    await page.waitForFunction(() => typeof setLevel === 'function');
    await page.waitForTimeout(2500);
    const echt = await page.evaluate(d => {
      let lijst = null, i = 0;
      for (const l of [VK_LEVELS, TEST_LEVELS, BAB_LEVELS, STAD_LEVELS, OAK_LEVELS])
        l.forEach((def, j) => { if (!lijst && def.name.toLowerCase().includes(d.toLowerCase())){ lijst = l; i = j; } });
      if (!lijst) return null;
      setLevel(i, lijst); beginPlay('medium'); return level.name;
    }, naam);
    if (!echt){ console.log(naam.padEnd(32) + 'geen level'); await page.close(); continue; }
    await page.waitForFunction(() => !laadWacht, { timeout: 40000 }).catch(() => {});
    await page.waitForTimeout(600);                  // de lichtkaart en de bak-rij afmaken
    await page.evaluate(() => { window.__bevries(); });
    const uit = [];
    for (const px of plekken){
      await page.evaluate(x => { paused = true; world = x; ph = 0; pvh = 0; onGround = true; shake = 0; }, px);
      {
        const r = await page.evaluate(([pak, v]) => {
          const pakF = eval('(' + pak + ')');
          const meet = aan => { window[v] = aan; window.__zaai(); window.__stap(3); return pakF(); };
          const a = meet(false), b = meet(true);
          let max = 0, n = 0;
          for (let i = 0; i < a.data.length; i++){
            const d = Math.abs(a.data[i] - b.data[i]);
            if (d){ n++; if (d > max) max = d; }
          }
          return { max, n, tot: a.data.length / 4 };
        }, [beeldPak.toString(), vlag]);
        if (r.max > 0) stuk++;
        uit.push(r.max === 0 ? 'gelijk' : ('max ' + r.max + ' op ' + r.n + ' bytes'));
      }
    }
    console.log(echt.slice(0, 30).padEnd(32) + uit.join('  ') + (fouten.length ? '   FOUT: ' + fouten[0] : ''));
    await page.close();
  }
  await browser.close(); srv.close();
  if (stuk){ console.log('\n' + stuk + ' plek(ken) verschillen: de wijziging verandert het beeld.'); process.exitCode = 1; }
  else console.log('\nAlle plekken pixel voor pixel gelijk.');
})();
