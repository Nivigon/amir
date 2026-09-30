// Maakt de goudaap-reels uit de baviaan-spriteset.
//
//     node tools/goudaapje_kleur.js
//
// Uit enemies/baviaan/ komt enemies/goudaapje/: dezelfde baviaan, omgekleurd naar
// honinggoud met een blauw gezicht en een rode borst. De tekening zelf blijft staan;
// per kleurvlak wordt de helderheid op een eigen kleurladder gelegd (een gradient-map),
// zodat de vacht, de schaduwen en de contour precies blijven zoals ze getekend zijn en
// het toch echt goud wordt in plaats van olijf.
//
// Vier vlakken, elk herkend aan tint, verzadiging en helderheid van het origineel:
//   coat  de bruine vacht      -> honinggoud
//   cool  de blauwe snuit      -> helderblauw (blijft blauw, dat is de bijkleur)
//   red   de rode borst en streep -> rood (blijft rood)
//   limb  de grijze ledematen  -> goudbruin
// De donkere contour en de tanden blijven met opzet hun eigen kleur.
//
// Alleen de reeksen die het goudaapje in het spel gebruikt worden omgezet (niet het
// hoofdschudden, de pootslag of de opgefokte idle: die zijn voor de eindbaas-baviaan).
// De originelen in enemies/baviaan/ blijven staan als bron. Verandert er een frame,
// draai dit script dan opnieuw, en daarna tools/gen-offline-manifest.py.
//
// Nodig: node en playwright (npm i -g playwright).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.dirname(__dirname);
const SRC = path.join(ROOT, 'enemies', 'baviaan');
const DST = path.join(ROOT, 'enemies', 'goudaapje');
const REELS = ['hang_idle', 'afzet', 'val', 'landing', 'run', 'hap', 'brul', 'idle_grom', 'dood', 'sprong'];

// per vlak een helderheid -> kleur ladder (gradient-map)
const honey  = [[0, [104, 58, 18]], [0.30, [184, 120, 30]], [0.54, [226, 172, 52]], [0.72, [242, 202, 96]], [0.88, [250, 226, 150]], [1, [253, 246, 214]]];
const turq   = [[0, [8, 42, 56]], [0.40, [16, 112, 142]], [0.70, [42, 176, 206]], [1, [152, 228, 242]]];
const rood   = [[0, [70, 10, 8]], [0.50, [150, 26, 20]], [0.80, [202, 44, 32]], [1, [228, 92, 68]]];
const bruinL = [[0, [42, 28, 12]], [0.50, [96, 64, 28]], [1, [152, 112, 60]]];
const SCH = { coat: honey, cool: turq, red: rood, limb: bruinL };

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
        const [h, s, v] = r2h(p[i], p[i + 1], p[i + 2]); let key = null;
        if (v < 0.13) key = null;                                 // donkere contour: laten staan
        else if (s < 0.22 && v > 0.80) key = null;                // tanden en witte glans: laten staan
        else if (s > 0.14 && h >= 150 && h <= 265) key = 'cool';  // blauwe snuit
        else if (s > 0.32 && (h <= 18 || h >= 338)) key = 'red';  // rode borst en streep
        else if (s < 0.20) key = 'limb';                          // grijze ledematen
        else key = 'coat';                                        // vacht en de rest
        if (!key) continue;
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

  fs.mkdirSync(DST, { recursive: true });
  let n = 0;
  await doFile(path.join(SRC, 'baviaan.png'), path.join(DST, 'baviaan.png')); n++;
  for (const reel of REELS){
    const sd = path.join(SRC, reel), dd = path.join(DST, reel);
    fs.mkdirSync(dd, { recursive: true });
    for (const f of fs.readdirSync(sd).filter(x => x.endsWith('.png'))){ await doFile(path.join(sd, f), path.join(dd, f)); n++; }
    process.stdout.write(`\r${reel} klaar, totaal ${n} frames`);
  }
  fs.copyFileSync(path.join(SRC, 'idle_grom_metadata.json'), path.join(DST, 'idle_grom_metadata.json'));
  console.log(`\nklaar: ${n} frames -> ${DST}`);
  await browser.close();
})();
