#!/usr/bin/env node
// De bouwertest: kijkt na of de bouwer een level heel laat.
//
// Voor elk level uit de HTML (De Runen, De Vorst en de testlevels) doet hij wat een speler doet die het
// level in de bouwer opent en meteen weer opslaat: readLevel, syncLevel, en de tekst die eruit
// komt weer inlezen. Wat er dan anders is dan bij het origineel, is de bouwer kwijtgeraakt of
// veranderd. Hij meldt per level de velden die niet gelijk bleven, en wat er in de console
// stond. Hij verandert niets aan de levels.
//
//   node tools/bouwertest.js              alle levels
//   node tools/bouwertest.js "Test 4"     alleen de levels waarvan de naam dit bevat
//   --shots map                           daarna een schermafdruk van de bouwer, boven en onder de grond
//
// Nodig: Node en Playwright, net als de speelrobot. Hij start zelf een webserver.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('bouwertest: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const shots = opt('--shots', null);
const filter = args.find((a, i) => !a.startsWith('--') && args[i - 1] !== '--shots') || '';

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json', '.css': 'text/css' };
function server(){
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT)){ res.writeHead(403); res.end(); return; }
      fs.readFile(p, (err, data) => {
        if (err){ res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
        res.end(data);
      });
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}
async function start(){
  try { return await chromium.launch(); }
  catch (e){
    const map = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
    const kandidaten = fs.existsSync(map) ? fs.readdirSync(map).filter(d => /^chromium-\d+$/.test(d)).sort().reverse() : [];
    for (const d of kandidaten){
      const exe = path.join(map, d, 'chrome-linux', 'chrome');
      if (fs.existsSync(exe)) return chromium.launch({ executablePath: exe });
    }
    throw e;
  }
}

(async () => {
  const srv = await server();
  const browser = await start();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const console_ = [];
  // een lettertype van buiten dat niet laadt (geen internet) telt niet mee, een 404 hier wel
  page.on('console', m => { if (m.type() === 'error' && !/ERR_CERT|ERR_NAME|ERR_INTERNET|ERR_PROXY|ERR_TUNNEL/.test(m.text())) console_.push(m.text()); });
  page.on('pageerror', e => console_.push('fout: ' + e.message));
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof readLevel === 'function' && typeof TEST_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);                 // de plaatjes: schoonLevel rekent met hun maten

  const uitslag = await page.evaluate(filter => {
    // bron is de ruwe tekst waar het level uit kwam: die hoort er niet bij als je vergelijkt
    // de bouwer zet lijsten op volgorde van x: dat is geen verschil
    const vorm = lv => {
      const o = JSON.parse(JSON.stringify(lv, (k, v) => k === 'bron' ? undefined : v));
      for (const k of Object.keys(o))
        if (Array.isArray(o[k]) && o[k].every(q => q && typeof q.x === 'number'))
          o[k] = o[k].map(q => JSON.stringify(q)).sort();
      return o;
    };
    const uit = [];
    // elke episode die er is: De Runen, De Vorst (als die er staat) en de testlevels
    const reeksen = [POORT_LEVELS, TEST_LEVELS, BAB_LEVELS];
    for (const lijst of reeksen){
      for (const def of lijst){
        if (filter && !def.name.toLowerCase().includes(filter.toLowerCase())) continue;
        const voor = vorm(readLevel(JSON.stringify(def)));
        level = readLevel(JSON.stringify(def));
        syncLevel();
        const na = vorm(readLevel(bjson.value));
        const anders = [];
        for (const k of new Set(Object.keys(voor).concat(Object.keys(na))))
          if (JSON.stringify(voor[k]) !== JSON.stringify(na[k])) anders.push(k);
        uit.push({ naam: def.name, anders });
      }
    }
    return uit;
  }, filter);

  let fout = 0;
  for (const u of uitslag){
    if (u.anders.length){ fout++; console.log('FOUT  ' + u.naam + ': kwijt of veranderd: ' + u.anders.join(', ')); }
    else console.log('goed  ' + u.naam);
  }

  if (shots){
    fs.mkdirSync(shots, { recursive: true });
    await page.evaluate(() => { const b = document.getElementById('btnbuild'); if (b) b.click(); });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(shots, 'bouwer.png') });
  }

  if (console_.length){ console.log('console:'); for (const c of console_) console.log('  ' + c); }
  console.log(uitslag.length + ' levels, ' + fout + ' met verlies');
  await browser.close(); srv.close();
  process.exit(fout || console_.length ? 1 : 0);
})();
