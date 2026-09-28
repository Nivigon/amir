#!/usr/bin/env node
// De vijandtest: zet een vijand in een klein proeflevel en kijkt wat zijn AI doet.
//
// De speelrobot loopt een heel level uit; deze test zet per scenario een vijand (of een paar) neer,
// met een kei of een ravijn als het scenario daarom vraagt, en laat Amir een vaste manier van spelen
// volgen: stilstaan, gebukt zitten, weglopen, op een kei staan, of vechten als een redelijke speler
// (hij ontwijkt wat te zien is en steekt als het kan). Het draait in het echte spel in Chromium, op
// vaste 60 beelden per seconde, en meldt per scenario:
//
//   - wie Amir raakte en wanneer (uit de regel in de code waar de klap vandaan kwam),
//   - wie Amir versloeg, en na hoeveel tijd,
//   - per vijand: in welke toestanden hij hoeveel tijd stond, en hoe vaak hij wisselde,
//   - REGEL 7: een vijand die over een kei of ravijn kwam,
//   - HANGT: een vijand die lang in dezelfde toestand stond zonder iets te doen terwijl Amir bereikbaar was,
//   - WEG: een vijand die het scherm uit ging en niet terugkwam,
//   - wat de scenario zelf als eis stelt (verwacht), met OK of AFWIJKING.
//
//   node tools/vijandtest.js                  alle scenario's
//   node tools/vijandtest.js slang            alleen de scenario's waarvan de naam dit bevat
//   node tools/vijandtest.js --lijst          alleen de namen
//   node tools/vijandtest.js slang --spoor    ook per vijand elke halve seconde x en toestand
//   node tools/vijandtest.js --keer 3         elk scenario drie keer (de AI heeft toeval)
//   --json uit.json   de ruwe uitkomsten wegschrijven;  --tegelijk 3  zoveel scenario's naast elkaar
//   --breed 1280 --hoog 720 --fps 60
//
// Nodig: Node en Playwright, net als de speelrobot.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('vijandtest: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const HTML = path.join(ROOT, 'amir-king-of-africa.html');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const fps = Number(opt('--fps', 60));
const breed = Number(opt('--breed', 1280)), hoog = Number(opt('--hoog', 720));
const keer = Number(opt('--keer', 1));
const filter = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--') && ['--keer', '--json', '--breed', '--hoog', '--fps', '--tegelijk'].includes(args[i - 1])));

// ---- de scenario's ----------------------------------------------------------------------------
// Amir begint op x 0 en kijkt naar links; de vijanden staan links van hem (negatieve x). Een
// scenario is een klein level plus een gedrag voor Amir, en wat we ervan verwachten.
//   gedrag: stil, gebukt, weg (rent naar rechts), naar (loopt naar links, steekt niet), vechter,
//           springer (springt steeds), heen (loopt heen en weer, steekt niet)
//   start:  waar Amir begint (standaard 0), speer: in de hand (standaard ja)
//   verwacht: { maxRaak, minRaak, doden, geenRegel7, geenHangen }
// een klif aan het eind (links), fakkels ervoor; zonder vijanden in het level komt de vrije modus met zijn
// eigen slangen, dus dan staat er een heel ver weg (net als in Test 15)
const vlak = extra => Object.assign({ cliffs: [{ x: -9500 }], ends: [{ x: -9000 }] }, extra,
                                    { spawns: (extra.spawns && extra.spawns.length) ? extra.spawns : [{ x: -60000, k: 'groen' }] });
const SCENARIOS = [
  // --- de groene slang ---
  { naam: 'slang: stilstaan', level: vlak({ spawns: [{ x: -900, k: 'groen' }] }), gedrag: 'stil', duur: 12,
    verwacht: { minRaak: 2 } },
  { naam: 'slang: vechter', level: vlak({ spawns: [{ x: -900, k: 'groen' }] }), gedrag: 'vechter', duur: 10,
    verwacht: { doden: 1, maxRaak: 0 } },
  { naam: 'slang: op een kei', level: vlak({ rocks: [{ x: -200, s: 1 }], spawns: [{ x: -900, k: 'groen' }] }),
    start: -200, gedrag: 'stil', duur: 12, verwacht: { geenRegel7: true } },
  { naam: 'slang: achter een ravijn', level: vlak({ gaps: [{ x: -300, w: 260 }], spawns: [{ x: -1000, k: 'groen' }] }),
    gedrag: 'stil', duur: 14, verwacht: { maxRaak: 0, geenRegel7: true } },
  { naam: 'slang: drie tegelijk', level: vlak({ spawns: [{ x: -900, k: 'groen' }, { x: -1000, k: 'groen' }, { x: -1100, k: 'groen' }] }),
    gedrag: 'stil', duur: 10, verwacht: {} },
  { naam: 'slang: van twee kanten', level: vlak({ spawns: [{ x: -900, k: 'groen' }, { x: 900, k: 'groen' }] }),
    gedrag: 'vechter', duur: 14, verwacht: { doden: 2 } },
  { naam: 'slang: overheen springen', level: vlak({ spawns: [{ x: -900, k: 'groen' }] }), gedrag: 'springer', duur: 12,
    verwacht: {} },
  { naam: 'slang: weglopen', level: vlak({ spawns: [{ x: -2900, k: 'groen' }] }), start: -2000, gedrag: 'weg', duur: 16,
    verwacht: { maxRaak: 0 } },
  // --- de zwarte slang ---
  { naam: 'zwarte slang: stilstaan', level: vlak({ spawns: [{ x: -1200, k: 'zwart' }] }), gedrag: 'stil', duur: 14,
    verwacht: { minRaak: 1 } },
  { naam: 'zwarte slang: gebukt', level: vlak({ spawns: [{ x: -1200, k: 'zwart' }] }), gedrag: 'gebukt', duur: 14,
    verwacht: {} },
  { naam: 'zwarte slang: vechter', level: vlak({ spawns: [{ x: -1200, k: 'zwart' }] }), gedrag: 'vechter', duur: 16,
    verwacht: { doden: 1 } },
  { naam: 'zwarte slang: achter een kei', level: vlak({ rocks: [{ x: -500, s: 1 }], spawns: [{ x: -1300, k: 'zwart' }] }),
    gedrag: 'stil', duur: 14, verwacht: { geenRegel7: true } },
  { naam: 'zwarte slang: achter een ravijn', level: vlak({ gaps: [{ x: -500, w: 260 }], spawns: [{ x: -1300, k: 'zwart' }] }),
    gedrag: 'stil', duur: 14, verwacht: { geenRegel7: true } },
  // --- de schorpioen ---
  { naam: 'schorpioen: stilstaan', level: vlak({ spawns: [{ x: -900, k: 'scorp' }] }), gedrag: 'stil', duur: 14,
    verwacht: { minRaak: 1 } },
  { naam: 'schorpioen: vechter', level: vlak({ spawns: [{ x: -900, k: 'scorp' }] }), gedrag: 'vechter', duur: 14,
    verwacht: { doden: 1, maxRaak: 1 } },
  { naam: 'schorpioen: op een kei', level: vlak({ rocks: [{ x: -200, s: 1 }], spawns: [{ x: -900, k: 'scorp' }] }),
    start: -200, gedrag: 'stil', duur: 14, verwacht: { geenRegel7: true } },
  { naam: 'schorpioen: achter een ravijn', level: vlak({ gaps: [{ x: -300, w: 260 }], spawns: [{ x: -900, k: 'scorp' }] }),
    gedrag: 'stil', duur: 12, verwacht: { maxRaak: 0, geenRegel7: true } },
  { naam: 'schorpioen: springer', level: vlak({ spawns: [{ x: -900, k: 'scorp' }] }), gedrag: 'springer', duur: 14,
    verwacht: {} },
  { naam: 'schorpioen: aanlopen', level: vlak({ spawns: [{ x: -1800, k: 'scorp' }] }), gedrag: 'naar', duur: 8, verwacht: {} },
  { naam: 'schorpioen: aanlopen, telefoon', level: vlak({ spawns: [{ x: -1800, k: 'scorp' }] }), gedrag: 'naar', duur: 8, scherm: [852, 393], verwacht: {} },
  // --- de zwaardvechter ---
  { naam: 'zwaard: stilstaan', level: vlak({ spawns: [{ x: -1300, k: 'zwaard' }] }), tot: -700, gedrag: 'stil', duur: 12,
    verwacht: { minRaak: 2 } },
  { naam: 'zwaard: vechter', level: vlak({ spawns: [{ x: -1300, k: 'zwaard' }] }), tot: -700, gedrag: 'vechter', duur: 14,
    verwacht: { doden: 1, maxRaak: 1 } },
  { naam: 'zwaard: op een kei', level: vlak({ rocks: [{ x: -700, s: 1 }], spawns: [{ x: -1300, k: 'zwaard' }] }), direct: true,
    start: -700, gedrag: 'stil', duur: 12, verwacht: { maxRaak: 0, geenRegel7: true } },
  { naam: 'zwaard: achter een ravijn', level: vlak({ gaps: [{ x: -1150, w: 260 }], spawns: [{ x: -1500, k: 'zwaard' }] }),
    tot: -850, gedrag: 'stil', duur: 12, verwacht: { maxRaak: 0, geenRegel7: true } },
  { naam: 'zwaard: twee tegelijk', level: vlak({ spawns: [{ x: -1300, k: 'zwaard' }, { x: -1500, k: 'zwaard', c: 'blauw' }] }),
    tot: -700, gedrag: 'vechter', duur: 20, verwacht: { doden: 2 } },
  { naam: 'zwaard: weglopen', level: vlak({ spawns: [{ x: -3300, k: 'zwaard' }] }), start: -2000, tot: -2700, gedrag: 'weg', duur: 12,
    verwacht: {} },
  { naam: 'zwaard: aanlopen, telefoon', level: vlak({ spawns: [{ x: -1800, k: 'zwaard' }] }), gedrag: 'naar', duur: 8, scherm: [852, 393], verwacht: {} },
  // --- de hyena's ---
  // een hyena komt na zijn storm terug (HY_RONDES): stilstaan kost dus meer dan twee beten
  { naam: 'hyena: stilstaan', level: vlak({ spawns: [{ x: -300, k: 'hyenas', n: 2 }] }), gedrag: 'stil', duur: 30,
    verwacht: { minRaak: 3 } },
  { naam: 'hyena: vechter', level: vlak({ spawns: [{ x: -300, k: 'hyenas', n: 2 }] }), gedrag: 'vechter', duur: 16,
    verwacht: { doden: 2 } },
  { naam: 'hyena: springer', level: vlak({ spawns: [{ x: -300, k: 'hyenas', n: 2 }] }), gedrag: 'springer', duur: 30,
    verwacht: {} },
  { naam: 'hyena: op een kei', level: vlak({ rocks: [{ x: -200, s: 1 }], spawns: [{ x: -300, k: 'hyenas', n: 2 }] }),
    start: -200, gedrag: 'stil', duur: 16, verwacht: { geenRegel7: true } },
  { naam: 'hyena: tussen twee keien', level: vlak({ rocks: [{ x: -600, s: 1 }, { x: 250, s: 1 }], spawns: [{ x: -300, k: 'hyenas', n: 2 }] }),
    start: -150, gedrag: 'stil', duur: 16, verwacht: { maxRaak: 0, geenRegel7: true } },
  // --- de panter (eindbaas) ---
  { naam: 'panter: stilstaan', level: vlak({ spawns: [{ x: -100, k: 'panter' }], arena: { c: -300 } }), start: -150, gedrag: 'stil', duur: 16,
    verwacht: { minRaak: 2 } },
  { naam: 'panter: vechter', level: vlak({ spawns: [{ x: -100, k: 'panter' }], arena: { c: -300 } }), start: -150, gedrag: 'vechter', duur: 45,
    verwacht: { doden: 1 } },
  { naam: 'panter: gebukt', level: vlak({ spawns: [{ x: -100, k: 'panter' }], arena: { c: -300 } }), start: -150, gedrag: 'gebukt', duur: 16,
    verwacht: {} },
  // op de kei raakt zijn klauw je niet: dan blijft hij aan de voet liggen loeren (prowl, stil)
  { naam: 'panter: op een kei', level: vlak({ rocks: [{ x: -300, s: 1 }], spawns: [{ x: -100, k: 'panter' }], arena: { c: -300 } }),
    start: -300, gedrag: 'stil', duur: 16, verwacht: { geenRegel7: true, maxRaak: 0, hangtMag: ['prowl'] } },
  // --- de fosforslangen ---
  { naam: 'fosfor: stilstaan', level: vlak({ spawns: [{ x: -1300, k: 'fosfor' }] }), tot: -850, gedrag: 'stil', duur: 14,
    verwacht: { minRaak: 1 } },
  { naam: 'fosfor: gebukt (het trucje)', level: vlak({ spawns: [{ x: -1300, k: 'fosfor' }] }), tot: -850, gedrag: 'fosfortruc', duur: 16,
    verwacht: {} },
  { naam: 'fosfor: vechter', level: vlak({ spawns: [{ x: -1300, k: 'fosfor' }] }), tot: -850, gedrag: 'vechter', duur: 20,
    verwacht: {} },
  { naam: 'fosfor: achter een ravijn', level: vlak({ gaps: [{ x: -1000, w: 200 }], spawns: [{ x: -1250, k: 'fosfor' }] }), direct: true,
    tot: -840, gedrag: 'stil', duur: 14, verwacht: { maxRaak: 0, geenRegel7: true, hangtMag: ['zie', 'wacht'] } },   // ze blijven staren
  // --- de baviaan ---
  // hij hangt achter Amir aan de rotswand, net als in Test 15, en springt neer zodra Amir van zijn plek is
  { naam: 'baviaan: vlak', level: vlak({ baviaan: { x: 540, y: 1.45, s: 1.4, f: 0 } }),
    start: -1200, gedrag: 'stil', duur: 20, verwacht: { minRaak: 1 } },
  { naam: 'baviaan: Amir op een kei', level: vlak({ rocks: [{ x: -1200, s: 1 }], baviaan: { x: 540, y: 1.45, s: 1.4, f: 0 } }),
    start: -1200, gedrag: 'stil', duur: 20, verwacht: {} },
  { naam: 'baviaan: achter een ravijn (geen kooi)', level: vlak({ gaps: [{ x: -700, w: 260 }], baviaan: { x: 540, y: 1.45, s: 1.4, f: 0 } }),
    start: -1200, gedrag: 'stil', duur: 20, verwacht: { maxRaak: 0, geenRegel7: true } },
  { naam: 'baviaan: weglopen', level: vlak({ baviaan: { x: 540, y: 1.45, s: 1.4, f: 0 } }),
    start: -300, gedrag: 'naar', duur: 20, verwacht: {} },
];

// ---- de webserver en de browser, net als de speelrobot ----------------------------------------
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

// ---- waar komt een klap vandaan: de regels in de HTML waar hurtPlayer wordt aangeroepen ---------
// De stapel van een klap noemt de regel in de HTML; de dichtstbijzijnde kop erboven zegt wie het was.
const BRON = fs.readFileSync(HTML, 'utf8').split('\n');
function klapBron(regel){
  const koppen = [[/---- the snakes/, 'slang'], [/---- de schorpioenen ---/, 'schorpioen'], [/---- de panters ---/, 'panter'],
                  [/---- de hyena's ---/, 'hyena'], [/---- de zwaardvechters ---/, 'zwaard'], [/---- de speerval: bukken/, 'speerval'],
                  [/^function updateVenom/, 'gif (zwarte slang)'], [/^function bavGevecht/, 'baviaan'], [/^function fosforBijt/, 'fosfor'],
                  [/^function [A-Za-z]/, null]];
  for (let i = regel - 1; i >= 0 && i > regel - 400; i--){
    for (const [re, naam] of koppen) if (re.test(BRON[i])){
      if (naam) return naam;
      const m = BRON[i].match(/^function ([A-Za-z0-9_]+)/);
      return m ? m[1] : '?';
    }
  }
  return '?';
}

// ---- dit draait in de pagina, na elk beeld ------------------------------------------------------
function inPagina([sc, taai]){
  const T = window.__vt_ = { klaar: false, klappen: [], doden: [], spoor: [], toestand: {}, regel7: [], hangt: {}, ev: [],
                             t0: null, beelden: 0 };
  const lijsten = () => [['slang', snakes], ['schorpioen', scorps], ['zwaard', zwaarden], ['hyena', hyenas],
                          ['panter', panthers], ['fosfor', fosforSlangen]];
  const ids = new WeakMap(); let volg = 0;
  const idVan = (naam, e) => { if (!ids.has(e)) ids.set(e, naam + ' ' + (++volg)); return ids.get(e); };
  // klappen tellen: hurtPlayer inpakken, met de regel waar hij vandaan kwam
  const regelUit = st => {
    const r = (st || '').split('\n').slice(2).map(l => l.match(/amir-king-of-africa\.html:(\d+):\d+/)).find(Boolean);
    return r ? Number(r[1]) : 0;
  };
  const oudHurt = hurtPlayer;
  hurtPlayer = function(fromLeft){
    const voor = lives, inv = invuln;
    oudHurt(fromLeft);
    if (inv <= 0 && (lives !== voor || invuln > 0 || taai))
      T.klappen.push({ t: T.t, regel: regelUit(new Error().stack), x: Math.round(world), h: Math.round(ph), gebukt: +duckT.toFixed(2) });
  };
  const oudBijt = fosforBijt;
  fosforBijt = function(s){ T.klappen.push({ t: T.t, regel: -1, bron: 'fosfor', x: Math.round(world), h: Math.round(ph) }); oudBijt(s); };
  if (sc.direct) spawnPoint = x => x;               // de vijand precies op zijn plek, ook in beeld
  const oudDood = vijandDood;
  vijandDood = function(baas){ T.doden.push({ t: T.t, baas: !!baas }); oudDood(baas); };
  // Amir in een vaste stand: de speer in de hand, en in taai-modus komen zijn levens terug
  if (sc.speer !== false){ spearFound = true; spear = true; spearX = null; setSpearLabel(); }
  world = sc.start || 0; lastSolid = world; ph = Math.max(0, terrainH(world)); facing = -1;
  // staat hij op een kei, dan bovenop (terrainH kent geen keien)
  for (const p of platsNear(nowScale(), Infinity)) if (!p.terrace && world > p.left && world < p.right) ph = Math.max(ph, p.topH);
  pvh = 0; onGround = true; jump = null;
  const keien = (level.rocks || []).map(r => measurePlat({ x: r.x, scale: r.s || r.scale || 1 }, nowScale()));
  const kant = new WeakMap();
  const laatste = new WeakMap();                  // per vijand: sinds wanneer in deze toestand, en waar
  let heenDir = -1, heenT = 0, sprongT = 0;
  const reik = () => 293 * nowScale() + 40 * nowScale();   // de verste speerpunt plus de punt zelf, in wereld-px
  const vijandenNu = () => {
    const uit = [];
    for (const [naam, l] of lijsten()) for (const e of l){
      const dood = ['dying', 'dood', 'gone', 'weg'].includes(e.state);
      if (!dood && !(e.wacht > 0) && e.state !== 'lurk') uit.push({ naam, e, x: e.x, st: e.state || '' });
    }
    const b = level.baviaan, r = b && bavRust.get(b);
    if (b && r && r.fase && r.fase !== 'dood') uit.push({ naam: 'baviaan', e: b, x: b.x + (r.wx || 0), st: r.fase });
    return uit;
  };
  // een redelijke speler: ontwijkt wat te zien is, en steekt als het kan
  function vechter(dt){
    keys['ArrowLeft'] = false; keys['ArrowRight'] = false; keys['ArrowDown'] = false; keys['Shift'] = false;
    const vs = vijandenNu();
    if (!vs.length) return;
    vs.sort((a, b) => Math.abs(a.x - world) - Math.abs(b.x - world));
    const sc0 = nowScale(), R = reik();
    // eerst: ontwijken wat eraan komt
    for (const v of vs){
      const e = v.e, dx = v.x - world, gap = Math.abs(dx), naar = e.dir !== undefined ? (Math.sign(-dx) === Math.sign(e.dir)) : true;
      if (v.naam === 'hyena' && e.state === 'storm' && naar && gap < 330){ startJump(); return; }
      if (v.naam === 'hyena' && e.state === 'telegraaf' && gap < 420){ startJump(); return; }
      if (v.naam === 'schorpioen' && e.state === 'charge' && naar && gap < 360){ startJump(); return; }
      if (v.naam === 'panter'){
        if (e.state === 'tackle' && gap < 400){ startJump(); return; }
        if (e.state === 'claw' && e.frame < 4){ startJump(); return; }
        if ((e.state === 'leap' || (e.state === 'wind' && e.atk === 'leap')) && gap < 700){ keys['ArrowDown'] = true; return; }
        if (e.state === 'wind' && e.atk === 'dive' || e.state === 'dive'){ keys[dx < 0 ? 'ArrowRight' : 'ArrowLeft'] = true; keys['Shift'] = true; return; }
      }
      if (v.naam === 'zwaard' && e.state === 'slag' && e.frame < ZW.raak[0] && gap > R * 0.95 && gap < zwReik() + 60){
        keys[dx < 0 ? 'ArrowRight' : 'ArrowLeft'] = true; return;   // buiten zijn bereik stappen
      }
      if (v.naam === 'fosfor' && (e.state === 'aanval' || e.state === 'dreig') && atkFrame < 0 && gap > R){ keys['ArrowDown'] = true; return; }
    }
    // gif in de lucht dat op hem af komt: bukken
    for (const g of venom) if (Math.abs(g.x - world) < 260 && Math.sign(world - g.x) === Math.sign(g.vx)){ keys['ArrowDown'] = true; return; }
    const v = vs[0], dx = v.x - world, gap = Math.abs(dx);
    facing = dx < 0 ? -1 : 1;
    const raakbaar = v.naam !== 'panter' || v.st === 'land' || v.st === 'rest';
    // de zwaardvechter heeft zijn midden voor zijn anker, de rest ongeveer op x
    const bereik = R + (v.naam === 'zwaard' ? ZW_LIJF.half * zwScale() : v.naam === 'hyena' ? HY.bodyW * hyScale() * 0.3 : 40 * sc0);
    if (gap < bereik && raakbaar){ if (onGround && !jump) startAttack(); return; }
    if (v.naam === 'panter' && !raakbaar){
      // op afstand blijven tot hij neerkomt: niet in zijn klauw lopen
      if (gap < CLAW_RANGE * CHAR_H * sc0 + 40) keys[dx < 0 ? 'ArrowRight' : 'ArrowLeft'] = true;
      return;
    }
    if (v.naam === 'zwaard' && v.st === 'slag') return;           // wachten tot zijn haal voorbij is
    if (v.naam === 'fosfor' && v.st !== 'steen' && v.st !== 'wacht' && v.st !== 'terug') return;   // laat ze komen
    if (v.naam === 'baviaan') return;
    if (gap > bereik * 0.8) keys[dx < 0 ? 'ArrowLeft' : 'ArrowRight'] = true;
  }
  window.__vtStap = tt => {
    if (T.klaar) return;
    if (T.t0 === null) T.t0 = tt;
    const t = T.t = tt - T.t0; T.beelden++;
    const dt = 1 / 60;
    if (taai && lives < 3){ lives = 3; drawLives(); dead = false; deadEl.classList.remove('on'); }
    // het gedrag
    // tot: eerst naar links lopen tot hier, dan pas het gedrag (het spel zet een vijand altijd buiten beeld neer)
    if (sc.tot !== undefined && !T.aangekomen){
      if (world > sc.tot) keys['ArrowLeft'] = true;
      else { keys['ArrowLeft'] = false; T.aangekomen = true; }
    }
    const g = (sc.tot !== undefined && !T.aangekomen) ? 'lopen' : sc.gedrag;
    if (g === 'stil'){ keys['ArrowLeft'] = keys['ArrowRight'] = keys['ArrowDown'] = false; }
    else if (g === 'gebukt'){ keys['ArrowDown'] = true; }
    else if (g === 'weg'){ keys['ArrowRight'] = true; keys['Shift'] = true; }
    else if (g === 'naar'){ keys['ArrowLeft'] = true; }
    else if (g === 'springer'){ sprongT -= dt; if (onGround && !jump && sprongT <= 0){ startJump(); sprongT = 0.9; } }
    else if (g === 'heen'){ heenT += dt; if (heenT > 1.2){ heenT = 0; heenDir = -heenDir; } keys['ArrowLeft'] = heenDir < 0; keys['ArrowRight'] = heenDir > 0; }
    else if (g === 'fosfortruc'){
      // bukken zodra ze vertrekken, en steken naar een versteende die binnen bereik is
      const gr = fosforGroepen[0];
      const steen = fosforSlangen.find(s => s.state === 'steen' && Math.abs(s.x - world) < reik() + 40);
      if (steen && steen.t > 0.3){ keys['ArrowDown'] = false; if (duckT <= 0){ facing = steen.x < world ? -1 : 1; startAttack(); } }
      else keys['ArrowDown'] = !!(gr && gr.fase === 'aanval');
    }
    else if (g === 'vechter') vechter(dt);
    // wat de vijanden doen
    for (const v of vijandenNu()){
      const e = v.e, id = idVan(v.naam, e), st = v.st;
      const ts = T.toestand[id] || (T.toestand[id] = { tijd: {}, wissel: 0, van: Math.round(v.x), laatst: '', min: 1e9, max: -1e9 });
      ts.tijd[st] = (ts.tijd[st] || 0) + dt;
      if (ts.laatst !== st){ ts.wissel++; ts.laatst = st; }
      // wanneer kwam hij in beeld, en wat deed hij toen al (een aanloop moet je kunnen zien)
      if (ts.inBeeld === undefined && Math.abs(v.x - world) < W / 2 / viewZoom()) ts.inBeeld = [+t.toFixed(2), st];
      if (ts.eerst === undefined && ['stance', 'charge', 'wind', 'claw', 'telegraaf', 'storm', 'slag', 'bite', 'aanval', 'dreig', 'hap', 'leap', 'tackle'].includes(st))
        ts.eerst = [+t.toFixed(2), st, Math.round(Math.abs(v.x - world))];
      ts.min = Math.min(ts.min, v.x); ts.max = Math.max(ts.max, v.x); ts.tot = Math.round(v.x);
      if (T.beelden % 30 === 0) T.spoor.push([+t.toFixed(1), id, Math.round(v.x), st, Math.round(e.base || 0)]);
      // hangen: lang in dezelfde toestand, niet vooruit, en Amir in zijn buurt en op zijn hoogte
      if (!laatste.has(e)) laatste.set(e, { st, t, x: v.x });
      const l = laatste.get(e);
      if (l.st !== st || Math.abs(v.x - l.x) > 40){ laatste.set(e, { st, t, x: v.x }); }
      else if (t - l.t > 6 && Math.abs(v.x - world) < 700 && !['walk', 'idle', 'rond', 'patrouille', 'wacht', 'dreigen', 'rust', 'rest'].includes(st)){
        const k = id + ' ' + st;
        if (!T.hangt[k]) T.hangt[k] = { t: +t.toFixed(1), x: Math.round(v.x), amir: Math.round(world) };
      }
      // regel 7
      if (e.over || v.naam === 'baviaan') continue;
      const b = e.base || 0;
      const k7 = kant.get(e) || new Map(); kant.set(e, k7);
      const obst = [];
      for (const gp of gapList()) if (gatOp(gp.x, b)) obst.push(['ravijn op ' + Math.round(gp.x), gp.x - gp.w / 2, gp.x + gp.w / 2]);
      for (const p of keien) if (Math.abs((p.base || 0) - b) < 2) obst.push(['kei op ' + Math.round(p.x), p.left, p.right]);
      for (const [wat, lo, hi] of obst){
        const z = v.x < lo ? -1 : v.x > hi ? 1 : 0;
        if (!z) continue;
        const oud = k7.get(wat);
        if (oud && oud !== z) T.regel7.push({ t: +t.toFixed(2), wie: id, wat, x: Math.round(v.x) });
        k7.set(wat, z);
      }
    }
    // de baviaan: regel 7 voor een ravijn (over een kei springen mag hij)
    const b = level.baviaan, r = b && bavRust.get(b);
    if (b && r && r.fase && r.fase !== 'dood'){
      const bx = b.x + (r.wx || 0);
      for (const gp of gapList()){
        const z = bx < gp.x - gp.w / 2 ? -1 : bx > gp.x + gp.w / 2 ? 1 : 0;
        const k = 'bav ' + gp.x;
        if (z && T[k] && T[k] !== z && !bavKooi(b)) T.regel7.push({ t: +t.toFixed(2), wie: 'baviaan', wat: 'ravijn op ' + Math.round(gp.x), x: Math.round(bx) });
        if (z) T[k] = z;
        if (!z && r.fase === 'run') T.ev.push({ t: +t.toFixed(2), wat: 'baviaan rent boven het ravijn op ' + Math.round(gp.x), x: Math.round(bx) });
      }
    }
    if (t >= sc.duur) T.klaar = true;
  };
}

(async () => {
  const lijst = SCENARIOS.filter(s => !filter || s.naam.toLowerCase().includes(filter.toLowerCase()));
  if (args.includes('--lijst')){ for (const s of lijst) console.log(s.naam); return; }
  if (!lijst.length){ console.log('geen scenario gevonden: ' + filter); process.exit(2); }
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await start();
  let fouten = 0;
  const taken = [];
  for (const sc of lijst) for (let n = 0; n < keer; n++) taken.push([sc, n]);
  const uitkomst = new Array(taken.length);
  // een scenario draaien; de uitkomst komt in volgorde op het scherm, ook al lopen er een paar tegelijk
  async function draai([sc, n]){
    const page = await browser.newPage({ viewport: { width: sc.scherm ? sc.scherm[0] : breed, height: sc.scherm ? sc.scherm[1] : hoog } });
    const cons = new Set();
    page.on('pageerror', e => cons.add('fout: ' + e.message));
    page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) cons.add('console: ' + m.text()); });
    await page.addInitScript(fps => {
      let vt = 1000;
      window.__vt = () => vt;
      window.requestAnimationFrame = cb => setTimeout(() => {
        vt += 1000 / fps;
        cb(vt);
        if (window.__vtStap){ try { window.__vtStap(vt / 1000); } catch (e){ console.error('vijandtest: ' + e.message + ' ' + e.stack); } }
      }, 0);
    }, fps);
    await page.goto(url);
    await page.waitForFunction(() => typeof setLevel === 'function' && typeof TEST_LEVELS !== 'undefined');
    await page.waitForTimeout(1200);
    const def = Object.assign({ name: 'vijandtest' }, sc.level);
    await page.evaluate(([def, sc]) => {
      setLevel(0, [def]);
      level.onsterfelijk = sc.taai !== false;          // standaard taai: Amir gaat niet dood, zo speelt de vijand door
      beginPlay('medium');
    }, [def, sc]);
    await page.waitForTimeout(600);                  // de baviaan moet zijn plaatjes hebben
    await page.evaluate(inPagina, [sc, sc.taai !== false]);
    const klok = Date.now();
    for (;;){
      await page.waitForTimeout(300);
      const k = await page.evaluate(() => window.__vt_.klaar);
      if (k || (Date.now() - klok) / 1000 > sc.duur * 25) break;
    }
    const R = await page.evaluate(() => { const T = window.__vt_; return { klappen: T.klappen, doden: T.doden, spoor: T.spoor, toestand: T.toestand,
                                                                           regel7: T.regel7, hangt: T.hangt, ev: T.ev, eind: { x: Math.round(world), levens: lives } }; });
    await page.close();
    for (const k of R.klappen) if (!k.bron) k.bron = klapBron(k.regel);
    R.naam = sc.naam; R.n = n; R.console = [...cons];
    return R;
  }
  function verslag(sc, n, R){
    const v = sc.verwacht || {}, af = [];
    if (v.maxRaak !== undefined && R.klappen.length > v.maxRaak) af.push('te vaak geraakt (' + R.klappen.length + ', hoogstens ' + v.maxRaak + ')');
    if (v.minRaak !== undefined && R.klappen.length < v.minRaak) af.push('te weinig geraakt (' + R.klappen.length + ', minstens ' + v.minRaak + ')');
    if (v.doden !== undefined && R.doden.length < v.doden) af.push('niet verslagen (' + R.doden.length + ' van ' + v.doden + ')');
    if (v.geenRegel7 && R.regel7.length) af.push('regel 7');
    if (Object.keys(R.hangt).some(k => !(v.hangtMag || []).includes(k.split(' ').pop()))) af.push('hangt');
    if (R.console.length) af.push('console');
    if (af.length) fouten++;
    console.log((af.length ? 'AFWIJKING ' : 'OK        ') + sc.naam + (keer > 1 ? ' (#' + (n + 1) + ')' : '') + (af.length ? ': ' + af.join(', ') : ''));
    console.log('    geraakt ' + R.klappen.length + 'x' + (R.klappen.length ? ' (' + R.klappen.map(k => k.t.toFixed(1) + 's ' + k.bron + (k.h > 2 ? ' op ' + k.h : '') + (k.gebukt >= 1 ? ' gebukt' : '')).join(', ') + ')' : '')
              + ', verslagen ' + R.doden.length + (R.doden.length ? ' (' + R.doden.map(d => d.t.toFixed(1) + 's').join(', ') + ')' : ''));
    for (const [id, ts] of Object.entries(R.toestand)){
      const tijden = Object.entries(ts.tijd).sort((a, b) => b[1] - a[1]).map(([s, d]) => s + ' ' + d.toFixed(1)).join(', ');
      console.log('    ' + id.padEnd(13) + ' ' + ts.van + ' naar ' + ts.tot + ' (bereik ' + Math.round(ts.min) + '..' + Math.round(ts.max) + '), ' + ts.wissel + ' wissels: ' + tijden);
      if (ts.eerst) console.log('                  eerste aanval ' + ts.eerst[0] + 's (' + ts.eerst[1] + ' op ' + ts.eerst[2] + ' px)' + (ts.inBeeld ? ', in beeld ' + ts.inBeeld[0] + 's (' + ts.inBeeld[1] + ')' : ', nooit in beeld')
                                  + (ts.inBeeld && ts.inBeeld[0] > ts.eerst[0] ? '  BUITEN BEELD BEGONNEN' : ''));
    }
    for (const r7 of R.regel7) console.log('    REGEL 7 ' + r7.t.toFixed(2) + 's ' + r7.wie + ' over de ' + r7.wat + ', nu op ' + r7.x);
    for (const [k, h] of Object.entries(R.hangt)) console.log('    HANGT   ' + k + ' sinds ' + h.t + 's op ' + h.x + ' (Amir op ' + h.amir + ')');
    for (const e of [...new Set(R.ev.map(e => e.wat))]) console.log('    ' + e);
    for (const c of R.console) console.log('    ' + c);
    if (args.includes('--spoor')) for (const s of R.spoor) console.log('      ' + s.join(' '));
  }
  // een paar tegelijk: een pagina tekent op een kern
  const tegelijk = Math.max(1, Number(opt('--tegelijk', 3)));
  let volgende = 0, getoond = 0;
  async function werker(){
    while (volgende < taken.length){
      const i = volgende++;
      uitkomst[i] = await draai(taken[i]);
      while (getoond < taken.length && uitkomst[getoond]){ verslag(taken[getoond][0], taken[getoond][1], uitkomst[getoond]); getoond++; }
    }
  }
  await Promise.all(Array.from({ length: tegelijk }, werker));
  const alles = uitkomst;
  if (opt('--json')) fs.writeFileSync(opt('--json'), JSON.stringify(alles, null, 1));
  console.log('\n' + (alles.length - fouten) + ' van ' + alles.length + ' zonder afwijking');
  await browser.close();
  srv.close();
})();
