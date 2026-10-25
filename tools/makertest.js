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
//    een verborgen zegel met masker dat ook een rijzer stuurt, een onzichtbaar zegel op het dak van de gang,
//    een rune, een kalebas, een prop
//  - een tweede ravijn (kolom 11 en 12) met een rijzer van 2 breed erin, drie cellen diep, die tot de grondlijn komt
//  - een masker (Verborgen1) van twee cellen, een zwarte cel, en een vrije blokvorm
//  - een gespiegelde stenen poort in savannekleur (kolom 16) met twee schorpioenen erin, die de rune opent
function proefGrid(){
  const rijen = [];
  for (let r = 0; r < 12; r++) rijen.push('.'.repeat(24).split(''));
  for (let c = 0; c < 24; c++) rijen[7][c] = 'S';
  rijen[7][21] = 'V'; rijen[7][22] = 'V'; rijen[7][23] = 'V';
  rijen[7][11] = 'V'; rijen[7][12] = 'V';
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
      { c: 3, r: 5, k: 'richel', s: 0.5, f: true, dx: 10, dy: -5, look: 'sneeuw', note: '' },
      { c: 15, r: 6, k: 'zegel', masker: 'Verborgen1', verstop: true, rijzer: { c: 11, r: 10 }, note: '' },
      { c: 11, r: 10, k: 'rijzer', doel: { c: 11, r: 7 }, breed: 2, v: 300, wacht: 0, duur: 0, note: '' },
      { c: 18, r: 6, k: 'rune', masker: 'Verborgen1', poort: { c: 16, r: 6 }, note: '' },
      { c: 16, r: 6, k: 'poort', boog: 'boog_steen', f: true, look: 'savanne', vijand: 'scorp', n: 2, note: '' },
      { c: 19, r: 5, k: 'hppotion', note: '' },
      { c: 20, r: 6, k: 'zegel', onzichtbaar: true, note: '' },
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
    const onz = a.objecten.find(o => o.k === 'zegel' && o.onzichtbaar); if (!onz || onz.verstop) uit.push('onzichtbaar zegel kwijt of ook verstopt');
    const zegel = a.objecten.find(o => o.k === 'zegel'); if (!zegel || !zegel.verstop || zegel.masker !== 'Verborgen1') uit.push('zegel verloor verstop of masker');
    const wiel = a.objecten.find(o => o.k === 'tandwiel'); if (!wiel || !wiel.platform || wiel.platform.c !== 13) uit.push('tandwiel verloor zijn platform');
    const rz = a.objecten.find(o => o.k === 'rijzer'); if (!rz || !rz.doel || rz.doel.r !== 7 || rz.breed !== 2) uit.push('rijzer verloor zijn doel of breedte');
    if (!zegel || !zegel.rijzer || zegel.rijzer.c !== 11 || zegel.rijzer.r !== 10) uit.push('zegel verloor zijn rijzer');
    const vij = a.objecten.find(o => o.k === 'vijand' && o.soort === 'groen'); if (!vij || !vij.params || vij.params.speed !== 2) uit.push('vijand verloor zijn snelheid');
    const pt = a.objecten.find(o => o.k === 'poort'); if (!pt || pt.boog !== 'boog_steen' || !pt.f || pt.look !== 'savanne' || pt.vijand !== 'scorp' || pt.n !== 2) uit.push('poort verloor zijn boog, spiegeling of vijanden: ' + JSON.stringify(pt));
    const ru = a.objecten.find(o => o.k === 'rune'); if (!ru || !ru.poort || ru.poort.c !== 16 || ru.poort.r !== 6) uit.push('rune verloor zijn poort');
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
    const rz = (lv.rijzers || [])[0];
    if (!rz || rz.r - rz.l !== 350 || rz.van !== -450 || rz.tot !== -1) uit.push('geen rijzer van 2 cellen (350 px), van -450 tot -1: ' + JSON.stringify(lv.rijzers));
    else { if (!(lv.gaps || []).some(g => Math.abs(g.x - g.w / 2 - rz.l) < 1 && Math.abs(g.x + g.w / 2 - rz.r) < 1)) uit.push('de rijzer sluit niet op zijn ravijn aan: ' + JSON.stringify(rz) + ' ' + JSON.stringify(lv.gaps));
      if (!(lv.zegels || []).some(z => z.rijs === rz.id)) uit.push('geen zegel dat de rijzer stuurt: ' + JSON.stringify(lv.zegels)); }
    const sp = lv.spawns || [];
    if (!sp.find(s => s.k === 'groen' && s.speed === 2)) uit.push('zandslang zonder snelheid 2: ' + JSON.stringify(sp));
    if (!sp.find(s => s.k === 'bandiet' && s.dolk)) uit.push('geen bandiet met dolk');
    if (!(lv.zegels || []).find(z => z.verstop && z.stuurt && z.stuurt[0] === 'Verborgen1')) uit.push('geen verborgen zegel aan het masker');
    if (!(lv.zegels || []).find(z => z.onzichtbaar && !z.verstop && z.dak)) uit.push('geen onzichtbaar zegel op het dak: ' + JSON.stringify(lv.zegels));
    if (!(lv.runes || []).length) uit.push('geen rune');
    const pt = (lv.poorten || [])[0];
    if (!pt || pt.id !== 'b1' || pt.k !== 'boog_steen' || !pt.f || pt.look !== 'savanne' || pt.y !== undefined) uit.push('geen gespiegelde poort b1 op de grond: ' + JSON.stringify(lv.poorten));
    else {
      const uitP = sp.filter(s => s.poort === 'b1');
      if (uitP.length !== 2 || uitP.some(s => s.k !== 'scorp' || s.x !== pt.x)) uit.push('niet twee schorpioenen in poort b1: ' + JSON.stringify(uitP));
      if (!(lv.runes || []).some(r => r.poort === 'b1')) uit.push('geen rune die poort b1 opent: ' + JSON.stringify(lv.runes));
    }
    if (!(lv.maskers || []).length) uit.push('geen masker');
    if (!(lv.ledges || []).length) uit.push('geen richel');
    else if (lv.ledges[0].look !== 'sneeuw') uit.push('de richel heeft zijn kleur (sneeuw) niet mee: ' + JSON.stringify(lv.ledges[0]));
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
    for (const k of ['maskers', 'vormen', 'zegels', 'spawns', 'takels', 'rijzers', 'terraces', 'zwevers', 'holtes', 'ledges', 'hppotions']){
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
    if (na.n !== 15) uit.push('aantal voorwerpen na plakken: ' + na.n + ' in plaats van 15');
    // knippen: het gebied is nu het geplakte stuk; Ctrl+X maakt het leeg
    await page.keyboard.press('Control+x');
    const leeg = await page.evaluate(() => ({ cel: MK.grid[2].slice(14, 18).join(' '), n: MK.objects.length }));
    if (leeg.cel !== 'lucht lucht lucht lucht' || leeg.n !== 13) uit.push('na knippen: ' + JSON.stringify(leeg));
    await page.keyboard.press('Control+z');
    const terug = await page.evaluate(() => MK.objects.length);
    if (terug !== 15) uit.push('ongedaan maken na knippen: ' + terug + ' voorwerpen in plaats van 15');
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

  // 6a. het palet: elk gereedschap en elke vijand-soort staat ergens in de boom, de linkerkolom laat de groep van het
  // gereedschap open zien, en het menu onder een categorie klapt per groep opzij uit (Vijanden, Bandieten, Bandiet)
  await check('palet: elke tool en vijand staat in de boom, de kolom en de flyouts volgen de groepen', async () => {
    return page.evaluate(() => {
      const f = [];
      for (const t of MK_TYPES) if (t.id !== 'select' && t.id !== 'lucht' && t.id !== 'vijand' && !mkPaletZoek(t.id)) f.push('niet in het palet: ' + t.id);
      for (const soort in MK_VIJ_INFO) if (!mkPaletZoek('vijand', soort)) f.push('vijand niet in het palet: ' + soort);
      MK.cat = 'vijanden'; MK.sub = null; MK.tool = 'vijand'; MK.vijandSoort = 'bandiet:dolk'; mkLegenda();
      const rijen = [...document.querySelectorAll('#mklegbtns button')].map(b => b.textContent.trim());
      if (!rijen.some(t => t.endsWith('Met dolk'))) f.push('de kolom laat de open groep van het gereedschap niet zien: ' + rijen.join(' | '));
      if (rijen.some(t => t.endsWith('Zandslang'))) f.push('een dichte groep laat zijn items zien');
      const aan = document.querySelector('#mklegbtns button.on'); if (!aan || !aan.textContent.includes('Met dolk')) f.push('het gekozen gereedschap is niet aangezet in de kolom');
      const knop = [...document.querySelectorAll('#mkcatbar button')].find(b => b.textContent === 'Vijanden');
      mkMenuToon(mkPaletKnoopOp(['vijanden']), knop);
      const r1 = [...document.querySelectorAll('#mkmenu button')].find(b => b.textContent.includes('Bandieten')); if (!r1) f.push('geen groep Bandieten in het menu');
      if (r1){ r1.dispatchEvent(new Event('mouseenter')); const l1 = mkMenuLagen[1]; if (!l1 || !l1.classList.contains('on')) f.push('de flyout van Bandieten gaat niet open');
        const r2 = l1 && [...l1.querySelectorAll('button')].find(b => b.textContent.includes('Bandiet') && !b.textContent.includes('Schild'));
        if (r2){ r2.dispatchEvent(new Event('mouseenter')); const l2 = mkMenuLagen[2]; if (!l2 || !l2.classList.contains('on')) f.push('de flyout van Bandiet gaat niet open');
          const r3 = l2 && [...l2.querySelectorAll('button')].find(b => b.textContent.includes('Elite')); if (r3) r3.click(); else f.push('geen Elite in de flyout van Bandiet');
          if (MK.vijandSoort !== 'bandiet:elite') f.push('kiezen in de flyout zet de soort niet: ' + MK.vijandSoort);
          if (document.querySelectorAll('.mkmenu.on').length) f.push('na het kiezen staat er nog een menu open'); } }
      MK.tool = 'select'; MK.cat = 'terrein'; MK.sub = null; mkMenuSluit(); mkLegenda();
      return f;
    });
  });
  // 6a2. de maat: geen groep in het palet en geen paneel met meer dan MK_PALET_MAX rijen, en geen gereedschap zonder
  // groep (dan stond hij in Overig). Ook andersom: de klachten komen echt als je het fout doet.
  await check('maat: geen lijst in het palet of het paneel langer dan MK_PALET_MAX, en de klacht komt als het wel zo is', async () => {
    return page.evaluate(() => {
      const f = mkPaletKlachten().slice();
      MK.inspectDicht = false; MK.tool = 'select';
      const soorten = ['vijand', 'zegel', 'rune', 'prop', 'platform', 'tandwiel', 'rijzer', 'poort', 'overhang', 'richel', 'hppotion'];
      const bewaar = MK.objects;
      for (const k of soorten){
        const o = { c:5, r:MK.ground - 1, k, note:'' };
        if (k === 'vijand') o.soort = 'groen';
        if (k === 'poort'){ o.hek = true; o.regie = true; o.wand = 'spits'; o.vijand = 'groen'; }   // alles in gebruik: elk kopje open
        if (k === 'rijzer'){ o.look = 'rots'; o.kleur = { r:MK.ground - 3 }; }
        MK.objects = [o]; MK.sel = o; mkNotePaneel();
        for (const m of mkPaneelKlachten()) f.push(k + ': ' + m);
      }
      // andersom: een paneel met te veel losse rijen moet een klacht geven
      const extra = []; for (let i = 0; i <= MK_PALET_MAX; i++){ const d = document.createElement('div'); d.className = 'mkveld'; d.textContent = 'proef'; document.getElementById('mkinspbody').appendChild(d); extra.push(d); }
      if (!mkPaneelKlachten().length) f.push('een paneel met te veel rijen geeft geen klacht');
      for (const d of extra) d.remove();
      MK.objects = bewaar; MK.sel = null; mkNotePaneel();
      // en een gereedschap zonder groep, of een te volle groep, ook
      const t = { id:'proefding', naam:'Proefding', kleur:'#fff', obj:true };
      MK_TYPES.push(t); let k = mkPaletKlachten({ items: mkPaletBoom() });
      if (!k.some(m => m.includes('Overig') && m.includes('Proefding'))) f.push('een gereedschap zonder groep geeft geen klacht: ' + k.join(' | '));
      t.groep = 'terrein/grond'; const meer = []; for (let i = 0; i < MK_PALET_MAX; i++){ const q = { id:'proef' + i, naam:'Proef ' + i, kleur:'#fff', obj:true, groep:'terrein/grond' }; MK_TYPES.push(q); meer.push(q); }
      k = mkPaletKlachten({ items: mkPaletBoom() });
      if (!k.some(m => m.includes('terrein/grond') && m.includes('splits'))) f.push('een te volle groep geeft geen klacht: ' + k.join(' | '));
      t.groep = 'terrein/nieuw'; k = mkPaletKlachten({ items: mkPaletBoom() });
      if (!k.some(m => m.includes('terrein/nieuw') && m.includes('MK_GROEPEN'))) f.push('een groep zonder naam geeft geen klacht: ' + k.join(' | '));
      MK_TYPES.splice(MK_TYPES.indexOf(t), 1); for (const q of meer) MK_TYPES.splice(MK_TYPES.indexOf(q), 1);
      return f;
    });
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

  // 5e. een rijzer van even breedte spiegelen: zijn cellen blijven op hun plek in het gebied, en het zegel blijft eraan gekoppeld
  await check('rijzer: spiegelen houdt zijn cellen en de koppeling met het zegel heel', async () => {
    await laad(proefGrid());
    const r = await page.evaluate(() => {
      MK.gebied = { c0: 11, r0: 6, c1: 15, r1: 10 }; mkKopieer(); mkSpiegel();            // de rijzer op (11,10) en het zegel op (15,6), 5 cellen breed
      const rz = mkKlembord.objects.find(o => o.k === 'rijzer'), z = mkKlembord.objects.find(o => o.k === 'zegel');
      const uit = { rz: rz && { dc: rz.dc, dr: rz.dr }, rel: z && z.rijsRel };
      mkPlak = { c: 0, r: 0 }; mkPlakZet();                                                 // plakken linksboven, waar niets staat
      const pz = MK.objects.find(o => o.k === 'zegel' && o.c === 0 && o.r === 0), pr = MK.objects.find(o => o.k === 'rijzer' && o.r === 4);
      uit.plak = { zegel: !!pz, rijzer: pr && pr.c, cellen: pr && mkRijsCellen(pr), gekoppeld: !!(pz && pr && mkRijsVan(pz) === pr) };
      const lv = mkNaarLevel(); uit.n = (lv.rijzers || []).length; uit.rijs = (lv.zegels || []).map(z => z.rijs).filter(Boolean).sort();
      return uit;
    });
    const uit = [];
    if (!r.rz || r.rz.dc !== 3 || r.rz.dr !== 4) uit.push('rijzer na spiegelen op ' + JSON.stringify(r.rz) + ' in plaats van (3,4): een even breedte schuift een cel');
    if (!r.rel || r.rel.dc !== 3 || r.rel.dr !== 4) uit.push('koppeling zegel -> rijzer na spiegelen: ' + JSON.stringify(r.rel));
    if (!r.plak.zegel || r.plak.rijzer !== 3 || !r.plak.gekoppeld) uit.push('na plakken: ' + JSON.stringify(r.plak));
    if (r.plak.cellen && (r.plak.cellen[0] !== 3 || r.plak.cellen[1] !== 4)) uit.push('de geplakte rijzer beslaat ' + r.plak.cellen + ' in plaats van 3,4');
    if (r.n !== 2 || r.rijs.join() !== 'r1,r2') uit.push('export na plakken: ' + r.n + ' rijzers, zegels sturen ' + r.rijs.join());
    return uit;
  });

  // 5f. een poort met zijn rune kopiëren en spiegelen: de poort kijkt de andere kant op en de rune blijft hem openen
  await check('poort: spiegelen en plakken houdt de koppeling met de rune heel', async () => {
    await laad(proefGrid());
    const r = await page.evaluate(() => {
      MK.gebied = { c0: 16, r0: 6, c1: 18, r1: 6 }; mkKopieer(); mkSpiegel();
      mkPlak = { c: 0, r: 0 }; mkPlakZet();
      const pp = MK.objects.find(o => o.k === 'poort' && o.r === 0), pr = MK.objects.find(o => o.k === 'rune' && o.r === 0);
      const lv = mkNaarLevel();
      return { poort: pp && { c: pp.c, f: !!pp.f }, rune: pr && pr.c, gekoppeld: !!(pp && pr && mkPoortVan(pr) === pp),
               ids: (lv.poorten || []).map(o => o.id), opent: (lv.runes || []).map(o => o.poort).filter(Boolean).sort(),
               spawns: (lv.spawns || []).filter(s => s.poort).map(s => s.poort).sort() };
    });
    const uit = [];
    if (!r.poort || r.poort.c !== 2 || r.poort.f) uit.push('de geplakte poort: ' + JSON.stringify(r.poort) + ' (verwacht kolom 2, niet gespiegeld)');
    if (r.rune !== 0 || !r.gekoppeld) uit.push('de geplakte rune is niet aan de geplakte poort gekoppeld: ' + JSON.stringify(r));
    if (r.ids.join() !== 'b1,b2' || r.opent.join() !== 'b1,b2' || r.spawns.join() !== 'b1,b1,b2,b2') uit.push('export na plakken: ' + JSON.stringify(r));
    return uit;
  });

  // 5g. een poort met hek, regie en een rotswand: de knop Poort met hek, de round-trip, de vertaling, spiegelen en levelcheck
  await check('poort met hek: hek, regie met regiepunt, rotswand en schaal gaan mee, ook gespiegeld', async () => {
    const g = proefGrid();
    g.objecten.push({ c: 14, r: 6, k: 'poort', boog: 'boog_rots', vijand: 'schildman', hek: true, regie: true, bij: 12, s: 1.2,
                      wand: 'pieken', wandF: true, wandH: 4, wandX: -0.5, note: '' });
    await laad(g);
    const uit = [];
    const r = await page.evaluate(() => {
      const a = mkNaarJSON(); mkUitJSON(a); const b = mkNaarJSON();
      const lv = mkNaarLevel(), meld = mkControle();
      const ph = b.objecten.find(o => o.k === 'poort' && o.c === 14);
      // de knop Poort met hek in het palet zet een poort met hek neer
      MK.tool = 'poorthek'; mkLegenda();
      return { ph, zelfde: JSON.stringify(a) === JSON.stringify(b), poorten: lv.poorten, spawns: lv.spawns.filter(s => s.poort === 'b2'),
               meld: meld.filter(m => /b2/.test(m.tekst || m.t || JSON.stringify(m))).map(m => JSON.stringify(m))};
    });
    if (!r.zelfde) uit.push('round-trip van de poort met hek is niet gelijk');
    const ph = r.ph || {};
    if (!ph.hek || !ph.regie || ph.bij !== 12 || ph.s !== 1.2 || ph.wand !== 'pieken' || !ph.wandF || ph.wandH !== 4 || ph.wandX !== -0.5) uit.push('de grid-export verloor velden: ' + JSON.stringify(ph));
    const b1 = (r.poorten || []).find(o => o.id === 'b1'), b2 = (r.poorten || []).find(o => o.id === 'b2');
    if (!b2 || !b2.hek || !b2.regie || b2.wand !== 'pieken' || !b2.wandF || b2.wandH !== 4 || b2.wandX !== -0.5 || b2.s !== 1.2) uit.push('poort b2 in het spel-level: ' + JSON.stringify(b2));
    else if (b2.bij !== b2.x - 2 * 175) uit.push('regiepunt: bij ' + b2.bij + ', verwacht ' + (b2.x - 2 * 175));
    if (b1 && (b1.hek || b1.regie || b1.wand || b1.s)) uit.push('poort b1 kreeg velden die hij niet heeft: ' + JSON.stringify(b1));
    if (r.spawns.length !== 1 || r.spawns[0].k !== 'schildman') uit.push('geen schildbandiet in poort b2: ' + JSON.stringify(r.spawns));
    // alleen poortvijanden: dan geen standaard-slang achter het eind erbij (die is er alleen tegen de vrije slangen van een level zonder spawn)
    const alleenPoort = await page.evaluate(() => { const was = MK.objects; MK.objects = was.filter(o => o.k !== 'vijand'); const lv = mkNaarLevel(); MK.objects = was;
      const leeg = was.filter(o => o.k !== 'vijand' && o.k !== 'poort'); MK.objects = leeg; const lv0 = mkNaarLevel(); MK.objects = was; return { los: lv.spawns.filter(s => !s.poort), leeg: lv0.spawns }; });
    if (alleenPoort.los.length) uit.push('een level met alleen poortvijanden kreeg losse spawns: ' + JSON.stringify(alleenPoort.los));
    if (alleenPoort.leeg.length !== 1) uit.push('een level zonder enige vijand hoort een standaard-slang te krijgen: ' + JSON.stringify(alleenPoort.leeg));
    if (r.meld.some(m => /letop|fout/i.test(m))) uit.push('de controle meldt de poort met regie: ' + r.meld.join(' | '));
    // spiegelen en plakken: de poort, zijn rotswand en zijn regiepunt keren om
    const s2 = await page.evaluate(() => {
      MK.gebied = { c0: 12, r0: 6, c1: 14, r1: 6 }; mkKopieer(); mkSpiegel(); mkPlak = { c: 0, r: 0 }; mkPlakZet();
      const q = MK.objects.find(o => o.k === 'poort' && o.r === 0);
      return q && { c: q.c, f: !!q.f, wandF: !!q.wandF, wandX: q.wandX, bij: q.bij, hek: !!q.hek, wand: q.wand };
    });
    if (!s2 || s2.c !== 0 || !s2.f || s2.wandF || s2.wandX !== 0.5 || s2.bij !== 2 || !s2.hek || s2.wand !== 'pieken') uit.push('gespiegeld geplakt: ' + JSON.stringify(s2) + ' (verwacht kolom 0, gespiegeld, wand niet gespiegeld, wandX 0.5, regiepunt kolom 2)');
    // een klik met Poort met hek
    await page.evaluate(() => { MK.tool = 'poorthek'; mkLegenda(); });
    const xy = await celXY(6, 10); await page.mouse.click(xy.x, xy.y); await page.waitForTimeout(50);
    const nieuw = await page.evaluate(() => { const q = MK.objects.find(o => o.c === 6 && o.r === 10); return q && { k: q.k, hek: !!q.hek }; });
    if (!nieuw || nieuw.k !== 'poort' || !nieuw.hek) uit.push('Poort met hek zette geen poort met hek neer: ' + JSON.stringify(nieuw));
    // en het spel-level door levelcheck
    await laad(g);
    const lv = await page.evaluate(() => mkNaarLevel());
    const f = path.join(os.tmpdir(), 'makertest-poorthek.json');
    fs.writeFileSync(f, JSON.stringify(lv));
    const lc = spawnSync('python3', [path.join(ROOT, 'tools', 'levelcheck.py'), f], { encoding: 'utf8' });
    uit.push(...((lc.stdout || '') + (lc.stderr || '')).split('\n').filter(l => /FOUT/.test(l)).slice(0, 4));
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
    delete slecht.objecten.find(o => o.k === 'zegel').rijzer;      // de rijzer heeft dan geen schakelaar meer
    slecht.eind = null;
    await laad(slecht);
    const m = await page.evaluate(() => mkControle());
    const t = m.map(x => x.tekst).join(' | ');
    if (!m.some(x => /start/i.test(x.tekst) && x.ernst === 'fout')) uit.push('geen fout over de start zonder vloer: ' + t);
    if (!m.some(x => /platform/i.test(x.tekst))) uit.push('geen melding over het platform zonder doel: ' + t);
    if (!m.some(x => /rijzer/i.test(x.tekst) && x.ernst === 'fout')) uit.push('geen fout over de rijzer zonder zegel: ' + t);
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
