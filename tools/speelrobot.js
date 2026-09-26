#!/usr/bin/env node
// De speelrobot: speelt een level in het echte spel, en meldt wat er gebeurt.
//
// levelcheck.py rekent een level na; de robot loopt het. Hij laadt het spel in Chromium, zet
// het level klaar en loopt naar links, op een vaste 60 beelden per seconde (virtuele tijd: los
// van hoe snel deze computer is, dus een sprong is hier even hoog als bij een speler). Hij
//
//   - springt als hij ergens tegenaan loopt,
//   - springt over een ravijn zonder gang eronder, en laat zich in een ingang vallen,
//   - laat de pijl los als hij dalend boven iets hangt waar hij op kan landen,
//   - blijft op een kei even staan en springt er aan de rand vanaf,
//   - pakt zijn speer op en steekt naar een doornbos of een vijand voor hem,
//   - drinkt een kalebas zodra hij er een heeft en niet vol zit.
//
// Hij meldt waar hij landt (en hoe hoog hij kwam), wat een val kost, waar hij vastloopt, en
// wat er in de console staat. Hij is geen speler: een eindbaas verslaat hij niet, en een sprong
// die precies getimed moet worden mist hij. Loopt hij vast waar levelcheck.py niets meldt, kijk
// dan wat daar staat: is het het level, dan hoort er een regel bij in levelcheck.py.
//
//   node tools/speelrobot.js "Test 4"              een level uit de HTML, op (een stuk van) de naam
//   node tools/speelrobot.js level.json            een level uit de bouwer
//   --taai            levens komen terug (en uit een ravijn wordt hij teruggezet), zo speelt hij door
//   --lopen           zonder sprint
//   --max 90          hoogstens zoveel seconden speeltijd
//   --shots map       schermafdrukken, elke --elke seconden (standaard 1,5)
//   --spoor           elke tiende seconde: tijd, x, hoogte, op de grond, levens
//   --vijanden        per vijand: op welke hoogte hij liep, en hoe hoog hij kwam
//   --breed 1280 --hoog 720 --fps 60
//
// Nodig: Node en Playwright (npm i -g playwright) met Chromium. De robot start zelf een
// webserver op de map van het spel.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('speelrobot: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const doel = args[0];
if (!doel || doel.startsWith('--')){ console.log(fs.readFileSync(__filename, 'utf8').split('\n').slice(1, 30).join('\n')); process.exit(0); }
const fps = Number(opt('--fps', 60)), maxS = Number(opt('--max', 90));
const breed = Number(opt('--breed', 1280)), hoog = Number(opt('--hoog', 720));
const shots = opt('--shots', null), elke = Number(opt('--elke', 1.5));

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

// Dit draait in de pagina, na elk beeld. Het gebruikt de globale namen van het spel.
function robot([lopen, taai]){
  const B = window.__robot = { spoor: [], ev: [], klaar: null, t0: null, beelden: 0, vijand: {} };
  let lastX = world, stuckT = 0, lastT = null, lastLives = lives, wasGround = true, top = 0;
  let vastX = null, vastT = 0, laatsteSp = -1;
  const schaal = () => (H * (Number(sizeEl.value) / 100)) / CHAR_H;
  keys['ArrowLeft'] = true; if (!lopen) keys['Shift'] = true;
  window.__robotStap = tt => {
    if (B.klaar) return;
    if (B.t0 === null){ B.t0 = tt; lastT = tt; }
    const dt = tt - lastT; lastT = tt; B.beelden++;
    const t = tt - B.t0, r2 = v => Math.round(v);
    if (won){ B.klaar = { uitkomst: 'gewonnen', t, x: r2(world), h: r2(ph) }; return; }
    if (dead && !taai){ B.klaar = { uitkomst: 'dood', t, x: r2(world), h: r2(ph) }; return; }
    if (lives !== lastLives){
      B.ev.push({ t: +t.toFixed(2), wat: 'levens ' + lastLives + ' naar ' + lives, x: r2(world), h: r2(ph) });
      if (taai && lives < lastLives){
        if (ph < -200 && !holteAt(world)){              // in een ravijn: terug naar vaste grond
          B.ev.push({ t: +t.toFixed(2), wat: 'in een ravijn, teruggezet', x: r2(world) });
          world = lastSolid; ph = Math.min(0, terrainH(world)); pvh = 0; onGround = true; fell = false; jump = null; coyote = 0;
        }
        lives = 3; dead = false; deadEl.classList.remove('on'); drawLives();
      }
      lastLives = lives;
    }
    if (!onGround) top = Math.max(top, ph);
    if (onGround && !wasGround) B.ev.push({ t: +t.toFixed(2), wat: 'land', x: r2(world), h: +ph.toFixed(1), top: +top.toFixed(1) });
    if (!onGround && wasGround) top = ph;
    wasGround = onGround;
    const sc = schaal(), hw = PLAYER_HALF_W * CHAR_H * sc, vl = grondVloer(world, ph);
    // dalend boven iets waar hij op kan landen: pijl los
    let loslaten = false;
    if (!onGround && pvh < 0)
      for (const p of platsNear(sc))
        if (world + hw > p.left && world - hw < p.right && ph > p.topH && p.topH > (vl === null ? -1e9 : vl) + 20) loslaten = true;
    keys['ArrowLeft'] = !loslaten;
    // een kalebas bij zich en niet vol: drinken
    if (hppotionCarry > 0 && lives < 3 && !dead) drinkHppotion();
    // de speer oppakken, en steken naar wat voor hem staat
    if (!spearFound && spearNear()) toggleSpear();
    const voor = [];
    for (const b of thickets) if (b.stage < THICKET_HITS) voor.push([b.x, b.base]);
    for (const l of [snakes, scorps, zwaarden, hyenas, panthers, fosforSlangen]) for (const e of l) if (!e.dead) voor.push([e.x, e.base || 0]);
    const iets = voor.some(([x, b]) => x < world + 40 && x > world - 200 && Math.abs(b - ph) < 60);
    if (spear && iets && onGround && !jump) startAttack();
    // de vijanden: op welke hoogte liepen ze, en hoe hoog kwamen ze
    for (const [naam, l] of [['slang', snakes], ['schorpioen', scorps], ['zwaard', zwaarden], ['hyena', hyenas], ['panter', panthers], ['fosfor', fosforSlangen]]){
      l.forEach((e, i) => {
        const k = naam + ' ' + (i + 1), v = B.vijand[k] || (B.vijand[k] = { laag: 1e9, hoog: -1e9, top: -1e9, van: r2(e.x), tot: r2(e.x) });
        const b = e.base || 0;
        v.laag = Math.min(v.laag, b); v.hoog = Math.max(v.hoog, b); v.top = Math.max(v.top, b + (e.lift || 0)); v.tot = r2(e.x);
      });
    }
    // een ravijn voor hem zonder gang eronder: aan de rand springen
    const g = inGap(world - 60);
    if (onGround && ph >= -1 && g && !holteAt(g.x) && !inGap(world)) startJump();
    // op een kei: eerst neerkomen, dan aan de rand eraf springen
    if (onGround){
      const ps = platsNear(sc).filter(p => !p.terrace);
      const op = ps.some(p => world + hw > p.left && world - hw < p.right && Math.abs(p.topH - ph) < 2);
      const verder = ps.some(p => world - 12 > p.left && world - 12 < p.right + 2 * hw && p.topH >= ph - 2);   // nog kei voor hem
      if (op && jump && jump.phase === 'land') keys['ArrowLeft'] = false;
      else if (op && !verder && vl !== null && ph > vl + 1) startJump();
    }
    // vast tegen iets: springen (behalve voor een doornbos, dat steekt hij weg)
    if (Math.abs(world - lastX) < 0.3 && onGround) stuckT += dt; else stuckT = 0;
    lastX = world;
    if (stuckT > 0.1 && onGround && !(iets && spear)){ startJump(); stuckT = 0; }
    // helemaal vast: acht seconden niet meer dan 30 px verder
    if (vastX === null || world < vastX - 30){ vastX = world; vastT = t; }
    if (t - vastT > 8){ B.klaar = { uitkomst: 'vast', t, x: r2(world), h: r2(ph), grond: onGround }; return; }
    if (t - laatsteSp >= 0.1){ laatsteSp = t; B.spoor.push([+t.toFixed(1), r2(world), r2(ph), onGround ? 1 : 0, lives]); }
  };
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await start();
  const page = await browser.newPage({ viewport: { width: breed, height: hoog } });
  const console_ = new Set();
  page.on('pageerror', e => console_.add('fout: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') console_.add('console: ' + m.text()); });
  page.on('response', r => { if (r.status() >= 400) console_.add(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+\//, '')); });
  // virtuele tijd: elk beeld is precies 1/fps seconde, hoe lang het tekenen hier ook duurt
  await page.addInitScript(fps => {
    let vt = 1000;
    window.__vt = () => vt;
    window.requestAnimationFrame = cb => setTimeout(() => {
      vt += 1000 / fps;
      cb(vt);
      if (window.__robotStap){ try { window.__robotStap(vt / 1000); } catch (e){ console.error('robot: ' + e.message); } }
    }, 0);
  }, fps);
  await page.goto(url);
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof TEST_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);                 // de plaatjes
  const def = doel.endsWith('.json') ? JSON.parse(fs.readFileSync(doel, 'utf8')) : null;
  const naam = await page.evaluate(([doel, def]) => {
    let lijst = null, i = 0;
    if (def) lijst = [def];
    else for (const l of [LICHT_LEVELS, BRON_LEVELS, RENEW_LEVELS, WINTER_LEVELS, DARK_LEVELS, TEST_LEVELS])
      l.forEach((d, j) => { if (!lijst && d.name.toLowerCase().includes(doel.toLowerCase())){ lijst = l; i = j; } });
    if (!lijst) return null;
    setLevel(i, lijst);
    beginPlay('medium');
    return level.name;
  }, [doel, def]);
  if (!naam){ console.log('geen level gevonden: ' + doel); await browser.close(); srv.close(); process.exit(2); }
  console.log(naam + ' (' + fps + ' beelden per seconde, ' + breed + ' bij ' + hoog + ')');
  await page.evaluate(robot, [args.includes('--lopen'), args.includes('--taai')]);
  const klok = Date.now();
  let n = 0, volgende = 0;
  for (;;){
    await page.waitForTimeout(250);
    const st = await page.evaluate(() => ({ k: window.__robot.klaar, t: window.__robot.t0 === null ? 0 : window.__vt() / 1000 - window.__robot.t0 }));
    if (shots && st.t >= volgende){
      fs.mkdirSync(shots, { recursive: true });
      await page.screenshot({ path: path.join(shots, 's' + String(n++).padStart(3, '0') + '.png') });
      volgende = st.t + elke;
    }
    if (st.k || st.t > maxS || (Date.now() - klok) / 1000 > maxS * 20) break;
  }
  const B = await page.evaluate(() => ({ r: window.__robot, x: Math.round(world), h: Math.round(ph) }));
  const k = B.r.klaar || { uitkomst: 'tijd op', x: B.x, h: B.h };
  console.log('uitkomst: ' + k.uitkomst + ' op x=' + k.x + ', hoogte ' + k.h + (k.t ? ', na ' + k.t.toFixed(1) + ' s' : ''));
  for (const e of B.r.ev) console.log('  ' + e.t.toFixed(2).padStart(6) + '  ' + e.wat.padEnd(26) + ' x=' + e.x + (e.h !== undefined ? ' h=' + e.h : '') + (e.top !== undefined ? ' (top ' + e.top + ')' : ''));
  if (args.includes('--vijanden'))
    for (const [k2, v] of Object.entries(B.r.vijand))
      console.log('  ' + k2.padEnd(14) + ' van x=' + v.van + ' tot x=' + v.tot + ', liep op ' + (v.laag === v.hoog ? v.laag : v.laag + ' tot ' + v.hoog) + ', kwam tot ' + v.top);
  if (args.includes('--spoor')) for (const r of B.r.spoor) console.log('  spoor ' + r.join(' '));
  // mp3 speelt Chromium zonder de codecs niet af: de terugvalpaden van de geluiden geven hier
  // 404's die in een gewone browser niet voorkomen
  for (const f of console_) if (!/\.mp3|Failed to load resource|fonts\.g/.test(f)) console.log('  ' + f);
  await browser.close();
  srv.close();
})();
