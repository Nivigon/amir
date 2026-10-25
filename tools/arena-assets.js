#!/usr/bin/env node
// De arena-download nameten: welke bestanden vraagt de Arena modus van de sandbox echt op, en staan
// die allemaal in de arena-set van offline-assets.json (manifest.delen.arena, uit gen-offline-manifest.py)?
//
// Hij laadt het spel in Chromium (zonder service worker, zodat elk verzoek zichtbaar is), opent de
// Arena modus met alle soorten aan en op een hoog tempo, zet Amir onsterfelijk en laat het een
// poos lopen. Daarna vergelijkt hij elk opgevraagd bestand (png, jpg, mp3, json) met de arena-set:
//
//   FOUT   het spel vroeg een bestand dat niet in de arena-set staat (offline zou het ontbreken)
//   LET OP een bestand uit de lijst gaf 404 (dan klopt het spel of de lijst niet)
//
//   node tools/arena-assets.js                 nameten, standaard 45 seconden spelen
//   node tools/arena-assets.js --duur 90       langer spelen
//   node tools/arena-assets.js --toon          ook alle opgevraagde bestanden tonen
//   node tools/arena-assets.js --beeld klein   de kleine spriteset (standaard: allebei, na elkaar)
//   node tools/arena-assets.js --soorten schildman,bandiet
//                                              alleen deze soorten aan (sleutels uit SB_ARENA_SOORTEN); de
//                                              verwachting is dan de basis plus die soorten, zoals de knop
//                                              Alleen de Arena modus ze ophaalt (standaard: alle soorten)
//
// Nodig: Node en Playwright (npm i -g playwright) met Chromium.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('arena-assets: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const duur = Number(opt('--duur', 45));
const toon = args.includes('--toon');
const beelden = opt('--beeld', null) ? [opt('--beeld')] : ['groot', 'klein'];
const soorten = opt('--soorten', null) ? opt('--soorten').split(',') : null;   // null: alle

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

// Dit draait in de pagina: de arena open, alles aan, snel, onsterfelijk, en starten.
function arenaOpzet(soorten){
  startSandbox(true);
  const c = sbArenaCfg;
  c.modus = 'stroom'; c.onst = true; c.kal.aan = true; c.kal.stroom = 3;
  for (const s of SB_ARENA_SOORTEN){ const p = c.per[s.k]; p.aan = !soorten || soorten.includes(s.k); p.bij = p.aan; p.van = 1; p.tot = 1; p.max = 3; p.t = 0; }
  // de gedragsknoppen die een eigen set laden: de elite-garde en de dolk
  if (!soorten || soorten.includes('bandiet')) for (const id of ['sbanelite', 'sbandolk', 'sbanduin']){ const b = document.getElementById(id); if (b && !b.classList.contains('on')) b.click(); }
  sbWizSluit();
  sbArenaStart(false);
}

async function meet(browser, poort, beeld, manifest){
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, serviceWorkers: 'block' });
  const page = await context.newPage();
  await page.addInitScript((b) => { try { localStorage.setItem('amir.beeld', b); } catch (e) {} }, beeld);
  const gevraagd = new Set(), vooraf = new Set(), vierNulVier = new Set(), console_ = [];
  let arenaAan = false;                              // vanaf de start van de arena; wat eerder komt is het opstarten en het menu
  page.on('response', r => {
    const u = new URL(r.url());
    if (u.hostname !== '127.0.0.1') return;
    const rel = decodeURIComponent(u.pathname.replace(/^\//, ''));
    if (!/\.(png|jpe?g|mp3|json)$/i.test(rel) || rel === 'offline-assets.json') return;
    gevraagd.add(rel);
    if (!arenaAan) vooraf.add(rel);
    if (r.status() === 404) vierNulVier.add(rel);
  });
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console_.push(m.text()); });
  await page.goto(`http://127.0.0.1:${poort}/amir-king-of-africa.html`);
  await page.waitForFunction(() => typeof startSandbox === 'function' && typeof sbArenaCfg !== 'undefined');
  const beeldNu = await page.evaluate(() => BEELD);
  await page.waitForTimeout(3000);                   // het menu laadt zijn levelkaartje; dat hoort niet bij de arena
  arenaAan = true;
  await page.evaluate(arenaOpzet, soorten);
  await page.waitForTimeout(duur * 1000);
  // ook alle muziek: in de sandbox kiest de speler zelf een nummer
  await page.evaluate(() => { for (const k in MUZIEK){ const a = new Audio(); a.preload = 'auto'; a.src = MUZIEK[k].src || MUZIEK[k]; a.load(); } });
  await page.waitForTimeout(3000);
  const stand = await page.evaluate(() => ({ kills: sbArenaCfg.kills, t: Math.round(sbArenaCfg.t0),
    levend: [scorps, snakes, panthers, hyenas, bandieten, schildmannen, meelmannen, kooimannen, fosforSlangen].map(l => l.length) }));
  await context.close();

  // dezelfde keuze als voorSet in sw.js: een toestel haalt van elke familie met een kleine versie
  // maar een van de twee binnen, dus wat het spel in die set opvraagt moet ook in die helft staan
  const kleinVan = new Set((manifest.assets).filter(r => r.startsWith('klein/')).map(r => r.slice('klein/'.length)));
  const inSet = r => beeldNu === 'groot' ? !r.startsWith('klein/') : (r.startsWith('klein/') || !kleinVan.has(r));
  // de basis plus de soorten die aan staan, zoals voorDeel in sw.js
  const keuze = soorten || Object.keys(manifest.soorten || {});
  const lijst = (manifest.delen && manifest.delen.arena || []).slice();
  for (const k of keuze){ if (!(manifest.soorten || {})[k]) console.log('LET OP  onbekende soort: ' + k); else lijst.push(...manifest.soorten[k]); }
  const set = new Set(lijst.filter(inSet));
  const alles = new Set(manifest.assets);
  // Een vijand die alleen voor de arena-start opgevraagd is, laadt het menu voor het gekozen levelkaartje
  // (laadLevel in setLevel; bij het opstarten de nieuwste test). Dat is niet de arena: offline ontbreekt hij
  // zonder gevolgen, want dat level wordt niet gespeeld. LET OP in plaats van FOUT.
  const menuLaad = r => vooraf.has(r) && /^(klein\/)?enemies\//.test(r) && !/\.(json|mp3)$/i.test(r);
  const mist = [...gevraagd].filter(r => !set.has(r) && !menuLaad(r)).sort();
  const menuMist = [...gevraagd].filter(r => !set.has(r) && menuLaad(r)).sort();
  const nietInLijst = mist.filter(r => !alles.has(r));
  console.log(`\n== beeld ${beeld} (het spel speelt ${beeldNu}), soorten ${soorten ? soorten.join(',') : 'alle'}: ${gevraagd.size} bestanden opgevraagd in ${stand.t} s, ${stand.kills} verslagen, levend ${stand.levend.join('/')}`);
  if (toon) for (const r of [...gevraagd].sort()) console.log('   ' + r);
  for (const r of [...vierNulVier].sort()) console.log('LET OP  404: ' + r);
  if (menuMist.length) console.log('LET OP  ' + menuMist.length + ' bestanden laadt het menu voor het gekozen levelkaartje, niet de arena (bijvoorbeeld ' + menuMist[0] + '); offline ontbreken die zonder gevolgen');
  for (const r of mist) console.log('FOUT    niet in de arena-set voor ' + beeldNu + ': ' + r + (nietInLijst.includes(r) ? ' (ook niet in de hele lijst)' : kleinVan.has(r) ? ' (er is een kleine versie, maar het spel vraagt de grote)' : ''));
  const meldingen = console_.filter(t => /ontbreekt|404|Failed/.test(t));
  for (const t of meldingen.slice(0, 10)) console.log('console: ' + t);
  return mist.length + vierNulVier.size;
}


(async () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'offline-assets.json'), 'utf8'));
  const s = await server();
  const poort = s.address().port;
  const browser = await start();
  let fouten = 0;
  try {
    for (const b of beelden) fouten += await meet(browser, poort, b, manifest);
  } finally {
    await browser.close(); s.close();
  }
  console.log(fouten ? `\n${fouten} FOUT` : '\nOK: alles wat de arena opvraagt staat in de arena-set');
  process.exit(fouten ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
