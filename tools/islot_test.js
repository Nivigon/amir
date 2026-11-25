// Proefrit voor de spullen van Kivuli en de itemslots (ISLOT) in de sandbox: per ding een bandiet erbij, het ding in een
// slot (zoals de inventory doet), R of T drukken, en kijken of het werkt. node tools/islot_test.js [map voor de afdrukken]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const shots = process.argv[2] || null;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json', '.mp3': 'audio/mpeg', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => {
  const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e){ r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
}).listen(0, async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const fouten = new Set();
  page.on('pageerror', e => fouten.add('fout: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') fouten.add('console: ' + m.text()); });
  page.on('response', r => { if (r.status() >= 400) fouten.add(r.status() + ' ' + r.url()); });
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof startSandbox === 'function');
  await page.waitForTimeout(1500);
  await page.evaluate(() => startSandbox());
  await page.waitForFunction(() => !laadWacht && running, null, { timeout: 120000 });
  await page.waitForTimeout(1500);
  let n = 0;
  const schiet = async (naam) => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, String(n++).padStart(2, '0') + '_' + naam + '.png') }); } };
  const verslag = {};
  for (const [k, slot] of [['bones', 0], ['fangs', 1], ['ants', 0], ['mirrors', 1], ['klei', 0]]){
    await page.evaluate(() => { for (const b of bandieten) b.dead = true; bandieten.length = 0; lives = 9; drawLives && drawLives(); });
    await page.evaluate(([k, slot]) => { document.querySelector('.sbisl[data-isl="' + k + '"]').click(); islotZet(k, slot); }, [k, slot]);
    await page.evaluate(() => { sbFromRight = false; sbSpawn('bandiet', -1, world - W * 0.45); });
    await page.waitForTimeout(400);
    await page.keyboard.press(slot === 0 ? 'r' : 't');
    const r = {};
    if (k === 'klei'){
      r.sprongVoor = await page.evaluate(() => !!jump);
      await page.keyboard.press('ArrowUp'); await page.waitForTimeout(100);
      r.springtNiet = await page.evaluate(() => !jump);
      await page.keyboard.down('ArrowLeft'); await page.waitForTimeout(1200); await schiet(k + '_loopt'); await page.keyboard.up('ArrowLeft');
      r.klonten = await page.evaluate(() => islotKlonten.length);
      r.kleiT = await page.evaluate(() => +islotKleiT.toFixed(1));
    } else {
      for (let i = 0; i < 6; i++){ await page.waitForTimeout(500); if (i === 2 || i === 4) await schiet(k + '_' + i); }
      r.fx = await page.evaluate(() => islotFx.map(e => e.k + (e.beten != null ? ':' + e.beten + ' beten' : '')));
      r.bandiet = await page.evaluate(() => bandieten.map(b => ({ x: Math.round(b.x - world), blind: +(b.verblind || 0).toFixed(1), hp: b.hp, dood: !!b.dead || b.state === 'dying' })));
      if (k === 'mirrors') r.onzichtbaar = await page.evaluate(() => islotMirAan(0));
    }
    r.tas = await page.evaluate(() => JSON.stringify(islotTas) + ' slots ' + JSON.stringify(islot));
    verslag[k] = r;
    await page.waitForTimeout(3000);
  }
  // Shift+O moet opnieuw beginnen
  await page.keyboard.down('Shift'); await page.keyboard.press('o'); await page.keyboard.up('Shift');
  await page.waitForTimeout(500);
  verslag.na = await page.evaluate(() => ({ tas: JSON.stringify(islotTas), slots: JSON.stringify(islot), fx: islotFx.length }));
  console.log(JSON.stringify(verslag, null, 1));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
