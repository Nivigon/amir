// Proefrit voor de idle met de stokken op de schouders (STOK.idle): een vlak level met stokken, stilstaan, kijken of de
// idle na STOK.idle.wacht begint en rondloopt, dan lopen (terug naar de ren) en een slag (de idle stopt).
// node tools/stok_idle_test.js [map voor de afdrukken]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const shots = process.argv[2] || null;
const srv = http.createServer((q, r) => {
  const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e){ r.writeHead(404); r.end(); return; }
    const t = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json', '.mp3': 'audio/mpeg', '.webp': 'image/webp', '.jpg': 'image/jpeg' }[path.extname(f)] || 'application/octet-stream';
    r.writeHead(200, { 'Content-Type': t }); r.end(d); });
}).listen(0, async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const fouten = new Set();
  page.on('pageerror', e => fouten.add('fout: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') fouten.add('console: ' + m.text()); });
  page.on('response', r => { if (r.status() >= 400) fouten.add(r.status() + ' ' + r.url()); });
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof TEST_74 !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    const lv = JSON.parse(JSON.stringify(TEST_74));
    delete lv.stokKeuze; delete lv.onstKeuze; lv.onsterfelijk = true; lv.tips = []; lv.spawns = [];
    setLevel(0, [lv]); beginPlay('medium');
  });
  await page.waitForFunction(() => running && stokAan() && stokBank.idle && stokBank.idle.every(i => i.complete), null, { timeout: 30000 });
  await page.waitForFunction(() => !laadWacht, null, { timeout: 90000 });
  const snap = async n => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, n + '.png') }); } };
  const stand = () => page.evaluate(() => stokSetNu + ':' + stokFrameNu + ' t=' + stokIdleT.toFixed(2));
  const log = [];
  log.push('begin ' + await stand());
  await page.waitForTimeout(600); log.push('0,6 s ' + await stand()); await snap('0_staan');
  for (let i = 0; i < 6; i++){ await page.waitForTimeout(400); log.push('idle ' + await stand()); await snap('1_idle_' + i); }
  await page.keyboard.down('ArrowLeft'); await page.waitForTimeout(400); log.push('lopen ' + await stand()); await snap('2_lopen');
  await page.keyboard.up('ArrowLeft'); await page.waitForTimeout(1600); log.push('weer stil ' + await stand());
  await page.keyboard.press('f'); await page.waitForTimeout(100); log.push('slag ' + await stand());
  console.log(log.join('\n'));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
