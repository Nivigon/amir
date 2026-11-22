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
//   node tools/mptest.js --proef --winkeleerst   met Start in the shop: kijkt na dat ook elke gast in de winkel begint
//   node tools/mptest.js --kaart ishmul  Co-op Survival op een andere map (een id uit MP_KAARTEN.coop; standaard dye)
//   node tools/mptest.js --hl            de tweede Co-op episode (The Smugglers' Cellar): de lijn van een hinderlaag, het
//                                        leiband, wachten op het team, de regie (balken, camera, vijanden per shot), het
//                                        gevecht en de lijn weer open, en in level 7 de kelder als shot en als eind
//   node tools/mptest.js --winkel        de winkels van The Smugglers' Cellar: de deur tussen de hinderlagen, goud per kill,
//                                        de winkel in het huis zonder pauze en met alles van Survival, en goud, upgrades en
//                                        tas mee naar het volgende level (en na game over die van het begin van het level),
//                                        en een kist die maar een speler opent
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
// de Co-op episode (--ep): de levels samen uitspelen. Een spawn die bij een gast komt, het eind dat op iedereen wacht,
// een revive-ton bij de levende ergens midden in het level, door naar het volgende level met de score, game over en R
// voor hetzelfde level, en het slot na het laatste level
async function epProef(R){
  const [H, G] = R, allen = R.map(r => r.page);
  const elk = async (f, arg, max) => { for (const r of R) if (!await tot(r.page, f, arg, max)) return r.wie; return null; };
  const klaar = i => elk(i => running && !laadWacht && pvp.coop && pvp.coop.ep && pvp.coop.ep.i === i && pvp.coop.fase === 'ep' && level.name.startsWith('Co-op ' + (i + 1)), i, 60000);
  meld(await klaar(0) === null, 'level 1 loopt bij iedereen');
  for (const p of allen) await p.evaluate(() => { MPC_LEIBAND.max = 1e9; });   // deze proef zet spelers ver uit elkaar neer: het leiband uit (--hl test het)
  meld(await tot(H.page, () => pvp.coop.allenKlaar, null, 20000), 'de host ziet dat iedereen geladen is');
  for (const p of allen) await p.evaluate(() => { godMode = true; });
  const xs = await Promise.all(allen.map(p => p.evaluate(() => Math.round(world))));
  meld(new Set(xs).size === R.length, 'ieder een eigen startplek (' + xs.join(', ') + ')');
  await G.page.evaluate(() => { world = -1450; ph = 0; });
  meld(await tot(H.page, () => snakes.some(s => mpcLeeft(s)) && world > -600, null, 8000), 'de slang komt bij de gast, terwijl de host nog bij de start staat');
  meld(await tot(G.page, () => snakes.some(s => s.mpId != null), null, 5000), 'en de gast ziet hem');
  meld(await tot(H.page, () => snakes.some(s => s.mpSoort === 'slang'), null, 3000), 'hij telt mee voor de punten (mpSoort)');
  await H.page.evaluate(() => { world = levelEndX() - 30; ph = 0; });
  await wacht(1500);
  meld(await H.page.evaluate(() => pvp.coop.fase === 'ep'), 'de host alleen bij de fakkels: het level is niet uit');
  // een revive midden in het level, bij de host
  await H.page.evaluate(() => { MPC.reviveNa = 1; world = -6100; ph = 0; });
  if (R[2]) await R[2].page.evaluate(() => { world = -6250; ph = 0; });   // de ton komt bij de levende die het dichtst bij het lijk staat
  await G.page.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  meld(await tot(G.page, () => dead, null, 3000), 'de gast valt');
  meld(await tot(H.page, () => Object.keys(pvp.coop.reviveTon).length > 0, null, 6000), 'er komt een revive-ton');
  const tx = await H.page.evaluate(() => Object.values(pvp.coop.reviveTon)[0].x);
  meld(Math.abs(tx + 6100) <= 330 && await H.page.evaluate(x => !inGap(x), tx), 'de ton staat bij de host, midden in het level (' + Math.round(tx) + ')');
  meld(await tot(G.page, x => tonnen.some(t => t.revive && !t.weg && Math.abs(t.x - x) < 2), tx, 5000), 'de gast ziet de ton ook');
  for (let i = 0; i < 3; i++){ await H.page.evaluate(() => { const t = tonnen.find(t => t.revive && !t.weg); if (t) tonRaak(t, 1, true); }); await wacht(300); }
  meld(await tot(H.page, () => pvp.coop.symbolen.length > 0 || !Object.keys(pvp.coop.doodT).length, null, 4000), 'de ton is stuk en het symbool valt');
  await H.page.evaluate(() => { if (pvp.coop.symbolen.length) world = pvp.coop.symbolen[0].x; });   // met drie kan de tweede gast het al gepakt hebben
  meld(await tot(G.page, () => !dead && lives === 1 && Math.abs(world + 6100) < 600, null, 6000), 'de gast staat op naast de host (' + await G.page.evaluate(() => Math.round(world)) + ')');
  // samen naar de fakkels
  await H.page.evaluate(() => { MPC.reviveNa = 20; });
  const sc1 = await H.page.evaluate(() => { pvp.coop.score += 77; pvp.coop.kills += 3; return pvp.coop.score; });   // een stand die mee moet
  for (const p of allen) await p.evaluate(() => { godMode = true; world = levelEndX() - 30; ph = 0; });
  meld(await tot(H.page, () => pvp.coop.fase === 'klaar' || (pvp.coop.ep.i === 1), null, 5000), 'iedereen bij de fakkels: level 1 is uit');
  meld(await klaar(1) === null, 'level 2 loopt bij iedereen');
  meld(await H.page.evaluate(s => pvp.coop.score >= s && pvp.coop.ep.s0 >= s, sc1), 'de score gaat mee naar level 2 (' + sc1 + ' en ' + await H.page.evaluate(() => pvp.coop.score) + ')');
  // game over in level 2, en R speelt level 2 opnieuw
  await H.page.evaluate(() => pvp.coop.allenKlaar = pvp.coop.allenKlaar);
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  meld(await elk(() => pvp.coop.fase === 'uit' && /Game over/.test(pvpEl('mpeind').textContent) && /level 2/.test(pvpEl('mpeind').textContent), null, 8000) === null, 'iedereen dood: game over in level 2, bij iedereen');
  for (const p of allen) await p.evaluate(() => mpCoopOpnieuw());
  meld(await klaar(1) === null, 'R bij iedereen: level 2 opnieuw');
  // door naar 3 en het slot
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = true; world = levelEndX() - 30; ph = 0; });
  meld(await klaar(2) === null, 'level 3 loopt bij iedereen');
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = true; world = levelEndX() - 30; ph = 0; });
  meld(await elk(() => pvp.coop.fase === 'uit' && /Episode complete/.test(pvpEl('mpeind').textContent), null, 10000) === null, 'na level 3: Episode complete, bij iedereen');
  for (const p of allen) await p.evaluate(() => mpCoopOpnieuw());
  meld(await klaar(0) === null && await H.page.evaluate(() => pvp.coop.score === 0), 'R bij iedereen: weer level 1, score 0');
  for (const r of R){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
}
// de hinderlaag (--hl): The Smugglers' Cellar, level 1 en level 7
// de winkels in de Co-op episode (--winkel): The Smugglers' Cellar vanaf level 3
async function winkelProef(R){
  const [H, G] = R, allen = R.map(r => r.page);
  const elk = async (f, arg, max) => { for (const r of R) if (!await tot(r.page, f, arg, max)) return r.wie; return null; };
  const klaar = i => elk(i => running && !laadWacht && pvp.coop && pvp.coop.ep && pvp.coop.ep.i === i && pvp.coop.fase === 'ep' && level.name.startsWith('Ambush ' + (i + 1)), i, 60000);
  meld(await klaar(2) === null, 'Ambush 3 loopt bij iedereen');
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = true; MPC_LEIBAND.max = 1e9; });
  // de deuren van de winkels: elk tussen twee hinderlagen (of voor de eerste), dus te halen zonder dat de lijn het tegenhoudt
  const deuren = await H.page.evaluate(() => [2, 3, 5].map(i => {
    const lv = COOPEP2_LEVELS[i], b = lv.binnen[0], sc = nowScale();
    const oud = level; level = readLevel(JSON.stringify(lv));
    const dm = stadDeurMaat({ gevel: b.gevel, verdieping: 0 }, sc); level = oud;
    const lijnen = lv.hinderlagen.map(h => h.x);
    return { i, x: dm && Math.round(dm.cx), lijnen, eind: lv.kelder ? lv.kelder.x : lv.ends[0].x };
  }));
  for (const d of deuren) meld(d.x != null && d.x > d.eind && !d.lijnen.some(l => l > d.x - 120 && l < d.x + 120),
    'Ambush ' + (d.i + 1) + ': de winkeldeur op ' + d.x + ', niet op een lijn (' + d.lijnen.join(', ') + ')');
  // goud: een kill geeft iedereen goud
  const g0 = await G.page.evaluate(() => pvp.coop.goud);
  await H.page.evaluate(() => mpcKill({ mpSoort: 'bandiet' }));
  meld(await tot(G.page, g => pvp.coop.goud > g, g0, 4000), 'een kill geeft de gast goud (' + g0 + ' naar ' + await G.page.evaluate(() => pvp.coop.goud) + ')');
  meld(await H.page.evaluate(() => /Gold \d+/.test(pvpEl('pvpscore').textContent)), 'het goud staat in de HUD (' + await H.page.evaluate(() => pvpEl('pvpscore').textContent) + ')');
  // de kist: allebei tegelijk E, maar maar een krijgt het goud, en bij allebei is hij open
  meld(await H.page.evaluate(() => kisten.length === 1), 'er staat een kist in Ambush 3');
  for (const p of allen) await p.evaluate(() => { hinder.stand[0] = 'vrij'; });
  const kg = await Promise.all(allen.map(p => p.evaluate(() => { const k = kisten[0]; world = k.x; ph = k.h; onGround = true; jump = null; leibandOud = null; return pvp.coop.goud; })));
  await wacht(200);
  await Promise.all(allen.map(p => p.evaluate(() => kistE())));
  meld(await elk(() => kisten[0].open, null, 4000) === null, 'de kist is bij iedereen open');
  await wacht(800);
  const kn = await Promise.all(allen.map(p => p.evaluate(() => pvp.coop.goud)));
  const winst = kn.map((g, i) => g - kg[i]);
  meld(winst.filter(w => w === 20).length === 1 && winst.filter(w => w === 0).length === allen.length - 1, 'maar een speler krijgt het goud (' + winst.join(', ') + ')');
  // de eerste hinderlaag als open, zodat de gast bij de deur mag staan
  for (const p of allen) await p.evaluate(() => { hinder.stand[0] = 'vrij'; });
  const dx = deuren[0].x;
  await G.page.evaluate(x => { world = x; ph = 0; onGround = true; jump = null; leibandOud = null; }, dx);
  await wacht(300);
  meld(await G.page.evaluate(() => { const a = binnenEBij(); return a && a.soort === 'in'; }), 'E bij de deur: naar binnen');
  await G.page.evaluate(() => binnenE());
  meld(await tot(G.page, () => !stadTrapFade && binnenBij(world), null, 6000), 'de gast staat in de winkel (' + await G.page.evaluate(() => Math.round(world)) + ')');
  await wacht(500);
  meld(await G.page.evaluate(() => !!binnenBij(world)), 'de lijn van de volgende hinderlaag trekt hem niet terug de straat op');
  await G.page.evaluate(() => { const b = binnenBij(world); world = b.winkel.x + 60; onGround = true; });
  await wacht(200);
  await G.page.evaluate(() => binnenE());
  meld(await G.page.evaluate(() => winkelUIAan && !paused && winkelUIEl.classList.contains('coop')), 'de winkel is open, in Co-op-stijl, en het spel loopt door');
  const knoppen = await G.page.evaluate(() => [...document.querySelectorAll('#wkcoop .wkcoopknop')].map(b => b.id));
  const zou = await G.page.evaluate(() => MPC_WINKEL.filter(q => mpcWinkelVoorMij(q)).length);
  meld(knoppen.length >= zou, 'alles van Survival te koop (' + knoppen.length + ' knoppen: ' + knoppen.join(' ') + ')');
  meld(await G.page.evaluate(() => document.getElementById('wkklaar').style.display === 'none'), 'geen Ready in de episode');
  meld(await H.page.evaluate(() => !paused), 'de host speelt gewoon door');
  await G.page.evaluate(() => { pvp.coop.goud = 300; mpcWinkelToon(); for (const k of ['fc', 'slot', 'leven', 'gif', 'kracht']) document.getElementById('wkc_' + k).click(); });
  const na = await G.page.evaluate(() => ({ g: pvp.coop.goud, fc: pvp.coop.koop.fc, kr: pvp.coop.koop.kracht, rug: RUG_MAX, lv: pvp.levens, gif: gifCarry }));
  meld(na.fc && na.kr && na.rug === 2 && na.lv === 4 && na.gif === 1, 'gekocht: Full Circle, more damage, slot, extra life, gif (' + JSON.stringify(na) + ')');
  await G.page.evaluate(() => winkelUIDicht());
  meld(await G.page.evaluate(() => !winkelUIAan && !paused), 'Close: de winkel dicht');
  // samen naar het eind: level 4, met alles mee
  for (const p of allen) await p.evaluate(() => { hinder.stand = hinder.stand.map(() => 'vrij'); world = levelEndX() - 30; ph = 0; });
  meld(await klaar(3) === null, 'Ambush 4 loopt bij iedereen');
  const mee = await G.page.evaluate(() => ({ g: pvp.coop.goud, fc: pvp.coop.koop.fc, rug: RUG_MAX, rugN: rugSperen.length, lv: pvp.levens, lives, gif: gifCarry }));
  meld(mee.g === na.g + 10 && mee.fc && mee.rug === 2 && mee.rugN === 2 && mee.lv === 4 && mee.lives === 4 && mee.gif === 1,
    'mee naar level 4: goud plus 10, Full Circle, het slot gevuld, 4 levens, het gif (' + JSON.stringify(mee) + ')');
  // de kist van level 4 opent de gast alleen: hij krijgt het goud, de host niets, en bij de host is hij ook open
  const hg = await H.page.evaluate(() => pvp.coop.goud);
  await G.page.evaluate(() => { hinder.stand = hinder.stand.map(() => 'vrij'); const k = kisten[0]; world = k.x; ph = k.h; onGround = true; jump = null; leibandOud = null; });
  await wacht(200);
  await G.page.evaluate(() => kistE());
  meld(await tot(G.page, g => pvp.coop.goud === g + 25, mee.g, 4000) && await tot(H.page, () => kisten[0].open, null, 3000)
       && await H.page.evaluate(g => pvp.coop.goud === g, hg), 'de gast opent de kist alleen: 25 goud voor hem, bij de host open en geen goud');
  await G.page.evaluate(() => { pvp.coop.goud -= 25; });
  // game over in level 4: R geeft het goud van het begin van level 4 terug
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  await G.page.evaluate(() => { pvp.coop.goud = 1; });
  for (const p of allen) await p.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  meld(await elk(() => pvp.coop.fase === 'uit', null, 8000) === null, 'iedereen dood: game over');
  for (const p of allen) await p.evaluate(() => mpCoopOpnieuw());
  meld(await klaar(3) === null, 'R: level 4 opnieuw');
  meld(await G.page.evaluate(g => pvp.coop.goud === g && pvp.coop.koop.fc && RUG_MAX === 2, mee.g), 'het goud en de upgrades van het begin van level 4 (' + await G.page.evaluate(() => pvp.coop.goud) + ')');
  for (const r of R){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
}
async function hlProef(R){
  const [H, G] = R, allen = R.map(r => r.page);
  const elk = async (f, arg, max) => { for (const r of R) if (!await tot(r.page, f, arg, max)) return r.wie; return null; };
  const klaar = i => elk(i => running && !laadWacht && pvp.coop && pvp.coop.ep && pvp.coop.ep.i === i && pvp.coop.fase === 'ep' && level.name.startsWith('Ambush ' + (i + 1)) && pvp.coop.allenKlaar !== false, i, 60000);
  const zet = (p, x) => p.evaluate(x => { world = x; ph = 0; leibandOud = null; }, x);
  const zetAllen = async x => { for (const p of allen) await zet(p, x); };
  const ruim = () => H.page.evaluate(() => { for (const q of MPC_LIJSTEN) if (!q.los) q.l().forEach(o => { o.hp = 0; o.fase = 'dood'; o.doodT0 = 1; }); });
  meld(await klaar(0) === null, 'Ambush 1 loopt bij iedereen');
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = true; });
  // het leiband: de host springt ver vooruit, de gasten staan bij de start
  await zetAllen(-400); await wacht(400);
  await H.page.evaluate(x => { world = x; }, -400 - MPCLEI - 300);
  await wacht(300);
  const lx = await H.page.evaluate(() => Math.round(world));
  meld(lx >= -400 - MPCLEI - 5 && lx <= -400 - MPCLEI + 100, 'het leiband: de host komt niet verder dan ' + MPCLEI + ' van de anderen (' + lx + ')');
  // de lijn: de host loopt alleen naar de hinderlaag
  await zet(H.page, -2600); await wacht(200);
  await H.page.evaluate(() => { leibandOud = null; world = -3500; });
  await wacht(400);
  const hx = await H.page.evaluate(() => Math.round(world));
  meld(hx >= -3000, 'de lijn houdt de host tegen (' + hx + ')');
  await wacht(1200);
  meld(await H.page.evaluate(() => hinder.stand[0] === 'wacht' && !hinder.regie), 'alleen aan de lijn: de hinderlaag wacht op het team');
  // het hele team erbij: de regie begint bij iedereen
  await zetAllen(-3050);
  meld(await elk(() => hinder && hinder.regie && hinder.regie.i === 0, null, 4000) === null, 'iedereen aan de lijn: de regie begint bij iedereen');
  meld(await elk(() => amirVast() && document.getElementById('hlbalken').classList.contains('on'), null, 2000) === null, 'balken in beeld en Amir staat vast');
  meld(await tot(G.page, () => hinderCamX() !== null && Math.abs(camEase - hinderCamX()) < 300, null, 4000), 'de camera van de gast gaat naar het shot (' + await G.page.evaluate(() => hinderCamX()) + ')');
  meld(await tot(H.page, () => bandieten.filter(b => mpcLeeft(b)).length >= 2, null, 4000), 'de bandieten van shot 1 komen binnen');
  meld(await tot(G.page, () => bandieten.length >= 2, null, 4000), 'en de gast ziet ze');
  meld(await elk(() => hinder.stand[0] === 'vecht' && !hinder.regie && !amirVast(), null, 9000) === null, 'na de regie: het gevecht, Amir kan weer');
  meld(await tot(H.page, () => level.spawns.filter(s => s.hl === 0).every(s => s.used), null, 4000), 'alle vijanden van de hinderlaag zijn er');
  await H.page.evaluate(x => { world = x; }, -3050 + MPCLEI + 300); await wacht(300);
  meld(await H.page.evaluate(x => Math.round(world) === x, -3050 + MPCLEI + 300), 'in het gevecht staat het leiband uit (' + await H.page.evaluate(() => Math.round(world)) + ')');
  await zetAllen(-6000); await wacht(300);
  meld(await H.page.evaluate(() => world >= hinderGrens(0) && hinderGrens(0) < -3000), 'in het gevecht schuift de lijn tot achter de verste vijand (' + await H.page.evaluate(() => Math.round(hinderGrens(0))) + ') en niet verder');
  await ruim();
  meld(await elk(() => hinder.stand[0] === 'vrij', null, 6000) === null, 'alle vijanden op: de lijn gaat open bij iedereen');
  await zetAllen(-3500); await wacht(300);
  meld(await H.page.evaluate(() => world < -3400), 'en het team kan verder');
  // de tweede hinderlaag: een dode teamgenoot houdt hem tegen
  await zetAllen(-5700);   // nog buiten MPC_HL.verzamel van de tweede lijn (-6500): anders begint de regie voor de gast dood is
  await G.page.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  await tot(G.page, () => dead, null, 3000);
  await zetAllen(-6450);   // ook de dode: zijn lijk ligt bij de lijn
  await wacht(1500);
  meld(await H.page.evaluate(() => hinder.stand[1] === 'wacht' && !hinder.regie), 'een teamgenoot dood: de hinderlaag wacht op de revive' + (process.env.HL_DBG ? ' ' + await H.page.evaluate(() => JSON.stringify([hinder.stand, !!hinder.regie, world, pvpAnderNu(1)]).slice(0, 300)) + ' gast dood ' + await G.page.evaluate(() => dead) : ''));
  await G.page.evaluate(() => { mpcOpstaan(world, 0); godMode = true; });
  await tot(G.page, () => !dead, null, 3000);
  meld(await tot(H.page, () => hinder.regie && hinder.regie.i === 1, null, 5000), 'weer levend: de regie begint');
  await tot(H.page, () => hinder.stand[1] === 'vecht', null, 10000);
  await tot(H.page, () => level.spawns.filter(s => s.hl === 1).every(s => s.used), null, 4000);
  await ruim();
  meld(await elk(() => hinder.stand[1] === 'vrij', null, 6000) === null, 'de tweede lijn gaat open');
  // elke hinderlaag van level 2 tot en met 6: geen vijand op je bij FIGHT!, en elke vijand te halen vanaf de lijn
  for (let lv = 1; lv <= 5; lv++) if (!process.env.HL_LV || process.env.HL_LV.split(',').includes(String(lv + 1))) await hlLevel(lv);
  // door naar level 7: de kelder
  await H.page.evaluate(() => { pvp.coop.ep.door = true; pvpZend({ t: 'epnaar', i: 6 }); mpCoopStart(6); });
  meld(await klaar(6) === null, 'Ambush 7 loopt bij iedereen');
  await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
  for (const p of allen) await p.evaluate(() => { godMode = true; });
  for (let i = 0; i < 3; i++){
    const x = await H.page.evaluate(i => level.hinderlagen[i].x - 50 + 0, i);
    await zetAllen(x + 50);
    await wacht(200); await zetAllen(x + 50);
    if (shots){                                       // --shots map: de regie in beeld, per shot
      fs.mkdirSync(shots, { recursive: true });
      await tot(H.page, i => hinder.regie && hinder.regie.i === i, i, 8000);
      for (let k = 0; k < 4; k++){ await wacht(k ? 1900 : 1700); await G.page.screenshot({ path: path.join(shots, 'hl7_' + (i + 1) + '_' + (k + 1) + '.png') }); }
    }
    const ok = await tot(H.page, i => hinder.stand[i] === 'vecht', i, 16000);
    if (i === 2) meld(await G.page.evaluate(() => kelderState.fase !== 'dicht'), 'het shot From the cellar laat het luik openvliegen, ook bij de gast');
    await tot(H.page, i => level.spawns.filter(s => s.hl === i).every(s => s.used), i, 6000);
    const hoeveel = await H.page.evaluate(i => level.spawns.filter(s => s.hl === i && s.used).length + ' van ' + level.spawns.filter(s => s.hl === i).length, i);
    meld(ok, 'hinderlaag ' + (i + 1) + ' van level 7: regie en gevecht (' + hoeveel + ' vijanden binnen)');
    await ruim();
    meld(await elk(i => hinder.stand[i] === 'vrij', i, 6000) === null, 'hinderlaag ' + (i + 1) + ' open');
  }
  const kx = await H.page.evaluate(() => level.kelder.x + 120);
  async function hlLevel(lv){
    await H.page.evaluate(lv => { pvp.coop.ep.door = true; pvpZend({ t: 'epnaar', i: lv }); mpCoopStart(lv); }, lv);
    if (await klaar(lv) !== null){ meld(false, 'Ambush ' + (lv + 1) + ' laadt niet'); return; }
    await tot(H.page, () => pvp.coop.allenKlaar, null, 20000);
    for (const p of allen) await p.evaluate(() => { godMode = true; });
    if (process.env.HL_DEUR) console.log(await H.page.evaluate(() => JSON.stringify(level.spawns.filter(s => s.deur).map(s => [s.hl, s.deur.gevel, s.deur.verdieping, Math.round((stadDeurMaat(s.deur, nowScale()) || {}).cx)])) + ' lijnen ' + level.hinderlagen.map(h => h.x)));
    const n = await H.page.evaluate(() => level.hinderlagen.length);
    for (let i = 0; i < n; i++){
      const x = await H.page.evaluate(i => level.hinderlagen[i].x, i);
      await zetAllen(x + 50); await wacht(200); await zetAllen(x + 50);
      await tot(H.page, i => hinder.regie && hinder.regie.i === i, i, 8000);
      await tot(H.page, i => hinder.stand[i] === 'vecht', i, 16000);
      // het moment van FIGHT!: hoe dicht staat de dichtstbijzijnde vijand bij een speler
      const dichtT = await H.page.evaluate(() => { let m = 1e9, wie = ''; const xs = [world].concat(pvpAnderen().map(p => (pvpAnderNu(p) || {}).x).filter(v => v != null));
        for (const q of MPC_LIJSTEN) if (!q.los) for (const o of q.l()) if (mpcLeeft(o)) for (const px of xs) if (Math.abs(o.x - px) < m){ m = Math.abs(o.x - px); wie = q.k + '@' + Math.round(o.x) + (hinder.voor && hinder.voor.has(o) ? ' (al voor de regie)' : ''); } return Math.round(m) + ' ' + wie; });
      const dicht = parseFloat(dichtT);
      meld(dicht > 200, 'Ambush ' + (lv + 1) + ', hinderlaag ' + (i + 1) + ': bij FIGHT! staat geen vijand op je (dichtstbij ' + dichtT + ')');
      await tot(H.page, i => level.spawns.filter(s => s.hl === i).every(s => s.used), i, 8000);
      await wacht(6000);                                 // even laten lopen: wie niet komt, blijft staan
      const ver = await H.page.evaluate(i => { const g = hinderGrens(i), uit = [];
        for (const q of MPC_LIJSTEN) if (!q.los) for (const o of q.l()) if (mpcLeeft(o) && o.x < g - 150) uit.push(q.k + '@' + Math.round(o.x));
        return { g: Math.round(g), uit }; }, i);
      meld(!ver.uit.length, 'Ambush ' + (lv + 1) + ', hinderlaag ' + (i + 1) + ': elke vijand te halen vanaf de lijn (' + ver.g + ')' + (ver.uit.length ? ' buiten: ' + ver.uit.join(' ') : ''));
      await ruim();
      meld(await elk(i => hinder.stand[i] === 'vrij', i, 6000) === null, 'Ambush ' + (lv + 1) + ', hinderlaag ' + (i + 1) + ' open');
    }
  }
  await zet(H.page, kx); await wacht(1500);
  meld(await H.page.evaluate(() => pvp.coop.fase === 'ep'), 'de host alleen bij de kelder: het level is niet uit');
  await zetAllen(kx);
  meld(await elk(() => pvp.coop.fase === 'uit' && /Episode complete/.test(pvpEl('mpeind').textContent), null, 10000) === null, 'het hele team bij de kelder: Episode complete');
  for (const r of R){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
}
const MPCLEI = 1600;   // MPC_LEIBAND.max
// de vaste proef: wat de spelers niet vanzelf doen, stap voor stap, met OK of FOUT per stap. R de ramen (host, gast,
// en met drie spelers gast2), L wat er in de lobby gebeurde
const meld = (ok, t) => { console.log((ok ? 'OK   ' : 'FOUT ') + t); if (!ok) process.exitCode = 1; };
async function proef(R, L){
  const [H, G, G2] = R, drie = !!G2, allen = R.map(r => r.page);
  const elk = async (f, arg, max) => { for (const r of R) if (!await tot(r.page, f, arg, max)) return r.wie; return null; };
  if (L) for (const [ok, t] of L) meld(ok, t);
  const zet = p => p.evaluate(() => { godMode = true; });
  for (const p of allen) await p.evaluate(() => { MPC_LEIBAND.max = 1e9; });   // deze proef zet spelers ver uit elkaar neer: het leiband uit (--hl test het)
  meld(await tot(H.page, () => pvp.coop && pvp.coop.ronde >= 1 && tonnen.some(t => !t.weg), null, 60000), 'ronde 1 loopt en er staat een ton (host)');
  for (const p of allen) await zet(p);
  if (drie){
    const st = await Promise.all(R.map(r => r.page.evaluate(() => ({ mij: pvp.mij, x: Math.round(world), anders: pvpAnderen(), broek: pvp.broek.slice() }))));
    meld(st.every((v, i) => v.mij === i), 'ieder zijn eigen slot (' + st.map(v => v.mij).join(', ') + ')');
    meld(new Set(st.map(v => v.x)).size === 3, 'drie startplekken (' + st.map(v => v.x).join(', ') + ')');
    meld(st.every(v => v.anders.length === 2), 'iedereen ziet de twee anderen (' + st.map(v => v.anders.join('+')).join(', ') + ')');
    meld(st.every(v => v.broek.join() === st[0].broek.join()) && new Set(st[0].broek).size === 3, 'drie verschillende broeken, bij iedereen dezelfde (' + st[0].broek.join(', ') + ')');
    const ziet = await G2.page.evaluate(() => { const g = pvp.anders[1].g; return g && Math.abs(g.x - mpStarts()[1]) < 400; });
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
  // de losse speren van een ander (pvpLosZend, pvpLosTeken): een speer die de gast liet liggen zien de anderen ook, en weer weg als hij weg is
  const lsX = await G.page.evaluate(() => { const x = Math.round(world) - 200; losseSperen.push({ x, h: terrainH(x), zij: 1, soort: 'eigen', blauw: false, wiebel: 0 }); return x; });
  meld(await tot(H.page, v => ((pvp.anders[1] || {}).ls || []).some(q => q[0] === v), lsX, 3000), 'de host ziet de losse speer van de gast');
  if (drie) meld(await tot(G2.page, v => ((pvp.anders[1] || {}).ls || []).some(q => q[0] === v), lsX, 3000), 'en de tweede gast (doorgestuurd door de host)');
  await G.page.evaluate(x => { const i = losseSperen.findIndex(s => s.x === x); if (i >= 0) losseSperen.splice(i, 1); }, lsX);
  meld(await elk(v => pvp.mij === 1 || !((pvp.anders[1] || {}).ls || []).some(q => q[0] === v), lsX, 3000) === null, 'opgeraapt: bij iedereen weer weg');
  // de versie van de map (MPC_VERSIE): iedereen dezelfde, met de fakkels aan de muren, en om de drie rondes een andere
  const versie = () => Promise.all(R.map(r => r.page.evaluate(() => mpcVersieNu + ':' + (level.fakkels || []).length)));
  const v0 = await versie();
  meld(new Set(v0).size === 1 && /^(dag:0|avond:0|(nacht|donker):[1-9]\d*)$/.test(v0[0]), 'iedereen dezelfde versie van de map (' + v0.join(' ') + ')');
  await H.page.evaluate(() => { const C = pvp.coop; for (const q of MPC_LIJSTEN) mpcZet(q, []); C.rij = []; C.ronde = 3; C.fase = 'wacht'; C.klok = 0; });
  // een map met een vaste versie (Ishmul speelt altijd overdag) wisselt niet: dan blijft het bij iedereen die versie
  const vast = await H.page.evaluate(() => (mpcKaart().versies || []).length === 1);
  if (vast){ await H.page.waitForTimeout(4000); meld((await versie()).every(v => v.split(':')[0] === v0[0].split(':')[0]), 'ronde 4: de map heeft een vaste versie en blijft hem houden'); }
  else meld(await elk(v => mpcVersieNu !== v, v0[0].split(':')[0], 4000) === null, 'ronde 4: een andere versie van de map, bij iedereen');
  const v1 = await versie();
  meld(new Set(v1).size === 1, 'en weer bij iedereen dezelfde (' + v1.join(' ') + ')');
  // de winkel (stuk 3): de ronde is op na winkelNa rondes, iedereen naar de winkelkamer, kopen, Ready en terug
  const goudVoor = await Promise.all(R.map(r => r.page.evaluate(() => pvp.coop.goud)));
  await H.page.evaluate(() => { const C = pvp.coop; C.rij = []; C.fase = 'golf'; C.ronde = pvp.regels.coop.winkelNa; for (const q of MPC_LIJSTEN) mpcZet(q, []); });
  meld(await elk(() => pvp.coop.inWinkel && !stadTrapFade && !!binnenBij(world), null, 12000) === null, 'na winkelNa rondes: iedereen in de winkelkamer');
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
  if (args.includes('--ep') || args.includes('--hl') || args.includes('--winkel'))
    await H.page.evaluate(k => { window.__ep = true; window.__epKaart = k; }, args.includes('--hl') ? 'b0' : args.includes('--winkel') ? 'b2' : '0');
  if (opt('--kaart', null)) await H.page.evaluate(k => { window.__kaart = k; }, opt('--kaart', null));
  await H.page.evaluate(soorten => {
    mpWijzig(() => {
      pvp.inst.modus = window.__duel ? 'duel' : window.__ep ? 'ep' : 'coop';
      if (window.__ep) pvp.inst.kaart = window.__epKaart;
      else if (window.__kaart && pvp.inst.modus === 'coop') pvp.inst.kaart = window.__kaart;
      Object.assign(pvp.inst.coop, { start: 2, erbij: 1, pauze: 5 });
      for (const q of MP_SOORTEN) pvp.inst.coop.vij[q.k] = soorten ? (soorten.includes(q.k) ? (q.var ? 'beide' : 'aan') : 'uit') : (q.var ? 'beide' : 'aan');
    });
  }, soorten ? soorten.split(',') : null);
  await H.page.waitForTimeout(400);
  if (G2){
    lobby.push([await H.page.evaluate(() => pvp.spelers.join() === '0,1,2'), 'de host heeft drie spelers in de lobby']);
    const br = await Promise.all(ramen.map(r => r.page.evaluate(() => pvp.broek.slice(0, 3).join())));
    lobby.push([br.every(b => b === br[0]) && new Set(br[0].split(',')).size === 3, 'drie broekkleuren, bij iedereen dezelfde (' + br[0] + ')']);
    const kaart = () => [...pvpEl('mpteam').querySelectorAll('.mpkaart')].map(k => k.textContent).join(' | ');
    lobby.push([await G2.page.evaluate(() => pvpEl('mpteam').querySelectorAll('.mpkaart').length === 3 && /Host/.test(pvpEl('mpteam').textContent)), 'de tweede gast ziet iedereen in de lobby als kaartje (' + await G2.page.evaluate(kaart) + ')']);
    await G.page.evaluate(() => { const i = pvpEl('mpnaam'); i.value = 'Kofi'; i.dispatchEvent(new Event('input')); });
    await H.page.evaluate(() => { const i = pvpEl('mpnaam'); i.value = 'Zola'; i.dispatchEvent(new Event('input')); });
    await wacht(500);
    lobby.push([await G2.page.evaluate(() => pvp.naam[1] === 'Kofi' && pvp.naam[0] === 'Zola' && /Kofi/.test(pvpEl('mpteam').textContent)), 'een naam komt bij iedereen aan, ook via de host (' + await G2.page.evaluate(kaart) + ')']);
    await H.page.evaluate(() => { const c = window.__maakConn('g9'); pvpNieuweGast(c); window.__vierde = c; });
    await wacht(700);
    lobby.push([await H.page.evaluate(() => pvp.spelers.length === 3 && !window.__vierde.open), 'een vierde speler wordt geweigerd (vol)']);
    await G.page.evaluate(() => pvpEl('mpready').click());
    await H.page.waitForTimeout(300);
    lobby.push([await H.page.evaluate(() => pvpEl('mpstart').disabled && /1 of 2/.test(pvpEl('mpstartuitleg').textContent)), 'een gast Ready: Start mag nog niet (' + await H.page.evaluate(() => pvpEl('mpstartuitleg').textContent) + ')']);
    lobby.push([await G2.page.evaluate(() => !!pvpEl('mpteam').querySelector('.mpkaart.klaar')), 'de andere gast ziet op het kaartje wie Ready is']);
    await H.page.evaluate(() => mpWijzig(() => { pvp.inst.modus = 'duel'; }));
    await H.page.waitForTimeout(200);
    lobby.push([await H.page.evaluate(() => pvpEl('mpstart').disabled && /two players/.test(pvpEl('mpstartuitleg').textContent)), 'Duel met drie spelers mag niet']);
    await H.page.evaluate(() => mpWijzig(() => { pvp.inst.modus = window.__ep ? 'ep' : 'coop'; if (window.__ep) pvp.inst.kaart = window.__epKaart; else if (window.__kaart) pvp.inst.kaart = window.__kaart; }));
    await H.page.waitForTimeout(200);
    for (const r of [G, G2]) await r.page.evaluate(() => pvpEl('mpready').click());
  } else await G.page.evaluate(() => pvpEl('mpready').click());
  await H.page.waitForTimeout(300);
  // samen beginnen: de laatste gast laadt kunstmatig lang (mpLaadVast blijft waar), dan moet de host op het laadscherm wachten
  const traag = ramen[ramen.length - 1];
  await traag.page.evaluate(() => { window.__houd = true; const o = mpLaadVast; mpLaadVast = () => window.__houd || o(); });
  if (args.includes('--winkeleerst')) await H.page.evaluate(() => { pvp.inst.coop.winkelEerst = true; });   // Start in the shop
  const start = await H.page.evaluate(() => { const ok = !pvpEl('mpstart').disabled; mpStart(); return ok; });
  lobby.push([start, 'iedereen Ready: Start mag']);
  console.log('Start mocht: ' + start);
  await tot(H.page, () => /Waiting/.test(document.getElementById('laadtel').textContent), null, 90000);
  await wacht(3000);
  const hw = await H.page.evaluate(() => ({ w: laadWacht, t: document.getElementById('laadtel').textContent }));
  meld(hw.w && /Waiting/.test(hw.t), 'een gast laadt nog: de host blijft op het laadscherm (' + hw.t + ')');
  await traag.page.evaluate(() => { window.__houd = false; });
  let los = true;
  for (const r of ramen) los = await tot(r.page, () => running && !laadWacht, null, 90000) && los;
  meld(los, 'de gast is geladen: iedereen los');
  if (args.includes('--winkeleerst')){
    for (const r of ramen) meld(await tot(r.page, () => pvp.coop.inWinkel && binnenBij(world), null, 10000), r.wie + ': Start in the shop, ook ' + r.wie + ' staat in de winkel');
  }
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
  if (args.includes('--winkel')){ await winkelProef(ramen); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  if (args.includes('--hl')){ await hlProef(ramen); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  if (args.includes('--ep')){ await epProef(ramen); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
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
