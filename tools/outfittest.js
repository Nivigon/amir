#!/usr/bin/env node
'use strict';
// De outfittest: kijkt na dat Amir met de speer Mkuki is (Outfit 1) en met de stokken het oude tenue, en tekent elke outfit
// van MK_OUTFIT in een rij (idle, ren, stoot), zoals de lobby en de team-kaartjes dat doen. Schrijft per stap een plaatje.
//
//   node tools/outfittest.js [map]       standaard /tmp/outfittest
//   node tools/outfittest.js [map] --frames aanval/shove/shove_00.png,aanval/shove/shove_09.png
//                                        de rij outfits met deze frames (onder karakters/amir/) in plaats van idle, ren en stoot
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const ARGS = process.argv.slice(2), FI = ARGS.indexOf('--frames');
const EIGEN = FI >= 0 ? ARGS[FI + 1].split(',').map(r => 'karakters/amir/' + r) : null;
const ROOT = path.dirname(__dirname), UIT = ARGS.filter((a, i) => !a.startsWith('--') && i !== FI + 1)[0] || '/tmp/outfittest';
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
  const frames = EIGEN || ['karakters/amir/idle/idle_sp/idle_sp_00.png', 'karakters/amir/beweging/run/nieuw/ren_sp_4.png', 'karakters/amir/aanval/speerstrike/attack_sp_5.png'];
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
  // de losse speer (MK_LOS): klopt het samengestelde frame met het gebakken frame (Outfit 1, gewone speer), en hoe ziet
  // elke speersoort eruit in zijn hand
  const los = await page.evaluate(async () => {
    const L = [...SKIN.lijst.mkuki], kl = MK_OUTFIT.lijst[0];
    const oud = L.map(r => { const im = new Image(); im.src = 'karakters/amir/' + r; return im; });
    pfLaad();
    let verschil = [], mis = 0;
    for (let n = 0; n < 60; n++){
      mis = 0;
      for (const im of oud){ const mk = imgReady(im) && mkSkinVan(im, 'mkuki'); if (!mk || !mkLosBeeld(mk, im._skinRel, kl, null, document.createElement('canvas'))) mis++; }
      if (!mis) break;
      await new Promise(r => setTimeout(r, 500));
    }
    const px = c => { const g = c.getContext('2d', { willReadFrequently: true }); return g.getImageData(0, 0, c.width, c.height).data; };
    for (const im of oud){
      const mk = mkSkinVan(im, 'mkuki'), c = mkLosBeeld(mk, im._skinRel, kl, null, document.createElement('canvas'));
      if (!c) continue;
      const b = document.createElement('canvas'); b.width = c.width; b.height = c.height; b.getContext('2d').drawImage(mk, 0, 0);
      const p1 = px(c), p2 = px(b); let slecht = 0;
      for (let i = 0; i < p1.length; i += 4){
        const a = Math.max(p1[i + 3], p2[i + 3]); if (a < 128) continue;
        if (Math.abs(p1[i + 3] - p2[i + 3]) > 96 || Math.abs(p1[i] - p2[i]) + Math.abs(p1[i + 1] - p2[i + 1]) + Math.abs(p1[i + 2] - p2[i + 2]) > 120) slecht++;
      }
      verschil.push([im._skinRel, slecht]);
    }
    verschil.sort((a, b) => b[1] - a[1]);
    // de plaat: per speersoort een rij
    const soorten = [null, 'blauw', 'geel', 'oud2', 'pathfinder'], fr = ['idle/idle_sp/idle_sp_00.png', 'beweging/run/nieuw/ren_sp_4.png', 'aanval/speerstrike/attack_sp_5.png', 'aanval/combo/combo_07.png', 'beweging/rol/worp/worp_21.png'];
    const ims = fr.map(r => oud[L.indexOf(r)]).filter(Boolean);
    for (let n = 0; n < 40; n++){                       // eerst alles binnen: de Pathfinder, de vaantjes en de zonekaarten
      let ok = true;
      for (const s of soorten) for (const im of ims){ const c = mkLosBeeld(mkSkinVan(im, 'mkuki'), im._skinRel, MK_OUTFIT.lijst[2], { s, w: 0.6 }, document.createElement('canvas')); if (!c) ok = false; }
      if (ok && n > 4 && pfVaan[0] && imgReady(pfVaan[0])) break;
      await new Promise(r => setTimeout(r, 300));
    }
    const cw = 300, ch = 300, cv = document.createElement('canvas'); cv.width = cw * ims.length; cv.height = ch * soorten.length;
    const g = cv.getContext('2d'); g.fillStyle = '#e8965a'; g.fillRect(0, 0, cv.width, cv.height);
    soorten.forEach((s, j) => ims.forEach((im, i) => {
      // zoals een teamgenoot getekend wordt: broekBeeld met zijn soort en wind (sp en vw uit zijn stand)
      const c = broekBeeld(im, im, MK_OUTFIT.lijst[2], document.createElement('canvas'), { s, w: j === soorten.length - 1 ? 0.6 + 0.4 * (i % 2) : 0 });
      if (!c || c === im) return;
      const k = Math.min(cw / c.width * 1.3, ch / c.height);
      g.drawImage(c, i * cw + (cw - c.width * k) / 2, j * ch + ch - c.height * k, c.width * k, c.height * k);
    }));
    g.fillStyle = '#000'; g.font = '20px sans-serif'; soorten.forEach((s, j) => g.fillText(s || 'standaard', 10, j * ch + 24));
    return { mis, n: verschil.length, slechtst: verschil.slice(0, 8), plaat: cv.toDataURL('image/png') };
  });
  fs.writeFileSync(path.join(UIT, 'speersoorten.png'), Buffer.from(los.plaat.split(',')[1], 'base64'));
  console.log('los: ' + los.n + ' frames samengesteld, ' + los.mis + ' niet; meest afwijkend van het gebakken frame (pixels):', JSON.stringify(los.slechtst));
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
