// Proefrit voor Duka, de marktman, in de sandbox (Geheime winkel): hij laadt, loopt en doet zijn dingen, en gesnapt achter
// de toonbank bevriest de wereld, lacht hij, klapt hij, en valt Amir aan de voorkant uit de lucht.
// node tools/duka_test.js [map voor de afdrukken]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const shots = process.argv[2] || null;
const srv = http.createServer((q, r) => {
  const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e){ r.writeHead(404); r.end(); return; }
    const t = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.json': 'application/json', '.mp3': 'audio/mpeg', '.jpg': 'image/jpeg' }[path.extname(f)] || 'application/octet-stream';
    r.writeHead(200, { 'Content-Type': t }); r.end(d); });
}).listen(0, async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const fouten = new Set(); let fout = 0;
  page.on('pageerror', e => fouten.add('fout: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/status of 404|ERR_TUNNEL|ERR_PROXY|net::ERR/.test(m.text())) fouten.add('console: ' + m.text()); });   // een 404 meldt de response zelf, met de url
  page.on('response', r => { if (r.status() >= 400 && !/sounds\/duka\//.test(r.url())) fouten.add(r.status() + ' ' + r.url()); });
  const ok = (naam, waar, info) => { console.log((waar ? 'OK   ' : 'FOUT ') + naam + (info !== undefined ? '  ' + JSON.stringify(info) : '')); if (!waar) fout++; };
  let n = 0;
  const schiet = async naam => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, String(n++).padStart(2, '0') + '_' + naam + '.png') }); } };
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof startSandbox === 'function');
  await page.waitForTimeout(1500);
  await page.evaluate(() => startSandbox());
  await page.addStyleTag({ content: '#sandbox{display:none!important}' });
  await page.waitForFunction(() => !laadWacht && running, null, { timeout: 120000 });
  await page.waitForTimeout(800);
  await page.evaluate(() => { document.getElementById('sbwinkelgeheim').click(); });
  await page.waitForTimeout(300);
  // naar binnen, voor de toonbank
  await page.evaluate(() => { const b = level.binnen[0]; world = b.winkel.x + 300; ph = 0; facing = -1; camVorig = null; });
  await page.waitForFunction(() => winkelKlaar() && DUKA.frames && Object.values(DUKA.frames).every(F => F.every(im => !im || imgReady(im))), null, { timeout: 120000 });
  await page.waitForTimeout(800);
  ok('Duka staat er (idle)', await page.evaluate(() => !!dukaFrame(winkelMan) && winkelMan.w === level.binnen[0].winkel));
  await schiet('rust');
  for (const a of ['gaap', 'kalebas', 'schap']){
    await page.evaluate(a => { winkelMan.fase = 'actie'; dukaZet(winkelMan, a); }, a);
    await page.waitForTimeout(1600); await schiet(a);
  }
  // naar achteren en omdraaien
  await page.evaluate(() => { const o = winkelOpbouw(winkelMan.w); winkelMan.fase = 'rust'; winkelMan.klok = 0; winkelGeheim.kans = 1; });
  await page.waitForFunction(() => winkelMan.fase === 'achterin', null, { timeout: 20000 });
  await page.waitForTimeout(500);
  ok('achterin met zijn rug naar je toe', await page.evaluate(() => winkelGeheimOm()));
  await schiet('achterin');
  // Amir springt erover en loopt rechtop: hij hoort hem
  await page.evaluate(() => { const w = winkelMan.w; winkelGeheim.achter = true; world = w.x - 250; ph = 0; });
  await page.keyboard.down('ArrowLeft'); await page.waitForTimeout(900); await page.keyboard.up('ArrowLeft');
  ok('gesnapt: de regie loopt', await page.evaluate(() => !!dukaRegie), await page.evaluate(() => dukaRegie && dukaRegie.stap));
  const x0 = await page.evaluate(() => world);
  await schiet('kijk');
  await page.waitForFunction(() => dukaRegie && dukaRegie.stap === 'lach', null, { timeout: 8000 });
  await page.waitForTimeout(1500); await schiet('lach');
  ok('Amir staat stil tijdens de lach', Math.abs(await page.evaluate(() => world) - x0) < 1);
  await page.waitForFunction(() => dukaRegie && dukaRegie.weg, null, { timeout: 10000 });
  await page.waitForTimeout(60); await schiet('klap_wolk');
  await page.waitForFunction(() => !dukaRegie, null, { timeout: 5000 });
  const na = await page.evaluate(() => ({ x: world - winkelMan.w.x, ph: Math.round(ph), achter: winkelGeheim.achter }));
  ok('Amir valt aan de voorkant uit de lucht', na.x > 0 && na.ph > 20 && !na.achter, na);
  await page.waitForTimeout(150); await schiet('val');
  await page.waitForTimeout(900);
  ok('en staat weer op de grond', await page.evaluate(() => onGround && ph < 2));
  await schiet('geland');
  for (const f of fouten) console.log('  ' + f);
  ok('geen fouten', fouten.size === 0);
  await browser.close(); srv.close();
  console.log(fout ? fout + ' fout(en)' : 'alles goed');
  process.exit(fout ? 1 : 0);
});
