#!/usr/bin/env python3
"""Zonekaarten voor de val van Mkuki (karakters/amir/mkuki_spel/beweging/neer/), op kleur.

De val komt uit een Grok-clip, niet uit de Mkuki animeer tool, dus tools/mkuki_spel_zones.py kan hem niet bakken. Hier
leren we de kleuren van de kledingstukken van de zonekaarten die de tool wel gebakken heeft (de volle frames van de skin,
met hun <frame>_zones.png), en kleuren we daarmee elk val-frame in:
  1 broek #0000FF (donkergrijs), 2 schort #FFFF00 (zand), 3 riem #FF0000 (leer), 4 schuine band #00FF00 (leer),
  5 kralen #00FFFF (rood), 6 armbanden #FF8000 (koper). De rest (huid) blijft doorzichtig.

Per pixel: de kleur (RGB, HSV) en het gemiddelde in twee buurten eromheen (een randpixel van de broek ziet de broek
ernaast). Een random forest geeft per zone een kans; die kansen worden licht vervaagd (samenhangende stukken, geen ruis),
dan wint de grootste. Kleine losse stukjes vallen weg, gaatjes in een stuk gaan dicht, en een zone groeit over de donkere
omtrek van zijn kledingstuk heen tot de huid, zodat er na het omkleuren geen randje in de oude kleur blijft staan.

  python3 tools/neer_zones.py [--toon uit.png]

Schrijft neer_NN_zones.png naast elk frame, en de helft in klein/ (NEAREST, zoals tools/mkuki_spel_zones.py).
"""
import glob, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIN = os.path.join(REPO, 'karakters/amir/mkuki_spel/')
MAP = 'karakters/amir/mkuki_spel/beweging/neer/'
KAART = [(0, 0, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 255, 255), (255, 128, 0)]
OMTREK = 2                 # zoveel pixels groeit een kledingstuk over de donkere omtrek (v onder OMTREK_LUM) heen
OMTREK_LUM = 45
RG = {'kraal_s': 0.68, 'band_v': 150, 'schort_v': 105, 'leer_s': 0.63, 'leer_h': 16, 'broek_s': 0.24, 'riem_bij': 4, 'band_max': 600}
BAND_HALF = 3.0         # de halve breedte van de schuine band rond zijn lijn


def hsv(im):
    rgb = im[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    dd = np.maximum(d, 1e-6)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) * 60
    return np.where(d > 0, h, 0), s, mx * 255


def stukken(M, minimum):
    l, n = nd.label(M, structure=np.ones((3, 3)))
    if not n:
        return M
    sz = nd.sum(M, l, range(1, n + 1))
    return np.isin(l, [i + 1 for i, v in enumerate(sz) if v >= minimum])


# De schuine band per sleutelframe: een lijn van de kralen door de gesp naar beneden (in framepixels), op het oog gezet;
# de frames ertussen schuiven mee (lineair). Op kleur is de band niet te vinden: hij is bijna net zo bruin als de huid.
BAND_LIJN = {
        0: [(304,91), (275,117), (271,128)],
        4: [(294,94), (274,122), (271,131)],
        8: [(273,109), (267,145), (265,155)],
        10: [(270,134), (265,169), (262,184)],
        12: [(266,160), (254,199), (252,212)],
        14: [(250,186), (248,221), (261,230)],
        16: [(232,212), (252,234), (268,246)],
        20: [(238,226), (255,240), (268,250)],
        24: [(240,232), (262,245), (275,250)],
        28: [(243,238), (258,247), (272,252)],
        32: [(220,234), (240,255), (258,263)],
        36: [(218,247), (236,271), (261,282)],
        40: [(220,255), (235,274), (254,284)],
        45: [(218,253), (233,275), (256,285)] }


def band_lijn(i):
    ks = sorted(BAND_LIJN)
    if i in BAND_LIJN:
        return BAND_LIJN[i]
    a = max(k for k in ks if k < i); b = min(k for k in ks if k > i); t = (i - a) / (b - a)
    return [(pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t) for pa, pb in zip(BAND_LIJN[a], BAND_LIJN[b])]


def schuine_band(i, shape, vrij):
    """Alles binnen BAND_HALF van de lijn van frame i dat nog geen ander kledingstuk is."""
    H, W = shape
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    M = np.zeros(shape, bool)
    P = band_lijn(i)
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        dx, dy = x1 - x0, y1 - y0
        t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / float(dx * dx + dy * dy), 0, 1)
        M |= np.hypot(xx - (x0 + t * dx), yy - (y0 + t * dy)) <= BAND_HALF
    return M & vrij


def kaart(im, fi):
    h, s, v = hsv(im)
    op = im[..., 3] > 0
    huidig = op & (im[..., 3] > 60)
    kraal = huidig & ((h <= 13) | (h >= 345)) & (s >= RG['kraal_s']) & (v >= 60)
    band = huidig & (h >= 14) & (h <= 30) & (s >= 0.52) & (v >= RG['band_v'])
    schort = huidig & (h >= 22) & (h <= 45) & (s >= 0.18) & (s < 0.6) & (v >= RG['schort_v']) & ~band
    leer = huidig & (h >= RG['leer_h']) & (h <= 32) & (s >= RG['leer_s']) & (v >= 38) & (v < RG['band_v']) & ~kraal
    # de broek: grijs, of in een paar frames met een paarse zweem (Grok) blauwpaars en donker
    broek = huidig & (v >= 22) & (v < 125) & ((s < RG['broek_s']) | ((h >= 200) & (h <= 290) & (s < 0.62) & (v < 110)))
    # opruimen: kleine stukjes weg, gaatjes dicht
    broek = stukken(nd.binary_opening(broek, structure=np.ones((2, 2))), 150)
    broek = nd.binary_fill_holes(nd.binary_closing(broek, structure=np.ones((3, 3)))) & op
    schort = stukken(schort, 30)
    # de schort groeit door in zijn vale, groenig getinte randen (de flap achter het been): licht en niet rood
    huid = (h <= 20) & (s >= 0.33)
    vaal = huidig & (v >= 40) & (h >= 24) & (h <= 110) & (s < 0.7) & ~band & ~huid & ~broek & ~kraal
    schort = nd.binary_propagation(schort, structure=np.ones((3, 3)), mask=schort | vaal)
    schort = nd.binary_fill_holes(nd.binary_closing(schort, structure=np.ones((3, 3)))) & op & ~broek
    kraal = nd.binary_closing(kraal, structure=np.ones((3, 3))) & op
    l, n = nd.label(kraal, structure=np.ones((3, 3)))
    if n:                                             # het snoer is een (of twee) grote stukken; losse rode randjes weg
        sz = nd.sum(kraal, l, range(1, n + 1))
        kraal = np.isin(l, [i + 1 for i, v in enumerate(sz) if v >= max(10, 0.25 * sz.max())])
    band = stukken(nd.binary_closing(band, structure=np.ones((3, 3))) & op & ~schort & ~kraal, 8)
    leer = stukken(nd.binary_closing(leer, structure=np.ones((2, 2))) & op & ~schort & ~broek & ~band & ~kraal, 10)
    # een armband die tegen de schort aan ligt is een fel stuk schort
    l, n = nd.label(band, structure=np.ones((3, 3)))
    bijS = nd.binary_dilation(schort, iterations=2)
    for i in range(1, n + 1):
        C = l == i
        rand = C & ~nd.binary_erosion(C)
        # een armband raakt de schort hooguit met een stukje rand (de hand op de heup); een fel stuk schort ligt er half in
        if (bijS & rand).sum() > 0.35 * rand.sum() or C.sum() > RG['band_max']:
            schort |= l == i; band &= l != i
    # leer vlak bij de schort is de riem
    bij = nd.binary_dilation(schort, iterations=RG['riem_bij'])
    l, n = nd.label(leer, structure=np.ones((3, 3)))
    riem = np.isin(l, [i for i in range(1, n + 1) if (bij & (l == i)).any()])
    schuin = schuine_band(fi, op.shape, (im[..., 3] > 128) & ~broek & ~schort & ~kraal & ~band & ~riem)
    uit = np.zeros(op.shape, np.int8)
    for k, M in ((1, broek), (2, schort), (3, riem), (4, schuin), (5, kraal), (6, band)):
        uit[M & (uit == 0)] = k
    # de omtrek: donkere randpixels naast een kledingstuk horen erbij (anders een randje in de oude kleur)
    donker = op & (v < OMTREK_LUM)
    for _ in range(OMTREK):
        vrij = donker & (uit == 0)
        nieuw = np.zeros_like(uit)
        for k in (1, 2, 5, 6, 3, 4):
            g = nd.binary_dilation(uit == k, structure=np.ones((3, 3))) & vrij & (nieuw == 0)
            nieuw[g] = k
        uit[nieuw > 0] = nieuw[nieuw > 0]
    z = np.zeros(op.shape + (4,), np.uint8)
    for k, c in enumerate(KAART):
        z[uit == k + 1] = c + (255,)
    return z, uit


def main():
    toon = sys.argv[sys.argv.index('--toon') + 1] if '--toon' in sys.argv else None
    tegels = []
    for fp in sorted(glob.glob(os.path.join(REPO, MAP, 'neer_[0-9][0-9].png'))):
        im = np.array(Image.open(fp).convert('RGBA'))
        z, uit = kaart(im, int(os.path.basename(fp)[5:7]))
        H, W = z.shape[:2]
        zp = fp[:-4] + '_zones.png'
        Image.fromarray(z).save(zp, optimize=True)
        k = os.path.join(REPO, 'klein', os.path.relpath(zp, REPO))
        Image.fromarray(z).resize((max(1, W // 2), max(1, H // 2)), Image.NEAREST).save(k, optimize=True)
        tel = [int((uit == i).sum()) for i in range(1, 7)]
        print(os.path.basename(fp), 'broek %d schort %d riem %d band %d kralen %d banden %d' % tuple(tel))
        if toon:
            c = Image.new('RGBA', (W, H), (128, 128, 128, 255)); c.alpha_composite(Image.fromarray(im))
            o = z.copy(); o[..., 3] = (o[..., 3] > 0) * 200; d = c.copy(); d.alpha_composite(Image.fromarray(o))
            bb = Image.fromarray(im).getbbox()
            t = Image.new('RGBA', ((bb[2] - bb[0]) * 2 + 4, bb[3] - bb[1]), (0, 0, 0, 255))
            t.paste(c.crop(bb), (0, 0)); t.paste(d.crop(bb), (bb[2] - bb[0] + 4, 0)); tegels.append(t)
    if toon:
        w = max(t.width for t in tegels); h = max(t.height for t in tegels)
        kol = 3
        vel = Image.new('RGBA', (w * kol, h * ((len(tegels) + kol - 1) // kol)), (0, 0, 0, 255))
        for k, t in enumerate(tegels):
            vel.paste(t, ((k % kol) * w, (k // kol) * h))
        vel.save(toon)


if __name__ == '__main__':
    main()
