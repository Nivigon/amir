#!/usr/bin/env python3
"""Kleurt de kooiman-sprites om naar het bandietpalet, en maakt de kooi zwart-doorschijnend.

De aangeleverde frames (teal hoofddoek, blauw gewaad, groene broek, grijze kooivulling)
staan ongewijzigd in enemies/kooiman/bron/<set>/. Dit script leest die bron en schrijft de
speelversie naar enemies/kooiman/<set>/, zodat de kooiman in exact dezelfde kleuren loopt als
de bandiet:

  hoofddoek en gewaad -> marineblauw, de echte kleurtrap van de bandietjas (#201f3c, plooien
                         tot #15152d), opgemeten uit enemies/bandiet/idle/idle_00.png
  broek               -> kaki-olijf, de bandietbroek (#534b39, lichte kant #74725d)
  rode sjerp, huid, sandalen, de kooitralies: ongemoeid
  kooivulling         -> van (32,32,38) op 50% alpha naar puur zwart (0,0,0) op 50% alpha

De herkleuring behoudt de schaduwen: per kledingvlak wordt de helderheid van de bron op de
kleurtrap van de bandiet gelegd. De helderheidsgrenzen worden over alle frames samen bepaald,
zodat er geen flikkering tussen frames ontstaat.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kooiman/bron')
UIT  = os.path.join(ROOT, 'enemies/kooiman')
SETS = ('drag', 'smash', 'recovery')

def hx(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)

# De echte bandiettrappen (opgemeten): (positie 0..1 van donker naar licht, kleur)
COAT  = [(0.0, hx('#121127')), (0.45, hx('#201f3c')), (0.8, hx('#201f3c')), (1.0, hx('#2a2a49'))]
PANTS = [(0.0, hx('#473f30')), (0.5, hx('#534b39')), (0.85, hx('#5c5340')), (1.0, hx('#74725d'))]
# neutrale taupe voor de tralies, waar nu het gele glinsteren op zit (op helderheid)
TRALIE = [(0.0, hx('#2b2822')), (0.55, hx('#554e42')), (1.0, hx('#6f665a'))]

def hsv(rgb):
    a = rgb.astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); df = mx - mn
    val = mx
    sat = np.where(mx == 0, 0, df / np.where(mx == 0, 1, mx))
    hue = np.zeros_like(mx); m = df > 1e-6; dd = np.where(df == 0, 1, df)
    ir = (mx == r) & m; hue[ir] = ((g - b) / dd * 60 % 360)[ir]
    ig = (mx == g) & m; hue[ig] = ((b - r) / dd * 60 + 120)[ig]
    ib = (mx == b) & m; hue[ib] = ((r - g) / dd * 60 + 240)[ib]
    return hue, sat, val

def _dilate(mk):
    o = mk.copy()
    o[:-1, :] |= mk[1:, :]; o[1:, :] |= mk[:-1, :]
    o[:, :-1] |= mk[:, 1:]; o[:, 1:] |= mk[:, :-1]
    return o
def clean(mk):
    return _dilate(~_dilate(~_dilate(mk)))   # dilate(erode(dilate)): gaatjes dicht, 1px uitlopen

def masks(rgba):
    rgb = rgba[..., :3]; al = rgba[..., 3]
    hue, sat, val = hsv(rgb)
    op = al > 180
    def band(h0, h1, smin):
        hm = ((hue >= h0) & (hue < h1)) if h0 <= h1 else ((hue >= h0) | (hue < h1))
        return hm & (sat >= smin) & (val >= 0.08) & op
    robe  = clean(band(200, 250, 0.28)) & op
    scarf = clean(band(168, 200, 0.28)) & op
    pants = clean(band(78, 150, 0.20)) & op
    scarf = scarf & ~robe
    pants = pants & ~robe & ~scarf
    # kooivulling: semi-transparant en donker
    cage = (al > 100) & (al < 165) & (rgb.max(-1) < 80)
    # gele glinsteringen op de tralies (restant van de oude gele kooi). In de bron is de
    # broek nog groen (hue ~90-120), dus dit geel is alleen de kooi, geen kleding.
    geel = (hue >= 40) & (hue < 80) & (sat >= 0.20) & (val >= 0.34) & op
    return robe, scarf, pants, cage, geel

def lum_of(rgb):
    return (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255.0

def rampmap(out, mask, stops, lo, hi):
    if mask.sum() == 0:
        return
    l = lum_of(out)[mask]
    t = np.clip((l - lo) / max(hi - lo, 1e-3), 0, 1)
    pos = np.array([s[0] for s in stops]); cols = np.array([s[1] for s in stops])
    oc = np.empty((len(t), 3))
    for c in range(3):
        oc[:, c] = np.interp(t, pos, cols[:, c])
    out[mask] = oc

def rampval(out, mask, stops):
    """Als rampmap, maar op de eigen helderheid (max-kanaal) van de bronpixel, 0..1."""
    if mask.sum() == 0:
        return
    t = out[mask].max(-1) / 255.0
    pos = np.array([s[0] for s in stops]); cols = np.array([s[1] for s in stops])
    oc = np.empty((len(t), 3))
    for c in range(3):
        oc[:, c] = np.interp(t, pos, cols[:, c])
    out[mask] = oc

def main():
    files = []
    for s in SETS:
        for f in sorted(glob.glob(os.path.join(BRON, s, '*.png'))):
            files.append((s, f))
    if not files:
        sys.exit('geen bronframes gevonden in ' + BRON)

    # pas 1: helderheidsgrenzen per kledingvlak over alle frames samen
    acc = {'robe': [], 'scarf': [], 'pants': []}
    cache = {}
    for s, f in files:
        rgba = np.asarray(Image.open(f).convert('RGBA')).astype(np.float32)
        robe, scarf, pants, cage, geel = masks(rgba)
        cache[f] = (rgba, robe, scarf, pants, cage, geel)
        L = lum_of(rgba[..., :3])
        acc['robe'].append(L[robe]); acc['scarf'].append(L[scarf]); acc['pants'].append(L[pants])
    grens = {}
    for k, v in acc.items():
        allv = np.concatenate([a for a in v if len(a)])
        grens[k] = (np.percentile(allv, 4), np.percentile(allv, 96))

    # pas 2: herkleuren en wegschrijven
    n = 0
    for s, f in files:
        rgba, robe, scarf, pants, cage, geel = cache[f]
        out = rgba.copy()
        # eerst het gele glinsteren van de tralies neutraliseren (op de bron, voor de kleding)
        rampval(out[..., :3], geel, TRALIE)
        rampmap(out[..., :3], robe,  COAT,  *grens['robe'])
        rampmap(out[..., :3], scarf, COAT,  *grens['scarf'])
        rampmap(out[..., :3], pants, PANTS, *grens['pants'])
        # kooivulling puur zwart, alpha ongemoeid (blijft 50%)
        out[..., 0][cage] = 0; out[..., 1][cage] = 0; out[..., 2][cage] = 0
        dst = os.path.join(UIT, s, os.path.basename(f))
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst)
        n += 1
    print(f'{n} frames omgekleurd naar het bandietpalet, kooi zwart op 50% alpha')
    print('grenzen', {k: (round(a, 3), round(b, 3)) for k, (a, b) in grens.items()})

if __name__ == '__main__':
    main()
