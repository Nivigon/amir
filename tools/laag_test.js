// Proefrit voor de lage slag met de stokken (gebukt plus aanval, STOK.laag): een vlak level met stokken, een slang en
// een bandiet voor Amir, bukken, slaan, en schermafdrukken van het verloop. node tools/laag_test.js [map voor de afdrukken]
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
    delete lv.stokKeuze; delete lv.onstKeuze; lv.onsterfelijk = true; lv.tips = [];
    lv.spawns = [{ x: -230, k: 'groen' }, { x: -900, k: 'bandiet' }];
    setLevel(0, [lv]); beginPlay('medium');
  });
  await page.waitForFunction(() => running && stokAan() && stokBank.laag.every(i => i.complete), null, { timeout: 30000 });
  await page.waitForFunction(() => !laadWacht, null, { timeout: 90000 });
  await page.waitForTimeout(1500);
  const snap = async n => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, n + '.png') }); } };
  await snap('0_staan');
  await page.keyboard.down('ArrowDown');
  await page.waitForTimeout(500);
  await snap('1_gebukt');
  const slangVoor = await page.evaluate(() => { const s = snakes[0]; if (s){ s.x = playerX() - 150; s.vx = 0; } return snakes.map(s => s.state + '@' + Math.round(s.x - playerX())); });
  await page.keyboard.press('f');
  const log = [];
  for (let i = 0; i < 16; i++){
    await page.waitForTimeout(80);
    log.push(await page.evaluate(() => [atkStok, atkFrame, +duckT.toFixed(2), Math.round(world)].join(' ')));
    if (i % 2 === 0) await snap('2_slag_' + String(i).padStart(2, '0'));
  }
  await page.keyboard.up('ArrowDown');
  await page.waitForTimeout(600);
  await snap('3_na');
  console.log(log.join('\n'));
  console.log('slang voor:', slangVoor, 'na:', await page.evaluate(() => snakes.map(s => s.state)), 'ladingen:', await page.evaluate(() => swLading));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
