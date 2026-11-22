// Proefrit voor Silver Pride (ZH) in Test 91: laadt het level, drukt G en maakt schermafdrukken van het neerleggen, het
// pulseren, de uitbarsting en de brul van Tau. node tools/zilverhart_test.js [map voor de afdrukken]
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
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof STOK_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => { setLevel(STOK_LEVELS.indexOf(TEST_91), STOK_LEVELS); beginPlay('medium'); });
  await page.waitForFunction(() => !laadWacht && running && zhDummy, null, { timeout: 120000 });
  await page.waitForTimeout(2000);
  await page.evaluate(() => { world = -300; facing = -1; });
  await page.waitForTimeout(800);
  let n = 0;
  const schiet = async () => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, 's' + String(n++).padStart(3, '0') + '.png') }); } };
  await schiet();
  for (let ronde = 0; ronde < 2; ronde++){
    await page.keyboard.press('g');
    for (let i = 0; i < 30; i++){ await page.waitForTimeout(i >= 14 && i <= 20 ? 60 : 220); if (ronde === 0) await schiet(); }
    console.log('ronde', ronde, await page.evaluate(() => ({ lijst: zhLijst.length, dummy: zhDummy && { dood: zhDummy.dood, x: Math.round(zhDummy.x) } })));
    await page.waitForTimeout(6500);
    console.log('na het omvallen', await page.evaluate(() => ({ dood: zhDummy.dood })));
  }
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
