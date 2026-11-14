#!/usr/bin/env node
'use strict';
// De multiplayertest: speelt Co-op Survival met twee vensters in Chromium, zonder PeerJS. Elk venster krijgt een
// nagebootste verbinding (een conn met send en on), en Node geeft de berichten door. Daarna lopen twee simpele
// spelers naar de dichtstbijzijnde vijand en steken. Meldt per venster de fouten in de console, en wat het spel deed:
// de ronde, de score, de vijanden bij de host en bij de gast, doden en revives.
//
//   node tools/mptest.js                 een potje van 90 s, alle vijanden aan (Both)
//   node tools/mptest.js --duur 40       korter
//   node tools/mptest.js --shots map     elke 10 s een schermafdruk van allebei
//   node tools/mptest.js --soorten bandiet,slang   alleen deze soorten aan
//   node tools/mptest.js --stil          de spelers doen niets (dan gaan ze dood: game over en de revive)
//   node tools/mptest.js --sterf gast   die speler is meteen dood: de revive-ton, het symbool en het opstaan
//   node tools/mptest.js --taai          de spelers kunnen niet dood (godMode): om lang door te spelen
//   node tools/mptest.js --proef         de vaste proef: een ton breken als gast, een treffer van de gast, de winkel, game over, R, Escape
//   node tools/mptest.js --elk           elke soort makkelijk en moeilijk neerzetten, de gast raakt ze: fouten in het tekenen
//   node tools/mptest.js --debug         elke 4 s de stand van allebei: plek, levens en de vijanden
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
// de vaste proef: wat de spelers niet vanzelf doen, stap voor stap, met OK of FOUT per stap
async function proef(H, G){
  const meld = (ok, t) => { console.log((ok ? 'OK   ' : 'FOUT ') + t); if (!ok) process.exitCode = 1; };
  const zet = p => p.evaluate(() => { godMode = true; });
  meld(await tot(H.page, () => pvp.coop && pvp.coop.ronde >= 1 && tonnen.some(t => !t.weg), null, 60000), 'ronde 1 loopt en er staat een ton (host)');
  await zet(H.page); await zet(G.page);
  meld(await tot(G.page, () => tonnen.some(t => !t.weg && t.mpId != null)), 'de ton staat ook bij de gast');
  const voor = await G.page.evaluate(() => ({ g: pvp.coop.goud, k: hppotionCarry, id: tonnen.find(t => !t.weg).mpId }));
  for (let i = 0; i < 3; i++){ await G.page.evaluate(id => tonRaak(tonnen.find(t => t.mpId === id), 1, true), voor.id); await wacht(400); }
  meld(await tot(H.page, id => tonnen.find(t => t.mpId === id).weg, voor.id, 5000), 'drie treffers van de gast breken de ton bij de host');
  meld(await tot(G.page, id => tonnen.find(t => t.mpId === id).weg, voor.id, 5000), 'en bij de gast');
  meld(await tot(G.page, v => pvp.coop.goud > v.g || hppotionCarry > v.k, voor, 5000), 'de gast krijgt wat erin zat (goud of een kalebas)');
  meld(await tot(G.page, () => MPC_LIJSTEN.some(q => !q.los && q.l().some(o => o.mpId != null && mpcLeeft(o))), null, 40000), 'er is een vijand bij de gast');
  const kills = await H.page.evaluate(() => pvp.coop.kills);
  for (let i = 0; i < 12; i++){
    await G.page.evaluate(() => {
      const q = MPC_LIJSTEN.find(q => !q.los && q.l().some(o => o.mpId != null && mpcLeeft(o)));
      if (!q) return;
      const o = q.l().find(o => o.mpId != null && mpcLeeft(o));
      if (q.k === 'snakes' || q.k === 'scorps') enemyTakeHit(o);
      else if (q.k === 'bandieten') hitBandiet(o); else if (q.k === 'hyenas') hitHyena(o); else if (q.k === 'kooimannen') hitKooiman(o);
      else if (q.k === 'meelmannen') hitMeelman(o); else if (q.k === 'zweepmannen') hitZweepman(o); else if (q.k === 'kruisbogen') hitKruisboog(o, 'steek');
      else if (q.k === 'schildmannen') hitSchildman(o, 'steek'); else if (q.k === 'fosforSlangen') fosforRaak(o); else if (q.k === 'goudapen') gaapDood(o, false);
      else enemyTakeHit(o);
    });
    await wacht(600);
    if (await H.page.evaluate(k => pvp.coop.kills > k, kills)) break;
  }
  meld(await H.page.evaluate(k => pvp.coop.kills > k, kills), 'treffers van de gast doden een vijand bij de host (kills ' + kills + ' -> ' + await H.page.evaluate(() => pvp.coop.kills) + ')');
  meld(await tot(G.page, k => pvp.coop.kills > k, kills, 3000), 'en de gast ziet de score mee');
  // de winkel (stuk 3): de ronde is op na winkelNa rondes, allebei naar de winkelkamer, kopen, Ready en terug
  const goudVoor = await G.page.evaluate(() => pvp.coop.goud);
  await H.page.evaluate(() => { const C = pvp.coop; C.rij = []; C.fase = 'golf'; C.ronde = pvp.regels.coop.winkelNa; for (const q of MPC_LIJSTEN) mpcZet(q, []); });
  meld(await tot(H.page, () => pvp.coop.inWinkel && !stadTrapFade && !!binnenBij(world), null, 6000), 'na winkelNa rondes: de host in de winkelkamer');
  meld(await tot(G.page, () => pvp.coop.inWinkel && !stadTrapFade && !!binnenBij(world), null, 6000), 'en de gast ook');
  meld(await tot(G.page, v => pvp.coop.goud >= v + 5, goudVoor, 3000), 'de gast krijgt het goud van de overleefde ronde (' + goudVoor + ' -> ' + await G.page.evaluate(() => pvp.coop.goud) + ')');
  const scherm = await G.page.evaluate(() => { world = MPC_WINKEL_KAMER.toonbank + 40; onGround = true; jump = null; binnenE();
    return winkelUIAan && winkelUIEl.classList.contains('coop') && document.querySelectorAll('#wkcoop button').length === MPC_WINKEL.length; });
  meld(scherm, 'E bij de toonbank: het winkelscherm met de prijslijst van Co-op');
  if (shots){ fs.mkdirSync(shots, { recursive: true }); await G.page.screenshot({ path: path.join(shots, 'winkel_scherm.png') }); await H.page.screenshot({ path: path.join(shots, 'winkel_kamer_host.png') }); }
  const hGoud = await H.page.evaluate(() => pvp.coop.goud);
  const koop = await G.page.evaluate(() => {
    pvp.coop.goud = 300; const klik = k => document.getElementById('wkc_' + k).click();
    const voorFc = fcModus(); klik('kracht'); const zonder = !pvp.coop.koop.kracht;
    klik('fc'); klik('rond'); klik('kracht'); klik('slot'); klik('leven'); klik('geef');
    return { voorFc, zonder, fc: fcModus(), rug: RUG_MAX, levens: pvp.levens, lives, goud: pvp.coop.goud };
  });
  meld(koop.voorFc === null && koop.zonder, 'zonder Full Circle geen upgrade');
  meld(koop.fc === 'kracht_rond', 'Full Circle met allebei de upgrades (' + koop.fc + ')');
  meld(koop.rug === 2 && koop.levens === 4, 'het extra speerslot en een extra leven (rug ' + koop.rug + ', levens ' + koop.levens + ')');
  meld(koop.goud === 300 - 30 - 50 - 50 - 45 - 60 - 5, 'de prijzen kloppen (over: ' + koop.goud + ')');
  meld(await tot(H.page, v => pvp.coop.goud === v + 5, hGoud, 3000), 'Give 5 gold komt aan bij de host');
  await G.page.evaluate(() => document.getElementById('wkklaar').click());
  meld(await G.page.evaluate(() => !winkelUIAan && pvp.coop.mijnKlaar), 'Ready bij de gast: het scherm dicht');
  meld(await tot(H.page, () => pvp.coop.anderKlaar && pvp.coop.inWinkel, null, 3000), 'de host hoort het, en wacht nog op zichzelf');
  await H.page.evaluate(() => mpcKlaarDruk());
  meld(await tot(H.page, () => !pvp.coop.inWinkel && !stadTrapFade && !binnenBij(world) && pvp.coop.fase === 'wacht' && wapenrekken[0].n === pvp.regels.coop.rek, null, 6000), 'allebei Ready: de host weer op straat, het rek vol, de pauze loopt');
  meld(await tot(G.page, () => !pvp.coop.inWinkel && !stadTrapFade && !binnenBij(world), null, 6000), 'en de gast ook');
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
    return { soort, voor: [hp0[0], voor.hp], achter: [hp0[1], achter.hp] };
  });
  meld(rond.soort === 'rond' && rond.voor[1] < rond.voor[0] && rond.achter[1] < rond.achter[0],
       'Full Circle rondom raakt voor en achter (' + JSON.stringify(rond) + ')');
  // allebei dood: game over en het eindscherm
  for (const r of [H, G]) await r.page.evaluate(() => { godMode = false; invuln = 0; lives = 1; hurtPlayer(true); });
  meld(await tot(H.page, () => pvp.coop.fase === 'uit' && pvpEl('mpeind').classList.contains('on'), null, 5000), 'allebei dood: game over, het eindscherm bij de host');
  meld(await tot(G.page, () => pvp.coop.fase === 'uit' && pvpEl('mpeind').classList.contains('on'), null, 5000), 'en bij de gast');
  console.log('     ' + await G.page.evaluate(() => pvpEl('mpeind').innerText.replace(/\n+/g, ' | ')));
  for (const r of [H, G]) await r.page.evaluate(() => opnieuw());
  meld(await tot(H.page, () => pvp.coop && pvp.coop.fase !== 'uit' && !dead && !pvpEl('mpeind').classList.contains('on'), null, 8000), 'R bij allebei: een nieuw potje (host)');
  meld(await tot(G.page, () => pvp.coop && pvp.coop.fase !== 'uit' && !dead && !pvpEl('mpeind').classList.contains('on'), null, 8000), 'en bij de gast');
  await H.page.evaluate(() => toMenu());
  meld(await tot(H.page, () => pvp && pvp.fase === 'lobby' && !pvp.coop && pvpEl('menuPvp').classList.contains('lobby'), null, 5000), 'Escape: de host in de lobby');
  meld(await tot(G.page, () => pvp && pvp.fase === 'lobby' && !pvp.coop && pvpEl('menuPvp').classList.contains('lobby'), null, 5000), 'en de gast ook, de verbinding open');
  for (const r of [H, G]){ if (r.fouten.size){ console.log(r.wie + ' fouten:'); for (const f of r.fouten) console.log('  ' + f); } }
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
  for (const wie of ['host', 'gast']){
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await ctx.newPage();
    const fouten = new Set();
    page.on('pageerror', e => fouten.add('fout: ' + e.message + (e.stack ? ' @ ' + (e.stack.split('\n')[1] || '').trim() : '')));
    page.on('console', m => { if (m.type() === 'error') fouten.add('console: ' + m.text().slice(0, 300)); });
    page.on('response', r => { if (r.status() >= 400) fouten.add(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+\//, '')); });
    ramen.push({ wie, page, fouten, bus: [] });
  }
  // de nagebootste verbinding: send gaat via Node naar het andere venster
  for (const r of ramen){
    const ander = ramen.find(q => q !== r);
    await r.page.exposeFunction('__mpZend', s => { ander.bus.push(s); });
  }
  for (const r of ramen){
    await r.page.goto(url);
    await r.page.waitForFunction(() => typeof pvpVerbonden === 'function' && typeof mpCoopStart === 'function');
  }
  await Promise.all(ramen.map(r => r.page.waitForTimeout(1500)));
  for (const r of ramen){
    await r.page.evaluate(host => {
      const h = {};
      window.__conn = { open: true, relay: false, send: o => window.__mpZend(JSON.stringify(o)),
                        on: (k, f) => { h[k] = f; }, close: () => {} };
      window.__ontvang = s => { if (h.data) h.data(JSON.parse(s)); };
      showMenu('menuPvp');
      pvpVerbonden(window.__conn, host);
    }, r.wie === 'host');
  }
  // berichten doorgeven, zo vaak als het kan
  let loopt = true;
  const pomp = async r => {
    while (loopt){
      if (r.bus.length){
        const rij = r.bus.splice(0);
        await r.page.evaluate(rij => { for (const s of rij) window.__ontvang(s); }, rij).catch(() => {});
      } else await new Promise(ok => setTimeout(ok, 8));
    }
  };
  const pompen = ramen.map(pomp);
  const [H, G] = ramen;
  await H.page.evaluate(soorten => {
    mpWijzig(() => {
      pvp.inst.modus = 'coop';
      Object.assign(pvp.inst.coop, { start: 2, erbij: 1, pauze: 5 });
      for (const q of MP_SOORTEN) pvp.inst.coop.vij[q.k] = soorten ? (soorten.includes(q.k) ? (q.var ? 'beide' : 'aan') : 'uit') : (q.var ? 'beide' : 'aan');
    });
  }, soorten ? soorten.split(',') : null);
  await H.page.waitForTimeout(300);
  await G.page.evaluate(() => pvpEl('mpready').click());
  await H.page.waitForTimeout(300);
  const start = await H.page.evaluate(() => { const ok = !pvpEl('mpstart').disabled; mpStart(); return ok; });
  console.log('Start mocht: ' + start);
  // de spelers: naar de dichtstbijzijnde vijand lopen en steken; R na game over
  const speler = ([stil, taai, sterf]) => {
    if (!pvp || !pvp.coop || !running) return;
    if (taai && pvp.coop.fase !== 'uit' && !dead) godMode = true;
    if (sterf && !window.__gestorven && pvp.coop.ronde >= 1){ window.__gestorven = true; godMode = false; lives = 1; hurtPlayer(true); }
    const lijst = MPC_LIJSTEN.filter(q => !q.los).flatMap(q => q.l()).filter(o => mpcLeeft(o));
    keys['ArrowLeft'] = keys['ArrowRight'] = false;
    if (stil || dead) return;
    // eerst de revive: het symbool pakken, of de revive-ton breken
    const S = pvp.coop.symbool, rt = tonnen.find(t => t.revive && !t.weg);
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
  if (args.includes('--elk')){ await elk(H, G); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  if (args.includes('--proef')){ await proef(H, G); loopt = false; await Promise.all(pompen); await browser.close(); srv.close(); return; }
  const t0 = Date.now();
  let volgendeShot = 0, nShot = 0, doden = { host: 0, gast: 0 }, wasDood = { host: false, gast: false }, revives = { host: 0, gast: 0 };
  while ((Date.now() - t0) / 1000 < duur){
    await Promise.all(ramen.map(r => r.page.evaluate(speler, [stil, args.includes('--taai'), opt('--sterf', '') === r.wie]).catch(e => r.fouten.add('speler: ' + e.message))));
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
  loopt = false;
  await Promise.all(pompen);
  for (const r of ramen){
    console.log('\n== ' + r.wie + ' ==');
    console.log(JSON.stringify(r.laatst));
    console.log('doden: ' + doden[r.wie] + ', weer op: ' + revives[r.wie]);
    if (r.fouten.size){ console.log('fouten:'); for (const f of r.fouten) console.log('  ' + f); }
    else console.log('geen fouten');
  }
  await browser.close(); srv.close();
})();
