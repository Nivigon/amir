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

// Het proefgrid: klein, maar met elke soort erop. 36 breed, 12 hoog, grondlijn op rij 7.
//  - savanne op de grondlijn, met een ravijn (kolom 21 tot 23) boven een gang (rij 8 en 9, kolom 19 tot 23) achter de
//    start, met twee treden onder het gat (kolom 21 en 22) als weg naar boven
//    (het gat loopt een cel verder door dan de onderste trede, anders stoot Amir bij de sprong zijn hoofd tegen het dak)
//  - een lage rotsmesa (kolom 4 en 5, rij 6), een zwevende laag (kolom 16 tot 18, rij 4) met lucht eronder
//  - een muur door de grond (kolom 10, rij 6 en 7), sneeuw op kolom 0 en 1, straat op kolom 2 en 3 (grondSoort)
//  - start op kolom 19, eind op kolom 2
//  - een zandslang, een bandiet met dolk, een platform met doel plus een tandwiel, een overhang, een richel,
//    een verborgen zegel met masker dat ook een rijzer stuurt, een onzichtbaar zegel op het dak van de gang,
//    een rune, een kalebas, een prop, en een gespiegeld rotsstuk (een plaat op schaal 1,2) op de sneeuw
//  - een tweede ravijn (kolom 11 en 12) met een rijzer van 2 breed erin, drie cellen diep, die tot de grondlijn komt
//  - een masker (Verborgen1) van twee cellen, een zwarte cel, en een vrije blokvorm
//  - een gespiegelde stenen poort in savannekleur (kolom 16) met twee schorpioenen erin, die de rune opent
//  - achter de start (kolom 24 tot 35, zodat de x van al het andere gelijk blijft) een straat met de stad: gevel g1 (2 hoog)
//    en g2 (3 hoog), een galerij van g1 tot g2 op niveau 1, een trap rechts van g2 die op die galerij uitkomt, een rieten
//    kraam, een kruik als voetdecor en het paleis; een bandiet op de galerij, en een schildbandiet en een kruisboogbandiet
//    (wijk uit, inBeeld aan) op het dak van g1 (die krijgen dak op hun spawn); uit het deurgat van g1 een bandiet met dolk, en
//    uit een deur op de eerste verdieping van g2 (op de galerij) twee bandieten
function proefGrid(){
  const rijen = [];
  for (let r = 0; r < 12; r++) rijen.push('.'.repeat(36).split(''));
  for (let c = 0; c < 36; c++) rijen[7][c] = c >= 24 ? 'A' : 'S';
  rijen[7][21] = 'V'; rijen[7][22] = 'V'; rijen[7][23] = 'V';
  rijen[7][11] = 'V'; rijen[7][12] = 'V';
  for (let r = 8; r <= 9; r++) for (let c = 19; c <= 23; c++) rijen[r][c] = 'G';
  rijen[8][21] = 'R'; rijen[9][22] = 'R';
  for (let c = 4; c <= 5; c++) rijen[6][c] = 'R';
  for (let c = 16; c <= 18; c++) rijen[4][c] = 'F';
  rijen[6][10] = 'M'; rijen[7][10] = 'M';
  rijen[7][0] = 'W'; rijen[7][1] = 'W';
  rijen[7][2] = 'A'; rijen[7][3] = 'A';
  return {
    type: 'amir-levelmaker-grid', versie: 2, cols: 36, rows: 12, groundRow: 7, stadSeed: 7,
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
      { c: 0, r: 6, k: 'rotsdecor', prop: 'plaat_02', f: true, s: 1.2, note: '' },
      { c: 24, r: 6, k: 'gevel', id: 'g1', hoog: 2, note: '' },
      { c: 28, r: 6, k: 'gevel', id: 'g2', hoog: 3, note: '' },
      { c: 24, r: 6, k: 'galerij', van: 'g1', tot: 'g2', niveau: 1, note: '' },
      { c: 28, r: 6, k: 'trap', gevel: 'g2', kant: 'r', niveau: 0, balkon: 0, note: '' },
      { c: 24, r: 6, k: 'deur', gevel: 'g1', verdieping: 0, vijand: 'bandiet:dolk', note: '' },
      { c: 28, r: 6, k: 'deur', gevel: 'g2', verdieping: 1, vijand: 'bandiet', n: 2, note: '' },
      { c: 34, r: 6, k: 'kraam', soort: 'riet', note: '' },
      { c: 27, r: 6, k: 'voet', stuk: 'kruik', note: '' },
      { c: 32, r: 2, k: 'paleis', note: '' },
      { c: 27, r: 3, k: 'vijand', soort: 'bandiet', note: '' },
      { c: 25, r: 1, k: 'vijand', soort: 'schildman:makkelijk', note: '' },
      { c: 26, r: 1, k: 'vijand', soort: 'kruisboogbandiet', params: { wijk: 0, inBeeld: 1 }, note: '' },
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
    const de = a.objecten.filter(o => o.k === 'deur');
    if (de.length !== 2 || !de.some(o => o.gevel === 'g1' && o.verdieping === 0 && o.vijand === 'bandiet:dolk' && !o.n) || !de.some(o => o.gevel === 'g2' && o.verdieping === 1 && o.vijand === 'bandiet' && o.n === 2))
      uit.push('de deuren verloren hun gevel, verdieping, vijand of aantal: ' + JSON.stringify(de));
    return uit;
  });

  // 1b. Savanne | Stad: de schakelaar filtert het palet en onthoudt per stand je gereedschap, G wisselt, een
  // leemcel wordt een terras met look: 'leem', en het uitzicht is vanzelf de stad (of wat je kiest) en gaat mee in de JSON
  await check('stad: de schakelaar, de leemmuur en het uitzicht', async () => {
    const rijen = []; for (let r = 0; r < 8; r++) rijen.push('.'.repeat(10).split(''));
    for (let c = 0; c < 10; c++) rijen[5][c] = 'S';
    rijen[4][3] = 'E'; rijen[4][4] = 'E';
    rijen[5][1] = 'R'; rijen[5][6] = 'A'; rijen[5][7] = 'A';   // een strook rots en een strook straat op de grondlijn
    await laad({ type: 'amir-levelmaker-grid', versie: 2, cols: 10, rows: 8, groundRow: 5, grid: rijen.map(r => r.join('')),
                 start: { c: 9, r: 4 }, eind: { c: 0, r: 4 }, objecten: [] });
    return page.evaluate(() => {
      const f = [];
      const lv = mkNaarLevel();
      const leem = (lv.terraces || []).find(t => t.look === 'leem');
      if (!leem || leem.h !== 150 || leem.grond) f.push('geen leemmuur van 1 cel (150) als terras: ' + JSON.stringify(lv.terraces));
      const gsR = (lv.grondSoort || []).find(g => g.soort === 'rots'), gsA = (lv.grondSoort || []).find(g => g.soort === 'straat');
      if (!gsR || !gsA || (lv.grondSoort || []).length !== 2) f.push('geen strook rots en straat uit de grondlijn: ' + JSON.stringify(lv.grondSoort));
      if (gsA && Math.abs(gsA.van - gsA.tot) !== 350) f.push('de strook straat is geen 2 cellen (350 px): ' + JSON.stringify(gsA));
      if (lv.sneeuw) f.push('rots op de grondlijn geeft nog een sneeuw-veld: ' + JSON.stringify(lv.sneeuw));
      if (lv.lagen !== 'stad_dag') f.push('het uitzicht is vanzelf niet de stad: ' + lv.lagen);
      MK.uitzicht = 'basis'; if ('lagen' in mkNaarLevel()) f.push('Savanne, avond geeft toch lagen');
      MK.uitzicht = 'middag'; if (mkNaarLevel().lagen !== 'middag') f.push('een gekozen uitzicht komt niet in lagen');
      const j = mkNaarJSON(); mkUitJSON(JSON.parse(JSON.stringify(j)));
      if (MK.uitzicht !== 'middag' || mkUitzichtEl.value !== 'middag') f.push('het uitzicht gaat niet mee door de JSON');
      mkUitJSON(Object.assign({}, j, { uitzicht: 'onzin' })); if (MK.uitzicht !== '') f.push('een onbekend uitzicht wordt niet vanzelf');
      // de schakelaar
      mkThemaZet('savanne'); MK.tool = 'rots'; MK.cat = 'terrein';
      if (mkPaletZoek('leem', null, { items: mkPalet() })) f.push('leem staat in de stand Savanne');
      if (mkPaletZoek('straat', null, { items: mkPalet() })) f.push('straat staat in de stand Savanne');
      if (!mkPaletZoek('sneeuw', null, { items: mkPalet() })) f.push('sneeuw ontbreekt in de stand Savanne');
      mkThemaZet('stad');
      if (!mkPaletZoek('leem', null, { items: mkPalet() })) f.push('leem ontbreekt in de stand Stad');
      if (!mkPaletZoek('straat', null, { items: mkPalet() })) f.push('straat ontbreekt in de stand Stad');
      if (mkPaletZoek('sneeuw', null, { items: mkPalet() })) f.push('sneeuw staat in de stand Stad');
      if (!document.querySelector('#mkthema button.on[data-thema="stad"]')) f.push('de knop Stad gaat niet aan');
      MK.tool = 'leem';
      dispatchEvent(new KeyboardEvent('keydown', { key: 'g' }));
      if (MK.thema !== 'savanne') f.push('G wisselt niet naar Savanne');
      if (MK.tool !== 'rots') f.push('terug in Savanne is het gereedschap niet weer rots: ' + MK.tool);
      dispatchEvent(new KeyboardEvent('keydown', { key: 'G' }));
      if (MK.thema !== 'stad' || MK.tool !== 'leem') f.push('terug in Stad is het gereedschap niet weer leem: ' + MK.thema + ' ' + MK.tool);
      MK.tool = 'sneeuw'; mkThemaZet('savanne'); MK.tool = 'sneeuw'; mkThemaZet('stad');
      if (MK.tool === 'sneeuw') f.push('sneeuw blijft vast in de stand Stad');
      mkThemaZet('savanne'); MK.tool = 'select'; MK.cat = 'terrein'; MK.sub = null; MK.themaGeheugen = {}; mkLegenda();
      return f;
    });
  });

  // 1c. de losse stadsstukken (stap 3 van notities/plan-stad-maker.md): gevel, kraam, voetdecor en het paleis. Ze gaan
  // door de JSON, worden het veld stad (een gevel met x op zijn linkerkant, de rest op het midden van de kolom), elke
  // gevel houdt een eigen id, er is hoogstens een paleis, en de controle meldt een stuk of straatcel zonder straat eronder
  await check('stadsstukken: gevel, kraam, voetdecor, paleis, galerij en trap', async () => {
    const rijen = []; for (let r = 0; r < 8; r++) rijen.push('.'.repeat(16).split(''));
    for (let c = 0; c < 16; c++) rijen[5][c] = c >= 8 && c <= 13 ? 'A' : 'S';   // savanne, en een straat van kolom 8 tot 13
    rijen[4][1] = 'A';                                    // straat boven de grondlijn op savanne: LET OP
    rijen[4][11] = 'E';                                   // een leemmuur op de straat: goed
    await laad({ type: 'amir-levelmaker-grid', versie: 2, cols: 16, rows: 8, groundRow: 5, grid: rijen.map(r => r.join('')),
                 start: { c: 15, r: 4 }, eind: { c: 0, r: 4 }, stadSeed: 42, objecten: [
                   { c: 9, r: 4, k: 'gevel', id: 'g1', hoog: 3 },
                   { c: 3, r: 4, k: 'gevel', id: 'g1', hoog: 1, f: true },      // een dubbel id: wordt g2, en hij staat op savanne
                   { c: 12, r: 4, k: 'kraam', soort: 'doek', f: true },
                   { c: 10, r: 4, k: 'voet', stuk: 'kruik' },
                   { c: 7, r: 1, k: 'paleis' }, { c: 4, r: 1, k: 'paleis' } ] });   // twee paleizen: het laatste blijft
    const f = await page.evaluate(() => {
      const f = [];
      const gv = MK.objects.filter(o => o.k === 'gevel'), pal = MK.objects.filter(o => o.k === 'paleis');
      if (gv.length !== 2 || new Set(gv.map(o => o.id)).size !== 2 || !gv.some(o => o.id === 'g1')) f.push('de gevels hebben geen eigen id: ' + JSON.stringify(gv.map(o => o.id)));
      if (pal.length !== 1 || pal[0].c !== 4) f.push('niet precies een paleis (het laatste): ' + JSON.stringify(pal));
      const j1 = JSON.stringify(mkNaarJSON()); mkUitJSON(JSON.parse(j1));
      if (JSON.stringify(mkNaarJSON()) !== j1) f.push('de stadsstukken komen niet gelijk door de JSON');
      if (MK.stadSeed !== 42) f.push('de seed gaat niet mee door de JSON: ' + MK.stadSeed);
      const lv = mkNaarLevel(), S = lv.stad;
      if (!S) return f.concat('geen veld stad');
      if (S.seed !== 42) f.push('stad.seed is niet 42: ' + S.seed);
      if (S.gevels.length !== 2 || S.gevels[0].x !== -1050 || S.gevels[0].hoog !== 3 || S.gevels[0].f || S.gevels[1].x !== -2100 || S.gevels[1].f !== 1)
        f.push('de gevels kloppen niet (x op de linkerkant, van de start af): ' + JSON.stringify(S.gevels));
      if (S.kramen.length !== 1 || S.kramen[0].soort !== 'doek' || S.kramen[0].f !== 1 || Math.abs(S.kramen[0].x + 437.5) > 1) f.push('de kraam klopt niet: ' + JSON.stringify(S.kramen));
      if (S.voet.length !== 1 || S.voet[0].stuk !== 'kruik' || Math.abs(S.voet[0].x + 787.5) > 1) f.push('het voetdecor klopt niet: ' + JSON.stringify(S.voet));
      if (Math.abs(S.paleis + 1837.5) > 1) f.push('het paleis staat niet op kolom 4: ' + S.paleis);
      if (lv.lagen !== 'stad_dag') f.push('geen uitzicht stad_dag: ' + lv.lagen);
      if ('muziek' in lv) f.push('een eigen muziek in plaats van de stadmuziek: ' + lv.muziek);
      const gs = lv.grondSoort || [];
      if (!gs.some(g => g.soort === 'straat') || gs.filter(g => g.soort === 'savanne').length !== 2) f.push('met stad krijgt de savanne geen eigen strook (de basis is dan straat): ' + JSON.stringify(gs));
      // de controle: gevel g2 staat op savanne, de straatcel op kolom 1 ook; de rest staat op straat
      const m = mkControle().filter(q => q.ernst === 'letop').map(q => q.tekst);
      const g2 = gv.find(o => o.id !== 'g1').id;
      if (!m.some(t => t.startsWith('Gevel ' + g2) && t.includes('geen straat'))) f.push('geen LET OP voor de gevel op savanne: ' + JSON.stringify(m));
      if (m.some(t => t.startsWith('Gevel g1') || t.startsWith('Kraam') || t.startsWith('Voetdecor'))) f.push('een LET OP voor een stuk op de straat: ' + JSON.stringify(m));
      if (!m.some(t => t.startsWith('Straat boven de grondlijn op kolom 1 '))) f.push('geen LET OP voor de straatcel op savanne: ' + JSON.stringify(m));
      if (m.some(t => t.startsWith('Muur van leem'))) f.push('een LET OP voor de leemmuur op de straat: ' + JSON.stringify(m));
      // het klembord spiegelen: de gevel kijkt de andere kant op en blijft op zijn plek staan, twee keer is het origineel
      MK.gebied = { c0: 8, r0: 0, c1: 15, r1: 7 }; mkKopieer();
      const kg = () => mkKlembord.objects.find(o => o.k === 'gevel');
      const dc0 = kg().dc; mkSpiegel();
      if (!kg().f || kg().dc !== 4) f.push('gespiegeld staat de gevel niet op dezelfde plek (dc 4, gespiegeld): ' + JSON.stringify(kg()));
      if (mkKlembord.objects.find(o => o.k === 'kraam').f) f.push('de kraam spiegelt niet mee (hij was al gespiegeld)');
      mkSpiegel(); if (kg().dc !== dc0 || kg().f) f.push('twee keer spiegelen geeft de gevel niet terug: ' + JSON.stringify(kg()));
      // plakken: de geplakte gevel heeft het id van een gevel die er al staat en krijgt een nieuwe
      mkPlak = { c: 0, r: 0 }; mkPlakZet();
      const ids = MK.objects.filter(o => o.k === 'gevel').map(o => o.id);
      if (new Set(ids).size !== ids.length) f.push('na plakken twee gevels met hetzelfde id: ' + JSON.stringify(ids));
      // het palet: alleen in de stand Stad, met een kopje per stuk in het paneel
      mkThemaZet('savanne');
      if (mkPaletZoek('gevel', null, { items: mkPalet() })) f.push('de gevel staat in de stand Savanne');
      mkThemaZet('stad');
      for (const t of ['gevel', 'kraam', 'kraamdoek', 'voet', 'paleis']) if (!mkPaletZoek(t, null, { items: mkPalet() })) f.push(t + ' ontbreekt in de stand Stad');
      MK.tool = 'select'; MK.sel = MK.objects.find(o => o.k === 'gevel' && o.id === 'g1'); MK.inspectDicht = false; mkNotePaneel();
      const ss = document.getElementById('mkstadsoort');
      if (document.getElementById('mkstadctl').offsetParent === null || ss.value !== '3') f.push('het paneel van de gevel toont zijn hoogte niet: ' + ss.value);
      ss.value = '4'; ss.dispatchEvent(new Event('change'));
      if (MK.sel.hoog !== 4) f.push('Hoogte in het paneel zet de gevel niet op 4 hoog');
      return f;
    });
    // neerzetten met de muis: het paleis verschuift (er blijft er een), een kraam met doek is een kraam met soort doek,
    // en een nieuwe gevel krijgt een id dat er nog niet is
    await page.evaluate(() => { MK.sel = null; MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'paleis'; mkLegenda(); });   // het paneel dicht, zodat het geen cel afdekt
    let p = await celXY(6, 1); await page.mouse.click(p.x, p.y);
    await page.evaluate(() => { MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'kraamdoek'; mkLegenda(); });
    p = await celXY(14, 4); await page.mouse.click(p.x, p.y);
    await page.evaluate(() => { MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'gevel'; mkLegenda(); });
    p = await celXY(5, 4); await page.mouse.click(p.x, p.y);
    f.push(...await page.evaluate(() => {
      const f = [], pal = MK.objects.filter(o => o.k === 'paleis');
      if (pal.length !== 1 || pal[0].c !== 6) f.push('het paleis verschuift niet met een klik: ' + JSON.stringify(pal));
      const kr = MK.objects.find(o => o.k === 'kraam' && o.c === 14);
      if (!kr || kr.soort !== 'doek') f.push('Kraam met doek zet geen kraam met soort doek: ' + JSON.stringify(MK.objects.map(o => [o.k, o.c, o.r])));
      const ids = MK.objects.filter(o => o.k === 'gevel').map(o => o.id);
      if (!MK.objects.some(o => o.k === 'gevel' && o.c === 5) || new Set(ids).size !== ids.length) f.push('een nieuwe gevel zonder eigen id: ' + JSON.stringify(ids));
      mkThemaZet('savanne'); MK.tool = 'select'; MK.cat = 'terrein'; MK.sub = null; MK.themaGeheugen = {}; mkLegenda();
      return f;
    }));

    // de gekoppelde stukken (stap 4): een galerij sleep je van gevel naar gevel, een trap klik je op de zijkant van een gevel.
    // Ze hangen aan het id van een gevel, en die koppeling blijft heel bij spiegelen, plakken, de JSON, ongedaan maken en rijen
    // invoegen; zonder zijn gevel gaat een galerij of trap mee weg. In het level worden het stad.galerijen en stad.trappen.
    const rijen2 = []; for (let r = 0; r < 12; r++) rijen2.push((r === 9 ? 'A' : '.').repeat(40));
    await laad({ type: 'amir-levelmaker-grid', versie: 2, cols: 40, rows: 12, groundRow: 9, grid: rijen2,
                 start: { c: 39, r: 8 }, eind: { c: 0, r: 8 }, objecten: [
                   { c: 4, r: 8, k: 'gevel', id: 'g1', hoog: 2 }, { c: 9, r: 8, k: 'gevel', id: 'g2', hoog: 3 } ] });
    const puntXY = (x, y) => page.evaluate(([x, y]) => { const b = mkCanvas.getBoundingClientRect(), cel = mkCel();
      return { x: b.left + MK.panX + x * cel, y: b.top + MK.panY + y * cel }; }, [x, y]);
    await page.evaluate(() => { mkThemaZet('stad'); MK.sel = null; MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'galerij'; mkLegenda(); });
    const yDek = 9 - 730 / 150;                          // de tweede verdieping, waar je de galerij begint
    let a = await puntXY(5.5, yDek), b = await puntXY(10.5, yDek);
    await page.mouse.move(a.x, a.y); await page.mouse.down(); await page.mouse.move(b.x, b.y, { steps: 5 }); await page.mouse.up();
    await page.evaluate(() => { MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'trap'; mkLegenda(); });
    a = await puntXY(11.8, 8.5); await page.mouse.click(a.x, a.y);   // de rechterkant van g2, op de straat
    f.push(...await page.evaluate(() => {
      const f = [], gal = MK.objects.filter(o => o.k === 'galerij'), tr = MK.objects.filter(o => o.k === 'trap');
      if (gal.length !== 1 || gal[0].van !== 'g1' || gal[0].tot !== 'g2' || mkGalNiveau(gal[0]) !== 2) f.push('slepen van g1 naar g2 geeft geen galerij op de tweede verdieping: ' + JSON.stringify(gal));
      if (tr.length !== 1 || tr[0].gevel !== 'g2' || tr[0].kant !== 'r' || mkTrapNiveau(tr[0]) !== 0) f.push('een klik rechts op g2 geeft geen trap rechts van de straat af: ' + JSON.stringify(tr));
      if (!gal.length || !tr.length) return f;
      // het paneel: niveau, extra lengte, kant en balkon
      MK.tool = 'select'; MK.sel = gal[0]; MK.inspectDicht = false; mkNotePaneel();
      if (document.getElementById('mkkoppelctl').offsetParent === null) f.push('het paneel van de galerij is niet te zien');
      const ns = document.getElementById('mkkoppelniv'); ns.value = '1'; ns.dispatchEvent(new Event('change'));
      const sl = document.getElementById('mkgalr'); sl.value = '1.5'; sl.dispatchEvent(new Event('input'));
      if (mkGalNiveau(gal[0]) !== 1 || !gal[0].meer || gal[0].meer[1] !== 1.5) f.push('het paneel zet niveau of extra rechts niet: ' + JSON.stringify(gal[0]));
      MK.sel = tr[0]; mkNotePaneel();
      if (document.getElementById('mkgallrij').offsetParent !== null || document.getElementById('mktrapbalkrij').offsetParent === null) f.push('het paneel van de trap toont de knoppen van de galerij');
      const bs = document.getElementById('mktrapbalk'); bs.value = '2'; bs.dispatchEvent(new Event('input'));
      document.getElementById('mktrapkant').click(); document.getElementById('mktrapkant').click();   // heen en terug: weer rechts
      if (tr[0].balkon !== 2 || tr[0].kant !== 'r') f.push('het paneel zet balkon of kant niet: ' + JSON.stringify(tr[0]));
      // aanklikken op het plaatje: de galerij op zijn dek, de trap op zijn plaatje, het huis ertussen blijft de gevel
      const gm = mkGalerijMaat(gal[0]), tm = mkTrapMaat(tr[0]);
      if (mkObjOp(Math.floor((gm.c0 + gm.c1) / 2), Math.floor(gm.dek - 0.3)) !== gal[0]) f.push('de galerij is niet aan te klikken op zijn dek');
      if (mkObjOp(Math.floor(tm.x0 + tm.tw / 2), 8) !== tr[0]) f.push('de trap is niet aan te klikken op zijn plaatje');
      if (mkObjOp(5, 8) === null || mkObjOp(5, 8).k !== 'gevel') f.push('de ankercel van g1 geeft niet de gevel');
      // het level: id's worden indexen in stad.gevels (van de start af: g2 is 0, g1 is 1)
      const S = mkNaarLevel().stad || {};
      const G = (S.galerijen || [])[0], T = (S.trappen || [])[0];
      if (!G || G.van !== 0 || G.tot !== 1 || G.h !== 401 || JSON.stringify(G.meer) !== '[0,1.5]') f.push('stad.galerijen klopt niet: ' + JSON.stringify(S.galerijen));
      if (!T || T.gevel !== 0 || T.kant !== 'r' || T.niveau !== 0 || T.balkon !== 2) f.push('stad.trappen klopt niet: ' + JSON.stringify(S.trappen));
      // de JSON en ongedaan maken
      const j1 = JSON.stringify(mkNaarJSON()); mkUitJSON(JSON.parse(j1));
      if (JSON.stringify(mkNaarJSON()) !== j1) f.push('galerij en trap komen niet gelijk door de JSON');
      if (JSON.stringify(mkNaarLevel().stad) !== JSON.stringify(S)) f.push('na de JSON een ander veld stad');
      // een rij erboven: alles schuift mee, het level blijft gelijk
      mkRijBoven(1);
      const go = MK.objects.find(o => o.k === 'galerij');
      if (!go || go.r !== 9 || JSON.stringify(mkNaarLevel().stad) !== JSON.stringify(S)) f.push('na een rij erboven is de koppeling niet heel: ' + JSON.stringify(go));
      mkRijBoven(-1);
      // kopiëren en spiegelen: een gebied met beide gevels neemt galerij en trap mee; geplakt hangen ze aan de nieuwe gevels
      MK.gebied = { c0: 3, r0: 0, c1: 13, r1: 11 }; mkKopieer();
      if (mkKlembord.objects.filter(o => o.k === 'galerij' || o.k === 'trap').length !== 2) f.push('het klembord heeft de galerij en trap niet');
      mkSpiegel(); mkPlak = { c: 20, r: 0 }; mkPlakZet();
      const nieuwG = MK.objects.filter(o => o.k === 'gevel' && o.c >= 20).map(o => o.id);
      const pg = MK.objects.find(o => o.k === 'galerij' && o.c >= 20), pt = MK.objects.find(o => o.k === 'trap' && o.c >= 20);
      if (nieuwG.length !== 2 || nieuwG.includes('g1') || nieuwG.includes('g2')) f.push('de geplakte gevels hebben geen nieuw id: ' + JSON.stringify(nieuwG));
      if (!pg || !nieuwG.includes(pg.van) || !nieuwG.includes(pg.tot) || pg.van === pg.tot) f.push('de geplakte galerij hangt niet aan de geplakte gevels: ' + JSON.stringify(pg));
      if (!pg || JSON.stringify(pg.meer) !== '[1.5,0]') f.push('gespiegeld wisselt de extra lengte niet van kant: ' + JSON.stringify(pg && pg.meer));
      if (!pt || !nieuwG.includes(pt.gevel) || pt.kant !== 'l') f.push('de geplakte trap hangt niet aan zijn gespiegelde gevel, links: ' + JSON.stringify(pt));
      const gp = pt && mkGevelVan(pt.gevel), gb = MK.objects.find(o => o.k === 'gevel' && o.id === 'g2');
      if (gp && gp.hoog !== gb.hoog) f.push('de trap hangt aan de verkeerde geplakte gevel');
      if (MK.objects.find(o => o.k === 'galerij' && o.van === 'g1').meer[1] !== 1.5) f.push('spiegelen veranderde de originele galerij');
      // een gebied met maar een van de twee gevels: de galerij gaat niet mee (hij hangt aan een huis buiten het gebied)
      MK.gebied = { c0: 3, r0: 0, c1: 7, r1: 11 }; mkKopieer();
      if (mkKlembord.objects.some(o => o.k === 'galerij')) f.push('een galerij gaat mee zonder zijn tweede gevel');
      // een gevel weg: zijn galerij en trap gaan mee weg, het level blijft te maken, en ongedaan maken brengt ze terug
      mkBewaarNu(); const voor = JSON.stringify(mkNaarJSON());
      MK.objects = MK.objects.filter(o => !(o.k === 'gevel' && o.id === 'g2')); mkBewaarNu();
      if (MK.objects.some(o => (o.k === 'galerij' && (o.van === 'g2' || o.tot === 'g2')) || (o.k === 'trap' && o.gevel === 'g2'))) f.push('zonder g2 blijven zijn galerij of trap staan');
      try { mkNaarLevel(); } catch (e){ f.push('zonder gevel crasht mkNaarLevel: ' + e.message); }
      mkOngedaan();
      if (JSON.stringify(mkNaarJSON()) !== voor) f.push('ongedaan maken brengt de gevel met galerij en trap niet terug');
      // een galerij uit de JSON die naar een gevel wijst die er niet is: valt weg, ook in het level
      const j = mkNaarJSON(); j.objecten.push({ c: 1, r: 8, k: 'galerij', van: 'g9', tot: 'g1', niveau: 2 }, { c: 1, r: 8, k: 'trap', gevel: 'g9' });
      mkUitJSON(j);
      if (MK.objects.some(o => o.van === 'g9' || o.gevel === 'g9')) f.push('een galerij of trap zonder gevel blijft staan na laden');
      mkThemaZet('savanne'); MK.tool = 'select'; MK.cat = 'terrein'; MK.sub = null; MK.themaGeheugen = {}; MK.gebied = null; mkLegenda();
      return f;
    }));

    // de afwerking (stap 5): een vijand op een dak, galerij of balkon krijgt dak op zijn spawn, en de controle meldt wat niet
    // klopt: gevels door elkaar, een galerij boven een dak, een trap boven het dak, zonder vloer aan zijn voet of bij de
    // uitgang (FOUT), een trap boven een ravijn, en een vijand op een dak die daken niet kent. Elke melding heeft een cel.
    const rijen3 = []; for (let r = 0; r < 12; r++) rijen3.push((r === 9 ? 'A' : '.').repeat(40));
    await laad({ type: 'amir-levelmaker-grid', versie: 2, cols: 40, rows: 12, groundRow: 9, grid: rijen3,
                 start: { c: 39, r: 8 }, eind: { c: 0, r: 8 }, objecten: [
                   { c: 4, r: 8, k: 'gevel', id: 'g1', hoog: 2 }, { c: 6, r: 8, k: 'gevel', id: 'g2', hoog: 2 },   // door elkaar
                   { c: 12, r: 8, k: 'gevel', id: 'g3', hoog: 1 }, { c: 16, r: 8, k: 'gevel', id: 'g4', hoog: 3 },
                   { c: 12, r: 8, k: 'galerij', van: 'g3', tot: 'g4', niveau: 2 },                                // boven het dak van g3
                   { c: 16, r: 8, k: 'trap', gevel: 'g4', kant: 'r', niveau: 3, balkon: 2 },                      // boven het dak, geen vloer aan de voet
                   { c: 16, r: 8, k: 'trap', gevel: 'g4', kant: 'l', niveau: 0, balkon: 0 },                      // geen balkon en geen galerij op 401
                   { c: 24, r: 8, k: 'gevel', id: 'g5', hoog: 2 }, { c: 24, r: 8, k: 'trap', gevel: 'g5', kant: 'l', niveau: 0, balkon: 1.6 },
                   { c: 5, r: 3, k: 'vijand', soort: 'groen' },                                                   // op het dak van g1: kent geen daken
                   { c: 14, r: 3, k: 'vijand', soort: 'schildman' },                                              // op de galerij op 730
                   { c: 25, r: 3, k: 'vijand', soort: 'bandiet:dolk' },                                           // op het dak van g5 (816)
                   { c: 26, r: 3, k: 'vijand', soort: 'kruisboogbandiet', params: { wijk: 0 } } ] });             // de schutter ook op het dak van g5
    f.push(...await page.evaluate(() => {
      const f = [];
      const tg5 = MK.objects.find(o => o.k === 'trap' && o.gevel === 'g5'), vc = Math.floor(mkTrapMaat(tg5).voetX);
      MK.grid[MK.ground][vc] = 'ravijn';                                                                          // de voet van de trap bij g5 boven een ravijn
      const m = mkControle(), heeft = (ernst, re) => m.find(q => q.ernst === ernst && re.test(q.tekst));
      const moet = [['letop', /^Gevel g1 en g2 overlappen/, 'twee gevels door elkaar'], ['letop', /^De galerij van g3 tot g4 .*boven het dak van g3/, 'een galerij boven het dak'],
                    ['letop', /^De trap bij g4 \(rechts, niveau 3\) komt op .* hoger dan het dak/, 'een trap boven het dak'],
                    ['letop', /^De trap bij g4 \(rechts, niveau 3\) begint op .* geen galerij/, 'een trap zonder vloer aan zijn voet'],
                    ['fout', /^De trap bij g4 \(links, niveau 0\) heeft geen balkon/, 'een trap zonder vloer bij de uitgang'],
                    ['letop', /^De trap bij g5 .* boven een ravijn/, 'een trap met zijn voet boven een ravijn'],
                    ['letop', /^Zandslang op kolom 5 staat op het dak van g1, maar deze soort kent geen daken/, 'een vijand op een dak die daken niet kent']];
      for (const [e, re, wat] of moet){ const q = heeft(e, re); if (!q) f.push('geen ' + e + ' voor ' + wat + ': ' + JSON.stringify(m.map(q => q.tekst)));
        else if (q.c == null || q.r == null) f.push('de melding voor ' + wat + ' heeft geen cel om naar te springen'); }
      if (m.some(q => /Schildbandiet|Bandiet|Kruisboogbandiet/.test(q.tekst) && /dak|zweeft/.test(q.tekst))) f.push('een melding voor de bandiet, schildbandiet of kruisboogbandiet op een dak: ' + JSON.stringify(m.map(q => q.tekst)));
      if (heeft('letop', /^Gevel g4 en g5|^Gevel g3 en g4/)) f.push('een overlap voor huizen die elkaar niet raken');
      const sp = mkNaarLevel().spawns, sch = sp.find(x => x.k === 'schildman'), ban = sp.find(x => x.k === 'bandiet'), sl = sp.find(x => x.k === 'groen');
      if (!sch || sch.dak !== 730) f.push('de schildbandiet op de galerij krijgt geen dak: 730: ' + JSON.stringify(sch));
      if (!ban || ban.dak !== 816 || !ban.dolk) f.push('de bandiet op het dak van g5 krijgt geen dak: 816: ' + JSON.stringify(ban));
      if (!sl || 'dak' in sl || sl.boven) f.push('de zandslang op een dak krijgt toch dak of boven: ' + JSON.stringify(sl));
      const krb = sp.find(x => x.k === 'kruisboogbandiet');
      if (!krb || krb.dak !== 816 || krb.wijk !== false || krb.boven || 'y' in krb) f.push('de kruisboogbandiet op het dak van g5 krijgt geen dak: 816 met wijk: false: ' + JSON.stringify(krb));
      // en in het spel leest readLevel het zo
      const rl = readLevel(JSON.stringify(mkNaarLevel())).spawns.find(x => x.kind === 'schildman');
      if (!rl || rl.dak !== 730) f.push('readLevel leest het dak van de schildbandiet niet: ' + JSON.stringify(rl));
      const rk = readLevel(JSON.stringify(mkNaarLevel())).spawns.find(x => x.kind === 'kruisboogbandiet');
      if (!rk || rk.dak !== 816 || rk.wijk !== false) f.push('readLevel leest dak en wijk van de kruisboogbandiet niet: ' + JSON.stringify(rk));
      // een galerij op 401 langs g4: dan is er bij de uitgang wel een vloer
      MK.objects.push({ c: 16, r: 8, k: 'galerij', van: 'g4', tot: 'g4', niveau: 1, meer: [0, 1] }); mkStadKoppel();
      if (mkControle().some(q => q.ernst === 'fout' && /^De trap bij g4 \(links/.test(q.tekst))) f.push('een galerij bij de uitgang haalt de FOUT niet weg');
      return f;
    }));
    // het proefgrid heeft de stad goed staan: geen melding over de stad, en dak op de bandiet, de schildbandiet en de kruisboogbandiet
    await laad(proefGrid());
    f.push(...await page.evaluate(() => {
      const f = [], m = mkControle().filter(q => q.ernst !== 'info' && /Gevel|galerij|trap|daken|straat/i.test(q.tekst));
      if (m.length) f.push('het proefgrid geeft een melding over de stad: ' + JSON.stringify(m.map(q => q.tekst)));
      const lv = mkNaarLevel(), S = lv.stad || {};
      if ((S.gevels || []).length !== 2 || (S.galerijen || []).length !== 1 || (S.trappen || []).length !== 1 || (S.kramen || []).length !== 1 || (S.voet || []).length !== 1 || S.paleis == null || S.seed !== 7)
        f.push('het proefgrid geeft niet de hele stad: ' + JSON.stringify(S));
      if (!lv.spawns.some(x => x.k === 'bandiet' && x.dak === 401) || !lv.spawns.some(x => x.k === 'schildman' && x.dak === 816)) f.push('in het proefgrid geen dak op de bandiet (401) en de schildbandiet (816): ' + JSON.stringify(lv.spawns));
      if (!lv.spawns.some(x => x.k === 'kruisboogbandiet' && x.dak === 816 && x.wijk === false && x.inBeeld === true)) f.push('in het proefgrid geen kruisboogbandiet met dak 816, wijk uit en inBeeld aan: ' + JSON.stringify(lv.spawns));
      if (!(lv.hpBalk || []).includes('kruisboogbandiet')) f.push('de kruisboogbandiet staat niet in hpBalk: ' + JSON.stringify(lv.hpBalk));
      // de deuren: g1 is index 1 en g2 index 0 (van de start af); de vijand op de verdieping krijgt geen dak, de deur geeft de hoogte
      const d1 = lv.spawns.filter(x => x.deur && x.deur.gevel === 1), d2 = lv.spawns.filter(x => x.deur && x.deur.gevel === 0);
      if (d1.length !== 1 || d1[0].k !== 'bandiet' || !d1[0].dolk || d1[0].deur.verdieping !== 0) f.push('in het proefgrid geen bandiet met dolk uit het deurgat van g1: ' + JSON.stringify(d1));
      if (d2.length !== 2 || d2.some(x => x.k !== 'bandiet' || x.deur.verdieping !== 1 || 'dak' in x || x.boven)) f.push('in het proefgrid niet twee bandieten uit de deur op de eerste verdieping van g2: ' + JSON.stringify(d2));
      return f;
    }));
    return f;
  });

  // 1c. deuren (stap 8): een klik met Deur op een gevel zet een deur op de verdieping waar je klikte; in het paneel de vijand
  // eruit en Aantal; in het level een spawn met deur {gevel, verdieping}. De controle meldt een deur zonder vijand, een deur
  // die er niet is (het huis is lager) en een deur op een verdieping zonder galerij of balkon, of met een soort die geen daken kent.
  await check('deuren: een vijand uit het deurgat of een deur op een verdieping', async () => {
    const f = [];
    const rijen = []; for (let r = 0; r < 12; r++) rijen.push((r === 9 ? 'A' : '.').repeat(40));
    await laad({ type: 'amir-levelmaker-grid', versie: 2, cols: 40, rows: 12, groundRow: 9, grid: rijen,
                 start: { c: 39, r: 8 }, eind: { c: 0, r: 8 }, objecten: [
                   { c: 4, r: 8, k: 'gevel', id: 'g1', hoog: 2 }, { c: 9, r: 8, k: 'gevel', id: 'g2', hoog: 3 },
                   { c: 4, r: 8, k: 'galerij', van: 'g1', tot: 'g2', niveau: 1 } ] });
    const puntXY = (x, y) => page.evaluate(([x, y]) => { const b = mkCanvas.getBoundingClientRect(), cel = mkCel();
      return { x: b.left + MK.panX + x * cel, y: b.top + MK.panY + y * cel }; }, [x, y]);
    await page.evaluate(() => { mkThemaZet('stad'); MK.sel = null; MK.inspectDicht = true; mkNotePaneel(); MK.tool = 'deur'; mkLegenda(); });
    const mid = await page.evaluate(() => MK.objects.filter(o => o.k === 'gevel').map(g => { const [l, r] = mkGevelMuur(g); return (l + r) / 2; }));
    let a = await puntXY(mid[0], 8.5); await page.mouse.click(a.x, a.y);                 // g1 op de straat
    a = await puntXY(mid[1], 9 - 550 / 150); await page.mouse.click(a.x, a.y);           // g2 tussen 401 en 730: de eerste verdieping
    a = await puntXY(20, 8.5); await page.mouse.click(a.x, a.y);                          // naast de huizen: geen deur
    f.push(...await page.evaluate(() => {
      const f = [], de = MK.objects.filter(o => o.k === 'deur');
      const d1 = de.find(o => o.gevel === 'g1'), d2 = de.find(o => o.gevel === 'g2');
      if (de.length !== 2 || !d1 || mkDeurVerd(d1) !== 0 || !d2 || mkDeurVerd(d2) !== 1) return ['een klik op g1 en op de eerste verdieping van g2 geeft niet twee deuren: ' + JSON.stringify(de)];
      if (d1.vijand !== 'bandiet') f.push('een nieuwe deur heeft niet standaard een bandiet: ' + JSON.stringify(d1));
      // het paneel: de vijand en Aantal, niet de knoppen van de galerij of trap
      MK.tool = 'select'; MK.sel = d1; MK.inspectDicht = false; mkNotePaneel();
      if (document.getElementById('mkdeurvijrij').offsetParent === null || document.getElementById('mkgallrij').offsetParent !== null || document.getElementById('mktrapkantrij').offsetParent !== null)
        f.push('het paneel van een deur toont niet Vijand eruit, of wel de knoppen van de galerij of trap');
      const vs = document.getElementById('mkdeurvij'); vs.value = 'scorp'; vs.dispatchEvent(new Event('change'));
      const nr = document.getElementById('mkdeurn'); nr.value = '2'; nr.dispatchEvent(new Event('input'));
      if (d1.vijand !== 'scorp' || d1.n !== 2) f.push('het paneel zet vijand of aantal niet: ' + JSON.stringify(d1));
      if ([...vs.options].some(o => ['hyenas', 'panter', 'bandiet:hurk'].includes(o.value))) f.push('Vijand eruit biedt een hyena, panter of de hinderlaag aan');
      // aanklikken op het gat geeft de deur, het huis ernaast blijft de gevel
      const m = mkDeurMaat(d2);
      if (mkObjOp(Math.floor(m.cx), Math.floor((m.r0 + m.r1) / 2)) !== d2) f.push('de deur op de verdieping is niet aan te klikken in zijn gat');
      // het level: g2 is index 0, g1 index 1; twee schorpioenen uit het deurgat van g1, een bandiet op de verdieping van g2
      const lv = mkNaarLevel(), S = lv.spawns.filter(x => x.deur);
      const s1 = S.filter(x => x.deur.gevel === 1), s2 = S.filter(x => x.deur.gevel === 0);
      if (s1.length !== 2 || s1.some(x => x.k !== 'scorp' || x.deur.verdieping !== 0 || x.x !== s1[0].x)) f.push('niet twee schorpioenen uit het deurgat van g1: ' + JSON.stringify(s1));
      if (s2.length !== 1 || s2[0].k !== 'bandiet' || s2[0].deur.verdieping !== 1 || 'dak' in s2[0]) f.push('geen bandiet uit de deur op de eerste verdieping van g2: ' + JSON.stringify(s2));
      if (lv.spawns.some(x => !x.deur)) f.push('een level met alleen deurvijanden krijgt toch een standaard-slang: ' + JSON.stringify(lv.spawns));
      const g1x = lv.stad.gevels[1].x; if (!(s1[0].x > g1x && s1[0].x < g1x + 400)) f.push('de x van de deurvijand ligt niet in het huis: ' + s1[0].x + ' bij ' + g1x);
      const rl = readLevel(JSON.stringify(lv)).spawns.filter(x => x.deur);
      if (rl.length !== 3 || !rl.some(x => x.deur.gevel === 0 && x.deur.verdieping === 1)) f.push('readLevel leest deur niet: ' + JSON.stringify(rl));
      // de JSON
      const j = JSON.stringify(mkNaarJSON()); mkUitJSON(JSON.parse(j));
      if (JSON.stringify(mkNaarJSON()) !== j) f.push('de deuren komen niet gelijk door de JSON');
      // de controle: nu niets over de deuren
      const deurM = () => mkControle().filter(q => /^De deur van/.test(q.tekst));
      if (deurM().length) f.push('een melding voor goede deuren: ' + JSON.stringify(deurM().map(q => q.tekst)));
      const zoek = (ernst, re) => deurM().find(q => q.ernst === ernst && re.test(q.tekst));
      const e2 = MK.objects.find(o => o.k === 'deur' && o.gevel === 'g2'), e1 = MK.objects.find(o => o.k === 'deur' && o.gevel === 'g1');
      const moet = (ernst, re, wat) => { const q = zoek(ernst, re); if (!q) f.push('geen ' + ernst + ' voor ' + wat + ': ' + JSON.stringify(deurM().map(q => q.tekst))); else if (q.c == null || q.r == null) f.push('de melding voor ' + wat + ' heeft geen cel'); };
      e2.verdieping = 2; moet('fout', /^De deur van g2 \(2e verdieping\) heeft geen galerij of balkon/, 'een deur zonder galerij');
      e2.verdieping = 3; moet('fout', /^De deur van g2 \(3e verdieping\) is er niet/, 'een deur boven het dak');
      e2.verdieping = 1; e2.vijand = 'kooiman:smash'; moet('fout', /^De deur van g2 \(1e verdieping\): .* kent geen galerij/, 'een soort zonder daken op een verdieping');
      e2.vijand = 'bandiet'; e1.vijand = undefined; moet('letop', /^De deur van g1 \(straat\) heeft geen vijand/, 'een deur zonder vijand');
      // een gevel weg: zijn deur gaat mee
      MK.objects = MK.objects.filter(o => !(o.k === 'gevel' && o.id === 'g1')); mkStadKoppel();
      if (MK.objects.some(o => o.k === 'deur' && o.gevel === 'g1')) f.push('de deur van g1 blijft staan zonder zijn gevel');
      MK.tool = 'select'; mkThemaZet('savanne'); MK.themaGeheugen = {}; mkLegenda();
      return f;
    }));
    return f;
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
    const rp = (lv.props || []).find(q => q.k === 'plaat_02');
    if (!rp || !rp.f || rp.s !== 1.2 || (lv.props || []).length !== 1) uit.push('geen gespiegelde plaat_02 op schaal 1,2 als enige prop: ' + JSON.stringify(lv.props));
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
    // straat op kolom 2 en 3 en achter de start (12 cellen); met het veld stad krijgt de savanne ook zijn eigen stroken
    const straat = (lv.grondSoort || []).filter(g => g.soort === 'straat').map(g => Math.abs(g.van - g.tot)).sort((a, b) => a - b);
    if (straat.join() !== '350,2100' || !(lv.grondSoort || []).some(g => g.soort === 'savanne'))
      uit.push('geen stroken straat van 2 en 12 cellen (350 en 2100 px) naast savanne: ' + JSON.stringify(lv.grondSoort));
    if (!lv.stad || lv.lagen !== 'stad_dag') uit.push('de stad achter de start geeft geen veld stad of geen uitzicht stad_dag');
    if (!sp.some(s => s.k === 'bandiet' && s.dak === 401)) uit.push('de bandiet op de galerij krijgt geen dak: 401: ' + JSON.stringify(sp));
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
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(36)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
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
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(36)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
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
    await laad({ ...proefGrid(), grid: proefGrid().grid.map(() => '.'.repeat(36)), objecten: [], maskers: [], zwart: [], vormen: [], start: null, eind: null });
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
    const n0 = proefGrid().objecten.length;                            // het proefgrid, plus de geplakte richel en zandslang
    if (na.n !== n0 + 2) uit.push('aantal voorwerpen na plakken: ' + na.n + ' in plaats van ' + (n0 + 2));
    // knippen: het gebied is nu het geplakte stuk; Ctrl+X maakt het leeg
    await page.keyboard.press('Control+x');
    const leeg = await page.evaluate(() => ({ cel: MK.grid[2].slice(14, 18).join(' '), n: MK.objects.length }));
    if (leeg.cel !== 'lucht lucht lucht lucht' || leeg.n !== n0) uit.push('na knippen: ' + JSON.stringify(leeg));
    await page.keyboard.press('Control+z');
    const terug = await page.evaluate(() => MK.objects.length);
    if (terug !== n0 + 2) uit.push('ongedaan maken na knippen: ' + terug + ' voorwerpen in plaats van ' + (n0 + 2));
    return uit;
  });

  // 5e. de minimap en Test vanaf hier
  await check('minimap: klikken brengt die plek in beeld; Test vanaf hier start op het gebied', async () => {
    await laad(proefGrid());
    const uit = [];
    const mini = await page.evaluate(() => { const m = document.getElementById('mkmini'); const b = m.getBoundingClientRect(); return { w: m.width, h: m.height, x: b.left, y: b.top, bw: b.width, bh: b.height, zicht: getComputedStyle(m).display !== 'none' }; });
    if (!mini.zicht || mini.w < 40) uit.push('geen minimap: ' + JSON.stringify(mini));
    await page.evaluate(() => { MK.zoom = 2.5; mkTeken(); });
    await page.mouse.click(mini.x + mini.bw * (22.5 / 36), mini.y + mini.bh * (8.5 / 12));   // op cel (22, 8)
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
      // een deur hangt aan een gevel: met de gevel erbij, op een verdieping en met een vijand en Aantal
      { const g = { c:5, r:MK.ground - 1, k:'gevel', id:'g1', hoog:3, note:'' }, o = { c:5, r:MK.ground - 1, k:'deur', gevel:'g1', verdieping:1, vijand:'bandiet', n:3, note:'' };
        MK.objects = [g, o]; MK.sel = o; mkNotePaneel(); for (const m of mkPaneelKlachten()) f.push('deur: ' + m); }
      // elke vijandsoort, met al zijn knoppen van de standaard af (dan staat elk kopje open, zoals Gedrag van de kruisboogbandiet)
      for (const soort of Object.keys(MK_VIJ_KNOP)){
        const params = {}; for (const q of MK_VIJ_KNOP[soort]) params[q.key] = q.vink ? 1 - q.def : q.max;
        const o = { c:5, r:MK.ground - 1, k:'vijand', soort, params, note:'' };
        MK.objects = [o]; MK.sel = o; mkNotePaneel();
        for (const m of mkPaneelKlachten()) f.push('vijand ' + soort + ': ' + m);
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
  await check('vijand-knoppen: vault uit, panter over, twee hyena\'s, zicht uit en de vlaggen van de kruisboogbandiet komen op de spawn', async () => {
    const g = proefGrid();
    g.objecten = [
      { c: 6, r: 6, k: 'vijand', soort: 'bandiet', params: { vault: 0 }, note: '' },
      { c: 8, r: 6, k: 'vijand', soort: 'panter', params: { over: 1, zicht: 0 }, note: '' },
      { c: 12, r: 6, k: 'vijand', soort: 'hyenas', params: { n: 2 }, note: '' },
      { c: 14, r: 6, k: 'vijand', soort: 'scorp', params: { zicht: 1 }, note: '' },
      { c: 16, r: 6, k: 'vijand', soort: 'kruisboogbandiet', params: { wijk: 0, rand: 1, hoorn: 1, rap: 1, inBeeld: 0 }, note: '' },
      { c: 17, r: 6, k: 'vijand', soort: 'kruisboogbandiet', params: { wijk: 1, rand: 0, inBeeld: 1 }, note: '' },
    ];
    await laad(g);
    const sp = await page.evaluate(() => mkNaarLevel().spawns);
    const uit = [];
    const b = sp.find(x => x.k === 'bandiet'), pa = sp.find(x => x.k === 'panter'), h = sp.find(x => x.k === 'hyenas'), sc = sp.find(x => x.k === 'scorp');
    if (!b || b.vault !== false) uit.push('bandiet: vault ' + JSON.stringify(b && b.vault) + ' in plaats van false');
    if (!pa || pa.over !== true || pa.zicht !== false) uit.push('panter: ' + JSON.stringify(pa));
    if (!h || h.n !== 2) uit.push('hyenas: ' + JSON.stringify(h));
    if (!sc || 'zicht' in sc) uit.push('schorpioen met de standaard zicht hoort geen zicht-veld te krijgen: ' + JSON.stringify(sc));
    // de kruisboogbandiet: alleen wat van de standaard afwijkt gaat mee (wijk staat standaard aan, de rest uit)
    const kb = sp.filter(x => x.k === 'kruisboogbandiet');
    const kv = x => JSON.stringify(['wijk', 'rand', 'hoorn', 'rap', 'inBeeld'].map(k => k in x ? k + ':' + x[k] : '-'));
    if (kb.length !== 2) uit.push('geen twee kruisboogbandieten: ' + JSON.stringify(kb));
    else {
      if (kv(kb[0]) !== JSON.stringify(['wijk:false', 'rand:true', 'hoorn:true', 'rap:true', '-'])) uit.push('kruisboogbandiet 1 (wijk uit, rand, hoorn, rap): ' + JSON.stringify(kb[0]));
      if (kv(kb[1]) !== JSON.stringify(['-', '-', '-', '-', 'inBeeld:true'])) uit.push('kruisboogbandiet 2 (alleen inBeeld): ' + JSON.stringify(kb[1]));
    }
    // en in het spel: readLevel leest ze zo
    const lv = await page.evaluate(() => { const l = readLevel(JSON.stringify(mkNaarLevel())); return l.spawns.map(x => ({ kind: x.kind, vault: x.vault, over: x.over, zicht: x.zicht, n: x.n })); });
    const lb = lv.find(x => x.kind === 'bandiet'), lp = lv.find(x => x.kind === 'panter'), lh = lv.find(x => x.kind === 'hyenas');
    if (!lb || lb.vault !== false) uit.push('readLevel: bandiet vault ' + JSON.stringify(lb));
    if (!lp || lp.over !== true || lp.zicht !== false) uit.push('readLevel: panter ' + JSON.stringify(lp));
    if (!lh || lh.n !== 2) uit.push('readLevel: hyenas ' + JSON.stringify(lh));
    const lk = await page.evaluate(() => readLevel(JSON.stringify(mkNaarLevel())).spawns.filter(x => x.kind === 'kruisboogbandiet').map(x => ({ wijk: x.wijk, rand: x.rand, hoorn: x.hoorn, rap: x.rap, inBeeld: x.inBeeld })));
    if (lk.length !== 2 || lk[0].wijk !== false || !lk[0].rand || !lk[0].hoorn || !lk[0].rap || lk[1].inBeeld !== true || lk[1].wijk === false)
      uit.push('readLevel: kruisboogbandieten ' + JSON.stringify(lk));
    // het paneel van de kruisboogbandiet: een kopje Gedrag met zijn vijf vinkjes, open omdat er een afwijkt, en met de hoorn
    // staat inBeeld vast aan; zet je de hoorn uit, dan komt inBeeld los
    const pk = await page.evaluate(() => {
      MK.tool = 'select'; MK.sel = MK.objects.find(o => o.soort === 'kruisboogbandiet'); MK.inspectDicht = false; mkNotePaneel();
      const d = document.querySelector('#mkvijknop details.mkklap'), vk = d ? [...d.querySelectorAll('input[type=checkbox]')] : [];
      const uit = { kopje: d && d.querySelector('summary').textContent, open: d && d.open, n: vk.length, los: document.querySelectorAll('#mkvijknop > .mkveld').length,
                    inBeeld: vk[4] && { aan: vk[4].checked, vast: vk[4].disabled }, klacht: mkPaneelKlachten() };
      vk[2].checked = false; vk[2].dispatchEvent(new Event('change'));
      const vk2 = [...document.querySelectorAll('#mkvijknop details.mkklap input[type=checkbox]')];
      uit.na = { hoorn: MK.sel.params.hoorn, inBeeld: vk2[4] && { aan: vk2[4].checked, vast: vk2[4].disabled } };
      return uit;
    });
    if (pk.kopje !== 'Gedrag' || !pk.open || pk.n !== 5 || pk.los !== 1) uit.push('het paneel van de kruisboogbandiet: ' + JSON.stringify(pk));
    if (!pk.inBeeld || !pk.inBeeld.aan || !pk.inBeeld.vast) uit.push('met de hoorn staat inBeeld niet vast aan: ' + JSON.stringify(pk.inBeeld));
    if (pk.klacht.length) uit.push('het paneel van de kruisboogbandiet is te lang: ' + JSON.stringify(pk.klacht));
    if (pk.na.hoorn !== 0 || !pk.na.inBeeld || pk.na.inBeeld.aan || pk.na.inBeeld.vast) uit.push('de hoorn uit maakt inBeeld niet los: ' + JSON.stringify(pk.na));
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
    const alleenPoort = await page.evaluate(() => { const was = MK.objects; MK.objects = was.filter(o => o.k !== 'vijand' && o.k !== 'deur'); const lv = mkNaarLevel(); MK.objects = was;   // de deuren van het proefgrid ook weg
      const leeg = was.filter(o => o.k !== 'vijand' && o.k !== 'poort' && o.k !== 'deur'); MK.objects = leeg; const lv0 = mkNaarLevel(); MK.objects = was; return { los: lv.spawns.filter(s => !s.poort), leeg: lv0.spawns }; });
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
  // 7b. per voorwerp verbergen: een poort achter een masker zonder cellen, en de vaste looks als nep-terrein
  await check('masker per voorwerp: Verborgen door masker overleeft de round-trip en verbergt het hele voorwerp', async () => {
    const uit = [];
    const g = proefGrid();
    g.objecten.find(o => o.k === 'poort').achter = 'Alleen';
    g.objecten.find(o => o.k === 'rune').masker = 'Alleen';
    await laad(g);
    const r = await page.evaluate(() => {
      const j = mkNaarJSON(), lv = mkNaarLevel();
      const m = (lv.maskers || []).find(q => q.id === 'Alleen'), v1 = (lv.maskers || []).find(q => q.id === 'Verborgen1');
      const poort = MK.objects.find(o => o.k === 'poort');
      return { bewaard: j.maskers.some(q => q.id === 'Alleen' && !q.cells.length), achter: j.objecten.find(o => o.k === 'poort').achter,
        punt: !!(m && m.vakken.length && m.vakken.every(v => v.punt)), look: v1 && v1.look, nep: !!lv.nep,
        verborgen: mkObjVerborgen(poort), letop: mkControle().some(q => /steekt in masker/.test(q.tekst)) };
    });
    if (!r.bewaard) uit.push('het masker met alleen een voorwerp ging niet mee in de export');
    if (r.achter !== 'Alleen') uit.push('achter ging niet mee in de export: ' + r.achter);
    if (!r.punt) uit.push('het masker werd in het spel geen punt op de cel van de poort');
    if (r.look !== 'onzichtbaar' || !r.nep) uit.push('de grotwand werd geen nep-terrein: ' + r.look + ', nep ' + r.nep);
    if (r.verborgen !== 'Alleen') uit.push('mkObjVerborgen ziet de poort niet als verborgen: ' + r.verborgen);
    await page.evaluate(() => { MK.objects.find(o => o.k === 'poort').achter = undefined; MK.objects.find(o => o.k === 'poort').c = 7; MK.objects.find(o => o.k === 'poort').r = 6; });
    const let2 = await page.evaluate(() => mkControle().filter(q => /steekt in masker/.test(q.tekst)).length);
    if (!let2) uit.push('een poort naast het masker gaf geen LET OP');
    return uit;
  });
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
