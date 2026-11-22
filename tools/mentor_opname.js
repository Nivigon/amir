#!/usr/bin/env node
// De opname van de mentor (Test 87, The First Hunt): speelt het level met Amir en legt per beeld vast welk plaatje
// waar stond. Daaruit tekent het spel de mentor (zie "tutorial: de mentor" in de HTML en notities/tutorial.md).
//
// Per stuk (seg) staat hieronder een rij opdrachten: lopen tot een x, springen, kruipen, rollen, omdraaien en wachten.
// Een stuk eindigt altijd met omdraaien en een idle: vanaf `lus` speelt het spel die idle in een lus terwijl hij wacht.
// Het spoor gaat naar design/tutorial/mentor_spoor.json, op MENTOR.fps (30) beelden per seconde.
//
//   node tools/mentor_opname.js            opnemen en wegschrijven
//   node tools/mentor_opname.js --spoor    elke tiende seconde x, hoogte en op de grond, om de opdrachten af te stellen
//   node tools/mentor_opname.js --droog    niet wegschrijven
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright');

const ROOT = path.dirname(__dirname);
const UIT = path.join(ROOT, 'design/tutorial/mentor_spoor.json');
const args = process.argv.slice(2);

// de opdrachten. x is de wereld-x (Amir loopt naar links, dus negatief); `tot` loopt tot die x
const START = [ { tot: -450 }, { draai: 1 }, { idle: 0.6, stil: true }, { lus: 1 }, { idle: 2.6 } ];
const SEGS = [
  // 0: naar de kei, eroverheen
  [ { tot: -690 }, { spring: 14, tot: -1150 }, { draai: 1 }, { lus: 1 }, { idle: 2.6 } ],
  // 1: het terras op, de twee lagen op
  [ { tot: -1395 }, { spring: 10, tot: -1700 }, { spring: 16, tot: -1975 }, { spring: 16, tot: -2300 }, { draai: 1 }, { lus: 1 }, { idle: 2.6 } ],
  // 2: eraf, en kruipend onder het rotsdak door
  [ { tot: -2880 }, { kruip: true, tot: -3430 }, { tot: -3600 }, { draai: 1 }, { lus: 1 }, { idle: 2.6 } ],
  // 3: rollen
  [ { tot: -3760 }, { rol: 1, tot: -4100 }, { draai: 1 }, { lus: 1 }, { idle: 2.6 } ],
  // 4: de sprintsprong over het ravijn
  [ { sprint: true, tot: -4255 }, { spring: 16, sprint: true, tot: -5000 }, { draai: 1 }, { lus: 1 }, { idle: 2.6 } ],
  // 5: de race naar de top (seg 6 in het level is de race; seg 5 hierboven is de sprong)
  [ { sprint: true, tot: -5215 }, { spring: 14, sprint: true, tot: -5715 }, { spring: 14, sprint: true, tot: -6200 },
    { kruip: true, tot: -6575 }, { sprint: true, tot: -6790 }, { spring: 16, sprint: true, tot: -7240 },
    { spring: 16, sprint: true, tot: -7690 }, { spring: 16, sprint: true, tot: -8150 }, { draai: 1 }, { lus: 1 }, { idle: 3 } ]
];

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp3': 'audio/mpeg', '.css': 'text/css' };
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

// draait in de pagina: de opdrachten per beeld, en de vangst van elk beeld van Amir
function opname([START, SEGS]){
  const B = window.__op = { klaar: false, fout: null, beelden: [], idx: {}, start: null, segs: [], spoor: [], t: 0 };
  const toets = (k, neer) => dispatchEvent(new KeyboardEvent(neer ? 'keydown' : 'keyup', { key: k }));
  const lijst = [START, ...SEGS];
  let si = 0, ci = 0, cur = { f: [], lus: 0 }, st = null, laatste = null, tel = 0;
  const losAlles = () => { for (const k of ['ArrowLeft', 'ArrowRight', 'Shift', 'ArrowDown', 'ArrowUp']) if (keys[k]) toets(k, false); };
  mentorOpname = (img, x, y, w, h, fl, pcx, voet, scale) => {
    const s = pvpBron(img);
    if (!s) return;
    if (B.idx[s] == null){ B.idx[s] = B.beelden.length; B.beelden.push(s); }
    laatste = [Math.round(playerX()), Math.round(ph), B.idx[s], +((x - pcx) / scale).toFixed(1), +((y - voet) / scale).toFixed(1),
               +(w / scale).toFixed(1), +(h / scale).toFixed(1), fl ? 1 : 0, onGround ? 1 : 0];
  };
  window.__opStap = () => {
    if (B.klaar || laadWacht) return;                     // het level laadt nog: de lus staat stil
    B.t += 1 / 60;
    if (B.t > 400){ B.fout = 'te lang'; B.klaar = true; return; }
    const c = lijst[si][ci];
    if (!c){                                               // dit stuk is af
      if (si === 0) B.start = { f: cur.f.slice(cur.lus) }; else B.segs.push(cur);
      si++; ci = 0; cur = { f: [], lus: 0 }; st = null;
      if (si >= lijst.length){ losAlles(); B.klaar = true; }
      return;
    }
    // het vorige beeld vastleggen, op 30 per seconde (elk tweede beeld), behalve in het stille aanloopje van de start
    tel++;
    if (laatste && tel % 2 === 0 && !(si === 0 && !(c.idle || c.lus))) cur.f.push(laatste);
    if (laatste && tel % 2 === 0 && c.stil) cur.f.pop();
    if (tel % 6 === 0) B.spoor.push([si, ci, Math.round(world), Math.round(ph), onGround ? 1 : 0, duckT.toFixed(1)]);
    if (!st){                                              // een nieuwe opdracht begint
      st = { t: 0 };
      if (c.lus){ cur.lus = cur.f.length; ci++; st = null; return; }
      if (c.draai){ losAlles(); toets('ArrowRight', true); st.draai = 2; }
      if (c.rol){ st.rol = true; }
      if (c.spring){ st.spring = c.spring; }
    }
    st.t += 1 / 60;
    if (c.draai){ if (--st.draai <= 0){ toets('ArrowRight', false); ci++; st = null; } return; }
    if (c.idle){ losAlles(); if (st.t >= c.idle){ ci++; st = null; } return; }
    // lopen naar links, met of zonder sprint en gebukt; springen of rollen aan het begin van de opdracht
    if (!keys['ArrowLeft']) toets('ArrowLeft', true);
    if (c.sprint && !keys['Shift']) toets('Shift', true);
    if (!c.sprint && keys['Shift']) toets('Shift', false);
    if (c.kruip && !keys['ArrowDown']) toets('ArrowDown', true);
    if (!c.kruip && keys['ArrowDown']) toets('ArrowDown', false);
    if (st.spring != null){
      if (st.spring === c.spring) toets('ArrowUp', true);
      if (--st.spring <= 0){ toets('ArrowUp', false); st.spring = null; }
    }
    if (st.rol){ toets('v', true); toets('v', false); st.rol = false; }
    if (c.tot != null && world <= c.tot && (onGround || c.kruip)){ ci++; st = null; }
    if (st && st.t > 30){ B.fout = 'vast bij stuk ' + si + ' opdracht ' + ci + ' op x ' + Math.round(world); B.klaar = true; }
  };
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('pageerror', e => console.log('fout: ' + e.message));
  await page.addInitScript(() => {
    let vt = 1000;
    window.requestAnimationFrame = cb => setTimeout(() => {
      vt += 1000 / 60; cb(vt);
      if (window.__opStap){ try { window.__opStap(); } catch (e){ console.error('opname: ' + e.message); } }
    }, 0);
  });
  await page.goto(url);
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof TEST_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    const i = TEST_LEVELS.findIndex(l => l.name.includes('First Hunt'));
    const def = TEST_LEVELS[i];
    def._mentor = def.mentor; delete def.mentor;            // opnemen zonder mentor in beeld
    setLevel(i, TEST_LEVELS); beginPlay('medium');
  });
  await page.waitForTimeout(800);
  await page.evaluate(opname, [START, SEGS]);
  for (;;){
    await page.waitForTimeout(500);
    const k = await page.evaluate(() => window.__op.klaar);
    if (k) break;
  }
  const B = await page.evaluate(() => window.__op);
  if (args.includes('--spoor')) for (const r of B.spoor) console.log(r.join('\t'));
  if (B.fout){ console.log('FOUT: ' + B.fout); }
  console.log('beelden: ' + B.beelden.length + ', start ' + (B.start ? B.start.f.length : 0) + ', stukken ' + B.segs.map(s => s.f.length + '/' + s.lus).join(' '));
  if (!B.fout && !args.includes('--droog')){
    fs.mkdirSync(path.dirname(UIT), { recursive: true });
    const regel = f => '[' + f.join(',') + ']';
    const tekst = '{\n"fps": 30,\n"beelden": ' + JSON.stringify(B.beelden) + ',\n"start": {"f": [\n' + B.start.f.map(regel).join(',\n') + ']},\n"segs": [\n' +
      B.segs.map(s => '{"lus": ' + s.lus + ', "f": [\n' + s.f.map(regel).join(',\n') + ']}').join(',\n') + '\n]}\n';
    fs.writeFileSync(UIT, tekst);
    console.log('geschreven: ' + path.relative(ROOT, UIT) + ' (' + Math.round(tekst.length / 1024) + ' kB)');
  }
  await browser.close(); srv.close();
})();
