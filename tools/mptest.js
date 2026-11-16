#!/usr/bin/env node
'use strict';
// De multiplayertest: speelt Co-op Survival met drie vensters in Chromium (de host en twee gasten), zonder PeerJS. De
// host is het middelpunt van een ster: hij krijgt een nagebootste verbinding per gast (een conn met send en on), een
// gast een naar de host, en Node geeft de berichten door. Daarna lopen simpele spelers naar de dichtstbijzijnde vijand en
// steken. Meldt per venster de fouten in de console, en wat het spel deed: de ronde, de score, de vijanden bij de host en
// bij de gasten, doden en revives.
//
//   node tools/mptest.js                 een potje van 90 s met drie spelers, alle vijanden aan (Both)
//   node tools/mptest.js --spelers 2     met twee spelers (de host en een gast), zoals voor stap 2
//   node tools/mptest.js --duur 40       korter
//   node tools/mptest.js --shots map     elke 10 s een schermafdruk van allebei
//   node tools/mptest.js --soorten bandiet,slang   alleen deze soorten aan
//   node tools/mptest.js --stil          de spelers doen niets (dan gaan ze dood: game over en de revive)
//   node tools/mptest.js --sterf gast   die speler is meteen dood: de revive-ton, het symbool en het opstaan (ook gast2,
//                                        of gast,gast2 voor twee doden en twee revive-tonnen)
//   node tools/mptest.js --taai          de spelers kunnen niet dood (godMode): om lang door te spelen
//   node tools/mptest.js --proef         de vaste proef: de lobby met Ready van iedereen, een ton breken als gast, een treffer
//                                        van de gast, een vijand achter de tweede gast aan, de winkel met Ready van iedereen,
//                                        de revive per dode, game over pas als iedereen dood is, R, Escape
//   node tools/mptest.js --elk           elke soort makkelijk en moeilijk neerzetten, de gast raakt ze: fouten in het tekenen
//   node tools/mptest.js --debug         elke 4 s de stand van allebei: plek, levens en de vijanden
//   node tools/mptest.js --net 60,25,0.05   een echte lijn nabootsen: 60 ms vertraging, tot 25 ms jitter, 5% verlies op het
//                                        snelle kanaal (het betrouwbare kanaal verliest niets, maar wacht op volgorde: een
//                                        verloren pakket kost daar een extra rondje). Meldt aan het eind de ping en hoe
//                                        goed de andere Amir en de vijanden bij de gast de echte baan volgden: bij de best
//                                        passende vertraging (ms) de gemiddelde afwijking in px (lager is vloeiender en klopt beter)
//   node tools/mptest.js --duel --spelers 2   het Duel: allebei in de ronde, de gast valt, de ronde naar de host, ronde 2
//   node tools/mptest.js --stokken gast  deze spelers kiezen in de lobby de stokken (ook host, gast2, of host,gast): kijkt na
//                                        dat iedereen het weet, dat hun potje met stokken start zonder speer, en hun winkel
//   node tools/mptest.js --geensnel      zonder het nagebootste snelle kanaal (zoals via het relais)
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('mptest: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();
const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const duur = Number(opt('--duur', 90)), shots = opt('--shots', null), stil = args.includes('--stil');
const soorten = opt('--soorten', null);
const stokken = (opt('--stokken', '') || '').split(',').filter(Boolean);   // wie de stokken kiest
const net = (opt('--net', '0,0,0')).split(',').map(Number), [LAT, JIT, VERLIES] = [net[0] || 0, net[1] || 0, net[2] || 0];
const geenSnel = args.includes('--geensnel');
const N_SPELERS = Math.max(2, Math.min(3, Number(opt('--spelers', 3))));

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json', '.css': 'text/css', '.webp': 'image/webp' };
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

const wacht = ms => new Promise(ok => setTimeout(ok, ms));
async function tot(page, f, arg, max = 30000){
  const t = Date.now();
  while (Date.now() - t < max){ if (await page.evaluate(f, arg).catch(() => false)) return true; await wacht(200); }
  return false;
}
// de vaste proef: wat de spelers niet vanzelf doen, stap voor stap, met OK of FOUT per stap. R de ramen (host, gast,
// en met drie spelers gast2), L wat er in de lobby gebeurde
const meld = (ok, t) => { console.log((ok ? 'OK   ' : 'FOUT ') + t); if (!ok) process.exitCode = 1; };
async function proef(R, L){
  const [H, G, G2] = R, drie = !!G2, allen = R.map(r => r.page);
  const elk = async (f, arg, max) => { for (const r of R) if (!await tot(r.page, f, arg, max)) return r.wie; return null; };
  if (L) for (const [ok, t] of L) meld(ok, t);
  const zet = p => p.evaluate(() => { godMode = true; });
  meld(await tot(H.page, () => pvp.coop && pvp.coop.ronde >= 1 && tonnen.some(t => !t.weg), null, 60000), 'ronde 1 loopt en er staat een ton (host)');
  for (const p of allen) await zet(p);
  if (drie){
    const st = await Promise.all(R.map(r => r.page.evaluate(() => ({ mij: pvp.mij, x: Math.round(world), anders: pvpAnderen(), broek: pvp.broek.slice() }))));
    meld(st.every((v, i) => v.mij === i), 'ieder zijn eigen slot (' + st.map(v => v.mij).join(', ') + ')');
    meld(new Set(st.map(v => v.x)).size === 3, 'drie startplekken (' + st.map(v => v.x).join(', ') + ')');
    meld(st.every(v => v.anders.length === 2), 'iedereen ziet de twee anderen (' + st.map(v => v.anders.join('+')).join(', ') + ')');
    meld(st.every(v => v.broek.join() === st[0].broek.join()) && new Set(st[0].broek).size === 3, 'drie verschillende broeken, bij iedereen dezelfde (' + st[0].broek.join(', ') + ')');
    const ziet = await G2.page.evaluate(() => { const g = pvp.anders[1].g; return g && Math.abs(g.x - PVP.starts[1]) < 400; });
    meld(ziet, 'de tweede gast ziet de eerste gast op zijn plek (doorgestuurd door de host)');
  }
  meld(await tot(G.page, () => tonnen.some(t => !t.weg && t.mpId != null)), 'de ton staat ook bij de gast');
  if (drie) meld(await tot(G2.page, () => tonnen.some(t => !t.weg && t.mpId != null)), 'en bij de tweede gast');
  const voor = await G.page.evaluate(() => ({ g: pvp.coop.goud, k: hppotionCarry, id: tonnen.find(t => !t.weg).mpId }));
  const voor2 = drie ? await G2.page.evaluate(() => ({ g: pvp.coop.goud, k: hppotionCarry })) : null;
  for (let i = 0; i < 3; i++){ await G.page.evaluate(id => tonRaak(tonnen.find(t => t.mpId === id), 1, true), voor.id); await wacht(400); }
  meld(await tot(H.page, id => tonnen.find(t => t.mpId === id).weg, voor.id, 5000), 'drie treffers van de gast breken de ton bij de host');
  meld(await elk(id => tonnen.find(t => t.mpId === id).weg, voor.id, 5000) === null, 'en bij de gasten');
  meld(await tot(G.page, v => pvp.coop.goud > v.g || hppotionCarry > v.k, voor, 5000), 'de gast krijgt wat erin zat (goud of een kalebas)');
  if (drie) meld(await G2.page.evaluate(v => pvp.coop.goud === v.g && hppotionCarry === v.k, voor2), 'de tweede gast niet (de buit is voor wie brak)');
  meld(await tot(G.page, () => MPC_LIJSTEN.some(q => !q.los && q.l().some(o => o.mpId != null && mpcLeeft(o))), null, 40000), 'er is een vijand bij de gast');
  const kills = await H.page.evaluate(() => pvp.coop.kills);
  const geraakt = new Set();
  for (let i = 0; i < 24; i++){                     // een taaie vijand (het duel, de elite-garde) vraagt meer treffers
    geraakt.add(await G.page.evaluate(() => {
      const q = MPC_LIJSTEN.find(q => !q.los && q.l().some(o => o.mpId != null && mpcLeeft(o)));
      if (!q) return '-';
      const o = q.l().find(o => o.mpId != null && mpcLeeft(o));
      if (q.k === 'snakes' || q.k === 'scorps') enemyTakeHit(o);
      else if (q.k === 'bandieten') hitBandiet(o); else if (q.k === 'hyenas') hitHyena(o); else if (q.k === 'kooimannen') hitKooiman(o);
      else if (q.k === 'meelmannen') hitMeelman(o); else if (q.k === 'zweepmannen') hitZweepman(o); else if (q.k === 'kruisbogen') hitKruisboog(o, 'steek');
      else if (q.k === 'schildmannen') hitSchildman(o, 'steek'); else if (q.k === 'fosforSlangen') fosforRaak(o); else if (q.k === 'goudapen') gaapDood(o, false);
      else enemyTakeHit(o);
      return q.k + ' ' + o.mpId;
    }));
    await wacht(600);
    if (await H.page.evaluate(k => pvp.coop.kills > k, kills)) break;
  }
  meld(await H.page.evaluate(k => pvp.coop.kills > k, kills), 'treffers van de gast doden een vijand bij de host (kills ' + kills + ' -> ' + await H.page.evaluate(() => pvp.coop.kills) + ', geraakt: ' + [...geraakt].join(', ') + ')');
  meld(await elk(k => pvp.coop.kills > k, kills, 3000) === null, 'en de gasten zien de score mee');
  if (drie){
    // een vijand vlak bij de tweede gast gaat achter hem aan, en een slag van die vijand komt bij hem aan (au2), niet bij de eerste
    const doel = await H.page.evaluate(() => {
      const g = pvpAnderNu(2), b = mpcMaak({ k: 'bandiet', hard: false }, g.x - 120, 1, terrainH(g.x - 120));
      b.mpSoort = 'bandiet'; const d = mpcDoel(b); b.hp = 0; bandieten.splice(bandieten.indexOf(b), 1); return d;
    });
    meld(doel === 2, 'een vijand bij de tweede gast kiest hem als doel (' + doel + ')');
    await G2.page.evaluate(() => { godMode = false; invuln = 0; lives = 3; drawLives(); });
    await G.page.evaluate(() => { lives = 3; });
    await H.page.evaluate(() => { mpcWisselIn(2); try { hurtPlayer(true); } finally { mpcWisselUit(); } });
    meld(await tot(G2.page, () => lives === 2, null, 3000), 'een slag van een vijand die achter de tweede gast aan zit raakt hem (au2)');
    meld(await G.page.evaluate(() => lives === 3), 'en niet de eerste gast');
    await G2.page.evaluate(() => { godMode = true; lives = 3; drawLives(); });
  }
  // de versie van de map (MPC_VERSIE): iedereen dezelfde, met de fakkels aan de muren, en om de drie rondes een andere
  const versie = () => Promise.all(R.map(r => r.page.evaluate(() => mpcVersieNu + ':' + (level.fakkels || []).length)));
  const v0 = await versie();
  meld(new Set(v0).size === 1 && /^(dag:0|avond:0|nacht:8|donker:8)$/.test(v0[0]), 'iedereen dezelfde versie van de map (' + v0.join(' ') + ')');
  await H.page.evaluate(() => { const C = pvp.coop; for (const q of MPC_LIJSTEN) mpcZet(q, []); C.rij = []; C.ronde = 3; C.fase = 'wacht'; C.klok = 0; });
  meld(await elk(v => mpcVersieNu !== v, v0[0].split(':')[0], 4000) === null, 'ronde 4: een andere versie van de map, bij iedereen');
  const v1 = await versie();
  meld(new Set(v1).size === 1, 'en weer bij iedereen dezelfde (' + v1.join(' ') + ')');
  // de winkel (stuk 3): de ronde is op na winkelNa rondes, iedereen naar de winkelkamer, kopen, Ready en terug
  const goudVoor = await Promise.all(R.map(r => r.page.evaluate(() => pvp.coop.goud)));
  await H.page.evaluate(() => { const C = pvp.coop; C.rij = []; C.fase = 'golf'; C.ronde = pvp.regels.coop.winkelNa; for (const q of MPC_LIJSTEN) mpcZet(q, []); });
  meld(await elk(() => pvp.coop.inWinkel && !stadTrapFade && !!binnenBij(world), null, 6000) === null, 'na winkelNa rondes: iedereen in de winkelkamer');
  if (drie) meld(new Set(await Promise.all(R.map(r => r.page.evaluate(() => Math.round(world))))).size === 3, 'ieder op zijn eigen plek in de kamer');
  const goudNa = await Promise.all(R.map(r => r.page.evaluate(() => pvp.coop.goud)));
  meld(goudNa.every((g, i) => g >= goudVoor[i] + 5), 'iedereen krijgt het goud van de overleefde ronde (' + goudVoor.join('/') + ' -> ' + goudNa.join('/') + ')');
  const scherm = await G.page.evaluate(() => { world = MPC_WINKEL_KAMER.toonbank + 40; onGround = true; jump = null; binnenE();
    return winkelUIAan && winkelUIEl.classList.contains('coop') && document.querySelectorAll('#wkcoop button').length === MPC_WINKEL.filter(mpcWinkelVoorMij).length - 1 + pvp.spelers.length - 1; });   // alleen wat bij zijn wapen hoort
  meld(scherm, 'E bij de toonbank: het winkelscherm met de prijslijst van Co-op (Give 5 gold per teamgenoot)');
  if (shots){ fs.mkdirSync(shots, { recursive: true }); await G.page.screenshot({ path: path.join(shots, 'winkel_scherm.png') }); await H.page.screenshot({ path: path.join(shots, 'winkel_kamer_host.png') }); }
  const hGoud = await H.page.evaluate(() => pvp.coop.goud), g2Goud = drie ? await G2.page.evaluate(() => pvp.coop.goud) : 0;
  const koop = await G.page.evaluate(() => {
    pvp.coop.goud = 300; const klik = k => document.getElementById('wkc_' + k).click();
    const voorFc = fcModus(); klik('kracht'); const zonder = !pvp.coop.koop.kracht;
    klik('fc'); klik('rond'); klik('kracht'); klik('slot'); klik('leven'); klik('geef_0');
    if (document.getElementById('wkc_geef_2')) klik('geef_2');
    return { voorFc, zonder, fc: fcModus(), rug: RUG_MAX, levens: pvp.levens, lives, goud: pvp.coop.goud };
  });
  meld(koop.voorFc === null && koop.zonder, 'zonder Full Circle geen upgrade');
  meld(koop.fc === 'kracht_rond', 'Full Circle met allebei de upgrades (' + koop.fc + ')');
  meld(koop.rug === 2 && koop.levens === 4, 'het extra speerslot en een extra leven (rug ' + koop.rug + ', levens ' + koop.levens + ')');
  meld(koop.goud === 300 - 30 - 50 - 50 - 45 - 60 - 5 * (drie ? 2 : 1), 'de prijzen kloppen (over: ' + koop.goud + ')');
  // de Gris-gris bij de host (een eigen beurs, zodat de prijzen hierboven blijven kloppen): drie trappen, dan uitverkocht,
  // en een klap die het amulet vangt kost geen leven, een die het mist wel (GRISGRIS)
  const amu = await H.page.evaluate(() => {
    const goud = pvp.coop.goud; pvp.coop.goud = 400; mpcWinkelToon();
    const b = () => document.getElementById('wkc_amulet');
    for (let i = 0; i < 4; i++) b().click();
    const uit = { trap: pvp.coop.koop.amulet, kans: grisGrisKans(), over: pvp.coop.goud, knop: b().textContent };
    const rnd = Math.random, voor = lives, r = running, god = godMode; godMode = false;
    running = true; invuln = 0; Math.random = () => 0; hurtPlayer(true); uit.gevangen = lives === voor && invuln > 0;
    invuln = 0; Math.random = () => 0.99; hurtPlayer(true); uit.geraakt = lives === voor - 1;
    Math.random = rnd; lives = voor; invuln = 0; hurt = 0; dead = false; running = r; godMode = god; drawLives();
    pvp.coop.goud = goud; pvp.banner = ''; return uit;
  });
  meld(amu.trap === 3 && Math.abs(amu.kans - 0.3) < 1e-9 && amu.over === 400 - 40 - 75 - 110 && /Sold out/.test(amu.knop),
       'Gris-gris: drie trappen, 30%, de prijzen kloppen, dan uitverkocht (' + JSON.stringify(amu) + ')');
  meld(amu.gevangen && amu.geraakt, 'Gris-gris: gevangen kost geen leven, gemist wel');
  meld(await tot(H.page, v => pvp.coop.goud === v + 5, hGoud, 3000), 'Give 5 gold aan de host komt bij de host aan');
  if (drie) meld(await tot(G2.page, v => pvp.coop.goud === v + 5, g2Goud, 3000), 'en Give 5 gold aan de tweede gast bij hem (via de host)');
  await G.page.evaluate(() => document.getElementById('wkklaar').click());
  meld(await G.page.evaluate(() => !winkelUIAan && pvp.coop.mijnKlaar), 'Ready bij de gast: het scherm dicht');
  meld(await tot(H.page, () => pvp.coop.wkKlaar[1] && pvp.coop.inWinkel, null, 3000), 'de host hoort het, en wacht nog');
  if (drie) meld(await tot(G2.page, () => pvp.coop.wkKlaar[1] && /1 of 2 teammates ready/.test(pvpEl('pvpbanner').textContent), null, 3000), 'de tweede gast ziet het ook (1 of 2 teammates ready)');
  await H.page.evaluate(() => mpcKlaarDruk());
  if (drie){
    await wacht(800);
    meld(await H.page.evaluate(() => pvp.coop.inWinkel), 'de host en een gast Ready: nog in de winkel, de tweede gast is er nog niet');
    await G2.page.evaluate(() => mpcKlaarDruk());
  }
  meld(await tot(H.page, () => !pvp.coop.inWinkel && !stadTrapFade && !binnenBij(world) && pvp.coop.fase === 'wacht' && wapenrekken[0].n === pvp.regels.coop.rek, null, 6000), 'iedereen Ready: de host weer op straat, het rek vol, de pauze loopt');
  meld(await elk(() => !pvp.coop.inWinkel && !stadTrapFade && !binnenBij(world), null, 6000) === null, 'en de gasten ook');
  // Full Circle rondom: een verblinde bandiet voor de host en een achter hem; de draaislag raakt ze allebei
  const rond = await H.page.evaluate(async () => {
    godMode = true; pvp.coop.koop.fc = true; pvp.coop.koop.rond = true; facing = -1;
    const voor = mpcMaak({ k: 'bandiet', hard: false }, world - 150, 1, terrainH(world - 150));
    const achter = mpcMaak({ k: 'bandiet', hard: false }, world + 150, -1, terrainH(world + 150));
    voor.verblind = 5; achter.verblind = 0;
    const hp0 = [voor.hp, achter.hp];
    atkCooldown = 0; startAttack();
    const soort = fcSoort;
    await new Promise(ok => setTimeout(ok, 1200));
    voor.hp = 0; achter.hp = 0; bandieten.length = 0;
    return { soort, voor: [hp0[0], voor.hp], achter: [hp0[1], achter.hp] };
  });
  meld(rond.soort === 'rond' && rond.voor[1] < rond.voor[0] && rond.achter[1] < rond.achter[0],
       'Full Circle rondom raakt voor en achter (' + JSON.stringify(rond) + ')');
  if (drie){
    // de revive per dode: twee gasten dood, twee revive-tonnen, de camera bij de levende host, geen game over
    await H.page.evaluate(() => { MPC.reviveNa = 1.5; for (const q of MPC_LIJSTEN) mpcZet(q, []); pvp.coop.rij = []; });
    for (const r of [G, G2]) await r.page.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
    meld(await tot(G.page, () => dead, null, 3000) && await tot(G2.page, () => dead, null, 3000), 'twee gasten dood');
    meld(await tot(H.page, () => Object.keys(pvp.coop.reviveTon).sort().join() === '1,2' && tonnen.filter(t => t.revive && !t.weg).length === 2, null, 6000),
         'twee revive-tonnen, een per dode');
    meld(await H.page.evaluate(() => pvp.coop.fase !== 'uit' && !dead), 'geen game over zolang de host leeft');
    const cam = await G2.page.evaluate(() => { const c = mpCoopCam(); return c != null && Math.abs(c - pvp.anders[0].g.x) < 1; });
    meld(cam, 'de camera van een dode volgt de dichtstbijzijnde levende speler');
    meld(await tot(G2.page, () => pvpEl('pvpbanner').textContent === 'Waiting for revive', null, 2000), 'bovenin: Waiting for revive');
    // de host breekt de ton van de tweede gast en pakt het symbool: alleen die staat op
    const t2 = await H.page.evaluate(() => pvp.coop.reviveTon[2].mpId);
    for (let i = 0; i < 3; i++){ await H.page.evaluate(id => tonRaak(tonnen.find(t => t.mpId === id), 1, true), t2); await wacht(250); }
    meld(await tot(H.page, () => pvp.coop.symbolen.some(S => S.voor === 2), null, 3000), 'de revive-ton van de tweede gast laat zijn symbool vallen');
    meld(await tot(G.page, () => pvp.coop.symbolen.some(S => S.voor === 2), null, 3000), 'de eerste gast ziet het symbool ook');
    await H.page.evaluate(() => { const S = pvp.coop.symbolen.find(S => S.voor === 2); world = S.x; ph = S.h; });
    meld(await tot(G2.page, () => !dead && lives === 1, null, 4000), 'de host pakt het: de tweede gast staat op met 1 leven');
    meld(await G.page.evaluate(() => dead), 'de eerste gast ligt nog');
    meld(await tot(H.page, () => !pvp.coop.reviveTon[2] && !!pvp.coop.reviveTon[1], null, 3000), 'zijn ton staat er nog, die van de tweede gast niet meer');
    await G2.page.evaluate(() => { godMode = true; });
  }
  // iedereen dood: game over en het eindscherm
  for (const r of R) await r.page.evaluate(() => { if (dead) return; godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  meld(await tot(H.page, () => pvp.coop.fase === 'uit' && pvpEl('mpeind').classList.contains('on'), null, 5000), 'iedereen dood: game over, het eindscherm bij de host');
  meld(await elk(() => pvp.coop.fase === 'uit' && pvpEl('mpeind').classList.contains('on'), null, 5000) === null, 'en bij de gasten');
  console.log('     ' + await G.page.evaluate(() => pvpEl('mpeind').innerText.replace(/\n+/g, ' | ')));
  for (const r of R.slice(0, -1)) await r.page.evaluate(() => opnieuw());
  await wacht(800);
  meld(await H.page.evaluate(() => pvp.coop.fase === 'uit'), 'R bij ' + (R.length - 1) + ' van de ' + R.length + ': nog geen nieuw potje');
  await R[R.length - 1].page.evaluate(() => opnieuw());
  meld(await elk(() => pvp.coop && pvp.coop.fase !== 'uit' && !dead && !pvpEl('mpeind').classList.contains('on'), null, 8000) === null, 'R bij iedereen: een nieuw potje, bij iedereen');
  await (drie ? G2 : H).page.evaluate(() => toMenu());
  meld(await elk(() => pvp && pvp.fase === 'lobby' && !pvp.coop && pvpEl('menuPvp').classList.contains('lobby'), null, 5000) === null,
       'Escape' + (drie ? ' bij de tweede gast' : '') + ': iedereen in de lobby, de verbinding open');
  if (drie){
    await G2.page.evaluate(() => pvpEl('mpleave').click());
    meld(await tot(H.page, () => pvp && pvp.spelers.join() === '0,1' && pvp.fase === 'lobby', null, 4000), 'de tweede gast verlaat de lobby: de host houdt de eerste gast');
    meld(await tot(G.page, () => pvp && pvp.spelers.join() === '0,1' && pvp.fase === 'lobby', null, 4000), 'en de eerste gast weet het');
  }
  for (const r of R){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
}

// elke soort, makkelijk en moeilijk, bij de host neergezet; de gast tekent ze en raakt ze. Meldt de fouten van allebei
async function elk(H, G){
  await tot(H.page, () => pvp.coop && pvp.coop.ronde >= 1, null, 60000);
  for (const r of [H, G]) await r.page.evaluate(() => { godMode = true; });
  const soorten = await H.page.evaluate(() => MP_SOORTEN.map(q => q.k));
  for (const k of soorten) for (const hard of [false, true]){
    await H.page.evaluate(([k, hard]) => mpcSpawn({ k, hard }), [k, hard]);
    await wacht(1500);
    await G.page.evaluate(() => {
      for (const q of MPC_LIJSTEN) if (!q.los) for (const o of q.l()) if (o.mpId != null && mpcLeeft(o)){
        o.mpGemeld = 0;
        if (q.k === 'snakes' || q.k === 'scorps') enemyTakeHit(o); else if (q.k === 'bandieten') hitBandiet(o); else if (q.k === 'hyenas') hitHyena(o);
        else if (q.k === 'kooimannen') hitKooiman(o); else if (q.k === 'meelmannen') hitMeelman(o); else if (q.k === 'zweepmannen') hitZweepman(o);
        else if (q.k === 'kruisbogen') hitKruisboog(o, 'steek'); else if (q.k === 'schildmannen') hitSchildman(o, 'steek');
        else if (q.k === 'fosforSlangen') fosforRaak(o); else if (q.k === 'goudapen') gaapDood(o, false);
      }
    });
    const st = await G.page.evaluate(() => MPC_LIJSTEN.filter(q => q.l().length).map(q => q.k + ' ' + q.l().length).join(', '));
    console.log((hard ? 'moeilijk ' : 'makkelijk ') + k + ': bij de gast ' + st);
  }
  await wacht(8000);
  console.log('kills bij de host: ' + await H.page.evaluate(() => pvp.coop.kills) + ', score ' + await H.page.evaluate(() => pvp.coop.score));
  for (const r of [H, G]){ console.log(r.wie + (r.fouten.size ? ' fouten:' : ' geen fouten')); for (const f of r.fouten) console.log('  ' + f); }
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await chromium.launch();
  const ramen = [];
  for (const wie of ['host', 'gast', 'gast2'].slice(0, N_SPELERS)){
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await ctx.newPage();
    const fouten = new Set();
    page.on('pageerror', e => fouten.add('fout: ' + e.message + (e.stack ? ' @ ' + (e.stack.split('\n')[1] || '').trim() : '')));
    page.on('console', m => { if (m.type() === 'error') fouten.add('console: ' + m.text().slice(0, 300)); });
    page.on('response', r => { if (r.status() >= 400) fouten.add(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+\//, '')); });
    ramen.push({ wie, page, fouten, bus: [] });
  }
  // de nagebootste verbindingen, een ster: de host heeft een conn per gast ('g1', 'g2'), een gast een naar de host ('h').
  // send gaat via Node naar het venster aan de andere kant, met --net een vertraging, jitter en verlies. Het betrouwbare
  // kanaal levert per verbinding op volgorde: een verloren pakket wordt opnieuw verstuurd en alles erachter wacht. Het
  // snelle kanaal levert zonder volgorde en verliest gewoon.
  const toeval = () => Math.random() * JIT;
  const H0 = ramen[0];
  const overkant = (r, cid) => r === H0 ? { r: ramen[Number(cid.slice(1))], cid: 'h' } : { r: H0, cid: 'g' + ramen.indexOf(r) };
  for (const r of ramen){
    const laatst = {};
    await r.page.exposeFunction('__mpZend', (cid, s) => {
      const o = overkant(r, cid); if (!o.r) return;      // een lijn naar niemand (de vierde speler in de proef)
      let at = Date.now() + LAT + toeval();
      if (Math.random() < VERLIES) at += 2 * LAT + 2 * toeval() + 20;   // kwijt: na een rondje opnieuw
      at = Math.max(at, laatst[cid] || 0); laatst[cid] = at;
      o.r.bus.push({ cid: o.cid, s, at, snel: false });
    });
    await r.page.exposeFunction('__mpSnel', (cid, s) => {
      if (Math.random() < VERLIES) return;
      const o = overkant(r, cid); if (!o.r) return;
      o.r.bus.push({ cid: o.cid, s, at: Date.now() + LAT + toeval(), snel: true });
    });
  }
  for (const r of ramen){
    await r.page.goto(url);
    await r.page.waitForFunction(() => typeof pvpVerbonden === 'function' && typeof mpCoopStart === 'function');
  }
  await Promise.all(ramen.map(r => r.page.waitForTimeout(1500)));
  for (const r of ramen){
    await r.page.evaluate(([geenSnel]) => {
      window.__conns = {};
      // een conn zoals PeerJS hem geeft, met cid de naam van deze lijn in Node
      window.__maakConn = cid => {
        const h = {};
        const c = { open: true, relay: false, send: o => window.__mpZend(cid, JSON.stringify(o)),
                    on: (k, f) => { h[k] = f; }, close(){ if (!c.open) return; c.open = false; if (h.close) h.close(); } };
        c.ontvang = s => { if (c.open && h.data) h.data(JSON.parse(s)); };
        if (!geenSnel){                                // het snelle kanaal van pvpSnelOpen, nagebootst
          const dc = { readyState: 'open', bufferedAmount: 0, send: s => window.__mpSnel(cid, s), close(){} };
          c.peerConnection = { createDataChannel: () => dc };
          c.ontvangSnel = s => { if (c.open && dc.onmessage) dc.onmessage({ data: s }); };
        } else c.ontvangSnel = c.ontvang;
        window.__conns[cid] = c;
        return c;
      };
      window.__ontvang = (cid, s, snel) => { const c = window.__conns[cid]; if (c) (snel ? c.ontvangSnel : c.ontvang)(s); };
      // de baan meten: elk beeld (met Date.now, dezelfde klok in alle vensters) mijn eigen plek en die van de vijanden
      // (echt), en de plek waar ik de anderen en de vijanden teken (beeld). Node legt ze aan het eind naast elkaar.
      window.__baan = { echt: {}, beeld: {} };
      const leg = (w, k, x) => { const a = w[k] || (w[k] = []); if (a.length < 20000) a.push([Date.now(), Math.round(x * 10) / 10]); };
      const meetBeeld = () => {
        requestAnimationFrame(meetBeeld);
        if (typeof pvp === 'undefined' || !pvp || !running || !pvp.coop) return;
        const B = window.__baan;
        leg(B.echt, 'amir_' + pvp.mij, playerX());
        for (const p of pvpAnderen()) leg(B.beeld, 'amir_' + p, pvp.anders[p].g.x);
        for (const q of MPC_LIJSTEN) if (!q.los) for (const o of q.l()) if (o.mpId != null && mpcLeeft(o)) leg(pvp.host ? B.echt : B.beeld, 'v' + o.mpId, o.x);
      };
      requestAnimationFrame(meetBeeld);
      showMenu('menuPvp');
    }, [geenSnel]);
  }
  // berichten doorgeven, zo vaak als het kan
  let loopt = true;
  const pomp = async r => {
    while (loopt){
      const nu = Date.now(), klaar = r.bus.filter(b => b.at <= nu);
      if (klaar.length){
        r.bus = r.bus.filter(b => b.at > nu);
        klaar.sort((a, b) => a.at - b.at);
        await r.page.evaluate(rij => { for (const b of rij) window.__ontvang(b.cid, b.s, b.snel); }, klaar).catch(() => {});
      } else await new Promise(ok => setTimeout(ok, 4));
    }
  };
  const pompen = ramen.map(pomp);
  const [H, G, G2] = ramen;
  // verbinden: de eerste gast, dan de tweede (de host neemt hem aan zolang de lobby open is)
  const lobby = [];
  for (let i = 1; i < ramen.length; i++){
    await ramen[i].page.evaluate(() => pvpVerbonden(window.__maakConn('h'), false));
    await H.page.evaluate(i => { const c = window.__maakConn('g' + i); if (typeof pvpNieuweGast === 'function') pvpNieuweGast(c); else pvpVerbonden(c, true); }, i);
    await tot(ramen[i].page, () => pvp && pvp.fase === 'lobby', null, 5000);
  }
  for (const r of ramen) if (stokken.includes(r.wie)) await r.page.evaluate(() => pvpEl('mpwpstok').click());
  if (stokken.length){
    await H.page.waitForTimeout(300);
    const wapens = await Promise.all(ramen.map(r => r.page.evaluate(() => pvp.wapen.slice(0, 3).join())));
    const zou = ramen.map(r => stokken.includes(r.wie) ? 'stok' : 'speer').join();
    meld(wapens.every(w => w.startsWith(zou)), 'het wapen uit de lobby, bij iedereen hetzelfde (' + wapens[0] + ')');
  }
  if (args.includes('--duel')) await H.page.evaluate(() => { window.__duel = true; });
  await H.page.evaluate(soorten => {
    mpWijzig(() => {
      pvp.inst.modus = window.__duel ? 'duel' : 'coop';
      Object.assign(pvp.inst.coop, { start: 2, erbij: 1, pauze: 5 });
      for (const q of MP_SOORTEN) pvp.inst.coop.vij[q.k] = soorten ? (soorten.includes(q.k) ? (q.var ? 'beide' : 'aan') : 'uit') : (q.var ? 'beide' : 'aan');
    });
  }, soorten ? soorten.split(',') : null);
  await H.page.waitForTimeout(400);
  if (G2){
    lobby.push([await H.page.evaluate(() => pvp.spelers.join() === '0,1,2'), 'de host heeft drie spelers in de lobby']);
    const br = await Promise.all(ramen.map(r => r.page.evaluate(() => pvp.broek.slice(0, 3).join())));
    lobby.push([br.every(b => b === br[0]) && new Set(br[0].split(',')).size === 3, 'drie broekkleuren, bij iedereen dezelfde (' + br[0] + ')']);
    lobby.push([await G2.page.evaluate(() => /2 players|3 players|of 3/.test(pvpEl('mpspelers').textContent) && pvpEl('mpspelers').textContent.includes('(host)')), 'de tweede gast ziet wie er in de lobby staan (' + await G2.page.evaluate(() => pvpEl('mpspelers').textContent) + ')']);
    await H.page.evaluate(() => { const c = window.__maakConn('g9'); pvpNieuweGast(c); window.__vierde = c; });
    await wacht(700);
    lobby.push([await H.page.evaluate(() => pvp.spelers.length === 3 && !window.__vierde.open), 'een vierde speler wordt geweigerd (vol)']);
    await G.page.evaluate(() => pvpEl('mpready').click());
    await H.page.waitForTimeout(300);
    lobby.push([await H.page.evaluate(() => pvpEl('mpstart').disabled && /1 of 2/.test(pvpEl('mpstartuitleg').textContent)), 'een gast Ready: Start mag nog niet (' + await H.page.evaluate(() => pvpEl('mpstartuitleg').textContent) + ')']);
    await H.page.evaluate(() => mpWijzig(() => { pvp.inst.modus = 'duel'; }));
    await H.page.waitForTimeout(200);
    lobby.push([await H.page.evaluate(() => pvpEl('mpstart').disabled && /two players/.test(pvpEl('mpstartuitleg').textContent)), 'Duel met drie spelers mag niet']);
    await H.page.evaluate(() => mpWijzig(() => { pvp.inst.modus = 'coop'; }));
    await H.page.waitForTimeout(200);
    for (const r of [G, G2]) await r.page.evaluate(() => pvpEl('mpready').click());
  } else await G.page.evaluate(() => pvpEl('mpready').click());
  await H.page.waitForTimeout(300);
  const start = await H.page.evaluate(() => { const ok = !pvpEl('mpstart').disabled; mpStart(); return ok; });
  lobby.push([start, 'iedereen Ready: Start mag']);
  console.log('Start mocht: ' + start);
  if (stokken.length){
    await wacht(1500);
    for (const r of ramen){
      const st = await r.page.evaluate(() => ({ aan: stokAan(), spear, rug: RUG_MAX,
        winkel: typeof MPC_WINKEL !== 'undefined' ? MPC_WINKEL.filter(q => mpcWinkelVoorMij(q)).map(q => q.k).join() : '' }));
      const wil = stokken.includes(r.wie);
      meld(st.aan === wil && (!wil || (!st.spear && st.rug === 0)), r.wie + ': ' + (wil ? 'stokken, geen speer en geen rug' : 'de speer') + ' (' + JSON.stringify(st) + ')');
      if (!args.includes('--duel')) meld(wil ? (st.winkel.includes('hout') && st.winkel.includes('slam') && !/speer|gif|fc|slot/.test(st.winkel)) : !st.winkel.includes('hout'),
        r.wie + ': de winkel voor zijn wapen (' + st.winkel + ')');
    }
    // een stokslag van een gast bij de host: een halve treffer, met Hardwood sticks 0,75, en de counter een hele
    const gi = ramen.findIndex(r => r !== H && stokken.includes(r.wie));
    // de grondklap in Co-op: aan bij de stokspelers, 5 s afkoeling, en de golf van de gast doet bij de host zijn schade
    for (const r of ramen) if (stokken.includes(r.wie)){
      const g = await r.page.evaluate(() => ({ aan: gkAan(), koel: (() => { const k = gkKoelT; gkKoelT = 0; gkFase = 'land';
        atkStok = 'grondklap'; atkFrame = STOK.ms.grondklap.length - 1; atkAcc = 0; dead = false; hurt = 0; gkStokStap(1);
        const uit = gkKoelT; gkKoelT = k; return uit; })() }));
      meld(g.aan && g.koel === 5, r.wie + ': de grondklap aan, 5 s afkoeling (' + JSON.stringify(g) + ')');
    }
    if (gi > 0 && !args.includes('--duel') && await tot(H.page, () => bandieten.some(b => mpcLeeft(b) && b.mpId != null && b.hp >= 3), null, 20000)){
      const d = await H.page.evaluate(p => {
        const b = bandieten.find(b => mpcLeeft(b) && b.mpId != null && b.hp >= 3), uit = [];
        for (const [st, hw] of [['slag', 0], ['stapslag', 1], ['draaislag', 0]]){
          const voor = b.hp; b.inv = 0; b.mpGemeld = 0; b.rust = 0;
          mpcTrefferVanGast({ p, a: 'bandieten', id: b.mpId, f: 'hitBandiet', g: [], st, sf: STOK.actief[st][0], co: 0, hw });
          uit.push(+(voor - b.hp).toFixed(2));
        }
        return uit.join() + (atkStok == null && stokHoutGast == null ? '' : ' (de stand van de host lekt)');
      }, gi);
      meld(d === '0.5,0.75,1', 'de stokslag van de gast bij de host: slag, Hardwood, counter (' + d + ')');
    }
    if (gi > 0 && !args.includes('--duel') && await tot(H.page, () => bandieten.some(b => mpcLeeft(b) && b.mpId != null), null, 30000)){
      const gk = await H.page.evaluate(p => {
        const b = bandieten.find(b => mpcLeeft(b) && b.mpId != null);
        if (!b) return 'geen bandiet';
        const uit = [];
        for (const [onder, sch, kn] of [[false, 0.5, 1], [true, 0.5, 1], [false, 1, 1.6]]){   // de laatste: Ground slam: heavier (GK.zwaar)
          if (b.hp < 2) b.hp = 3;
          const voor = b.hp; b.inv = 0; b.mpGemeld = 0; b.rust = 0;
          const x0 = onder ? b.x + 20 : b.x + 400, tot = onder ? b.x - 20 : b.x + 300;   // dir -1: onder als x tussen tot en x0
          mpcTrefferVanGast({ p, a: 'bandieten', id: b.mpId, f: 'hitBandiet', g: [], st: 'grondklap', sf: 15, co: 0, hw: 0, gk: [x0, tot, -1, sch, kn] });
          uit.push(+(voor - b.hp).toFixed(2), b.gkVan === x0 && b.gkKnock === kn ? 'van' : 'mis');
        }
        return uit.join() + (gkRaak ? ' (gkRaak lekt)' : '');
      }, gi);
      await ramen[gi].page.evaluate(() => { const r = gkRaak; gkInslag(); gkRaak = r; });   // de klap van de gast: de anderen zien hem ('gk')
      await wacht(800);
      const zie = await H.page.evaluate(() => gkFx.golven.length + gkFx.stof.length);
      meld(zie > 0, 'de host ziet de grondklap van de gast (' + zie + ' golven en wolken)');
      meld(gk === '0.5,van,1,van,1,van', 'de golf van de gast bij de host: gewoon, recht eronder en heavier (' + gk + ')');
      // de lijken: een dode vijand is binnen 6 s weg, bij de host en bij de gast
      const lid = await H.page.evaluate(() => {
        const b = bandieten.find(b => mpcLeeft(b) && b.mpId != null); if (!b) return null;
        for (let i = 0; i < 12 && mpcLeeft(b); i++){ b.inv = 0; b.rust = 0; MPC_ORIG.hitBandiet(b); }
        return mpcLeeft(b) ? null : b.mpId;
      });
      if (lid != null){
        await wacht(6500);
        const nog = [];
        for (const r of ramen) if (await r.page.evaluate(id => bandieten.some(b => b.mpId === id), lid)) nog.push(r.wie);
        meld(!nog.length, 'het lijk is binnen 6 s weg' + (nog.length ? ' (nog bij ' + nog.join() + ')' : ''));
      } else meld(false, 'het lijk: geen bandiet dood te krijgen');
    }
  }
  // de spelers: naar de dichtstbijzijnde vijand lopen en steken; R na game over
  const speler = ([stil, taai, sterf]) => {
    if (!pvp || !pvp.coop || !running) return;
    if (taai && pvp.coop.fase !== 'uit' && !dead) godMode = true;
    if (sterf && !window.__gestorven && pvp.coop.ronde >= 1 && pvp.coop.fase !== 'uit'){ window.__gestorven = true; godMode = false; lives = 1; hurtPlayer(true); }
    const lijst = MPC_LIJSTEN.filter(q => !q.los).flatMap(q => q.l()).filter(o => mpcLeeft(o));
    keys['ArrowLeft'] = keys['ArrowRight'] = false;
    if (stil || dead) return;
    // eerst de revive: het symbool pakken, of de revive-ton breken
    const S = pvp.coop.symbolen[0], rt = tonnen.find(t => t.revive && !t.weg);
    if (S || rt){
      const x = S ? S.x : rt.x, d = x - world;
      if (S) keys[d < 0 ? 'ArrowLeft' : 'ArrowRight'] = Math.abs(d) > 10;
      else if (Math.abs(d) > 140) keys[d < 0 ? 'ArrowLeft' : 'ArrowRight'] = true;
      else if (Math.abs(d) < 90) keys[d < 0 ? 'ArrowRight' : 'ArrowLeft'] = true;
      else { facing = d < 0 ? -1 : 1; startAttack(); }
      return;
    }
    let doel = null;
    for (const o of lijst) if (!doel || Math.abs(o.x - world) < Math.abs(doel.x - world)) doel = o;
    if (!doel) return;
    const d = doel.x - world;
    if (Math.abs(d) > 120) keys[d < 0 ? 'ArrowLeft' : 'ArrowRight'] = true;
    else if (Math.abs(d) < 60) keys[d < 0 ? 'ArrowRight' : 'ArrowLeft'] = true;   // te dichtbij: de steek gaat over hem heen
    else {
      facing = d < 0 ? -1 : 1;
      const laag = snakes.includes(doel) || scorps.includes(doel) || fosforSlangen.includes(doel) || hyenas.includes(doel);
      if (laag) zwaaiNu(); else startAttack();      // laag de lage zwaai, anders de stoot
    }
  };
  const meet = () => {
    const C = pvp && pvp.coop;
    if (!C) return null;
    const tel = {};
    for (const q of MPC_LIJSTEN){ const n = q.l().length; if (n) tel[q.k] = n; }
    return { fase: C.fase, ronde: C.ronde, score: C.score, kills: C.kills, dood: dead, levens: lives, tel, x: Math.round(world),
             tonnen: tonnen.filter(t => !t.weg).length, eind: C.eind };
  };
  if (args.includes('--duel')){
    meld(await tot(H.page, () => pvp.fase === 'vecht' && running, null, 30000) && await tot(G.page, () => pvp.fase === 'vecht' && running, null, 30000), 'het Duel loopt bij allebei');
    meld(await H.page.evaluate(() => Math.round(world)) === -250 && await G.page.evaluate(() => Math.round(world)) === -2550, 'de host rechts, de gast links');
    meld(await tot(H.page, () => pvpAnderen().length === 1, null, 5000), 'de host ziet de gast');
    await G.page.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
    meld(await tot(H.page, () => pvp.sc[0] === 1, null, 5000), 'de gast valt: de ronde naar de host');
    meld(await tot(G.page, () => pvp.ronde === 2 && pvp.fase === 'vecht' && pvp.sc[0] === 1, null, 8000), 'ronde 2 begint, de gast weet de stand');
    meld(await G.page.evaluate(() => /You 0  -  1 Opponent/.test(pvpEl('pvpscore').textContent)), 'de stand bij de gast: ' + await G.page.evaluate(() => pvpEl('pvpscore').textContent));
    if (stokken.includes('host')){                    // een stokslag van de host op de gast, die 200 px voor hem staat (de stapslag reikt ver)
      await wacht(2500);
      const hx = await H.page.evaluate(() => { laadWacht = false; godMode = false; return world; });   // de host blijft in deze opzet op het laadscherm staan (ook zonder stokken)
      await G.page.evaluate(hx => { laadWacht = false; godMode = false; invuln = 0; world = hx - 200; facing = 1; window.__l0 = lives; }, hx);
      await wacht(600);
      await H.page.evaluate(() => { facing = -1; startAttack(); });
      meld(await tot(G.page, () => lives < window.__l0, null, 3000), 'de stokslag van de host raakt de gast in het Duel');
    }
    for (const r of ramen){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
    loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return;
  }
  if (args.includes('--elk')){ await elk(H, G); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  if (args.includes('--proef')){ await proef(ramen, lobby); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  const t0 = Date.now();
  let volgendeShot = 0, nShot = 0;
  const doden = {}, wasDood = {}, revives = {};
  for (const r of ramen){ doden[r.wie] = 0; wasDood[r.wie] = false; revives[r.wie] = 0; }
  while ((Date.now() - t0) / 1000 < duur){
    await Promise.all(ramen.map(r => r.page.evaluate(speler, [stil, args.includes('--taai'), opt('--sterf', '').split(',').includes(r.wie)]).catch(e => r.fouten.add('speler: ' + e.message))));
    for (const r of ramen){
      const m = await r.page.evaluate(meet).catch(() => null);
      if (!m) continue;
      if (m.dood && !wasDood[r.wie]) doden[r.wie]++;
      if (!m.dood && wasDood[r.wie]) revives[r.wie]++;
      wasDood[r.wie] = m.dood;
      r.laatst = m;
    }
    const s = (Date.now() - t0) / 1000;
    if (shots && s >= volgendeShot){
      fs.mkdirSync(shots, { recursive: true });
      for (const r of ramen) await r.page.screenshot({ path: path.join(shots, r.wie + '_' + String(nShot).padStart(2, '0') + '.png') });
      nShot++; volgendeShot = s + 10;
    }
    if (args.includes('--debug') && Math.floor(s / 4) !== Math.floor((s - 0.5) / 4)) for (const r of ramen) console.log(r.wie, Math.round(s), JSON.stringify(await r.page.evaluate(() => {
      const l = MPC_LIJSTEN.filter(q => !q.los).flatMap(q => q.l().map(o => q.k + ':' + Math.round(o.x) + ':' + o.state + ':' + Math.round(o.base || 0) + ':' + (o.mpSoort || '-')));
      return { w: Math.round(world), lives, goud: pvp.coop.goud, kal: hppotionCarry, f: pvp.coop.fase, r: pvp.coop.ronde, ton: tonnen.filter(t => !t.weg).map(t => Math.round(t.x) + (t.revive ? 'R' : '')), rek: wapenrekken[0] && wapenrekken[0].n, l };
    })));
    if (H.laatst && H.laatst.eind) break;
    await new Promise(ok => setTimeout(ok, 100));
  }
  for (const r of ramen) r.net = await r.page.evaluate(() => ({
    ping: typeof pvpPings === 'function' ? pvpPings() : null, snel: typeof pvpSnelAan === 'function' ? pvpSnelAan() : false,
    baan: window.__baan })).catch(() => null);
  // per vertraging D: hoe ver het beeld afwijkt van de echte plek D ms eerder; de beste D en die afwijking
  const vergelijk = (beeld, echt) => {
    const paren = Object.keys(beeld).filter(k => echt[k] && echt[k].length > 30);
    let best = null;
    for (let D = 0; D <= 600; D += 10){
      let som = 0, n = 0;
      for (const k of paren){
        const e = echt[k]; let j = 0;
        for (const [t, x] of beeld[k]){
          const te = t - D;
          while (j < e.length - 2 && e[j + 1][0] < te) j++;
          if (te < e[0][0] || te > e[e.length - 1][0]) continue;
          const [t0, x0] = e[j], [t1, x1] = e[j + 1], xe = t1 > t0 ? x0 + (x1 - x0) * Math.max(0, Math.min(1, (te - t0) / (t1 - t0))) : x0;
          const f = Math.abs(x - xe); if (f > 300) continue;   // een sprong (een nieuwe plek, opstaan): telt niet
          som += f; n++;
        }
      }
      if (n && (!best || som / n < best.afwijking)) best = { vertraging: D, afwijking: +(som / n).toFixed(2), n };
    }
    return best;
  };
  // de andere Amirs: per venster wat hij van de anderen tekent tegen hun echte baan; de vijanden: elke gast tegen de host
  if (ramen.every(r => r.net)){
    const pak = (b, pre) => Object.fromEntries(Object.entries(b).filter(([k]) => k.startsWith(pre)));
    const echtAmir = Object.assign({}, ...ramen.map(r => pak(r.net.baan.echt, 'amir')));
    for (const r of ramen) r.net.volgt = {
      amir: Object.fromEntries(Object.keys(r.net.baan.beeld).filter(k => k.startsWith('amir_'))
              .map(k => [ramen[Number(k.slice(5))].wie, vergelijk({ [k]: r.net.baan.beeld[k] }, echtAmir)])),   // per andere speler: een doorgestuurde gast loopt een sprong verder achter
      vijanden: r !== ramen[0] ? vergelijk(pak(r.net.baan.beeld, 'v'), pak(ramen[0].net.baan.echt, 'v')) : null
    };
    for (const r of ramen) delete r.net.baan;
  }
  loopt = false;
  await Promise.all(pompen);
  for (const r of ramen){
    console.log('\n== ' + r.wie + ' ==');
    if (r.net) console.log('lijn: ' + JSON.stringify(r.net));
    console.log(JSON.stringify(r.laatst));
    console.log('doden: ' + doden[r.wie] + ', weer op: ' + revives[r.wie]);
    if (r.fouten.size){ console.log('fouten:'); for (const f of r.fouten) console.log('  ' + f); }
    else console.log('geen fouten');
  }
  await browser.close(); srv.close();
})();
