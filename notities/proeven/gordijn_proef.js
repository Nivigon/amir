// Proef: gordijnen in de deurgaten, met wind. Vervangt de houten deur (stadDeurPlaatTeken).
window.GORD = (() => {
  const namen = ['indigo_streep', 'adire', 'bogolan', 'rood_oker', 'geel', 'olijf', 'terracotta'];
  const ims = {};
  for (const n of namen){ const im = new Image(); im.src = 'design/stad/gordijn/' + n + '.png'; ims[n] = im; }
  const G = { namen, ims, keuze: {}, wind: 1, cache: {} };
  // het gat in het deur-canvas (351 x 448): x 119, y 30, 214 x 413
  const ROD_W = 236, CX = 226, TOP = 30;
  function bron(n){                       // het gordijn op doelmaat, een keer
    if (G.cache[n]) return G.cache[n];
    const im = ims[n]; if (!im.complete || !im.naturalWidth) return null;
    const w = ROD_W, h = Math.round(im.naturalHeight * w / im.naturalWidth);
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(im, 0, 0, w, h);
    g.globalCompositeOperation = 'multiply'; g.fillStyle = 'rgba(214,170,128,0.45)'; g.fillRect(0, 0, w, h);
    g.globalCompositeOperation = 'destination-in'; g.drawImage(im, 0, 0, w, h); g.globalCompositeOperation = 'source-over';
    // de spleet tussen de banen: de breedste doorzichtige strook rond het midden
    const d = g.getImageData(0, 0, w, h).data; let spleet = 0, m = Math.round(w / 2);
    for (let y = Math.round(h * 0.1); y < h * 0.9; y += 4){
      let l = m, r = m;
      while (l > m - 40 && d[(y * w + l) * 4 + 3] < 128) l--;
      while (r < m + 40 && d[(y * w + r) * 4 + 3] < 128) r++;
      spleet = Math.max(spleet, r - l);
    }
    c.spleet = spleet; G.cache[n] = c; return c;
  }
  const doeken = {};
  G.teken = function(gi, o){
    o = o || { cw: 351, ch: 448, cx: 226, top: 30, rodW: 236, sq: 1, key: gi };
    const n = G.keuze[gi] || namen[gi % namen.length];
    const src = bron(n); if (!src) return null;
    const c = doeken[o.key] || (doeken[o.key] = document.createElement('canvas'));
    c.width = o.cw; c.height = o.ch;
    const k0 = o.rodW / ROD_W;
    const g = c.getContext('2d');
    const t = performance.now() / 1000, ph = gi * 1.7;
    // vlagen: een rustige ademhaling met af en toe een windstoot
    const vlaag = G.vlaagVast != null ? G.vlaagVast : 0.55 + 0.25 * Math.sin(t * 0.45 + ph) + 0.35 * Math.max(0, Math.sin(t * 0.23 + ph * 0.5)) ** 3;
    const A = 20 * k0 * G.wind * vlaag;
    const w = src.width, h = src.height, rod = Math.round(h * 0.075), mid = Math.round(w / 2);
    const x0 = o.cx - w * k0 / 2, y0 = o.top + 2, sq = o.sq * k0;
    g.drawImage(src, 0, 0, w, rod, x0, y0, w * k0, rod * sq);            // de stok staat stil
    // in rust vallen de banen over elkaar; bij een vlaag wijken ze onderaan even uiteen
    const open = Math.min(1, Math.max(0, (vlaag - 0.85) / 0.35)) * G.wind;
    const panelen = [[mid, w - mid, 1.3, 1], [0, mid, 0, 0]];       // de linker baan valt over de rechter
    for (const [sx, sw, pp, rechts] of panelen){
      for (let y = rod; y < h; y += 2){
        const fr = (y - rod) / (h - rod), k = Math.pow(fr, 1.35);
        const golf = 0.65 * Math.sin(t * 1.8 + y * 0.016 + ph + pp) + 0.35 * Math.sin(t * 3.3 + y * 0.045 + ph * 2 + pp);
        const dx = A * k * (golf + 0.9);                          // duwt mee met de wind, en golft
        const lift = 1 - 0.07 * G.wind * vlaag * k;               // de onderkant tilt een beetje op
        const extra = (src.spleet / 2 + 3) * (1 - open * Math.min(1, fr * 1.6)) * k0;   // zoveel trekt de baan naar het midden
        const dxo = rechts ? dx - extra + open * 4 * k * k0 : dx;
        g.drawImage(src, sx, y, sw, 2, x0 + sx * k0 + dxo, y0 + (rod + (y - rod) * lift) * sq, sw * k0 + extra, 2.6 * sq);
      }
    }
    // bewegende plooien: zachte verticale banden van licht en donker, alleen op de stof
    g.globalCompositeOperation = 'source-atop';
    const gr = g.createLinearGradient(x0, 0, x0 + w * k0, 0);
    for (let i = 0; i <= 12; i++){
      const u = i / 12, s = Math.sin(u * 19 + t * 2.1 + ph) * Math.sin(u * 7 - t * 0.9);
      gr.addColorStop(u, s > 0 ? 'rgba(255,240,220,' + (0.10 * s * vlaag).toFixed(3) + ')' : 'rgba(20,10,5,' + (-0.18 * s * vlaag).toFixed(3) + ')');
    }
    g.fillStyle = gr; g.fillRect(0, y0 + rod * sq, o.cw, o.ch);
    g.globalCompositeOperation = 'source-over';
    return c;
  };
  return G;
})();

const stadDeurPlaatOud = stadDeurPlaatTeken;
stadDeurPlaatTeken = function(gi, v, fy, f, lat, vanzelf, maat){
  if (GORD.mix && !GORD.keuze[gi]) return stadDeurPlaatOud(gi, v, fy, f, lat, vanzelf, maat);
  const D = STAD_DEUR, s = (v ? D.boven : 1) * (maat || 1);
  const latTop = fy - D.posten[3] * s * f - D.latei[3] * s * f + 1;
  if (!v){
    const im = GORD.teken(gi);
    if (im) ctx.drawImage(im, (D.midden + (D.plaatX - D.midden) * s) * f, fy - DEUR.grond * s * f, DEUR.canvas[0] * s * f, DEUR.canvas[1] * s * f);
  }
  const sx = (D.midden + (D.latei[0] - D.midden) * s) * f, sw = D.latei[2] * s * f, sy = latTop + D.latei[3] * s * f, sh = 14 * s * f;
  const gr = ctx.createLinearGradient(0, sy, 0, sy + sh);
  gr.addColorStop(0, 'rgba(30,16,8,0.45)'); gr.addColorStop(1, 'rgba(30,16,8,0)');
  ctx.fillStyle = gr; ctx.fillRect(sx + 8 * s * f, sy, sw - 16 * s * f, sh);
  lat(latTop);
};

// binnen: de deur naar buiten (binnen/deur_recht.png, 772 x 892, opening x 155..615, y 218..820)
// je ziet de achterkant van het doek, met daglicht van de straat erachter
const binnenPlaatOud = binnenPlaat;
binnenPlaat = function(im, x, voet, breed, groundY, scale, cx, f){
  binnenPlaatOud(im, x, voet, breed, groundY, scale, cx, f);
  if (!binnenImgs || im !== binnenImgs.deur) return;
  const h = breed * im.naturalHeight / im.naturalWidth, sx = cx + (x - world) - breed / 2, sy = groundY - voet * scale - h, k = breed / 772;
  // donker achter het doek
  const gr = ctx.createLinearGradient(0, sy + 218 * k, 0, sy + 820 * k);
  gr.addColorStop(0, 'rgba(14,8,6,0.97)'); gr.addColorStop(1, 'rgba(26,16,12,0.92)');
  ctx.fillStyle = gr; ctx.fillRect(sx + 160 * k, sy + 222 * k, 450 * k, 598 * k);
  const c = GORD.teken(window.GORD_BINNEN || 0, { cw: 772, ch: 892, cx: 386, top: 206, rodW: 480, sq: 0.80, key: 'binnen' });
  if (!c) return;
  ctx.save(); ctx.translate(sx + breed, sy); ctx.scale(-1, 1);          // de achterkant: gespiegeld
  ctx.drawImage(c, 0, 0, breed, h); ctx.restore();
};
