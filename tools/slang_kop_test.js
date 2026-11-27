// Proefrit voor de slangenkop (KOP) in de sandbox: met de stokken een slang die opkomt om te bijten, de stapslag en
// slag 2 erachteraan, en dan moet de kop eraf: rustig (langs of door de camera) en druk (klein, met een bandiet erbij).
// node tools/slang_kop_test.js [map voor de afdrukken]   (CHROME=/pad/naar/chrome als Playwright er zelf geen heeft)
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
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
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
  await page.addStyleTag({ content: '#sandbox{display:none!important}' });
  await page.waitForFunction(() => !laadWacht && running, null, { timeout: 120000 });
  await page.evaluate(() => { document.getElementById('sbstokken').click(); slangLaad('groen'); slangLaad('zwart'); });
  await page.waitForTimeout(2500);
  // de knikkerzak: precies 1 op 6
  const zak = await page.evaluate(() => { kopZakken = {}; let r = 0; for (let i = 0; i < 6; i++) r += kopKnikker('kop', 1, 6) ? 1 : 0; return r; });
  ok('knikkerzak: 1 op 6', zak === 1, zak);
  // een proef: een slang links voor Amir die opkomt om te bijten, dan de stapslag en slag 2
  const proef = async (versie, naam, extra) => {
    await page.evaluate(v => { kopSb = KOP_SB.indexOf(v); kopAltijd = v; kopLijst = []; for (const s of snakes) s.state = 'gone'; for (const b of bandieten) b.x += 20000; facing = -1; }, versie);
    if (extra) await page.evaluate(extra);
    // de stapslag in de lucht, in zijn raakframes de tweede druk (slag 2 staat dan klaar), en zodra slag 2 begint de slang
    // erbij, net buiten het bereik van de stapslag: slag 2 stapt door en raakt hem (zo gaat het ook in het spel)
    await page.waitForFunction(() => atkFrame < 0 && !(atkCooldown > 0) && !kopLijst.some(k => k.soort !== 'klein'), null, { timeout: 6000 }).catch(() => {});
    await page.waitForTimeout(500);
    await page.evaluate(() => { invuln = 9; kopLijst = []; });
    await page.keyboard.down('f'); await page.waitForTimeout(40); await page.keyboard.up('f');
    await page.waitForFunction(() => atkStok === 'stapslag' && atkFrame >= STOK.stapslag.buf, null, { timeout: 4000, polling: 10 }).catch(() => {});
    await page.keyboard.down('f'); await page.waitForTimeout(30); await page.keyboard.up('f');
    await page.waitForFunction(() => atkStok === 'slag2', null, { timeout: 4000, polling: 10 }).catch(() => {});
    await page.evaluate(() => { sbSpawn('groen', -1, playerX() - 200); const s = snakes[snakes.length - 1]; s.side = -1; s.state = 'bite'; s.frame = 2; s.acc = 0; s.biteUsed = true; });
    for (let i = 0; i < 30; i++){
      await page.waitForTimeout(25);
      await page.evaluate(() => { const s = snakes[snakes.length - 1]; if (s.state !== 'dying' && s.state !== 'gone'){ s.state = 'bite'; s.frame = 2; s.biteUsed = true; } });
      if (await page.evaluate(() => kopLijst.length > 0)) break;
    }
    const r = await page.evaluate(() => ({ n: kopLijst.length, soort: kopLijst[0] && kopLijst[0].soort, kop: !!snakes[snakes.length - 1].kop, stok: atkStok, st: snakes[snakes.length - 1].state, dx: Math.round(snakes[snakes.length - 1].x - playerX()) }));
    ok(naam, r.n === 1 && r.kop && (versie === 1 || r.soort === versie), r);
    for (let i = 0; i < 8; i++){ await page.waitForTimeout(70); await schiet(naam.replace(/\W+/g, '_') + '_' + i); }
    await page.waitForTimeout(400);
    return r;
  };
  await proef('door', 'door de camera');
  ok('hij is door de camera gevlogen', await page.evaluate(() => kopLijst.length === 0));
  await proef('langs', 'rakelings langs');
  const rust = await proef(1, 'rustig: de grote versie', null);
  ok('rustig is groot', rust.soort === 'door' || rust.soort === 'langs', rust.soort);
  const druk = await proef(1, 'druk: met een bandiet erbij', () => { sbSpawn('bandiet', -1, world - 420); });
  ok('druk is klein', druk.soort === 'klein', druk.soort);
  // Test 98 laadt, met de kop bij elke kill van slag 2
  const t98 = await page.evaluate(async () => { setLevel(STOK_LEVELS.indexOf(TEST_98), STOK_LEVELS); beginPlay('medium');
    await new Promise(r => setTimeout(r, 4000)); return { naam: level.name, kop: level.slangKop, altijd: kopAltijd }; });
  ok('Test 98 laadt, slangKop altijd', t98.naam === 'Test 98: Snake heads' && t98.kop === 1, t98);
  await schiet('test98');
  for (const f of [...fouten]) if (/TUNNEL/.test(f)) fouten.delete(f);   // de testomgeving zonder internet (fonts, Sheets)
  for (const f of fouten) console.log('  ' + f);
  ok('geen fouten in de console', !fouten.size);
  await browser.close(); srv.close();
  process.exit(fout ? 1 : 0);
});
