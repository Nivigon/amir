#!/usr/bin/env node
// De makertest: kijkt na of de Level Maker nieuwstijl heel blijft.
//
// Hij laadt het echte spel in Chromium, opent de Maker en doet wat een maker doet: een grid met alles erop
// inladen, exporteren en weer inlezen (round-trip), het grid naar een spel-level vertalen, rijen invoegen,
// snel schilderen met de muis, ongedaan maken, de Test starten en weer teruggaan. Elke stap is een controle
// die OK of FOUT meldt, en aan het eind staat wat er in de console stond. Het laatste level gaat ook door
// tools/levelcheck.py. Hij verandert niets aan het spel.
//
//   node tools/makertest.js                alle controles
//   node tools/makertest.js --shots map    daarna een schermafdruk van de Maker en van de Test
//   node tools/makertest.js --alleen rij   alleen de controles waarvan de naam dit bevat
//
// Nodig: Node en Playwright, net als de speelrobot. Hij start zelf een webserver.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const os = require('os');
const { spawnSync } = require('child_process');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('makertest: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const shots = opt('--shots', null);
const alleen = opt('--alleen', '');

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

// Het proefgrid: klein, maar met elke soort erop. 24 breed, 12 hoog, grondlijn op rij 7.
//  - savanne op de grondlijn, met een ravijn (kolom 21 tot 23) boven een gang (rij 8 en 9, kolom 19 tot 23) achter de
//    start, met twee treden onder het gat (kolom 21 en 22) als weg naar boven
//    (het gat loopt een cel verder door dan de onderste trede, anders stoot Amir bij de sprong zijn hoofd tegen het dak)
//  - een lage rotsmesa (kolom 4 en 5, rij 6), een zwevende laag (kolom 16 tot 18, rij 4) met lucht eronder
//  - een muur door de grond (kolom 10, rij 6 en 7), sneeuw op kolom 0 en 1
//  - start op kolom 19, eind op kolom 2
//  - een zandslang, een bandiet met dolk, een platform met doel plus een tandwiel, een overhang, een richel,
//    een verborgen zegel met masker, een rune, een kalebas, een prop
//  - een masker (Verborgen1) van twee cellen, een zwarte cel, en een vrije blokvorm
function proefGrid(){
  const rijen = [];
  for (let r = 0; r < 12; r++) rijen.push('.'.repeat(24).split(''));
  for (let c = 0; c < 24; c++) rijen[7][c] = 'S';
  rijen[7][21] = 'V'; rijen[7][22] = 'V'; rijen[7][23] = 'V';
  for (let r = 8; r <= 9; r++) for (let c = 19; c <= 23; c++) rijen[r][c] = 'G';
  rijen[8][21] = 'R'; rijen[9][22] = 'R';
  for (let c = 4; c <= 5; c++) rijen[6][c] = 'R';
  for (let c = 16; c <= 18; c++) rijen[4][c] = 'F';
  rijen[6][10] = 'M'; rijen[7][10] = 'M';
  rijen[7][0] = 'W'; rijen[7][1] = 'W';
  return {
    type: 'amir-levelmaker-grid', versie: 2, cols: 24, rows: 12, groundRow: 7,
    grid: rijen.map(r => r.join('')),
    start: { c: 19, r: 6 }, eind: { c: 2, r: 6 }, muziek: 'darkafrica', valschade: true,
    maskers: [{ id: 'Verborgen1', look: 'grot', cells: [[8, 6], [9, 6]] }],
    vormen: [{ t: 'blok', x: 3.5, y: 2.5, w: 2, h: 1, rot: 0, seed: 0 }],
    zwart: [[7, 8]],
    objecten: [
      { c: 6, r: 6, k: 'vijand', soort: 'groen', note: 'proef', params: { speed: 2 } },
      { c: 7, r: 6, k: 'vijand', soort: 'bandiet:dolk', note: '' },
      { c: 13, r: 6, k: 'platform', doel: { c: 13, r: 3 }, breed: 2, note: '' },
      { c: 14, r: 5, k: 'tandwiel', modus: 'schakellift', platform: { c: 13, r: 6 }, note: '' },
      { c: 17, r: 6, k: 'overhang', breed: 3, dik: 2, fijn: 0, look: 'rots', note: '' },
      { c: 3, r: 5, k: 'richel', s: 0.5, f: true, dx: 10, dy: -5, note: '' },
      { c: 15, r: 6, k: 'zegel', masker: 'Verborgen1', verstop: true, note: '' },
      { c: 18, r: 6, k: 'rune', masker: 'Verborgen1', note: '' },
      { c: 19, r: 5, k: 'hppotion', note: '' },
      { c: 1, r: 6, k: 'prop', note: 'een boom' },
    ],
  };
}

// een sorteerbare, vergelijkbare vorm van een export (volgorde van lijsten maakt niet uit)
function canon(x){ if (Array.isArray(x)) return x.map(canon); if (x && typeof x === 'object'){ const o = {}; for (const k of Object.keys(x).sort()) if (x[k] !== undefined) o[k] = canon(x[k]); return o; } return x; }
function vorm(o){
  const s = canon(o);
  const key = x => JSON.stringify(x);
  for (const k of ['objecten', 'maskers', 'vormen', 'zwart']) if (Array.isArray(s[k])) s[k] = s[k].map(x => key(x)).sort();
  return s;
}
function verschil(a, b, pad = ''){
  const uit = [];
  if (typeof a !== typeof b || Array.isArray(a) !== Array.isArray(b)){ uit.push(pad + ': ' + JSON.stringify(a) + ' <> ' + JSON.stringify(b)); return uit; }
  if (a && typeof a === 'object'){
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) uit.push(...verschil(a[k], b[k], pad + '.' + k));
    return uit;
  }
  if (a !== b) uit.push(pad + ': ' + JSON.stringify(a) + ' <> ' + JSON.stringify(b));
  return uit;
}

(async () => {
  const srv = await server();
  const browser = await start();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const console_ = [];
  page.on('console', m => { if (m.type() === 'error' && !/ERR_CERT|ERR_NAME|ERR_INTERNET|ERR_PROXY|ERR_TUNNEL/.test(m.text())) console_.push(m.text()); });
  page.on('pageerror', e => console_.push('fout: ' + e.message));
  page.on('dialog', d => d.accept());                // de bevestigingen (wissen) en meldingen klikken we weg
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof mkOpen === 'function' && typeof mkNaarLevel === 'function');
  await page.waitForTimeout(1200);
  await page.evaluate(() => { try { localStorage.removeItem('amir-mk'); } catch (e){} mkOpen(); });

  const uitslag = [];
  let fouten = 0;
  async function check(naam, fn){
    if (alleen && naam.indexOf(alleen) < 0) return;
    let res;
    try { res = await fn(); } catch (e){ res = ['uitzondering: ' + (e && e.message || e)]; }
    const ok = !res || (Array.isArray(res) && !res.length);
    if (!ok) fouten++;
    uitslag.push((ok ? 'OK   ' : 'FOUT ') + naam + (ok ? '' : '\n      ' + (Array.isArray(res) ? res : [String(res)]).slice(0, 12).join('\n      ')));
  }
  const laad = grid => page.evaluate(g => { mkUitJSON(g); mkLegenda(); mkNotePaneel(); mkPassend(); if (typeof mkBewaarNu === 'function') mkBewaarNu(); else mkBewaar(); }, grid);
  // het midden van een cel in schermcoordinaten
  const celXY = (c, r) => page.evaluate(([c, r]) => { const b = mkCanvas.getBoundingClientRect(), cel = mkCel();
    return { x: b.left + MK.panX + (c + 0.5) * cel, y: b.top + MK.panY + (r + 0.5) * cel }; }, [c, r]);

  // 1. round-trip: wat erin gaat komt er gelijk uit, ook na een tweede ronde
  await check('round-trip: export en import geven hetzelfde grid', async () => {
    await laad(proefGrid());
    const a = await page.evaluate(() => mkNaarJSON());
    await page.evaluate(a => mkUitJSON(a), a);
    const b = await page.evaluate(() => mkNaarJSON());
    const uit = verschil(vorm(a), vorm(b));
    // en de inhoud van het proefgrid moet erin zitten: het grid zelf, de punten, de voorwerpen
    const p = proefGrid();
    if (JSON.stringify(a.grid) !== JSON.stringify(p.grid)) uit.push('grid-tekst anders dan het proefgrid');
    if (a.objecten.length !== p.objecten.length) uit.push('aantal voorwerpen: ' + a.objecten.length + ' in plaats van ' + p.objecten.length);
    if (!a.start || a.start.c !== 19 || !a.eind || a.eind.c !== 2) uit.push('start of eind kwijt');
    if (!a.maskers.length || a.maskers[0].cells.length !== 2) uit.push('masker kwijt');
    if (a.zwart.length !== 1 || a.vormen.length !== 1) uit.push('zwarte cel of vorm kwijt');
    const zegel = a.objecten.find(o => o.k === 'zegel'); if (!zegel || !zegel.verstop || zegel.masker !== 'Verborgen1') uit.push('zegel verloor verstop of masker');
    const wiel = a.objecten.find(o => o.k === 'tandwiel'); if (!wiel || !wiel.platform || wiel.platform.c !== 13) uit.push('tandwiel verloor zijn platform');
    const vij = a.objecten.find(o => o.k === 'vijand' && o.soort === 'groen'); if (!vij || !vij.params || vij.params.speed !== 2) uit.push('vijand verloor zijn snelheid');
    return uit;
  });

  // 2. de vertaling naar een spel-level
  await check('vertaling: gaps, terrassen, zwevers, gang, takel, vijanden, zegel', async () => {
    await laad(proefGrid());
    const lv = await page.evaluate(() => mkNaarLevel());
    const uit = [];
    const gat = (lv.gaps || []).find(g => g.w >= 500 && g.w <= 550);
    if (!gat) uit.push('geen gat van 3 cellen (525 px): ' + JSON.stringify(lv.gaps));
    if (!(lv.holtes || []).length) uit.push('geen gang');
    const mesa = (lv.terraces || []).find(t => t.h === 150 && t.af && !t.grond);
    if (!mesa) uit.push('geen rotsmesa van 1 cel hoog (150) met af: ' + JSON.stringify(lv.terraces));
    const door = (lv.terraces || []).find(t => t.door === 150);
    if (!door) uit.push('geen muur door de grond (door: 150)');
    const zw = (lv.zwevers || []).find(z => z.h === 450 && z.onder === 300);
    if (!zw) uit.push('geen zwevende laag (h 450, onder 300): ' + JSON.stringify(lv.zwevers));
    if (!(lv.takels || []).length || !lv.takels[0].wielen) uit.push('geen takel met wiel');
    const sp = lv.spawns || [];
    if (!sp.find(s => s.k === 'groen' && s.speed === 2)) uit.push('zandslang zonder snelheid 2: ' + JSON.stringify(sp));
    if (!sp.find(s => s.k === 'bandiet' && s.dolk)) uit.push('geen bandiet met dolk');
    if (!(lv.zegels || []).find(z => z.verstop && z.stuurt && z.stuurt[0] === 'Verborgen1')) uit.push('geen verborgen zegel aan het masker');
    if (!(lv.runes || []).length) uit.push('geen rune');
    if (!(lv.maskers || []).length) uit.push('geen masker');
    if (!(lv.ledges || []).length) uit.push('geen richel');
    if (!(lv.hppotions || []).length) uit.push('geen kalebas');
    if (!lv.sneeuw || lv.sneeuw.soort !== 'savanne') uit.push('geen sneeuwdek op de savanne');
    if (!(lv.vormen || []).length) uit.push('geen vormen (vrije vorm en zwarte cel)');
    if (lv.ends[0].x >= lv.start) uit.push('eind ligt niet links van de start');
    if (lv.speerInHand !== true || lv.view !== 0.8 || lv.zicht !== true) uit.push('basisvelden (speerInHand, view 0.8, zicht) kloppen niet');
    return uit;
  });

  // 3. rijen invoegen: alles schuift mee, ook maskers, zwarte cellen en vormen
  await check('rij boven erbij: masker, zwarte cel, vorm en voorwerpen schuiven mee', async () => {
    await laad(proefGrid());
    const voor = await page.evaluate(() => mkNaarLevel());
    await page.evaluate(() => mkRijBoven(1));
    const na = await page.evaluate(() => ({ lv: mkNaarLevel(), g: mkNaarJSON() }));
    const uit = [];
    if (na.g.rows !== 13 || na.g.groundRow !== 8) uit.push('maat of grondlijn klopt niet: ' + na.g.rows + ' rijen, grondlijn ' + na.g.groundRow);
    for (const k of ['maskers', 'vormen', 'zegels', 'spawns', 'takels', 'terraces', 'zwevers', 'holtes', 'ledges', 'hppotions']){
      const d = verschil(voor[k], na.lv[k], k); if (d.length) uit.push(...d.slice(0, 3));
    }
    if (na.g.zwart[0][1] !== 9) uit.push('zwarte cel niet mee: rij ' + na.g.zwart[0][1] + ' in plaats van 9');
    if (na.g.maskers[0].cells[0][1] !== 7) uit.push('masker-cel niet mee: rij ' + na.g.maskers[0].cells[0][1] + ' in plaats van 7');
    if (Math.abs(na.g.vormen[0].y - 3.5) > 1e-6) uit.push('vorm niet mee: y ' + na.g.vormen[0].y + ' in plaats van 3.5');
    // en weer weg: dat moet weer het begin geven
    await page.evaluate(() => mkRijBoven(-1));
    const terug = await page.evaluate(() => mkNaarJSON());
    uit.push(...verschil(vorm(proefGrid()), vorm({ ...terug, cel: undefined, legenda: undefined, type: undefined, versie: undefined }), 'terug').filter(s => !/\.(cel|legenda|type|versie)/.test(s)).slice(0, 4));
    return uit;
  });

  // 4. verkleinen: niets blijft buiten het raster hangen
  await check('verkleinen: maskers, zwarte cellen en doelen buiten het raster gaan netjes weg', async () => {
    await laad(proefGrid());
    await page.evaluate(() => { mkZetMaat(10, 9, 7); });
    const g = await page.evaluate(() => mkNaarJSON());
    const uit = [];
    for (const m of g.maskers) for (const p of m.cells) if (p[0] >= 10 || p[1] >= 9) uit.push('masker-cel buiten het raster: ' + p);
    for (const p of g.zwart) if (p[0] >= 10 || p[1] >= 9) uit.push('zwarte cel buiten het raster: ' + p);
    for (const o of g.objecten) if (o.c >= 10 || o.r >= 9) uit.push('voorwerp buiten het raster: ' + o.k + ' ' + o.c + ',' + o.r);
    const lv = await page.evaluate(() => mkNaarLevel());
    if (!lv) uit.push('geen level');
    return uit;
  });

  // 5. snel schilderen met de muis: geen gaten in de streek
  await check('schilderen: een snelle sleep laat geen cellen over', async () => {
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(24)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
    await page.evaluate(() => { MK.tool = 'rots'; mkLegenda(); });
    const a = await celXY(2, 3), b = await celXY(21, 3);
    await page.mouse.move(a.x, a.y); await page.mouse.down();
    await page.mouse.move(b.x, b.y, { steps: 2 });     // twee stappen: ver uit elkaar, zoals een snelle hand
    await page.mouse.up();
    const rij = await page.evaluate(() => MK.grid[3].slice(2, 22));
    const leeg = rij.filter(v => v !== 'rots').length;
    const uit = [];
    if (leeg) uit.push(leeg + ' van 20 cellen zijn niet geschilderd: ' + rij.map(v => v === 'rots' ? 'R' : '.').join(''));
    // en een diagonale streek
    await page.evaluate(() => { MK.tool = 'savanne'; });
    const c1 = await celXY(2, 9), c2 = await celXY(10, 1);
    await page.mouse.move(c1.x, c1.y); await page.mouse.down(); await page.mouse.move(c2.x, c2.y, { steps: 2 }); await page.mouse.up();
    const n = await page.evaluate(() => { let n = 0; for (const rij of MK.grid) for (const v of rij) if (v === 'savanne') n++; return n; });
    if (n < 9) uit.push('diagonale streek: maar ' + n + ' cellen savanne (minstens 9 verwacht)');
    return uit;
  });

  // 5b. een rechthoek vullen met Shift+slepen, ook met het masker
  await check('rechthoek: Shift+slepen vult het hele vlak', async () => {
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(24)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
    await page.evaluate(() => { MK.tool = 'muur'; mkLegenda(); });
    const a = await celXY(3, 2), b = await celXY(8, 6);
    await page.keyboard.down('Shift'); await page.mouse.move(a.x, a.y); await page.mouse.down(); await page.mouse.move(b.x, b.y, { steps: 3 }); await page.mouse.up(); await page.keyboard.up('Shift');
    const n = await page.evaluate(() => { let n = 0, buiten = 0; for (let r = 0; r < MK.rows; r++) for (let c = 0; c < MK.cols; c++) if (MK.grid[r][c] === 'muur'){ n++; if (c < 3 || c > 8 || r < 2 || r > 6) buiten++; } return { n, buiten }; });
    const uit = [];
    if (n.n !== 30 || n.buiten) uit.push('rechthoek 6x5: ' + n.n + ' cellen muur, ' + n.buiten + ' erbuiten');
    await page.evaluate(() => { MK.tool = 'masker'; MK.maskId = 'Verborgen1'; mkLegenda(); });
    const c1 = await celXY(10, 1), c2 = await celXY(12, 3);
    await page.keyboard.down('Shift'); await page.mouse.move(c1.x, c1.y); await page.mouse.down(); await page.mouse.move(c2.x, c2.y, { steps: 3 }); await page.mouse.up(); await page.keyboard.up('Shift');
    const mk = await page.evaluate(() => (MK.maskers[0] || { cells: [] }).cells.length);
    if (mk !== 9) uit.push('masker-rechthoek 3x3: ' + mk + ' cellen');
    return uit;
  });

  // 5bb. de vulemmer: Alt+klik vult een aaneengesloten vlak
  await check('vulemmer: Alt+klik vult het vlak en niet erbuiten', async () => {
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(24)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
    await page.evaluate(() => { for (let r = 2; r <= 6; r++){ MK.grid[r][5] = 'muur'; MK.grid[r][10] = 'muur'; } for (let c = 5; c <= 10; c++){ MK.grid[2][c] = 'muur'; MK.grid[6][c] = 'muur'; } mkTeken(); MK.tool = 'gang'; mkLegenda(); });   // een omlijnde doos van muur, 5 tot 10 bij 2 tot 6
    const p = await celXY(7, 4);
    await page.keyboard.down('Alt'); await page.mouse.click(p.x, p.y); await page.keyboard.up('Alt');
    const t = await page.evaluate(() => { let binnen = 0, buiten = 0; for (let r = 0; r < MK.rows; r++) for (let c = 0; c < MK.cols; c++) if (MK.grid[r][c] === 'gang'){ if (c > 5 && c < 10 && r > 2 && r < 6) binnen++; else buiten++; } return { binnen, buiten }; });
    return (t.binnen === 12 && t.buiten === 0) ? [] : ['gevuld: ' + t.binnen + ' binnen de doos (12 verwacht), ' + t.buiten + ' erbuiten'];
  });

  // 5c. een breed voorwerp aanklikken op zijn balk, niet alleen op zijn ankercel
  await check('selecteren: een platform van 2 breed is ook op zijn rechterhelft aan te klikken', async () => {
    await laad(proefGrid());
    await page.evaluate(() => { MK.tool = 'select'; mkLegenda(); MK.sel = null; });
    const p = await celXY(14, 6);                       // het platform staat op kolom 13, 2 breed: kolom 14 ligt op zijn balk
    await page.mouse.click(p.x, p.y);
    const sel = await page.evaluate(() => MK.sel && MK.sel.k);
    const uit = [];
    if (sel !== 'platform') uit.push('geselecteerd: ' + sel + ' in plaats van platform');
    const q = await celXY(16, 5);                       // de overhang staat op kolom 17, 3 breed en 2 dik: kolom 16, een rij hoger, ligt op zijn balk
    await page.mouse.click(q.x, q.y);
    const sel2 = await page.evaluate(() => MK.sel && MK.sel.k);
    if (sel2 !== 'overhang') uit.push('geselecteerd: ' + sel2 + ' in plaats van overhang');
    return uit;
  });

  // 5d. een gebied kopiëren, spiegelen en plakken, en knippen
  await check('gebied: Shift+slepen in Selecteren, kopiëren, spiegelen, plakken en knippen', async () => {
    await laad(proefGrid());
    await page.evaluate(() => { MK.tool = 'select'; mkLegenda(); });
    const a = await celXY(3, 4), b = await celXY(6, 7);              // de mesa (kolom 4 en 5, rij 6), de richel op (3,5), de zandslang op (6,6), de grond op rij 7
    await page.keyboard.down('Shift'); await page.mouse.move(a.x, a.y); await page.mouse.down(); await page.mouse.move(b.x, b.y, { steps: 3 }); await page.mouse.up(); await page.keyboard.up('Shift');
    const g = await page.evaluate(() => MK.gebied && mkGebiedNorm(MK.gebied));
    const uit = [];
    if (!g || g.c0 !== 3 || g.c1 !== 6 || g.r0 !== 4 || g.r1 !== 7) uit.push('gebied: ' + JSON.stringify(g));
    await page.mouse.move(a.x, a.y + 250);
    await page.keyboard.press('Control+c');
    const k = await page.evaluate(() => mkKlembord && { w: mkKlembord.w, h: mkKlembord.h, obj: mkKlembord.objects.map(o => o.k + '@' + o.dc + ',' + o.dr).sort(), cel: mkKlembord.cells[2].join(' ') });
    if (!k || k.w !== 4 || k.h !== 4) uit.push('klembord: ' + JSON.stringify(k));
    if (!k || k.obj.join('|') !== 'richel@0,1|vijand@3,2') uit.push('voorwerpen op het klembord: ' + (k && k.obj.join('|')));
    if (!k || k.cel !== 'lucht rots rots lucht') uit.push('cellen op het klembord: ' + (k && k.cel));
    await page.keyboard.press('h');                                    // spiegelen: de mesa blijft in het midden, de richel gaat naar rechts
    const k2 = await page.evaluate(() => ({ obj: mkKlembord.objects.map(o => o.k + '@' + o.dc + ',' + o.dr + (o.f ? 'f' : '')).sort().join('|') }));
    if (k2.obj !== 'richel@3,1|vijand@0,2') uit.push('na spiegelen: ' + k2.obj);
    await page.keyboard.press('Control+v');
    const doel = await celXY(14, 0);                                   // de stempel op (14,0): rij 0 tot 3, kolom 14 tot 17 (lucht, geen voorwerpen)
    await page.mouse.move(doel.x, doel.y); await page.mouse.click(doel.x, doel.y);
    const na = await page.evaluate(() => ({ cel: MK.grid[2].slice(14, 18).join(' '), obj: MK.objects.filter(o => o.c >= 14 && o.c <= 17 && o.r >= 0 && o.r <= 3).map(o => o.k + '@' + o.c + ',' + o.r + (o.f ? 'f' : '')).sort().join('|'), plak: mkPlak, n: MK.objects.length }));
    if (na.cel !== 'lucht rots rots lucht') uit.push('geplakte cellen: ' + na.cel);
    if (na.obj !== 'richel@17,1|vijand@14,2') uit.push('geplakte voorwerpen: ' + na.obj);
    if (na.plak) uit.push('de stempel bleef hangen na het neerzetten');
    if (na.n !== 12) uit.push('aantal voorwerpen na plakken: ' + na.n + ' in plaats van 12');
    // knippen: het gebied is nu het geplakte stuk; Ctrl+X maakt het leeg
    await page.keyboard.press('Control+x');
    const leeg = await page.evaluate(() => ({ cel: MK.grid[2].slice(14, 18).join(' '), n: MK.objects.length }));
    if (leeg.cel !== 'lucht lucht lucht lucht' || leeg.n !== 10) uit.push('na knippen: ' + JSON.stringify(leeg));
    await page.keyboard.press('Control+z');
    const terug = await page.evaluate(() => MK.objects.length);
    if (terug !== 12) uit.push('ongedaan maken na knippen: ' + terug + ' voorwerpen in plaats van 12');
    return uit;
  });

  // 5e. de minimap en Test vanaf hier
  await check('minimap: klikken brengt die plek in beeld; Test vanaf hier start op het gebied', async () => {
    await laad(proefGrid());
    const uit = [];
    const mini = await page.evaluate(() => { const m = document.getElementById('mkmini'); const b = m.getBoundingClientRect(); return { w: m.width, h: m.height, x: b.left, y: b.top, bw: b.width, bh: b.height, zicht: getComputedStyle(m).display !== 'none' }; });
    if (!mini.zicht || mini.w < 40) uit.push('geen minimap: ' + JSON.stringify(mini));
    await page.evaluate(() => { MK.zoom = 2.5; mkTeken(); });
    await page.mouse.click(mini.x + mini.bw * (22.5 / 24), mini.y + mini.bh * (8.5 / 12));   // op cel (22, 8)
    const mid = await page.evaluate(() => { const cel = mkCel(); return { c: (mkCanvas.clientWidth / 2 - MK.panX) / cel, r: (mkCanvas.clientHeight / 2 - MK.panY) / cel }; });
    if (Math.abs(mid.c - 22.5) > 0.6 || Math.abs(mid.r - 8.5) > 0.6) uit.push('na de klik op de minimap staat cel ' + mid.c.toFixed(1) + ',' + mid.r.toFixed(1) + ' in het midden in plaats van 22.5,8.5');
    await page.keyboard.press('m');
    const weg = await page.evaluate(() => document.getElementById('mkmini').classList.contains('dicht'));
    if (!weg) uit.push('M verbergt de minimap niet');
    await page.keyboard.press('m');
    // Test vanaf hier: het gebied op kolom 6 (de zandslang), Amir begint daar
    await page.evaluate(() => { MK.gebied = { c0: 6, r0: 6, c1: 6, r1: 6 }; MK.inspectDicht = false; mkNotePaneel(); });
    const lv = await page.evaluate(() => mkNaarLevel({ vanaf: { c: 6, r: 6 } }));
    if (lv.start !== 87 && lv.start !== 88) uit.push('start met vanaf kolom 6: ' + lv.start + ' (het midden van kolom 6 verwacht, 87)');
    const slang = lv.spawns.find(s => s.k === 'groen'); if (!slang || Math.abs(slang.x - lv.start) > 1) uit.push('de zandslang op kolom 6 staat niet op de start: ' + JSON.stringify(slang));
    if (!(lv.rechtsWall > 0)) uit.push('zonder rechtsWall valt de echte start (rechts van hier) buiten de grens');
    await page.click('#mktestvanaf');
    await page.waitForTimeout(600);
    const st = await page.evaluate(() => ({ running, mkTestActief, start: level && level.start }));
    if (!st.running || !st.mkTestActief) uit.push('Test vanaf hier draait niet: ' + JSON.stringify(st));
    await page.click('#mkterug'); await page.waitForTimeout(200);
    return uit;
  });

  // 6. ongedaan maken en opnieuw
  await check('ongedaan maken: Ctrl+Z haalt een streek weg, Ctrl+Y zet hem terug', async () => {
    await laad(proefGrid());
    const uit = [];
    const heeft = await page.evaluate(() => typeof mkOngedaan === 'function');
    if (!heeft) return ['er is geen mkOngedaan'];
    const voor = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    await page.evaluate(() => { MK.tool = 'muur'; mkLegenda(); });
    const a = await celXY(5, 2), b = await celXY(9, 2);
    await page.mouse.move(a.x, a.y); await page.mouse.down(); await page.mouse.move(b.x, b.y, { steps: 6 }); await page.mouse.up();
    await page.waitForTimeout(100);
    const na = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    if (na === voor) uit.push('de streek veranderde niets');
    await page.mouse.move(a.x, a.y + 300);                // de muis van de cel af, zodat de toets niet het veld raakt
    await page.keyboard.press('Control+z');
    await page.waitForTimeout(50);
    const terug = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    if (terug !== voor) uit.push('na Ctrl+Z is het grid niet terug zoals het was');
    await page.keyboard.press('Control+y');
    await page.waitForTimeout(50);
    const opnieuw = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    if (opnieuw !== na) uit.push('na Ctrl+Y is de streek niet terug');
    // een voorwerp weghalen en terughalen
    await page.evaluate(() => { MK.tool = 'select'; mkLegenda(); MK.sel = MK.objects.find(o => o.k === 'rune'); mkNotePaneel(); mkTeken(); });
    await page.keyboard.press('Delete');
    await page.waitForTimeout(50);
    const zonder = await page.evaluate(() => MK.objects.some(o => o.k === 'rune'));
    if (zonder) uit.push('Delete haalde de rune niet weg');
    await page.keyboard.press('Control+z');
    await page.waitForTimeout(50);
    const met = await page.evaluate(() => MK.objects.some(o => o.k === 'rune'));
    if (!met) uit.push('Ctrl+Z bracht de rune niet terug');
    // de zoom blijft staan bij ongedaan maken
    const zoomVoor = await page.evaluate(() => MK.zoom);
    await page.keyboard.press('Control+y');
    const zoomNa = await page.evaluate(() => MK.zoom);
    if (zoomVoor !== zoomNa) uit.push('de zoom sprong bij opnieuw');
    return uit;
  });

  // 6b. de vijand-knoppen: een vinkje gaat als true/false mee, een schuifje als getal, en de standaard gaat niet mee
  await check('vijand-knoppen: vault uit, panter over, twee hyena\'s en zicht uit komen op de spawn', async () => {
    const g = proefGrid();
    g.objecten = [
      { c: 6, r: 6, k: 'vijand', soort: 'bandiet', params: { vault: 0 }, note: '' },
      { c: 8, r: 6, k: 'vijand', soort: 'panter', params: { over: 1, zicht: 0 }, note: '' },
      { c: 12, r: 6, k: 'vijand', soort: 'hyenas', params: { n: 2 }, note: '' },
      { c: 14, r: 6, k: 'vijand', soort: 'scorp', params: { zicht: 1 }, note: '' },
    ];
    await laad(g);
    const sp = await page.evaluate(() => mkNaarLevel().spawns);
    const uit = [];
    const b = sp.find(x => x.k === 'bandiet'), pa = sp.find(x => x.k === 'panter'), h = sp.find(x => x.k === 'hyenas'), sc = sp.find(x => x.k === 'scorp');
    if (!b || b.vault !== false) uit.push('bandiet: vault ' + JSON.stringify(b && b.vault) + ' in plaats van false');
    if (!pa || pa.over !== true || pa.zicht !== false) uit.push('panter: ' + JSON.stringify(pa));
    if (!h || h.n !== 2) uit.push('hyenas: ' + JSON.stringify(h));
    if (!sc || 'zicht' in sc) uit.push('schorpioen met de standaard zicht hoort geen zicht-veld te krijgen: ' + JSON.stringify(sc));
    // en in het spel: readLevel leest ze zo
    const lv = await page.evaluate(() => { const l = readLevel(JSON.stringify(mkNaarLevel())); return l.spawns.map(x => ({ kind: x.kind, vault: x.vault, over: x.over, zicht: x.zicht, n: x.n })); });
    const lb = lv.find(x => x.kind === 'bandiet'), lp = lv.find(x => x.kind === 'panter'), lh = lv.find(x => x.kind === 'hyenas');
    if (!lb || lb.vault !== false) uit.push('readLevel: bandiet vault ' + JSON.stringify(lb));
    if (!lp || lp.over !== true || lp.zicht !== false) uit.push('readLevel: panter ' + JSON.stringify(lp));
    if (!lh || lh.n !== 2) uit.push('readLevel: hyenas ' + JSON.stringify(lh));
    // het paneel toont een vinkje voor de bandiet
    await page.evaluate(() => { MK.tool = 'select'; MK.sel = MK.objects[0]; MK.inspectDicht = false; mkNotePaneel(); });
    const vink = await page.evaluate(() => document.querySelectorAll('#mkvijknop input[type=checkbox]').length);
    if (vink < 2) uit.push('het paneel van de bandiet toont ' + vink + ' vinkjes (vault en zicht verwacht)');
    return uit;
  });

  // 7. de controle: een grid met fouten geeft meldingen, het proefgrid geeft geen fout
  await check('controle: meldingen bij een start zonder vloer en een platform zonder doel', async () => {
    const heeft = await page.evaluate(() => typeof mkControle === 'function');
    if (!heeft) return ['er is geen mkControle'];
    const uit = [];
    await laad(proefGrid());
    const goed = await page.evaluate(() => mkControle());
    const fout = goed.filter(m => m.ernst === 'fout');
    if (fout.length) uit.push('het proefgrid geeft een fout: ' + fout.map(m => m.tekst).join(' | '));
    const slecht = proefGrid();
    slecht.start = { c: 10, r: 6 };                      // boven het ravijn
    slecht.objecten.find(o => o.k === 'platform').doel = null;
    slecht.eind = null;
    await laad(slecht);
    const m = await page.evaluate(() => mkControle());
    const t = m.map(x => x.tekst).join(' | ');
    if (!m.some(x => /start/i.test(x.tekst) && x.ernst === 'fout')) uit.push('geen fout over de start zonder vloer: ' + t);
    if (!m.some(x => /platform/i.test(x.tekst))) uit.push('geen melding over het platform zonder doel: ' + t);
    if (!m.some(x => /eind/i.test(x.tekst))) uit.push('geen melding over het ontbrekende eind: ' + t);
    return uit;
  });

  // 8. de Test starten en teruggaan, zonder fouten in de console en met het grid nog heel
  await check('test: het level speelt twee seconden zonder fout, en terug is het grid heel', async () => {
    await laad(proefGrid());
    const voor = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    const n0 = console_.length;
    await page.click('#mktest');
    await page.waitForTimeout(2200);
    const st = await page.evaluate(() => ({ running, mkTestActief, makerOpen, naam: level && level.name, speer: !!(level && level.speerInHand) }));
    const uit = [];
    if (!st.running || !st.mkTestActief || st.makerOpen) uit.push('de test draait niet: ' + JSON.stringify(st));
    if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, 'maker-test.png') }); }
    await page.click('#mkterug');
    await page.waitForTimeout(200);
    const st2 = await page.evaluate(() => ({ running, mkTestActief, makerOpen, json: JSON.stringify(mkNaarJSON()) }));
    if (st2.running || st2.mkTestActief || !st2.makerOpen) uit.push('terug in de Maker klopt niet: ' + JSON.stringify({ running: st2.running, mkTestActief: st2.mkTestActief, makerOpen: st2.makerOpen }));
    if (st2.json !== voor) uit.push('het grid is na de test anders');
    if (console_.length > n0) uit.push('console tijdens de test: ' + console_.slice(n0).join(' | '));
    if (shots) await page.screenshot({ path: path.join(shots, 'maker.png') });
    return uit;
  });

  // 9. de autosave: na een herlaad van de Maker staat het grid er nog
  await check('autosave: het grid komt terug na sluiten en openen', async () => {
    await laad(proefGrid());
    await page.evaluate(() => { if (typeof mkBewaarNu === 'function') mkBewaarNu(); else mkBewaar(); });
    const voor = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    await page.evaluate(() => { mkDicht(); mkOpen(); });
    const na = await page.evaluate(() => JSON.stringify(mkNaarJSON()));
    return voor === na ? [] : ['het grid is na heropenen anders'];
  });

  // 10. het spel-level door levelcheck.py
  await check('levelcheck: het proefgrid als spel-level geeft geen FOUT', async () => {
    await laad(proefGrid());
    const lv = await page.evaluate(() => mkNaarLevel());
    const f = path.join(os.tmpdir(), 'makertest-level.json');
    fs.writeFileSync(f, JSON.stringify(lv));
    const r = spawnSync('python3', [path.join(ROOT, 'tools', 'levelcheck.py'), f], { encoding: 'utf8' });
    const tekst = (r.stdout || '') + (r.stderr || '');
    const fouten = tekst.split('\n').filter(l => /FOUT/.test(l));
    return fouten.length ? fouten.slice(0, 6) : (r.status === 0 || /OK|LET OP|geen/i.test(tekst) ? [] : ['levelcheck gaf status ' + r.status + ': ' + tekst.slice(0, 300)]);
  });

  console.log(uitslag.join('\n'));
  if (console_.length){ console.log('\nconsole:'); for (const c of console_) console.log('  ' + c); }
  console.log('\n' + (fouten ? fouten + ' controle(s) FOUT' : 'alles OK'));
  await browser.close(); srv.close();
  process.exit(fouten ? 1 : 0);
})();
