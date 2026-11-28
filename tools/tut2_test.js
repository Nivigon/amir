#!/usr/bin/env node
// Speelt tutorial 2 (The Spear, TUT_2) uit met een simpele speler in Chromium, op vaste 60 fps, en meldt per station
// wanneer de gids verder ging. Faalt (FOUT) als hij ergens langer dan 60 s blijft hangen, of bij een fout in de console.
//   node tools/tut2_test.js               uitspelen
//   node tools/tut2_test.js --shots map   bij elk nieuw station en elke golf een schermafdruk
//   node tools/tut2_test.js --een         de golven een voor een (zonder op een dubbele zwaai te wachten)
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright');

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const SHOTS = args.includes('--shots') ? args[args.indexOf('--shots') + 1] : null;

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

// draait in de pagina: elk beeld een beslissing, als een speler met toetsen
function speler(opties){
  const B = window.__tt = { log: [], klaar: false, fout: null, t: 0, shot: 0, station: -1, golf: -1 };
  const toets = (k, neer) => { if (!!keys[k] === neer) return; dispatchEvent(new KeyboardEvent(neer ? 'keydown' : 'keyup', { key: k })); };
  const tik = k => { dispatchEvent(new KeyboardEvent('keydown', { key: k })); dispatchEvent(new KeyboardEvent('keyup', { key: k })); };
  let wachtF = 0;
  window.__ttStap = () => {
    if (B.klaar || laadWacht || !running) return;
    B.t += 1 / 60;
    if (won){ B.log.push(['gewonnen', B.t.toFixed(1)]); B.klaar = true; return; }
    if (B.t > 600){ B.fout = 'te lang'; B.klaar = true; return; }
    const m = mentor;
    if (!m || !m.spoor){ return; }
    if (m.i !== B.station){ B.station = m.i; B.sindsT = B.t; B.log.push(['station', m.i, B.t.toFixed(1), Math.round(world)]); B.shot++; }
    if (opties.debug && Math.round(B.t * 60) % 60 === 0) B.log.push(['dbg', B.t.toFixed(0), Math.round(world), m.fase, JSON.stringify(m.eis), duckT.toFixed(2), swFrame, swLading, m.deel, snakes.map(s => s.state + '@' + Math.round(s.x) + '/' + s.side).join(' ')]);
    if (B.t - B.sindsT > 60){ B.fout = 'vast in station ' + m.i + ' fase ' + m.fase + ' op x ' + Math.round(world); B.klaar = true; return; }
    if (m.golf && m.golf.n !== B.golf){ B.golf = m.golf.n; B.log.push(['golf', m.golf.n, B.t.toFixed(1)]); B.shot++; }
    if (B.fT > 0 && --B.fT === 0){ dispatchEvent(new KeyboardEvent('keyup', { key: 'f' })); keys['f'] = false; wachtF = 40; return; }
    if (wachtF > 0){ wachtF--; return; }
    const st = mentorStation();
    const levend = snakes.filter(s => s.tutSlang && s.state !== 'dying' && s.state !== 'gone');
    const naast = levend.length ? levend.reduce((a, b) => Math.abs(a.x - world) < Math.abs(b.x - world) ? a : b) : null;
    // een slang: omdraaien naar hem en uithalen als hij dichtbij is
    if (naast){
      toets('ArrowLeft', false);
      const rechts = naast.x > world, d = Math.abs(naast.x - world);
      if ((facing > 0) !== rechts){ toets(rechts ? 'ArrowRight' : 'ArrowLeft', true); wachtF = 2; return; }
      if (d > 260 && d < 420 && onGround){ toets(rechts ? 'ArrowRight' : 'ArrowLeft', true); return; }   // erop af
      toets('ArrowRight', false); toets('ArrowLeft', false);
      const laag = st && st.eis === 'golven' && st.golven.length > 1;
      if (laag){
        const al = levend.filter(s => Math.abs(s.x - world) < 255).length >= Math.min(2, levend.length);
        const tweeKanten = levend.some(s => s.x < world) && levend.some(s => s.x > world);
        if (!opties.een && !al && d > 100 && !tweeKanten){ toets('ArrowDown', false); toets(rechts ? 'ArrowRight' : 'ArrowLeft', true); return; }   // erin stappen tot ze allebei binnen de zwaai zijn
        toets('ArrowRight', false); toets('ArrowLeft', false);
        toets('ArrowDown', true);
        // twee: wachten tot de tweede ook in bereik is (behalve met --een)
        const tweede = levend.filter(s => Math.abs(s.x - world) < 255).length;
        if (d < 255 && (opties.een || tweede >= Math.min(2, levend.length) || d < 95)){ tik('f'); wachtF = 20; }
      } else {
        toets('ArrowDown', false);
        if (d < 230){ tik('f'); wachtF = 20; }
      }
      return;
    }
    if (!(st && st.eis === 'zwaai')) toets('ArrowDown', false);
    // de speer oprapen
    if (!spear && spearX != null){
      if (Math.abs(world - spearX) > 20){ toets(world > spearX ? 'ArrowLeft' : 'ArrowRight', true); return; }
      toets('ArrowLeft', false); toets('ArrowRight', false); tik('e'); wachtF = 30; return;
    }
    // de speerval: trilt hij, dan rollen (de rol is 0,6 s onkwetsbaar)
    const val = level.speervallen && level.speervallen[0];
    if (val && val.st === 'tril' && val.t > 0.6 && !rol && Math.abs(world - val.x) < 900){ tik('v'); wachtF = 30; return; }
    // gooien: op zo'n 480 px van het doel, F een tel vasthouden
    if (st && st.eis === 'doel' && spear && rolDoelen.length && m.fase === 'wacht'){
      const doel = rolDoelen[0], d = world - doel.x;
      if (d > 560){ toets('ArrowRight', false); toets('ArrowLeft', true); return; }
      if (d < 400){ toets('ArrowLeft', false); toets('ArrowRight', true); return; }
      toets('ArrowLeft', false); toets('ArrowRight', false);
      if (facing > 0){ tik('ArrowLeft'); return; }
      if (doel.heen && Math.abs(d - 480) > 40) return;          // het bewegende doel: wachten tot het op de goede plek is
      if (!keys['f']){ dispatchEvent(new KeyboardEvent('keydown', { key: 'f' })); keys['f'] = true; B.fT = 24; return; }
      return;
    }
    // de lage zwaai in de lucht: bukken, een paar beelden later F, en na de zwaai weer omhoog
    if (st && st.eis === 'zwaai' && m.fase === 'wacht' && Math.abs(world - mentorX()) < 220 && onGround){
      toets('ArrowLeft', false);
      if (!keys['ArrowDown']){ toets('ArrowDown', true); B.zw = 8; return; }
      if (B.zw > 0){ if (--B.zw === 0){ tik('f'); wachtF = 40; } return; }
      toets('ArrowDown', false); return;
    }
    // loopt hij tegen iets aan (de rots), dan springt hij
    B.vastF = keys['ArrowLeft'] && Math.abs(world - (B.vorigX == null ? 1e9 : B.vorigX)) < 0.5 ? (B.vastF || 0) + 1 : 0; B.vorigX = world;
    if (B.vastF > 20 && onGround){ dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowUp' })); B.springT = 12; B.vastF = 0; }
    if (B.springT > 0 && --B.springT === 0) dispatchEvent(new KeyboardEvent('keyup', { key: 'ArrowUp' }));
    // naar de gids, tot net achter hem; daar wachten
    const doel = mentorX() + 150;
    if (world > doel + 10) toets('ArrowLeft', true); else toets('ArrowLeft', false);
    if (m.fase === 'klaar' || (m.i === m.def.stations.length - 1 && m.fase === 'wacht')) toets('ArrowLeft', true);   // het slot: naar de fakkels
  };
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const fouten = [];
  page.on('pageerror', e => fouten.push('pagina: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|ERR_NAME|ERR_INTERNET/.test(m.text())) fouten.push('console: ' + m.text()); });   // geen internet in de test: fonts en Updates van buiten tellen niet
  page.on('response', r => { if (r.status() === 404) fouten.push('404: ' + r.url()); });
  await page.addInitScript(() => {
    let vt = 1000;
    window.requestAnimationFrame = cb => setTimeout(() => {
      vt += 1000 / 60; cb(vt);
      if (window.__ttStap){ try { window.__ttStap(); } catch (e){ console.error('tut2_test: ' + e.message); } }
    }, 0);
  });
  await page.goto(url);
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof TUT_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => { setLevel(1, TUT_LEVELS); runReset(); beginPlay('normal'); });
  await page.waitForTimeout(800);
  await page.evaluate(speler, { een: args.includes('--een'), debug: args.includes('--debug') });
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  let shot = 0;
  for (;;){
    await page.waitForTimeout(300);
    const s = await page.evaluate(() => ({ k: window.__tt.klaar, n: window.__tt.shot }));
    if (SHOTS && s.n > shot){
      shot = s.n;
      await page.waitForTimeout(900);
      await page.screenshot({ path: path.join(SHOTS, 'tut2_' + String(shot).padStart(2, '0') + '.png') });
    }
    if (s.k) break;
  }
  const B = await page.evaluate(() => window.__tt);
  for (const r of B.log) console.log(r.join('\t'));
  for (const f of fouten) console.log('FOUT ' + f);
  if (B.fout) console.log('FOUT: ' + B.fout);
  else if (!fouten.length) console.log('OK: uitgespeeld in ' + B.t.toFixed(1) + ' s');
  await browser.close(); srv.close();
  process.exit(B.fout || fouten.length ? 1 : 0);
})();
