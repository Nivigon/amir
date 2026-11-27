// Proefrit voor de shove (SHOVE): een vlak level met de speer (Mkuki), een bandiet vlak voor Amir, aanvallen, en kijken
// of hij geduwd wordt tot op steekafstand; daarna met een tweede bandiet op steekafstand (dan moet het een gewone steek
// zijn), en de kruisboogbandiet, zweepman, schildbandiet en kooiman. node tools/shove_test.js [map voor de afdrukken]
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
  const snap = async n => { if (shots){ fs.mkdirSync(shots, { recursive: true }); await page.screenshot({ path: path.join(shots, n + '.png') }); } };
  const start = async spawns => {
    await page.evaluate(sp => {
      const lv = JSON.parse(JSON.stringify(TEST_74));
      delete lv.stokken; delete lv.geenSpeer; delete lv.sneak; delete lv.stokKeuze; delete lv.onstKeuze; delete lv.grondklap;
      lv.wapenKeuze = false; lv.speerInHand = true; lv.onsterfelijk = true; lv.tips = []; lv.spawns = sp;
      setLevel(0, [lv]); beginPlay('medium');
    }, spawns);
    await page.waitForFunction(() => running && !laadWacht, null, { timeout: 90000 });
    await page.evaluate(() => { if (!spear){ spear = true; spearFound = true; } });
    await page.waitForFunction(() => shoveKlaar(), null, { timeout: 30000 });
    await page.waitForTimeout(1200);
  };
  // zet de vijanden van lijst L op afstanden (sprite-eenheden) voor Amir, en hou ze even stil
  const zet = (L, ds) => page.evaluate(([L, ds]) => {
    const lijst = window[L] || eval(L), k = nowScale(), kant = facing === 1 ? 1 : -1;
    lijst.forEach((s, i) => { if (ds[i] != null){ s.x = playerX() + kant * ds[i] * k; s.rust = 0.3; } });
    hurt = 0; invuln = 3;
    return lijst.map(s => Math.round((s.x - playerX()) * kant / k));
  }, [L, ds]);
  const afstand = L => page.evaluate(L => { const k = nowScale(), kant = facing === 1 ? 1 : -1; return eval(L).map(s => Math.round((s.x - playerX()) * kant / k) + ':' + s.state); }, L);
  const uit = [];
  const proef = async (naam, spawns, L, ds, verwacht) => {
    await start(spawns);
    const voor = await zet(L, ds);
    const dbg = await page.evaluate(() => { const d = shoveDoel(); return (d ? d.soort + '@' + Math.round(d.d / nowScale()) + ' half ' + Math.round(d.half / nowScale()) : 'geen doel') + ' cd ' + atkCooldown.toFixed(2) + ' vast ' + amirVast() + ' hurt ' + hurt.toFixed(2); });
    await page.keyboard.press('f');
    await page.waitForTimeout(60);
    const wat = await page.evaluate(() => shoveA ? 'shove' : atkFrame >= 0 ? 'steek' : 'niets');
    const reeks = [];
    for (let i = 0; i < 8; i++){ await page.waitForTimeout(90); reeks.push((await afstand(L))[0]); if (i % 2) await snap(naam + '_' + i); }
    const na = reeks;
    uit.push(`${naam}: ${wat} (verwacht ${verwacht})  voor ${voor.join(',')}  na ${na.join(',')}  ${wat === verwacht ? 'OK' : 'FOUT'}  [${dbg}]`);
  };
  await proef('bandiet', [{ x: -900, k: 'bandiet' }], 'bandieten', [110], 'shove');
  await proef('tweede', [{ x: -900, k: 'bandiet' }, { x: -1200, k: 'bandiet' }], 'bandieten', [110, 270], 'steek');
  await proef('vrij', [{ x: -900, k: 'bandiet' }], 'bandieten', [600], 'steek');
  await proef('schildman', [{ x: -900, k: 'schildman' }], 'schildmannen', [110], 'shove');
  await proef('kruisboog', [{ x: -900, k: 'kruisboogbandiet' }], 'kruisbogen', [110], 'shove');
  await proef('zweepman', [{ x: -900, k: 'zweepman' }], 'zweepmannen', [110], 'shove');
  await proef('kooiman', [{ x: -900, k: 'kooiman', duel: false }], 'kooimannen', [110], 'shove');
  await proef('hyena', [{ x: -900, k: 'hyenas' }], 'hyenas', [100], 'steek');
  // de meting: na de shove doet Amir niets. Hoe lang na het einde van de shove begint de vijand zijn aanval (uithaal, sprong)
  // en wanneer raakt hij Amir? Zo lang heeft Amir om rustig een steek te zetten (de steek raakt zo'n 0,2 s na de druk)
  const meet = async (naam, spawns, L, aanval) => {
    await start(spawns);
    await zet(L, [110]);
    await page.evaluate(([L, aanval]) => {
      const s = eval(L)[0], M = window.__m = { eind: null, uithaal: null, raak: null, t0: performance.now() };
      const oh = hurtPlayer;
      window.__hurtOrig = window.__hurtOrig || oh;
      hurtPlayer = function(){ if (M.raak == null) M.raak = performance.now(); return window.__hurtOrig.apply(this, arguments); };
      const kijk = () => {
        const nu = performance.now();
        if (M.eind == null && M.gestart && !shoveA) M.eind = nu;
        if (shoveA) M.gestart = true;
        if (M.eind != null && M.uithaal == null && aanval.includes(s.state)) M.uithaal = nu;
        if (nu - M.t0 < 6000) requestAnimationFrame(kijk);
      };
      requestAnimationFrame(kijk);
      invuln = 0; hurt = 0;
    }, [L, aanval]);
    await page.keyboard.press('f');
    await page.waitForTimeout(5000);
    const m = await page.evaluate(() => window.__m);
    const t = v => v == null || m.eind == null ? 'nooit' : ((v - m.eind) / 1000).toFixed(2) + ' s';
    return `${naam}: na het einde van de shove: aanval begint na ${t(m.uithaal)}, raakt Amir na ${t(m.raak)}`;
  };
  uit.push('', 'meting (tijd tussen het einde van de shove en de eerste slag):');
  uit.push(await meet('bandiet', [{ x: -900, k: 'bandiet' }], 'bandieten', ['slag']));
  uit.push(await meet('schildman', [{ x: -900, k: 'schildman' }], 'schildmannen', ['strike']));
  uit.push(await meet('zweepman', [{ x: -900, k: 'zweepman' }], 'zweepmannen', ['slag']));
  console.log(uit.join('\n'));
  console.log(fouten.size ? [...fouten].join('\n') : 'geen fouten in de console');
  await browser.close(); srv.close();
});
