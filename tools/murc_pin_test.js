// Proefrit voor de pin van Murghtaan 2 (MURC.pin): laadt het level, zet de kans op 1, en speelt drie potjes:
// niets doen (vier gemiste happen: een leven), elke hap pareren (de trap en het strafvenster), en rollen bij de
// landing (ontweken). Meldt de toestanden, de levens en de fouten in de console, en maakt met een map erbij
// schermafdrukken van de pin. node tools/murc_pin_test.js [map]
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
  let n = 0;
  for (const wijze of ['niets', 'pareer', 'rol']){
    await page.evaluate(() => { duoKeuze.murcOnst = 'leven'; duoKeuze.murcHy = 0; setLevel(1, MUR_LEVELS); beginPlay('medium'); });
    await page.waitForFunction(() => murcMeta && murg, null, { timeout: 30000 });
    await page.waitForTimeout(1200);
    await page.evaluate(w => {
      Object.assign(MURC.pin, MURC_PIN_STANDAARD, { kans: 1, afkoel: 0 });
      world = -2000; lives = 3; drawLives();
      window.__pinLog = [];
      // de speler: pareren op de hap, of rollen vlak voor de landing
      const stap = () => {
        const s = murg; if (!s) return requestAnimationFrame(stap);
        const L = window.__pinLog; if (!L.length || L[L.length - 1].s !== s.state) L.push({ s: s.state, lives });
        if (w === 'pareer' && s.state === 'pin'){
          const tot = murcPinTotHap(s);
          if (tot != null && tot < MURC.pin.voor * 0.5 && s.pin.gestoken !== s.pin.i && s.pin.druk !== s.pin.i){ s.pin.druk = s.pin.i; thrPress(); }
        }
        if (w === 'rol' && s.state === 'pinLand' && s.frame <= 2 && !rol && !window.__gerold){ window.__gerold = true; rolStart(); }
        requestAnimationFrame(stap);
      };
      window.__gerold = false; requestAnimationFrame(stap);
    }, wijze);
    for (let i = 0; i < 100; i++){
      await page.waitForTimeout(250);
      const st = await page.evaluate(() => murg.state);
      if (shots && (st === 'pin' || st.startsWith('pin')) && i % 2 === 0){
        fs.mkdirSync(shots, { recursive: true });
        await page.screenshot({ path: path.join(shots, wijze + '_' + String(n++).padStart(3, '0') + '.png') });
      }
      const klaar = await page.evaluate(() => window.__pinLog.some(l => l.s === 'pinStraf' || l.s === 'pinEraf' || l.s === 'pinMis') && !murg.state.startsWith('pin'));
      if (klaar) break;
    }
    const log = await page.evaluate(() => window.__pinLog);
    console.log(wijze + ': ' + log.map(l => l.s + '(' + l.lives + ')').join(' '));
  }
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
