#!/usr/bin/env node
// De poorttest: speelt Maker-grids met poorten in het echte spel en kijkt of de vijanden eruit komen zoals bedoeld.
//
// Hij laadt het spel in Chromium, opent de Maker nieuwstijl, zet een klein grid met een poort klaar en start de Test,
// op een vaste 60 beelden per seconde (virtuele tijd, zoals de speelrobot). Amir loopt naar het zegel of het regiepunt,
// en per scenario staat er wat er gezien is: waar en op welke hoogte elke vijand verscheen, of Amir vast stond in de
// regie, of hij levens verloor, en wat er na de dood en een herstart gebeurt. Elk scenario meldt OK of FOUT; een regel
// met (info) is alleen ter inzage. Draai hem na een wijziging aan de poort, het hek, de regie, de spawner of mkNaarLevel.
//
//   node tools/poorttest.js                 alle scenario's (ruim tien minuten)
//   node tools/poorttest.js --alleen gang   alleen de scenario's waarvan de naam dit bevat
//   node tools/poorttest.js --shots map     een schermafdruk per scenario
//
// Nodig: Node en Playwright, net als de speelrobot. Hij start zelf een webserver en verandert niets aan het spel.
'use strict';
const fs = require('fs'); const path = require('path'); const http = require('http');
function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('poorttest: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();
const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const alleen = (() => { const i = args.indexOf('--alleen'); return i >= 0 ? args[i + 1] : ''; })();
const shots = (() => { const i = args.indexOf('--shots'); return i >= 0 ? args[i + 1] : null; })();
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg' };
function server(){ return new Promise(ok => { const s = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(ROOT)){ res.writeHead(403); res.end(); return; }
  fs.readFile(p, (err, data) => { if (err){ res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(data); });
}); s.listen(0, '127.0.0.1', () => ok(s)); }); }
async function start(){
  try { return await chromium.launch(); }
  catch (e){
    const map = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
    const kandidaten = fs.existsSync(map) ? fs.readdirSync(map).filter(d => /^chromium-\d+$/.test(d)).sort().reverse() : [];
    for (const d of kandidaten){ const exe = path.join(map, d, 'chrome-linux', 'chrome'); if (fs.existsSync(exe)) return chromium.launch({ executablePath: exe }); }
    throw e;
  }
}

const FPS = 60;
// een grid: C kolommen, R rijen, grondlijn G; teken(rijen) past cellen aan
function grid(o){
  const C = o.cols || 32, R = o.rows || 12, G = o.ground == null ? 7 : o.ground;
  const rijen = []; for (let r = 0; r < R; r++) rijen.push('.'.repeat(C).split(''));
  for (let c = 0; c < C; c++) rijen[G][c] = 'S';
  if (o.teken) o.teken(rijen);
  return { type: 'amir-levelmaker-grid', versie: 2, cols: C, rows: R, groundRow: G, grid: rijen.map(r => r.join('')),
    start: o.start || { c: C - 4, r: G - 1 }, eind: o.eind || { c: 2, r: G - 1 }, muziek: 'darkafrica', valschade: false,
    maskers: o.maskers || [], vormen: [], zwart: o.zwart || [], objecten: o.objecten || [] };
}
const poort = (c, r, extra) => ({ c, r, k: 'poort', boog: 'boog_steen', note: '', ...extra });
const zegel = (c, r, pc, pr, extra) => ({ c, r, k: 'zegel', poort: { c: pc, r: pr }, note: '', ...extra });

(async () => {
  const srv = await server();
  const browser = await start();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const console_ = [];
  page.on('console', m => { if (m.type() === 'error' && !/ERR_CERT|ERR_NAME|ERR_INTERNET|ERR_PROXY|ERR_TUNNEL|mp3|Failed to load resource/.test(m.text())) console_.push(m.text()); });
  page.on('pageerror', e => console_.push('fout: ' + e.message));
  page.on('dialog', d => d.accept());
  await page.addInitScript(fps => {
    let vt = 1000, nr = 0; const wachters = [];
    window.__vt = () => vt; window.__nr = () => nr;
    window.__wacht = s => new Promise(ok => wachters.push({ tot: nr + Math.round(s * fps), ok }));
    window.__tot = f => new Promise(ok => wachters.push({ f, ok, tot: nr + 60 * fps }));
    window.requestAnimationFrame = cb => setTimeout(() => {
      vt += 1000 / fps; nr++;
      cb(vt);
      if (window.__spion){ try { window.__spion(); } catch (e){} }
      for (let i = wachters.length - 1; i >= 0; i--){ const w = wachters[i];
        let klaar = false; try { klaar = (w.f && w.f()) || nr >= w.tot; } catch (e){ klaar = true; }
        if (klaar){ wachters.splice(i, 1); w.ok(nr >= w.tot && w.f ? 'tijd op' : 'ok'); } }
    }, 0);
  }, FPS);
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof mkOpen === 'function' && typeof mkNaarLevel === 'function');
  await page.waitForTimeout(1200);
  await page.evaluate(() => { try { localStorage.removeItem('amir-mk'); } catch (e){} mkOpen(); });

  const uitslag = []; let fouten = 0;
  async function check(naam, fn){
    if (alleen && naam.indexOf(alleen) < 0) return;
    let res; const n0 = console_.length;
    try { res = await fn(); } catch (e){ res = ['uitzondering: ' + (e && e.stack || e)]; }
    res = res || [];
    if (console_.length > n0) res.push('console: ' + console_.slice(n0).join(' | '));
    const ok = !res.some(r => !String(r).startsWith('(info)')); if (!ok) fouten++;
    uitslag.push((ok ? 'OK   ' : 'FOUT ') + naam + (res.length ? '\n      ' + res.slice(0, 14).join('\n      ') : ''));
    console.log(uitslag[uitslag.length - 1]);
    // terug naar de Maker
    await page.evaluate(() => { for (const k in keys) keys[k] = false; if (mkTestActief) mkTerug(); });
  }
  // een grid laden en de Test starten; geeft het spel-level terug
  async function speel(g){
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const lvl = await page.evaluate(() => mkNaarLevel());
    await page.evaluate(() => mkTest());
    await page.evaluate(() => {
      window.__eerste = []; const gezien = new WeakSet();
      window.__spion = () => { if (!level) return;
        const lijsten = [['slang', snakes], ['scorp', scorps], ['bandiet', bandieten], ['schildman', schildmannen], ['kooiman', kooimannen], ['meelman', meelmannen], ['fosfor', fosforSlangen], ['zweepman', zweepmannen]];
        for (const [k, l] of lijsten) for (const v of l) if (!gezien.has(v)){ gezien.add(v); window.__eerste.push({ k, x: Math.round(v.x), b: Math.round(v.base), t: +(__vt() / 1000).toFixed(2), amir: Math.round(world) }); } };
    });
    await page.evaluate(() => __wacht(0.5));
    return lvl;
  }
  const toets = (k, aan) => page.evaluate(([k, aan]) => { keys[k] = aan; }, [k, aan]);
  const wacht = s => page.evaluate(s => __wacht(s), s);
  const tot = (code, maxS) => page.evaluate(([code, maxS]) => __tot(new Function('return (' + code + ')'), maxS), [code, maxS || 30]);
  const st = () => page.evaluate(() => ({
    x: Math.round(world), h: Math.round(ph), lives, dead, vast: amirVast(), regie: !!poortRegie, t: __vt() / 1000,
    poorten: (level.poorten || []).map(o => ({ id: o.id, x: o.x, open: !!o.open, hekP: o.hekP || 0, y: o.y })),
    spawns: (level.spawns || []).map(s => ({ k: s.kind || s.k, x: s.x, used: !!s.used, armed: !!s.armed, poort: s.poort, boven: s.boven, y: s.y, w: s.poortWacht })),
    vij: [...snakes.map(s => ({ k: 'slang:' + s.kind, x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...scorps.map(s => ({ k: 'scorp', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...bandieten.map(s => ({ k: 'bandiet', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...schildmannen.map(s => ({ k: 'schildman', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...kooimannen.map(s => ({ k: 'kooiman', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...meelmannen.map(s => ({ k: 'meelman', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...fosforSlangen.map(s => ({ k: 'fosfor', x: Math.round(s.x), b: Math.round(s.base), st: s.state })),
          ...zweepmannen.map(s => ({ k: 'zweepman', x: Math.round(s.x), b: Math.round(s.base), st: s.state }))],
    eerste: window.__eerste || [],
    hint: (document.getElementById('hint') || {}).textContent || '' }));
  const loopTot = async (x, maxS) => { // naar links lopen tot world <= x
    await toets('ArrowLeft', true);
    const r = await tot('world <= ' + x, maxS || 20);
    await toets('ArrowLeft', false);
    return r;
  };
  const foto = async naam => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, naam + '.png') }); } };

  // ---- 1. de basis: een zegel opent een poort met een slang; de slang komt bij de poort ----
  await check('basis: zegel opent poort, zandslang komt op de plek van de poort op de grond', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: 'groen' }), zegel(18, 6, 12, 6)] }));
    const px = lvl.poorten[0].x;
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(1.5);
    let s = await st();
    if (!s.poorten[0].open) uit.push('de poort is niet open na het zegel: ' + JSON.stringify(s.poorten) + ' x=' + s.x);
    if (!s.eerste.length) uit.push('geen slang na 1,5 s: ' + JSON.stringify(s.spawns));
    else { const v = s.eerste[0]; if (Math.abs(v.x - px) > 60) uit.push('de slang kwam niet bij de poort: ' + JSON.stringify(v) + ' poort x=' + px); if (v.b !== 0) uit.push('de slang kwam niet op de grond: ' + JSON.stringify(v)); }
    await foto('basis');
    return uit;
  });

  // ---- 2. het zegel ver van de poort: de vijand wacht achter de opening tot Amir in de buurt is ----
  await check('ver: zegel 25 cellen van de poort; de vijand komt pas als Amir bij de poort komt, en komt dan echt', async () => {
    const uit = [];
    const lvl = await speel(grid({ cols: 36, start: { c: 32, r: 6 }, objecten: [poort(4, 6, { vijand: 'scorp', n: 2 }), zegel(29, 6, 4, 6)] }));
    const px = lvl.poorten[0].x;
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    let s = await st();
    if (!s.poorten[0].open) uit.push('poort niet open: ' + JSON.stringify(s.poorten));
    if (s.spawns.some(q => q.poort && q.used)) uit.push('de spawn is al afgeschreven terwijl Amir ver weg is: ' + JSON.stringify(s.spawns));
    if (s.eerste.length) uit.push('de vijand kwam al terwijl Amir ' + Math.abs(s.x - px) + ' px van de poort was: ' + JSON.stringify(s.eerste));
    await loopTot(px + 400, 40);
    await wacht(1.5);
    s = await st();
    if (s.eerste.length !== 2) uit.push('niet twee schorpioenen bij de poort nadat Amir erheen liep: ' + JSON.stringify(s.eerste) + ' spawns ' + JSON.stringify(s.spawns));
    else { if (Math.abs(s.eerste[0].x - px) > 120) uit.push('niet bij de poort: ' + JSON.stringify(s.eerste));
      if (s.eerste[1].t - s.eerste[0].t < 0.9) uit.push('niet na elkaar: ' + JSON.stringify(s.eerste));
      if (Math.abs(s.eerste[0].amir - px) > 1600) uit.push('kwam al van te ver: ' + JSON.stringify(s.eerste)); }
    return uit;
  });

  // ---- 3. drie schorpioenen na elkaar ----
  await check('aantal: drie schorpioenen komen om POORT.tussen na elkaar', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: 'scorp', n: 3 }), zegel(18, 6, 12, 6)] }));
    await loopTot(lvl.zegels[0].x + 10);
    const tijden = [];
    for (let i = 0; i < 80; i++){ await wacht(0.05); const s = await st(); if (s.vij.length > tijden.length) tijden.push(+s.t.toFixed(2)); if (tijden.length === 3) break; }
    const s = await st();
    if (tijden.length !== 3) uit.push('niet drie schorpioenen: ' + JSON.stringify(s.vij) + ' spawns ' + JSON.stringify(s.spawns));
    else { const d1 = tijden[1] - tijden[0], d2 = tijden[2] - tijden[1]; if (Math.abs(d1 - 1.1) > 0.2 || Math.abs(d2 - 1.1) > 0.2) uit.push('tussentijden ' + d1.toFixed(2) + ' en ' + d2.toFixed(2)); }
    return uit;
  });

  // ---- 4. elke vijandsoort uit de poort ----
  const soorten = ['groen', 'zwart', 'knock', 'scorp', 'fosfor', 'bandiet', 'bandiet:dolk', 'bandiet:elite', 'schildman', 'schildman:makkelijk', 'meelman', 'kooiman:smash', 'kooiman:vogel', 'zweepman'];
  for (const soort of soorten){
    await check('soort ' + soort + ': komt uit de poort op de plek van de poort', async () => {
      const uit = [];
      const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: soort }), zegel(18, 6, 12, 6)] }));
      const px = lvl.poorten[0].x;
      await loopTot(lvl.zegels[0].x + 10);
      await wacht(3);
      const s = await st();
      if (!s.eerste.length) uit.push('geen vijand: ' + JSON.stringify(s.spawns) + ' hint ' + s.hint);
      else { const v = s.eerste[0]; if (Math.abs(v.x - px) > 120) uit.push('kwam niet bij de poort (' + px + '): ' + JSON.stringify(s.eerste)); if (Math.abs(v.b) > 2) uit.push('niet op de grond: ' + JSON.stringify(s.eerste)); }
      uit.push('(info) eerste ' + JSON.stringify(s.eerste.slice(0, 3)) + ' poort ' + px + ' amir ' + s.x);
      return uit;
    });
  }

  // ---- 5. poort op een mesa (terras van rots, 1 hoog) ----
  await check('mesa: poort op een rotsterras, de vijand komt op het terras', async () => {
    const uit = [];
    const g = grid({ teken: r => { for (let c = 9; c <= 15; c++) r[6][c] = 'R'; }, objecten: [poort(12, 5, { vijand: 'groen' }), zegel(18, 6, 12, 5)] });
    const lvl = await speel(g);
    const p = lvl.poorten[0];
    if (p.y !== 150) uit.push('poort y: ' + JSON.stringify(p));
    const sp = lvl.spawns.find(s => s.poort); if (!sp || !sp.boven) uit.push('spawn niet boven: ' + JSON.stringify(sp));
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    const s = await st();
    if (!s.vij.length) uit.push('geen vijand'); else if (Math.abs(s.vij[0].b - 150) > 2) uit.push('vijand niet op het terras: ' + JSON.stringify(s.vij));
    await foto('mesa');
    return uit;
  });
  for (const soort of ['scorp', 'bandiet', 'schildman', 'kooiman:smash', 'meelman', 'fosfor']){
    await check('mesa ' + soort + ': komt op het terras en niet op de grond eronder', async () => {
      const uit = [];
      const g = grid({ teken: r => { for (let c = 9; c <= 15; c++) r[6][c] = 'R'; }, objecten: [poort(12, 5, { vijand: soort }), zegel(18, 6, 12, 5)] });
      const lvl = await speel(g);
      await loopTot(lvl.zegels[0].x + 10);
      await wacht(2.5);
      const s = await st();
      if (!s.vij.length) uit.push('geen vijand'); else if (Math.abs(s.vij[0].b - 150) > 2) uit.push('vijand niet op het terras (150): ' + JSON.stringify(s.vij));
      return uit;
    });
  }

  // ---- 6. poort op het dak van een gang ----
  await check('dak: poort op het dak van een gang, de vijand komt op de savanne en niet in de gang', async () => {
    const uit = [];
    const g = grid({ teken: r => { for (let c = 9; c <= 15; c++) for (let rr = 8; rr <= 10; rr++) r[rr][c] = 'G'; r[7][16] = 'V'; },
                     objecten: [poort(12, 6, { vijand: 'groen' }), zegel(19, 6, 12, 6)] });
    const lvl = await speel(g);
    const p = lvl.poorten[0]; if (p.y !== 0) uit.push('poort y op het dak: ' + JSON.stringify(p));
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    const s = await st();
    if (!s.vij.length) uit.push('geen vijand'); else if (Math.abs(s.vij[0].b) > 2) uit.push('vijand niet op het dak: ' + JSON.stringify(s.vij));
    return uit;
  });
  for (const soort of ['scorp', 'bandiet', 'schildman', 'kooiman:smash', 'kooiman:vogel', 'meelman', 'fosfor']){
    await check('dak ' + soort + ': op de savanne boven de gang', async () => {
      const uit = [];
      const g = grid({ teken: r => { for (let c = 9; c <= 15; c++) for (let rr = 8; rr <= 10; rr++) r[rr][c] = 'G'; r[7][16] = 'V'; },
                       objecten: [poort(12, 6, { vijand: soort }), zegel(19, 6, 12, 6)] });
      const lvl = await speel(g);
      await loopTot(lvl.zegels[0].x + 10);
      await wacht(2.5);
      const s = await st();
      if (!s.vij.length) uit.push('geen vijand'); else if (Math.abs(s.vij[0].b) > 2) uit.push('vijand niet op het dak (0): ' + JSON.stringify(s.vij));
      return uit;
    });
  }

  // ---- 7. poort in een gang ----
  for (const soort of ['groen', 'scorp', 'bandiet', 'schildman', 'fosfor', 'kooiman:smash']){
    await check('gang ' + soort + ': poort op de gangvloer, de vijand komt in de gang', async () => {
      const uit = [];
      // gang rij 8 tot 10, kolom 6 tot 20; ingang: ravijn op kolom 19 en 20
      const g = grid({ teken: r => { for (let c = 6; c <= 20; c++) for (let rr = 8; rr <= 10; rr++) r[rr][c] = 'G'; r[7][19] = 'V'; r[7][20] = 'V'; },
                       start: { c: 26, r: 6 }, objecten: [poort(10, 10, { vijand: soort }), zegel(15, 10, 10, 10)] });
      const lvl = await speel(g);
      const p = lvl.poorten[0]; if (p.y !== undefined) uit.push('(info) poort in gang heeft y: ' + JSON.stringify(p));
      await loopTot(lvl.zegels[0].x + 10, 25);
      let s = await st();
      if (s.h > -400) uit.push('Amir niet in de gang: h=' + s.h + ' x=' + s.x);
      await wacht(3);
      s = await st();
      if (!s.vij.length) uit.push('geen vijand: ' + JSON.stringify(s.spawns));
      else { const v = s.eerste[0]; if (Math.abs(v.b - (-600)) > 2) uit.push('vijand niet op de gangvloer (-600): ' + JSON.stringify(s.eerste)); if (Math.abs(v.x - p.x) > 120) uit.push('vijand kwam niet bij de poort: ' + JSON.stringify(s.eerste) + ' poort ' + p.x); }
      uit.push('(info) spawn ' + JSON.stringify(lvl.spawns.find(q => q.poort)) + ' eerste ' + JSON.stringify(s.eerste.slice(0, 2)));
      await foto('gang-' + soort.replace(':', '_'));
      return uit;
    });
  }

  // ---- 8. hek + regie + schildbandiet ----
  await check('regie: hek met regie en schildbandiet; Amir staat vast tot hij eruit is, en komt daarna los', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(10, 6, { vijand: 'schildman', hek: true, regie: true })] }));
    const px = lvl.poorten[0].x;
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie', 20);
    if (r !== 'ok'){ uit.push('de regie begon niet'); return uit; }
    const s0 = await st();
    if (!s0.vast) uit.push('Amir staat niet vast tijdens de regie');
    await wacht(0.5);
    const s1 = await st();
    if (Math.abs(s1.x - s0.x) > 5) uit.push('Amir loopt tijdens de regie: ' + s0.x + ' -> ' + s1.x);
    const r2 = await tot('!poortRegie', 20);
    const s2 = await st();
    if (r2 !== 'ok') uit.push('de regie eindigde niet binnen 20 s: ' + JSON.stringify(s2.poorten) + ' ' + JSON.stringify(s2.vij));
    uit.push('(info) regie duurde ' + (s2.t - s0.t).toFixed(1) + ' s; schildman ' + JSON.stringify(s2.vij) + ' poort ' + px + ' amir ' + s2.x + ' levens ' + s2.lives);
    if (!s2.vij.length) uit.push('geen schildbandiet na de regie');
    if (s2.lives < 3) uit.push('Amir verloor levens tijdens de regie');
    await wacht(0.5);
    const s3 = await st();
    if (s3.vast) uit.push('Amir staat na de regie nog vast');
    await toets('ArrowLeft', false);
    await foto('regie');
    return uit;
  });

  // ---- 9. regie zonder hek met een slang: bijt hij Amir terwijl die vast staat? ----
  await check('regie slang: poort met regie (geen hek) en een zandslang, Amir staat vast', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(14, 6, { vijand: 'groen', n: 2, regie: true })] }));
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie', 20);
    if (r !== 'ok'){ uit.push('de regie begon niet'); return uit; }
    const s0 = await st();
    const r2 = await tot('!poortRegie', 20);
    const s2 = await st();
    uit.push('(info) regie duurde ' + (s2.t - s0.t).toFixed(1) + ' s; levens ' + s0.lives + ' -> ' + s2.lives + '; afstand bij start ' + Math.abs(s0.x - lvl.poorten[0].x) + '; vij ' + JSON.stringify(s2.vij));
    if (s2.lives < s0.lives) uit.push('Amir werd geraakt terwijl hij vast stond in de regie');
    await toets('ArrowLeft', false);
    return uit;
  });

  // ---- 10. hek zonder regie, door een zegel ----
  await check('hek zegel: zegel takelt het hek op, de vijand komt op 80% en Amir staat niet vast', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: 'scorp', hek: true }), zegel(18, 6, 12, 6)] }));
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(0.3);
    let s = await st();
    if (s.vast) uit.push('Amir staat vast zonder regie');
    if (s.poorten[0].open) uit.push('poort al open voor het hek op is');
    const r = await tot('level.poorten[0].open', 10);
    s = await st();
    if (r !== 'ok') uit.push('poort ging niet open: ' + JSON.stringify(s.poorten));
    if (s.poorten[0].hekP < 0.75) uit.push('open bij hekP ' + s.poorten[0].hekP);
    await wacht(1);
    s = await st();
    if (!s.vij.length) uit.push('geen schorpioen na het hek: ' + JSON.stringify(s.spawns));
    return uit;
  });

  // ---- 11. dood en herstart: poort dicht, vijand weer binnen, zegel weer uit ----
  await check('herstart: na de dood is de poort dicht en komt de vijand opnieuw als het zegel weer aangaat', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: 'groen', hek: true }), zegel(18, 6, 12, 6)] }));
    await loopTot(lvl.zegels[0].x + 10);
    await tot('level.poorten[0].open', 10);
    await wacht(1);
    let s = await st();
    if (!s.vij.length) uit.push('geen slang de eerste keer');
    await page.evaluate(() => { lives = 1; invuln = 0; hurtPlayer(true); });
    await wacht(0.2);
    s = await st(); if (!s.dead) uit.push('Amir ging niet dood');
    await page.evaluate(() => restart());
    await wacht(0.5);
    s = await st();
    if (s.poorten[0].open || s.poorten[0].hekP) uit.push('poort niet dicht na herstart: ' + JSON.stringify(s.poorten));
    if (s.vij.length) uit.push('vijanden na herstart: ' + JSON.stringify(s.vij));
    if (s.spawns.some(q => q.used)) uit.push('spawns nog gebruikt: ' + JSON.stringify(s.spawns));
    await loopTot(lvl.zegels[0].x + 10);
    const r = await tot('level.poorten[0].open', 10);
    if (r !== 'ok') uit.push('poort ging de tweede keer niet open');
    await wacht(1.2);
    s = await st();
    if (!s.vij.length) uit.push('geen slang de tweede keer: ' + JSON.stringify(s.spawns));
    return uit;
  });

  // ---- 12. twee poorten, twee zegels; en twee regiepoorten met hetzelfde regiepunt ----
  await check('twee poorten: elk zegel opent alleen zijn eigen poort', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(8, 6, { vijand: 'groen' }), poort(13, 6, { vijand: 'scorp' }), zegel(18, 6, 13, 6), zegel(11, 6, 8, 6)] }));
    await loopTot(lvl.zegels.find(z => z.poort === 'b2').x + 10);
    await wacht(1.5);
    let s = await st();
    if (!s.poorten.find(p => p.id === 'b2').open || s.poorten.find(p => p.id === 'b1').open) uit.push('verkeerde poort open: ' + JSON.stringify(s.poorten));
    if (s.vij.length !== 1 || s.vij[0].k !== 'scorp') uit.push('na zegel 1: ' + JSON.stringify(s.vij));
    await loopTot(lvl.zegels.find(z => z.poort === 'b1').x + 10);
    await wacht(1.5);
    s = await st();
    if (!s.poorten.every(p => p.open)) uit.push('niet beide open: ' + JSON.stringify(s.poorten));
    if (!s.vij.some(v => v.k === 'slang:groen')) uit.push('geen slang uit b1: ' + JSON.stringify(s.vij));
    return uit;
  });
  await check('twee regiepoorten met hetzelfde regiepunt gaan samen open', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(8, 6, { vijand: 'groen', regie: true, bij: 16 }), poort(13, 6, { vijand: 'scorp', regie: true, bij: 16 })] }));
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie && (window.__nrRegie = poortRegie.poorten.length, window.__xRegie = world, true)', 20);
    if (r !== 'ok'){ uit.push('geen regie'); return uit; }
    const s = await st();
    const xr = await page.evaluate(() => window.__xRegie);
    if (xr > lvl.poorten[0].bij + 100) uit.push('regie begon voor het regiepunt: x=' + xr + ' bij=' + lvl.poorten[0].bij);
    const nr = await page.evaluate(() => window.__nrRegie);
    if (nr !== 2) uit.push('niet twee poorten in de regie: ' + nr);
    await tot('!poortRegie', 20);
    const s2 = await st();
    if (!s2.vij.some(v => v.k === 'scorp') || !s2.vij.some(v => v.k === 'slang:groen')) uit.push('niet uit beide: ' + JSON.stringify(s2.vij));
    await toets('ArrowLeft', false);
    return uit;
  });

  // ---- 13. poort rechts van de start (achter Amir) ----
  await check('achter: poort rechts van de start, zegel links; de vijand komt van achter', async () => {
    const uit = [];
    const lvl = await speel(grid({ start: { c: 20, r: 6 }, objecten: [poort(24, 6, { vijand: 'bandiet' }), zegel(17, 6, 24, 6)] }));
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    const s = await st();
    if (!s.vij.length) uit.push('geen vijand: ' + JSON.stringify(s.spawns));
    else if (Math.abs(s.eerste[0].x - lvl.poorten[0].x) > 120) uit.push('niet bij de poort: ' + JSON.stringify(s.eerste) + ' ' + lvl.poorten[0].x);
    return uit;
  });

  // ---- 14. zegel dat een masker en een poort tegelijk opent ----
  await check('masker: een zegel opent een masker en de poort erachter tegelijk', async () => {
    const uit = [];
    const g = grid({ maskers: [{ id: 'Verborgen1', look: 'grot', cells: [[11, 6], [12, 6], [13, 6]] }],
                     objecten: [poort(12, 6, { vijand: 'groen' }), zegel(18, 6, 12, 6, { masker: 'Verborgen1' })] });
    const lvl = await speel(g);
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    const s = await st();
    if (!s.poorten[0].open) uit.push('poort niet open');
    if (!s.vij.length) uit.push('geen slang: ' + JSON.stringify(s.spawns));
    const m = await page.evaluate(() => (maskerLijst ? maskerLijst() : []).map(m => ({ id: m.id, onthuld: !!m.onthuld })));
    uit.push('(info) maskers ' + JSON.stringify(m));
    return uit;
  });

  // ---- 15. regiepoort met Amir die begint binnen bereik ----
  await check('regie bij de start: poort met regie vlak bij de start begint meteen', async () => {
    const uit = [];
    const lvl = await speel(grid({ start: { c: 14, r: 6 }, objecten: [poort(12, 6, { vijand: 'groen', regie: true })] }));
    await wacht(0.5);
    const s = await st();
    if (!s.regie && !s.poorten[0].open) uit.push('regie begon niet bij de start: ' + JSON.stringify(s.poorten) + ' x=' + s.x);
    await tot('!poortRegie', 20);
    const s2 = await st();
    uit.push('(info) levens ' + s2.lives + ' vij ' + JSON.stringify(s2.vij));
    return uit;
  });

  // ---- 16. de poort in de Maker: verwijderen terwijl een zegel ernaar wijst ----
  await check('maker: poort weghalen met een zegel eraan, dan vertalen en controle', async () => {
    const uit = [];
    const g = grid({ objecten: [poort(12, 6, { vijand: 'groen' }), zegel(18, 6, 12, 6)] });
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const r = await page.evaluate(() => {
      MK.tool = 'select'; mkLegenda(); MK.sel = MK.objects.find(o => o.k === 'poort'); mkNotePaneel(); mkTeken();
      const ev = new KeyboardEvent('keydown', { key: 'Delete', bubbles: true }); document.dispatchEvent(ev);
      const lvl = mkNaarLevel();
      mkControle();
      const z = MK.objects.find(o => o.k === 'zegel'); MK.sel = z; mkNotePaneel();
      const a = mkNaarJSON(); mkUitJSON(a);
      return { poorten: lvl.poorten, zegels: lvl.zegels, spawns: lvl.spawns.filter(s => s.poort), nog: MK.objects.filter(o => o.k === 'poort').length,
               sel: document.getElementById('mkpoortsel').value };
    });
    if (r.nog) uit.push('de poort is niet weg');
    if (r.poorten && r.poorten.length) uit.push('poorten in het level: ' + JSON.stringify(r.poorten));
    if ((r.zegels || []).some(z => z.poort)) uit.push('zegel wijst nog naar een poort: ' + JSON.stringify(r.zegels));
    if (r.spawns.length) uit.push('spawns met poort: ' + JSON.stringify(r.spawns));
    return uit;
  });

  // ---- 17. een vijand-object op dezelfde cel als een poort ----
  await check('maker: een los vijand-object op de cel van de poort', async () => {
    const uit = [];
    const g = grid({ objecten: [poort(12, 6, { vijand: 'groen' }), { c: 12, r: 6, k: 'vijand', soort: 'scorp', note: '' }, zegel(18, 6, 12, 6)] });
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const r = await page.evaluate(() => { const lvl = mkNaarLevel(); mkControle(); return { spawns: lvl.spawns, op: (mkObjOp(12, 6) || {}).k, meld: [...document.querySelectorAll('#mkcontrole li, #mkcontrolelijst li, .mkmeld')].map(e => e.textContent) }; });
    uit.push('(info) ' + JSON.stringify(r));
    return uit;
  });

  // ---- 18. levelcheck op een poortlevel uit de Maker ----
  await check('levelcheck: een Maker-level met poort, hek, regie en een vijand geeft geen FOUT', async () => {
    const uit = [];
    const g = grid({ objecten: [poort(12, 6, { vijand: 'schildman', hek: true, regie: true, wand: 'pieken' }), poort(8, 6, { vijand: 'scorp', n: 2 }), zegel(18, 6, 8, 6)] });
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const lvl = await page.evaluate(() => mkNaarLevel());
    const f = path.join(require('os').tmpdir(), 'poorttest-level.json'); fs.writeFileSync(f, JSON.stringify(lvl));
    const { spawnSync } = require('child_process');
    const p = spawnSync('python3', [path.join(ROOT, 'tools/levelcheck.py'), f], { encoding: 'utf8' });
    const regels = (p.stdout + p.stderr).split('\n').filter(l => /FOUT|LET OP/.test(l));
    if (regels.some(l => /FOUT/.test(l))) uit.push(...regels);
    else if (regels.length) uit.push('(info) ' + regels.join(' | '));
    return uit;
  });

  // ---- rand: regiepunt ver voorbij de poort ----
  await check('rand regiepunt ver: regie met bij 14 cellen voorbij de poort houdt Amir niet vast, de vijand komt als hij terugloopt, en de controle meldt het', async () => {
    const uit = [];
    const g = grid({ cols: 36, start: { c: 32, r: 6 }, objecten: [poort(26, 6, { vijand: 'groen', regie: true, bij: 12 })] });
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const meld = await page.evaluate(() => mkControle().filter(m => m.ernst === 'letop').map(m => m.tekst));
    if (!meld.some(t => /regiepunt/.test(t))) uit.push('de controle meldt het verre regiepunt niet: ' + JSON.stringify(meld));
    const lvl = await speel(g);
    const px = lvl.poorten[0].x;
    await loopTot(lvl.poorten[0].bij - 60, 40);
    await wacht(1);
    let s = await st();
    if (!s.poorten[0].open) uit.push('de poort ging niet open voorbij het regiepunt: ' + JSON.stringify(s.poorten));
    if (s.vast || s.regie) uit.push('Amir staat vast voor een poort buiten beeld');
    if (s.eerste.length) uit.push('de vijand kwam al terwijl de poort ' + Math.abs(s.x - px) + ' px weg was: ' + JSON.stringify(s.eerste));
    await toets('ArrowRight', true);                     // terug naar de poort: nu komt hij wel
    await tot('world >= ' + (px - 1000), 30);
    await toets('ArrowRight', false);
    await wacht(2);
    s = await st();
    if (s.eerste.length !== 1 || Math.abs(s.eerste[0].x - px) > 120) uit.push('de vijand kwam niet uit de poort toen Amir terugkwam: ' + JSON.stringify(s.eerste));
    uit.push('(info) eerste ' + JSON.stringify(s.eerste) + ' poort ' + px);
    return uit;
  });
  // ---- rand: Amir staat in de opening als de regie begint ----
  await check('rand in de opening: regiepunt op de kolom van de poort, de slang komt bovenop Amir', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(14, 6, { vijand: 'groen', n: 2, regie: true, bij: 14 })] }));
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie', 20);
    await toets('ArrowLeft', false);
    const s0 = await st();
    await tot('!poortRegie', 20);
    await wacht(1.5);
    const s = await st();
    uit.push('(info) regie ' + r + ' levens ' + s0.lives + ' -> ' + s.lives + ' amir ' + s0.x + ' poort ' + lvl.poorten[0].x + ' eerste ' + JSON.stringify(s.eerste));
    return uit;
  });
  // ---- rand: drie schildbandieten met regie ----
  await check('rand drie schildmannen: regie met hek en drie schildbandieten, Amir niet geraakt in de regie', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(10, 6, { vijand: 'schildman', n: 3, hek: true, regie: true })] }));
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie', 20);
    const s0 = await st();
    const r2 = await tot('!poortRegie', 25);
    await toets('ArrowLeft', false);
    const s = await st();
    uit.push('(info) regie ' + r + '/' + r2 + ' duur ' + (s.t - s0.t).toFixed(1) + ' levens ' + s0.lives + ' -> ' + s.lives + ' eerste ' + JSON.stringify(s.eerste));
    if (s.lives < s0.lives) uit.push('Amir geraakt tijdens de regie');
    if (s.eerste.length !== 3) uit.push('niet drie schildmannen: ' + JSON.stringify(s.eerste));
    return uit;
  });
  // ---- rand: poort op een zwevende laag ----
  await check('rand zwever: poort op een zwevende laag, slang en bandiet komen op de laag', async () => {
    const uit = [];
    const lvl = await speel(grid({ teken: r => { for (let c = 9; c <= 15; c++) r[4][c] = 'F'; }, objecten: [poort(12, 3, { vijand: 'groen' }), poort(10, 3, { vijand: 'bandiet' }), zegel(18, 6, 12, 3), zegel(17, 6, 10, 3)] }));
    uit.push('(info) poorten ' + JSON.stringify(lvl.poorten) + ' spawns ' + JSON.stringify(lvl.spawns.filter(q => q.poort)));
    await loopTot(lvl.zegels[1].x + 10);
    await wacht(2.5);
    const s = await st();
    if (s.eerste.length < 2) uit.push('niet beide: ' + JSON.stringify(s.eerste));
    for (const v of s.eerste) if (Math.abs(v.b - 450) > 2) uit.push('niet op de laag (450): ' + JSON.stringify(v));
    return uit;
  });
  // ---- rand: dood tijdens de regie ----
  await check('rand dood in regie: Amir sterft tijdens de regie, na herstart begint de regie opnieuw en niets blijft hangen', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(10, 6, { vijand: 'schildman', hek: true, regie: true })] }));
    await toets('ArrowLeft', true);
    await tot('!!poortRegie', 20);
    await toets('ArrowLeft', false);
    await wacht(1);
    await page.evaluate(() => { lives = 1; invuln = 0; godMode = false; hurtPlayer(true); });
    await wacht(0.3);
    let s = await st();
    if (!s.dead) uit.push('niet dood: ' + JSON.stringify({ lives: s.lives, vast: s.vast }));
    await page.evaluate(() => restart());
    await wacht(0.3);
    s = await st();
    if (s.poorten[0].open || s.poorten[0].hekP) uit.push('poort niet dicht na herstart: ' + JSON.stringify(s.poorten));
    uit.push('(info) na herstart: regie ' + s.regie + ' vast ' + s.vast + ' x ' + s.x + ' vij ' + JSON.stringify(s.vij));
    await toets('ArrowLeft', true);
    const r = await tot('!!poortRegie', 20);
    const r2 = await tot('!poortRegie', 25);
    await toets('ArrowLeft', false);
    s = await st();
    if (r !== 'ok') uit.push('de regie begon niet opnieuw');
    if (r2 !== 'ok') uit.push('de regie eindigde niet');
    if (s.vast) uit.push('Amir staat nog vast');
    if (!s.vij.length) uit.push('geen schildman na de tweede regie');
    return uit;
  });
  // ---- rand: alleen poortvijanden, geen los vijand-object ----
  await check('rand standaardslang: een level met alleen een poortvijand krijgt geen losse slang erbij', async () => {
    const uit = [];
    const g = grid({ objecten: [poort(12, 6, { vijand: 'groen' }), zegel(18, 6, 12, 6)] });
    await page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); mkBewaarNu(); }, g);
    const lvl = await page.evaluate(() => mkNaarLevel());
    const los = lvl.spawns.filter(q => !q.poort);
    if (los.length) uit.push('losse spawns erbij: ' + JSON.stringify(los) + ' (ends ' + JSON.stringify(lvl.ends) + ')');
    return uit;
  });
  // ---- rand: het zegel en de poort op dezelfde cel ----
  await check('rand zegel op de poort: zegel op dezelfde cel als de poort', async () => {
    const uit = [];
    const lvl = await speel(grid({ objecten: [poort(12, 6, { vijand: 'scorp' }), zegel(12, 6, 12, 6)] }));
    await loopTot(lvl.zegels[0].x + 10);
    await wacht(2);
    const s = await st();
    uit.push('(info) open ' + s.poorten[0].open + ' eerste ' + JSON.stringify(s.eerste) + ' levens ' + s.lives);
    if (!s.eerste.length) uit.push('geen vijand');
    return uit;
  });

  console.log('\n' + (fouten ? fouten + ' controle(s) FOUT' : 'alles OK'));
  await browser.close(); srv.close();
})();
