// Proefrit voor de Ardhi-wapens (ARDHI) in de sandbox: de speer wordt Ardhi's Reach, de knikkerzak geeft precies 1 op 10
// (worp) en 1 op 33 (steek, stok), de druppel geeft een leven terug, een geworpen Ardhi-speer zet wortels om twee
// bandieten in een groep (en ze staan vast), en de stokken krijgen Ardhi's Grip.
// node tools/ardhi_test.js [map voor de afdrukken]
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
  const fouten = new Set(); let fout = 0;
  page.on('pageerror', e => fouten.add('fout: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') fouten.add('console: ' + m.text()); });
  page.on('response', r => { if (r.status() >= 400) fouten.add(r.status() + ' ' + r.url()); });
  const ok = (naam, waar, info) => { console.log((waar ? 'OK   ' : 'FOUT ') + naam + (info !== undefined ? '  ' + JSON.stringify(info) : '')); if (!waar) fout++; };
  let n = 0;
  const schiet = async naam => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, String(n++).padStart(2, '0') + '_' + naam + '.png') }); } };
  await page.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await page.waitForFunction(() => typeof startSandbox === 'function');
  await page.waitForTimeout(1500);
  await page.evaluate(() => startSandbox());
  await page.addStyleTag({ content: '#sandbox{display:none!important}' });   // de knoppen uit beeld voor de afdrukken
  await page.waitForFunction(() => !laadWacht && running, null, { timeout: 120000 });
  await page.waitForTimeout(1500);
  // de speer
  await page.evaluate(() => { spearFound = true; spear = true; document.getElementById('sbardhi').click(); });
  await page.waitForTimeout(600);
  ok('een speer is Ardhi\'s Reach', await page.evaluate(() => speerBlauw === 'ardhi' || rugSperen.some(r => r.blauw === 'ardhi')));
  await page.evaluate(() => { speerVolgorde = ['ardhi', 'pathfinder', 'standaard', 'geel', 'blauw', 'oud']; speerSorteer(); });
  await page.waitForTimeout(400); await schiet('speer_in_hand');
  // de knikkerzak
  const zak = await page.evaluate(() => { ardhiZakken = {}; let w = 0, s = 0; for (let i = 0; i < 10; i++) w += ardhiKnikker('worp', 1, 10) ? 1 : 0; for (let i = 0; i < 33; i++) s += ardhiKnikker('steek', 1, 33) ? 1 : 0; return { w, s }; });
  ok('knikkerzak: 1 op 10 en 1 op 33', zak.w === 1 && zak.s === 1, zak);
  // het leven terug: de druppel
  await page.evaluate(() => { levensStart = () => 3; lives = 1; ardhiZakken = { worp: [true] }; worpTref = true; jav = { blauw: 'ardhi', state: 'vlucht', t: 0 }; ardhiTreffer({ x: world - 200 }); worpTref = false; jav = null; });
  ok('een raak knikker zet de druppel', await page.evaluate(() => !!ardhiHeelNu));
  await page.waitForTimeout(450); await schiet('druppel_licht');
  await page.waitForTimeout(1200);
  ok('het leven kwam erbij', await page.evaluate(() => lives === 2 && !ardhiHeelNu), await page.evaluate(() => lives));
  await page.evaluate(() => { lives = 3; ardhiZakken = { steek: [true] }; atkFrame = 2; ardhiTreffer({ x: world - 200 }); atkFrame = -1; });
  ok('met volle levens geen druppel', await page.evaluate(() => !ardhiHeelNu));
  // de wortels: drie bandieten dicht bij elkaar
  const w = await page.evaluate(() => {
    for (const d of [260, 330, 420]) sbSpawn('bandiet', 1, world + d);
    const b = bandieten.slice(-3);
    worpTref = true; jav = { blauw: 'ardhi', state: 'vlucht', t: 0 };
    ardhiWortelRaak(b[0]);
    worpTref = false; jav = null;
    return { n: b.filter(o => o.wortel).length, x: b.map(o => Math.round(o.x)) };
  });
  ok('twee bandieten staan in de wortels', w.n === 2, w);
  await page.waitForTimeout(150); await schiet('wortels_op');
  await page.waitForTimeout(700); await schiet('wortels');
  const x2 = await page.evaluate(() => bandieten.slice(-3).map(o => ({ x: Math.round(o.x), w: !!o.wortel })));
  ok('wie vastzit kwam niet van zijn plek', x2.filter(o => o.w).length === 2 && x2.filter(o => o.w).every(o => w.x.includes(o.x)), x2);
  await page.waitForTimeout(1800);
  ok('de wortels zijn weer weg', await page.evaluate(() => !ardhiWortels.length));
  const alleen = await page.evaluate(() => { const b = bandieten.slice(-3); for (const o of b.slice(1)) o.x += 5000; worpTref = true; jav = { blauw: 'ardhi', state: 'vlucht', t: 0 }; ardhiWortelRaak(b[0]); worpTref = false; jav = null; return ardhiWortels.length; });
  ok('een vijand alleen krijgt geen wortels', alleen === 0, alleen);
  // de stokken: Ardhi's Grip
  await page.evaluate(() => { for (const o of bandieten) o.x += 9000; document.getElementById('sbstokken').click(); });
  await page.waitForTimeout(2500);
  ok('de stokken zijn Ardhi\'s Grip', await page.evaluate(() => stokSkinNu() === 'ardhi' && stokHoutNu() === 4));
  await schiet('stokken');
  await page.keyboard.press('Space'); await page.waitForTimeout(250); await schiet('stokslag');
  await page.waitForTimeout(800);
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  console.log(fout ? fout + ' FOUT' : 'alles OK');
  await browser.close(); srv.close();
  process.exit(fout || fouten.size ? 1 : 0);
});
