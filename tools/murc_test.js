// Proefrit voor Murghtaan 2 (de charge): laadt het level, zet Amir in de arena, volgt de toestanden van Murghtaan,
// maakt schermafdrukken en raakt hem daarna vijf keer. node tools/murc_test.js [map voor de afdrukken]
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
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof MUR_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => { setLevel(1, MUR_LEVELS); beginPlay('medium'); });
  await page.waitForFunction(() => murcMeta && murg, null, { timeout: 30000 });
  await page.waitForTimeout(1500);
  await page.evaluate(() => { world = -2000; });
  const log = [];
  let n = 0;
  for (let i = 0; i < 60; i++){
    await page.waitForTimeout(250);
    const st = await page.evaluate(() => ({ s: murg.state, set: murg.set, f: murg.frame, x: Math.round(murg.x), face: murg.face, amir: Math.round(playerX()) }));
    log.push(st);
    if (shots && i % 2 === 0){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, 's' + String(n++).padStart(3, '0') + '.png') }); }
  }
  const toest = []; for (const l of log) if (!toest.length || toest[toest.length - 1].s !== l.s) toest.push(l);
  console.log(toest.map(l => l.s + '@' + l.x + (l.face === 1 ? '>' : '<')).join(' '));
  for (let k = 0; k < 5; k++){ await page.evaluate(() => { murg.inv = 0; hitMurg(murg); }); }
  await page.waitForTimeout(4000);
  console.log('na 5 treffers:', await page.evaluate(() => ({ state: murg && murg.state, won })));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
