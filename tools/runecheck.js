#!/usr/bin/env node
// De runecheck: is elke schijf die je met je speer moet raken op elk scherm te raken, en zie je
// hem dan ook?
//
// levelcheck.py rekent met getallen uit de code, maar de schijf op een rots zit op de alfa van een
// plaat, en die plaat moet geladen zijn. Daarom doet dit script het in het echte spel: het laadt de
// HTML in Chromium, zet elk level klaar op een reeks schermformaten en vraagt het spel zelf
// (runeStroken voor een rune op een rots, en dezelfde boog tegen muurSymRaak voor de rotswand) van
// welke afstanden de speer de schijf raakt. Daarna kijkt het of die strook ook in beeld ligt: de
// camera staat op Amir, dus verder dan een half scherm voor hem uit ziet hij de schijf niet meer.
//
//   node tools/runecheck.js                 alle levels, alle schermen
//   node tools/runecheck.js "Poort"         alleen de levels waarvan de naam dit bevat
//   node tools/runecheck.js --formaat 25    het schuifje Formaat (standaard 25)
//   node tools/runecheck.js --schermen 1280x720,852x393
//
// FOUT: niet te raken, of nergens te raken met de schijf in beeld. LET OP: er blijft minder dan
// MARGE px over, of je moet vanaf de laatste pixels van de strook gooien.
//
// Nodig: Node en Playwright (npm i -g playwright) met Chromium. Het script start zelf een webserver.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');

function laadPlaywright(){
  const plekken = ['playwright', path.join(process.execPath, '../../lib/node_modules/playwright')];
  for (const p of plekken){ try { return require(p); } catch (e) { /* volgende */ } }
  console.error('runecheck: Playwright ontbreekt (npm i -g playwright)');
  process.exit(2);
}
const { chromium } = laadPlaywright();

const ROOT = path.dirname(__dirname);
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
if (args.includes('--help')){ console.log(fs.readFileSync(__filename, 'utf8').split('\n').slice(1, 19).join('\n')); process.exit(0); }
const losse = [];                                  // de vlaggen met hun waarde eruit: wat overblijft is het filter
for (let i = 0; i < args.length; i++){
  if (args[i] === '--formaat' || args[i] === '--schermen'){ i++; continue; }
  if (!args[i].startsWith('--')) losse.push(args[i]);
}
const filter = losse[0] || '';
const formaat = Number(opt('--formaat', 25));
const MARGE = 60;                                  // zoveel px ruimte wil je overhouden in beeld
const schermen = (opt('--schermen', '1280x720,852x393,1440x620,1920x1080'))
  .split(',').map(s => s.split('x').map(Number)).map(([w, h]) => ({ w, h }));

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg', '.webmanifest': 'application/manifest+json', '.css': 'text/css' };
function server(){
  return new Promise(res => {
    const srv = http.createServer((req, rep) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      fs.readFile(p, (e, d) => {
        if (e){ rep.statusCode = 404; rep.end('nee'); return; }
        rep.setHeader('Content-Type', TYPES[path.extname(p).toLowerCase()] || 'application/octet-stream');
        rep.end(d);
      });
    }).listen(0, '127.0.0.1', () => res(srv));
  });
}

// in de pagina: per level de schijven nameten. De rotsplaten laden pas als een rune ze vraagt, dus
// eerst een keer vragen en dan wachten tot ze binnen zijn.
async function meet(filter){
  const uit = [];
  const wacht = ms => new Promise(r => setTimeout(r, ms));
  const lijsten = [POORT_LEVELS, TEST_LEVELS, BAB_LEVELS];
  const werk = [];
  for (const lijst of lijsten) lijst.forEach((def, i) => werk.push([lijst, def, i]));
  for (const [lijst, def, i] of werk){
    if (filter && !def.name.toLowerCase().includes(filter.toLowerCase())) continue;
    if (!(def.runes && def.runes.length) && !def.muur) continue;
    setLevel(i, lijst);
    const klaar = () => (level.runes || []).every(e => !!ravijnRotsMaat(nowScale(), e))
                     && (!level.muur || !!muurSet(nowScale()));
    for (let n = 0; n < 60 && !klaar(); n++) await wacht(100);
    const sc = nowScale(), rPx = RAVIJN_RUNE.r * CHAR_H * sc, inBeeld = W / 2 - rPx;
    const rij = { naam: def.name, breed: W, hoog: H, inBeeld: Math.round(inBeeld), schijven: [] };
    for (const e of (level.runes || [])){
      const M = ravijnRotsMaat(sc, e), R = M && ravijnRune(sc, e);
      rij.schijven.push({ wat: 'rune op ' + (e.rots || 'spits') + ' op x=' + Math.round(e.x),
                          hoog: Math.round(runeHoog(e)), strook: M ? runeStroken(e, sc) : null,
                          rots: M ? [Math.round(M.l), Math.round(M.l + M.wPx)] : null,
                          schijfX: R ? Math.round(R.x) : null });
    }
    if (level.muur){
      const S = muurSet(sc);
      rij.schijven.push({ wat: (level.muur.soort === 'grot' ? 'grot' : 'rotswand') + ' op x=' + Math.round(level.muur.x),
                          hoog: S ? Math.round((S.voetY - S.symY) / sc) : null, strook: S ? muurStrook(sc) : null,
                          rots: S ? [Math.round(level.muur.x - S.w), Math.round(level.muur.x)] : null,
                          schijfX: S ? Math.round(level.muur.x - (S.w - S.symX)) : null });
    }
    uit.push(rij);
  }
  return uit;

  // dezelfde boog als runeStroken, maar tegen de schijf van de rotswand (muurSymRaak); het steen
  // van de rots houdt de speer tegen, behalve op de hoogte van de schijf zelf (zoals muurSteen)
  function muurStrook(scale){
    const m = level.muur, S = muurSet(scale);
    if (!S || !S.alfa) return null;
    const sx = m.x - (S.w - S.symX);
    const vol = (x, h) => {
      const u = Math.round(muurKol(m, S, x)), v = Math.round(muurRij(S, h, scale));
      if (u < 0 || v < 0 || u >= S.w || v >= S.h) return false;
      if ((x - sx) * -1 < S.raakR && Math.abs(v - S.symY) < S.raakR * 1.5) return false;
      return S.alfa[v * S.w + u] > 128;
    };
    const worpen = (level.worp === 'schaal')
      ? Array.from({ length: THR_HOEK_MAX / 2 + 1 }, (_, i) => [i * 2, 1 - (1 - THR_LOB_V) * i * 2 / THR_LOB_DEG])
      : [[THR_LOB_DEG, THR_LOB_V], [0, 1]];
    const g = GRAVITY * JAV.gDeel, dt = 1 / 60, raakt = [];
    const ox = (THR_TIP.x - THR_ANCHOR) * THR_S * scale, oh = (THR_GROUND - THR_TIP.y) * THR_S;
    for (let d = 0; d <= 2400; d += 10){
      let ok = false;
      for (const [gr, deel] of worpen){
        const a = gr * Math.PI / 180, V = JAV.tiles * JAV.tile * CHAR_H * scale * deel;
        let x = m.x + d - ox, h = oh, vx = -V * Math.cos(a), vh = Math.sin(a) * V / scale, uit2 = false;
        for (let t = 0; t < 4 && h > 0 && !ok; t += dt){
          const stap = Math.max(1, Math.ceil(Math.abs(vx * dt) / 14)), s = dt / stap;
          let klaar = false;
          for (let i = 0; i < stap; i++){
            const nx = x + vx * s, nh = h + vh * s;
            if (muurSymRaak(nx, nh, scale)){ ok = true; break; }
            const v = vol(nx, nh);
            if (v && uit2){ klaar = true; break; }
            if (!v) uit2 = true;
            x = nx; h = nh; vh -= g * s;
          }
          if (klaar) break;
        }
        if (ok) break;
      }
      const laatste = raakt[raakt.length - 1];
      if (ok){ if (laatste && laatste[1] === d - 10) laatste[1] = d; else raakt.push([d, d]); }
    }
    // de strook is gemeten vanaf de muurlijn, de schijf staat verderop in de rots: omrekenen naar de
    // afstand tot de schijf zelf, zodat hij net als bij een rune tegen het beeld te leggen is
    const diep = S.w - S.symX;
    return raakt.map(([a, b]) => [Math.round(a + diep), Math.round(b + diep)]);
  }
}

(async () => {
  const srv = await server();
  const url = 'http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html';
  const browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  let fouten = 0, letop = 0;
  console.log('Formaat ' + formaat + ', marge ' + MARGE + ' px');
  for (const s of schermen){
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h } });
    await page.goto(url);
    await page.waitForFunction(() => typeof setLevel === 'function' && typeof runeStroken === 'function');
    await page.evaluate(f => { document.getElementById('size').value = String(f);
                               document.getElementById('size').dispatchEvent(new Event('input')); }, formaat);
    await page.waitForTimeout(2500);               // de rotsplaten en de muur moeten binnen zijn
    const rijen = await page.evaluate(meet, filter);
    console.log('\n== ' + s.w + ' bij ' + s.h + ' ==');
    for (const r of rijen){
      console.log('  ' + r.naam + '  (in beeld tot ' + r.inBeeld + ' px voor je)');
      for (const d of r.schijven){
        const st = d.strook;
        let melding = '', soort = '';
        if (!st){ melding = 'niet na te meten: de plaat is er niet'; soort = 'FOUT'; }
        else if (!st.length){ melding = 'nergens te raken: het steen of de boog zit ervoor'; soort = 'FOUT'; }
        else {
          const past = st.filter(([a]) => a <= r.inBeeld);
          const ruim = st.filter(([a]) => a <= r.inBeeld - MARGE);
          melding = 'te raken van ' + st.map(q => q[0] + '-' + q[1]).join(', ') + ' px';
          if (!past.length) soort = 'FOUT', melding += ': nergens met de schijf in beeld';
          else if (!ruim.length) soort = 'LET OP', melding += ': alleen de laatste ' + (r.inBeeld - past[0][0]) + ' px liggen in beeld';
        }
        if (soort === 'FOUT') fouten++; else if (soort === 'LET OP') letop++;
        const waar = d.rots ? ', rots ' + d.rots[0] + '..' + d.rots[1] + ', schijf op x=' + d.schijfX : '';
        console.log('    ' + (soort || 'ok').padEnd(7) + ' ' + d.wat + ' (schijf op ' + d.hoog + waar + ') ' + melding);
      }
    }
    await page.close();
  }
  await browser.close();
  srv.close();
  console.log('\n' + fouten + (fouten === 1 ? ' fout' : ' fouten') + ', ' + letop + ' keer let op');
  process.exit(fouten ? 1 : 0);
})();
