// Proefrit voor Reinier (de bijlveteraan, Elite tests): laadt Reinier: Test 1, zet Amir voor hem, volgt zijn toestanden en
// aanvallen, maakt schermafdrukken en raakt hem daarna tot hij dood is. node tools/reinier_test.js [map voor de afdrukken]
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
  await page.waitForFunction(() => typeof setLevel === 'function' && typeof REI_LEVELS !== 'undefined');
  await page.waitForTimeout(1500);
  await page.evaluate(() => { setLevel(0, REI_LEVELS); beginPlay('medium'); });
  await page.waitForTimeout(2000);
  await page.evaluate(() => { godMode = true; world = -1500; });   // dichtbij: dan spawnt hij (zoals elke vijand)
  await page.waitForFunction(() => REI_DATA && reinieren.length, null, { timeout: 30000 });
  await page.waitForTimeout(500);
  await page.evaluate(() => { world = reinieren[0].x + 700; });
  const log = []; let n = 0;
  for (let i = 0; i < 64; i++){
    await page.waitForTimeout(200);
    const st = await page.evaluate(() => { const s = reinieren[0]; return s ? { s: s.st + (s.soort && s.st === 'aanval' ? ':' + s.soort : ''), x: Math.round(s.x), amir: Math.round(playerX()) } : null; });
    if (st) log.push(st);
    if (shots && i % 2 === 0){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, 'r' + String(n++).padStart(3, '0') + '.png') }); }
  }
  const toest = []; for (const l of log) if (!toest.length || toest[toest.length - 1].s !== l.s) toest.push(l);
  console.log(toest.map(l => l.s + '@' + l.x).join(' '));
  for (let k = 0; k < 20; k++){ await page.evaluate(() => { const s = reinieren[0]; if (s){ s.inv = 0; hitReinier(s); } }); }
  await page.waitForTimeout(2500);
  if (shots) await page.screenshot({ path: path.join(shots, 'r_dood.png') });
  console.log('na de treffers:', await page.evaluate(() => { const s = reinieren[0]; return s ? { st: s.st, hp: s.hp } : 'weg'; }));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
