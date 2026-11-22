#!/usr/bin/env node
'use strict';
// De outfittest: kijkt na dat Amir met de speer Mkuki is (Outfit 1) en met de stokken het oude tenue, en tekent elke outfit
// van MK_OUTFIT in een rij (idle, ren, stoot), zoals de lobby en de team-kaartjes dat doen. Schrijft per stap een plaatje.
//
//   node tools/outfittest.js [map]       standaard /tmp/outfittest
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const ROOT = path.dirname(__dirname), UIT = process.argv[2] || '/tmp/outfittest';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg' };
const wacht = ms => new Promise(ok => setTimeout(ok, ms));
async function tot(page, f, max = 30000){ const t = Date.now(); while (Date.now() - t < max){ if (await page.evaluate(f).catch(() => false)) return true; await wacht(200); } return false; }
(async () => {
  fs.mkdirSync(UIT, { recursive: true });
  const s = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (e, d) => { if (e){ res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
  });
  await new Promise(ok => s.listen(0, '127.0.0.1', ok));
  const b = await chromium.launch(), page = await b.newPage({ viewport: { width: 1280, height: 720 } });
  const fouten = [];
  page.on('pageerror', e => fouten.push(e.message));
  await page.goto('http://127.0.0.1:' + s.address().port + '/amir-king-of-africa.html');
  await wacht(1500);
  // de rij outfits: idle, ren en stoot per outfit, plus het oude tenue
  await page.evaluate(() => { skinZet(null); skinLijstLaad('mkuki'); mkSkinVoorladen(); });   // het menu staat soms in een level met een eigen skin
  await tot(page, () => SKIN.lijst.mkuki && SKIN.lijst.mkuki.size > 100);
  const frames = ['karakters/amir/idle/idle_sp/idle_sp_00.png', 'karakters/amir/beweging/run/nieuw/ren_sp_4.png', 'karakters/amir/aanval/speerstrike/attack_sp_5.png'];
  await page.evaluate(fr => { window._fr = fr.map(p => { const im = new Image(); im.src = p; return im; }); }, frames);
  await wacht(3000);
  const data = await page.evaluate(async () => {
    const L = [null].concat(MK_OUTFIT.lijst);
    // eerst elke outfit een keer tekenen: dan komen de skinframes en de zonekaarten binnen
    for (let n = 0; n < 30; n++){ for (const kl of L) for (const im of _fr) broekBeeld(im, im, kl, document.createElement('canvas')); await new Promise(r => setTimeout(r, 200)); }
    const cw = 300, ch = 300, cv = document.createElement('canvas'); cv.width = cw * L.length; cv.height = ch * _fr.length;
    const g = cv.getContext('2d'); g.fillStyle = '#e8965a'; g.fillRect(0, 0, cv.width, cv.height);
    L.forEach((kl, i) => _fr.forEach((im, j) => {
      const bb = broekBeeld(im, im, kl, document.createElement('canvas')), w = bb.naturalWidth || bb.width, h = bb.naturalHeight || bb.height;
      const k = Math.min(cw / w * 1.6, ch / h);
      g.drawImage(bb, i * cw + (cw - w * k) / 2, j * ch + ch - h * k, w * k, h * k);
    }));
    g.fillStyle = '#000'; g.font = '20px sans-serif'; L.forEach((kl, i) => g.fillText(kl ? kl.naam : 'oud (stokken)', i * cw + 10, 24));
    return cv.toDataURL('image/png');
  });
  fs.writeFileSync(path.join(UIT, 'outfits.png'), Buffer.from(data.split(',')[1], 'base64'));
  // de sandbox: Amir met de speer is Mkuki
  await page.evaluate(() => { startSandbox(); });
  await tot(page, () => running && !laadWacht, 90000);
  await wacht(3000);
  const stand = await page.evaluate(() => ({ kl: broekNu() && broekNu().id, stok: STOK_AAN }));
  await page.screenshot({ path: path.join(UIT, 'sandbox.png') });
  console.log('sandbox:', JSON.stringify(stand));
  console.log(fouten.length ? 'fouten:\n  ' + fouten.join('\n  ') : 'geen fouten');
  await b.close(); s.close();
})();
