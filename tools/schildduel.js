#!/usr/bin/env node
// Het schildduel: speelt het gevecht tegen de schildbandiet in het echte spel, met een paar
// speelstijlen, en meet hoe het gevecht loopt. Om de timing af te stemmen: hoe lang duurt het,
// hoe vaak raakt hij Amir, en in welk stuk van zijn aanval raakt Amir hem.
//
//   node tools/schildduel.js                 alle stijlen, elk een paar keer
//   node tools/schildduel.js geduld          alleen deze stijl
//   --keer 4   --max 40   --reactie 0.25    (reactietijd in seconden, voor de stijlen die reageren)
//   --spoor                                  per beeld de staat van de schildbandiet en Amir
//   --fotos map                              schermafdrukken op vaste frames van de sprong (het beeld staat dan stil)
//   --breed 1280 --hoog 720                  het scherm (standaard 960x540, dat is sneller; Amir is daar kleiner,
//                                            dus ontwijken is er makkelijker dan op een laptop)
//
// De stijlen:
//   stil      staat stil met de speer, steekt als hij binnen bereik is (hoeveel druk zet hij?)
//   spam      loopt op hem af en steekt zo vaak als het kan, ontwijkt nooit
//   geduld    steekt als hij loopt, stapt achteruit zodra hij afzet, en straft het herstel
//   door      sprint bij de afzet onder de sprong door naar zijn rug, en straft het herstel van achter
//   snel      geduld, maar onderbreekt zijn tell als hij al binnen bereik is
//   mens      geduld, maar met een reactietijd en wat toeval (zoals een speler)
//
// Nodig: Node en Playwright met Chromium (zoals tools/speelrobot.js).
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
function laadPlaywright(){
  for (const p of ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')]){ try { return require(p); } catch (e) {} }
  console.error('schildduel: Playwright ontbreekt (npm i -g playwright)'); process.exit(2);
}
const { chromium } = laadPlaywright();
const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const STIJLEN = ['stil', 'spam', 'geduld', 'door', 'snel', 'mens'];
const gekozen = args.filter(a => STIJLEN.includes(a));
const stijlen = gekozen.length ? gekozen : STIJLEN;
const keer = Number(opt('--keer', 3)), maxS = Number(opt('--max', 40)), reactie = Number(opt('--reactie', 0.25));
const breed = Number(opt('--breed', 960)), hoog = Number(opt('--hoog', 540));
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg' };
function server(){
  return new Promise(ok => {
    const s = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT)){ res.writeHead(403); res.end(); return; }
      fs.readFile(p, (err, data) => {
        if (err){ res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(data);
      });
    });
    s.listen(0, '127.0.0.1', () => ok(s));
  });
}
async function start(){
  try { return await chromium.launch(); }
  catch (e){
    const map = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
    for (const d of (fs.existsSync(map) ? fs.readdirSync(map) : []).filter(d => /^chromium-\d+$/.test(d)).sort().reverse()){
      const exe = path.join(map, d, 'chrome-linux', 'chrome');
      if (fs.existsSync(exe)) return chromium.launch({ executablePath: exe });
    }
    throw e;
  }
}

// draait in de pagina, na elk beeld
function duel([stijl, reactie, seed, spoorAan]){
  let rnd = seed * 9301 + 49297;
  const rand = () => { rnd = (rnd * 9301 + 49297) % 233280; return rnd / 233280; };
  const B = window.__duel = { klaar: null, ev: [], spoor: [], geraakt: 0, treffers: {}, aanvallen: 0, t0: null };
  const sc = () => (H * (Number(sizeEl.value) / 100)) / CHAR_H;
  const amirH = () => CHAR_H * sc();
  const verleden = [];                     // wat de speler ziet, met vertraging
  let lastLives = lives, laatsteStaat = '', laatsteSchild = SCHB.schild, plan = null, planTot = 0;
  keys['ArrowLeft'] = true;                // eerst naar de speer
  window.__duelStap = tt => {
    if (B.klaar) return;
    if (B.t0 === null) B.t0 = tt;
    const t = tt - B.t0;
    if (typeof laadWacht !== 'undefined' && laadWacht){ B.t0 = tt - 0; return; }
    if (lives < lastLives){ B.geraakt += lastLives - lives; B.ev.push([+t.toFixed(2), 'Amir geraakt', Math.round(world)]); lives = 3; drawLives(); dead = false; }
    lastLives = lives;
    if (!spearFound || !spear){
      if (spearNear()){ toggleSpear(); keys['ArrowLeft'] = false; }
      else { keys['ArrowLeft'] = true; }
      return;
    }
    const s = schildmannen[0];
    if (!s){ if (B.gezien){ B.klaar = { uitkomst: 'verslagen', t }; return; } keys['ArrowLeft'] = true; keys['ArrowRight'] = false; keys['Shift'] = false; if (t > 30) B.klaar = { uitkomst: 'geen vijand', t }; return; }
    B.gezien = true;
    if (s.state === 'dood' || s.state === 'weg'){ B.klaar = { uitkomst: 'verslagen', t }; for (const k in keys) keys[k] = false; return; }
    if (t > window.__duelMax){ B.klaar = { uitkomst: 'tijd op', t }; return; }
    const st = s.state + (s.state === 'strike' ? s.frame : '');
    if (s.state === 'strike' && laatsteStaat.indexOf('strike') !== 0){ B.aanvallen++; }
    if (s.schild < laatsteSchild || (s.state === 'dood')){
      const fase = laatsteStaat.replace(/\d+$/, m => { const f = +m; return f <= 5 ? '-tell' : f <= 16 ? '-lucht' : '-herstel'; });
      B.treffers[fase] = (B.treffers[fase] || 0) + 1;
      B.ev.push([+t.toFixed(2), 'raak (' + fase + '), schild ' + s.schild, Math.round(s.x)]);
    }
    if (window.__foto && !window.__foto.gedaan.has(st) && window.__foto.wil.includes(st)){ window.__foto.gedaan.add(st); window.__houd = st; }
    laatsteSchild = s.schild; laatsteStaat = st;
    if (spoorAan && Math.round(t * 60) % 3 === 0) B.spoor.push([+t.toFixed(2), Math.round(world), Math.round(s.x), st, s.schild, atkFrame, Math.round(knock), Math.round(s.knockV || 0)]);

    // wat de speler ziet: met vertraging (stijl mens) of meteen
    verleden.push({ t, state: s.state, frame: s.frame, x: s.x });
    const vertr = stijl === 'mens' ? reactie : stijl === 'stil' || stijl === 'spam' ? 0 : 0.15;
    while (verleden.length > 1 && verleden[1].t <= t - vertr) verleden.shift();
    const z = verleden[0];
    const dx = s.x - world, afst = Math.abs(dx), naar = dx < 0 ? 'ArrowLeft' : 'ArrowRight', weg = dx < 0 ? 'ArrowRight' : 'ArrowLeft';
    const A = amirH();
    const zetToets = (k) => { keys['ArrowLeft'] = k === 'ArrowLeft'; keys['ArrowRight'] = k === 'ArrowRight'; };
    const kijkNaar = () => { const moet = dx < 0 ? -1 : 1; if (facing !== moet){ zetToets(naar); return false; } return true; };
    const steek = () => { if (kijkNaar()){ zetToets(null); startAttack(); } };
    keys['Shift'] = false;
    const tell = z.state === 'strike' && z.frame <= 5;
    const lucht = z.state === 'strike' && z.frame >= 6 && z.frame <= 16;
    const herstel = z.state === 'strike' && z.frame >= 17;
    const inBereik = afst < 1.3 * A;
    if (stijl === 'stil'){ zetToets(null); if (inBereik) steek(); return; }
    if (stijl === 'spam'){ if (!inBereik) zetToets(naar); else steek(); return; }
    // geduld / mens / door / snel: ontwijk de sprong zodra hij afzet, straf het herstel
    if (plan && t < planTot){
      if (plan === 'weg'){ zetToets(weg); return; }
      if (plan === 'door'){ zetToets(naar); keys['Shift'] = true; return; }
    }
    plan = null;
    if (stijl === 'snel' && tell && z.frame <= 1 && inBereik){ steek(); return; }   // de tell onderbreken
    if (lucht && !(z.frame > 12)){
      if (stijl === 'door'){ plan = 'door'; planTot = t + 0.45; }
      else { plan = 'weg'; planTot = t + (stijl === 'mens' ? 0.25 + rand() * 0.3 : 0.35); }
      return;
    }
    if (tell || lucht){ zetToets(null); return; }            // wachten op de afzet
    const wil = stijl === 'mens' ? 1.25 + rand() * 0.15 : 1.25;
    if (herstel || z.state === 'flinch' || z.state === 'loop'){
      if (afst > wil * A){ zetToets(naar); return; }
      steek(); return;
    }
    zetToets(null);
  };
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await start();
  const totaal = {};
  for (const stijl of stijlen) for (let k = 0; k < keer; k++){
    const page = await browser.newPage({ viewport: { width: breed, height: hoog } });
    await page.addInitScript(() => {
      let vt = 1000; window.__vt = () => vt;
      window.requestAnimationFrame = cb => setTimeout(function stap(){ if (window.__houd){ setTimeout(stap, 20); return; } vt += 1000 / 60; cb(vt); if (window.__duelStap){ try { window.__duelStap(vt / 1000); } catch (e){ console.error('duel: ' + e.stack); } } }, 0);
    });
    page.on('pageerror', e => console.log('  fout: ' + e.message));
    page.on('console', m => { if (m.type() === 'error' && /duel/.test(m.text())) console.log('  ' + m.text()); });
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 180000 });
    await page.waitForFunction(() => typeof setLevel === 'function');
    await page.waitForTimeout(800);
    await page.evaluate(() => {
      const def = { name: 'Schildduel', lagen: 'tafelbergen', view: 0.8,
        spawns: [ {x: -1300, k: 'schildman'} ], rocks: [], gaps: [], ledges: [], village: [], npcs: [], water: [], thickets: [], props: [],
        cliffs: [ {x: -9000} ], ends: [ {x: -8500} ], tips: [] };
      laadVorig = 'Schildduel'; setLevel(0, [def]); beginPlay('medium');
    });
    await page.evaluate(m => { window.__duelMax = m; }, maxS);
    await page.evaluate(duel, [stijl, reactie, k + 1, args.includes('--spoor')]);
    const klok = Date.now();
    const fotos = opt('--fotos', null);
    if (fotos){ fs.mkdirSync(fotos, { recursive: true });
      await page.evaluate(() => { window.__foto = { gedaan: new Set(), wil: ['strike2','strike4','strike6','strike10','strike14','strike17','strike18','strike20','strike24','strike28','flinch4','flinch6','flinch10','flinch16'] }; }); }
    for (;;){
      await page.waitForTimeout(fotos ? 60 : 300);
      if (fotos){ const h = await page.evaluate(() => window.__houd); if (h){ await page.screenshot({ path: path.join(fotos, stijl + '_' + h + '.png') }); await page.evaluate(() => { window.__houd = null; }); } }
      const klaar = await page.evaluate(() => window.__duel.klaar);
      if (args.includes('--dbg')) console.log(await page.evaluate(() => JSON.stringify({ vt: Math.round(window.__vt()), t0: window.__duel.t0,
        w: Math.round(world), sp: spear, lw: typeof laadWacht !== 'undefined' && laadWacht, n: schildmannen.length, s: schildmannen[0] && schildmannen[0].state })));
      if (klaar || Date.now() - klok > 240000) break;
    }
    const D = await page.evaluate(() => window.__duel);
    const k2 = D.klaar || { uitkomst: 'afgebroken', t: 0 };
    console.log(stijl.padEnd(7) + ' #' + (k + 1) + '  ' + k2.uitkomst.padEnd(10) + ' na ' + k2.t.toFixed(1).padStart(5) + ' s   Amir geraakt ' + D.geraakt +
      '   aanvallen ' + D.aanvallen + '   treffers ' + JSON.stringify(D.treffers));
    if (args.includes('-v')) for (const e of D.ev) console.log('      ' + e.join('  '));
    if (args.includes('--spoor')) for (const r of D.spoor) console.log('      ' + r.join(' '));
    const T = totaal[stijl] || (totaal[stijl] = { n: 0, t: 0, g: 0, win: 0 });
    T.n++; T.t += k2.t; T.g += D.geraakt; if (k2.uitkomst === 'verslagen') T.win++;
    await page.close();
  }
  console.log('\nsamen:');
  for (const [s, T] of Object.entries(totaal))
    console.log('  ' + s.padEnd(7) + ' verslagen ' + T.win + '/' + T.n + ', gemiddeld ' + (T.t / T.n).toFixed(1) + ' s, Amir ' + (T.g / T.n).toFixed(1) + ' keer geraakt');
  await browser.close(); srv.close();
})();
