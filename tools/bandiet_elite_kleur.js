// Maakt de elite-bandiet (de garde van de valse koning) uit de gewone bandietset.
//
//     node tools/bandiet_elite_kleur.js
//
// Uit enemies/bandiet/ komt enemies/bandiet_elite/: dezelfde bandiet, omgekleurd naar
// roetzwart met een klein goud accent. De tekening zelf blijft staan; de helderheid
// wordt per pixel op een kleurladder gelegd (een gradient-map), zodat de plooien, de
// schaduwen en de contour precies blijven zoals ze getekend zijn.
//
// Twee vlakken, herkend aan helderheid en verzadiging van het origineel:
//   metaal  de lichte, weinig verzadigde glans (het kromzwaard, de gespen) -> goud
//   doek    al het andere (het bruine lijf, de kleding)                    -> houtskool
// De donkere contour (heel donker) blijft met opzet zwart staan.
//
// Alle reeksen worden omgezet (run, slag, look, worp, dood, hurk, schouder, spot, vault,
// en de dolk), en de json-metadata wordt meegekopieerd. De originelen in enemies/bandiet/
// blijven staan als bron. Verandert er een frame, draai dit dan opnieuw, en daarna
// tools/gen-offline-manifest.py.
//
// Nodig: node en playwright (npm i -g playwright).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.dirname(__dirname);
const SRC = path.join(ROOT, 'enemies', 'bandiet');
const DST = path.join(ROOT, 'enemies', 'bandiet_elite');

// helderheid -> kleur ladder (gradient-map), per vlak
const houtskool = [[0, [10, 10, 12]], [0.42, [28, 29, 34]], [0.70, [54, 56, 64]], [1, [96, 99, 112]]];
const goud      = [[0, [86, 60, 18]], [0.50, [172, 130, 42]], [0.80, [218, 176, 72]], [1, [248, 224, 150]]];
const SCH = { doek: houtskool, metaal: goud };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<!doctype html><body></body>');
  await page.evaluate((SCH) => {
    window.SCH = SCH;
    window.recolorB64 = async (b64) => {
      const r2h = (r, g, b) => { r /= 255; g /= 255; b /= 255;
        const mx = Math.max(r, g, b), mn = Math.min(r, g, b), dd = mx - mn; let h = 0;
        if (dd > 1e-6){ if (mx === r) h = ((g - b) / dd) % 6; else if (mx === g) h = (b - r) / dd + 2; else h = (r - g) / dd + 4; h *= 60; if (h < 0) h += 360; }
        return [h, mx > 0 ? dd / mx : 0, mx]; };
      const mapRamp = (L, ramp) => { for (let i = 1; i < ramp.length; i++){ if (L <= ramp[i][0]){ const a = ramp[i - 1], b = ramp[i], t = (L - a[0]) / (b[0] - a[0] || 1);
        return [0, 1, 2].map(k => Math.round(a[1][k] + (b[1][k] - a[1][k]) * t)); } } return ramp[ramp.length - 1][1]; };
      const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0);
      const d = ctx.getImageData(0, 0, c.width, c.height), p = d.data, S = window.SCH;
      for (let i = 0; i < p.length; i += 4){ if (p[i + 3] === 0) continue;
        const [h, s, v] = r2h(p[i], p[i + 1], p[i + 2]); let key = 'doek';
        if (v < 0.12) continue;                                   // donkere contour: zwart laten
        else if (v > 0.60 && s < 0.30) key = 'metaal';            // de lichte glans van het staal en de gespen -> goud
        else key = 'doek';                                        // het lijf en de kleding -> houtskool
        const L = Math.pow((0.299 * p[i] + 0.587 * p[i + 1] + 0.114 * p[i + 2]) / 255, 0.82);
        const o = mapRamp(L, S[key]); p[i] = o[0]; p[i + 1] = o[1]; p[i + 2] = o[2];
      }
      ctx.putImageData(d, 0, 0); return c.toDataURL('image/png');
    };
  }, SCH);

  const doFile = async (src, dst) => {
    const b64 = fs.readFileSync(src).toString('base64');
    const url = await page.evaluate((b) => window.recolorB64(b), b64);
    fs.writeFileSync(dst, Buffer.from(url.split(',')[1], 'base64'));
  };

  // loop de bandietmap recursief af: png omkleuren, json en txt meekopieren, mappen spiegelen
  let n = 0, kopie = 0;
  const walk = async (sub) => {
    const sd = path.join(SRC, sub), dd = path.join(DST, sub);
    fs.mkdirSync(dd, { recursive: true });
    for (const f of fs.readdirSync(sd)){
      const s = path.join(sd, f), d = path.join(dd, f);
      if (fs.statSync(s).isDirectory()){ await walk(path.join(sub, f)); continue; }
      if (f.endsWith('.png')){ await doFile(s, d); n++; if (n % 20 === 0) process.stdout.write(`\r${n} frames omgekleurd`); }
      else { fs.copyFileSync(s, d); kopie++; }
    }
  };
  fs.mkdirSync(DST, { recursive: true });
  await walk('');
  console.log(`\nklaar: ${n} frames omgekleurd, ${kopie} bestanden gekopieerd -> ${DST}`);
  await browser.close();
})();
