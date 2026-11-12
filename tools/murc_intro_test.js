// Proefrit voor de opening van Murghtaan 3 (MURC_INTRO): laadt het level (onaantastbaar), loopt naar de muur, en volgt
// de toestanden: vreten, omkijken met de freeze, de whoop, de roedel van drie (ritme, nooit twee tegelijk in de uitval),
// en na de roedel (die het script na een tijdje doodt) de tweede freeze en de charge. Meldt fouten in de console.
// node tools/murc_intro_test.js [map voor schermafdrukken]
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
  await page.evaluate(() => { duoKeuze.murcOnst = 'onst'; duoKeuze.murcHy = 1; setLevel(2, MUR_LEVELS); beginPlay('medium'); });
  await page.waitForFunction(() => typeof murcMeta !== 'undefined' && murcMeta && murg, null, { timeout: 30000 });
  await page.waitForFunction(() => !laadWacht, null, { timeout: 120000 });
  await page.waitForTimeout(800);
  await page.evaluate(() => {
    window.__log = []; window.__dubbel = 0; window.__amirMin = Infinity;
    const stap = () => {
      const s = murg; if (!s) return requestAnimationFrame(stap);
      const L = window.__log, st = s.state + (murcVries ? '*' : '');
      if (!L.length || L[L.length - 1] !== st) L.push(st);
      const bezig = hyenas.filter(h => h.murcRoedel && (h.state === 'telegraaf' || h.state === 'storm')).length;
      if (bezig > 1) window.__dubbel++;
      if (s.muurX != null) window.__amirMin = Math.min(window.__amirMin, world - s.muurX);
      requestAnimationFrame(stap);
    };
    requestAnimationFrame(stap);
  });
  // Amir loopt naar links tot de muur (de toets vasthouden)
  const foto = async n => { if (!shots) return; fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, n + '.png') }); };
  await page.evaluate(() => { world = murg.muurX + murAmir() * 6; });
  await page.waitForTimeout(600); await foto('01_vreet');
  for (let i = 0; i < 60; i++){                        // stap voor stap naar de muur (zoals lopen, 330 px/s)
    await page.waitForTimeout(100);
    if (await page.evaluate(() => { if (!murcVries) world -= 33; return !!murcVries; })) break;
  }
  await page.waitForTimeout(700); await foto('02_freeze');
  await page.waitForTimeout(1800); await foto('03_whoop');
  await page.waitForTimeout(3000); await foto('04_roedel');
  for (let i = 0; i < 12; i++){ await page.waitForTimeout(1000); if (i === 5) await foto('05_roedel'); }
  const roedel = await page.evaluate(() => hyenas.filter(h => h.murcRoedel).map(h => h.state + '@' + Math.round(h.x - world)));
  console.log('roedel na 15 s:', roedel.join(' '));
  // de roedel sterft
  await page.evaluate(() => { for (const h of hyenas) if (h.murcRoedel){ h.state = 'dood'; h.fall = 0; } });
  for (let i = 0; i < 30; i++){ await page.waitForTimeout(100); if (await page.evaluate(() => !!murcVries)) break; }
  await page.waitForTimeout(300); await foto('06_tweede');
  await page.waitForTimeout(2500); await foto('07_charge');
  const r = await page.evaluate(() => ({ log: window.__log, dubbel: window.__dubbel, amirMin: Math.round(window.__amirMin), intro: murg.intro, actief: murg.actief }));
  console.log('toestanden:', r.log.join(' > '));
  console.log('twee tegelijk in de uitval (beelden):', r.dubbel, ' Amir minstens zo ver rechts van de muur:', r.amirMin, ' intro:', r.intro, ' actief:', r.actief);
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
