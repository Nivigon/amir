// Kivuli in de winkel van Co-op Survival: speelt een bezoek af en maakt schermafbeeldingen (zie "Kivuli" in notities/multiplayer.md).
// node tools/kivuli_test.js <versie 1|2|3> <duka 1|2> [uitmap]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..'), V = +(process.argv[2] || 1), DK = +(process.argv[3] || 1), UIT = process.argv[4] || '/tmp/kivuli';
fs.mkdirSync(UIT, { recursive: true });
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e){ r.writeHead(404); r.end(); return; } r.writeHead(200, {'Content-Type': {'.html':'text/html','.js':'text/javascript','.png':'image/png','.json':'application/json','.webp':'image/webp','.jpg':'image/jpeg','.woff2':'font/woff2','.mp3':'audio/mpeg'}[path.extname(f)]||'application/octet-stream'}); r.end(d); }); })
.listen(0, async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('pageerror', e => console.log('fout:', e.message));
  const foto = async (n) => { await p.screenshot({ path: UIT + '/v' + V + '_' + n + '.png' }); console.log(n, await p.evaluate(() => JSON.stringify({ f: kiv.fase, a: kiv.anim, x: Math.round(kiv.x || 0), klok: kiv.klok && +kiv.klok.toFixed(1), voorraad: kiv.voorraad, duka: kiv.dukaFase, uit: pvp.coop.inWinkel }))); };
  await p.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await p.waitForFunction(() => typeof mpSoloOpen === 'function'); await p.waitForTimeout(1500);
  await p.evaluate(() => mpSoloOpen()); await p.waitForTimeout(800);
  await p.evaluate(([V, DK]) => { Object.assign(pvp.inst.coop, { winkelEerst: true, goud0: 200, kivuli: V, kivVaak: 1, kivDuka: DK }); mpStart(); }, [V, DK]);
  await p.waitForFunction(() => pvp && pvp.coop && running && !laadWacht && pvp.coop.inWinkel, null, { timeout: 120000 });
  await p.evaluate(() => { const h = document.getElementById('hint'); if (h) h.style.display = 'none'; });
  await p.waitForTimeout(3500); await foto('1_binnen');
  await p.waitForTimeout(4000); await foto('2_wacht');
  if (V === 2){ await p.evaluate(() => { world = kiv.w.x + KIV.plek[2].nadert - 90; }); await p.waitForTimeout(500); await foto('3a_deur'); await p.waitForTimeout(3000); await foto('3_komt'); await p.waitForTimeout(5000); await foto('3b_leunt'); }
  await p.evaluate(() => { world = kiv.x + (kiv.v === 2 ? -130 : 130); facing = kiv.v === 2 ? 1 : -1; });
  await p.waitForTimeout(400);
  console.log('E', await p.evaluate(() => JSON.stringify({ e: binnenEBij(), og: onGround, kan: kivKanPraat(), hier: kivHier(), aan: kiv.aan, kw: !!kiv.w, uit: kiv.uit, weg: kiv.weg, fase: kiv.fase, w: world })));
  await p.evaluate(() => binnenE());
  await p.waitForTimeout(2500); await foto('4_jasopen');
  await p.evaluate(() => { const k = kiv.voorraad[1] || kiv.voorraad[0]; mpcWinkelKoop(MPC_WINKEL.find(q => q.k === k)); });
  await p.waitForTimeout(1200); await foto('5_gekocht');
  await p.evaluate(() => winkelUIDicht()); await p.waitForTimeout(2200); await foto('6_dicht');
  await p.evaluate(() => { kiv.klok = 0.5; }); await p.waitForTimeout(2000); await foto('7_draai');
  await p.waitForTimeout(3000); await foto('8_weg');
  await p.waitForTimeout(4000); await foto('9_duka');
  await p.waitForTimeout(3500); await foto('10_daarna');
  await b.close(); srv.close();
});
