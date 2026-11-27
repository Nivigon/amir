#!/usr/bin/env python3
"""Riem (zone 3, #FF0000) en schuine band (zone 4, #00FF00) in de zonekaarten van de shove (Mkuki, SHOVE).

De shove-frames komen uit een Grok-clip, niet uit de Mkuki animeer tool, dus tools/mkuki_spel_zones.py kan ze niet bakken
(dat script bakt de zonekaarten van de tool-frames uit de mkuki-checkout). De kaarten waren op kleur geraden en hadden de
riem en de band niet. Dit script zet ze erbij, op de kaarten die er al liggen:

- de riem: het donkere leer bovenaan de schort. De schort en de broek worden dichtgemaakt (closing), en wat daarbinnen in
  een strook onder de bovenrand donker is (luminantie onder RIEM_LUM, niet-zone of schort) is riem. Zo valt ook de
  donkere wikkel over de schort in de duwframes (8 tot 12) eronder, en blijft de lichte omslag van de schort geel.
- de schuine band: alleen te zien in de frames waar de borst vrij is (0 tot 2; daarna zitten de armen ervoor). Per frame
  een middellijn (BAND), alles wat ondoorzichtig is binnen BAND_HALF ervan en nog geen zone heeft (geen kralen).

Schrijft shove_NN_zones.png en shove_NN_lijf_zones.png (die zijn gelijk) en de helft in klein/ (NEAREST, zoals
tools/mkuki_spel_zones.py). Draai het een keer op de kaarten zonder riem: een tweede keer vindt dezelfde pixels terug.

  python3 tools/shove_zones.py [--toon uit.png]
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = 'karakters/amir/mkuki_spel/aanval/shove/'
N = 13
GEEL, BLAUW, ROOD, GROEN = (255, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)
RIEM_SLUIT, RIEM_STROOK, RIEM_LUM, RIEM_OPZIJ = 10, 20, 105, 8
BAND = {0: [((336, 79), (297, 128))], 1: [((333, 92), (312, 136))], 2: [((321, 135), (319, 151))]}
BAND_HALF = 3.2


def kleur(z, c):
    return (z[..., :3] == c).all(-1) & (z[..., 3] > 0)


def riem(im, z):
    zon = z[..., 3] > 0
    S = kleur(z, GEEL) | kleur(z, ROOD)               # rood: een kaart waar de riem al in staat
    SB = S | kleur(z, BLAUW)
    r = RIEM_SLUIT
    st = nd.iterate_structure(nd.generate_binary_structure(2, 1), r)
    C = nd.binary_closing(np.pad(SB, r + 2), structure=st)[r + 2:-r - 2, r + 2:-r - 2] | SB
    lum = im[..., :3] @ [0.3, 0.59, 0.11]
    op = im[..., 3] > 128
    H = C.shape[0]
    yy = np.arange(H)[:, None]
    top = np.where(C.any(0), C.argmax(0), H)[None, :]
    B = (yy >= top - 2) & (yy <= top + RIEM_STROOK) & op & (lum < RIEM_LUM) & (S | (~zon & C))
    B = nd.binary_opening(B, structure=np.ones((2, 2)))
    lab, n = nd.label(B)
    if n:
        sz = nd.sum(B, lab, range(1, n + 1))
        B = np.isin(lab, [k + 1 for k, v in enumerate(sz) if v >= max(15, 0.1 * sz.max())])
    B = nd.binary_closing(B, structure=np.ones((3, 3))) & op & C
    # de riem loopt opzij door voorbij de schort, tot de rand van het lijf: per rij hooguit RIEM_OPZIJ pixels verder
    vrij = op & ~zon & (lum < RIEM_LUM)
    for _ in range(RIEM_OPZIJ):
        B |= nd.binary_dilation(B, structure=np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]], bool)) & vrij
    return B


def band(im, z, lijnen):
    H, W = z.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    M = np.zeros((H, W), bool)
    for (x0, y0), (x1, y1) in lijnen:
        dx, dy = x1 - x0, y1 - y0
        t = np.clip(((xx - x0) * dx + (yy - y0) * dy) / float(dx * dx + dy * dy), 0, 1)
        M |= np.hypot(xx - (x0 + t * dx), yy - (y0 + t * dy)) <= BAND_HALF
    rgb = im[..., :3]
    kraal = (rgb[..., 0] > 100) & (rgb[..., 0] > 1.8 * rgb[..., 1])
    return M & (im[..., 3] > 128) & ((z[..., 3] == 0) | kleur(z, GROEN)) & ~kraal


def main():
    toon = sys.argv[sys.argv.index('--toon') + 1] if '--toon' in sys.argv else None
    tegels = []
    for i in range(N):
        b = os.path.join(REPO, MAP, 'shove_%02d' % i)
        im = np.array(Image.open(b + '_lijf.png').convert('RGBA')).astype(int)
        z = np.array(Image.open(b + '_zones.png').convert('RGBA'))
        R = riem(im, z)
        G = band(im, z, BAND.get(i, [])) & ~R
        z[R] = ROOD + (255,)
        z[G] = GROEN + (255,)
        uit = Image.fromarray(z)
        H, W = z.shape[:2]
        for naam in ('_zones.png', '_lijf_zones.png'):
            uit.save(b + naam, optimize=True)
            k = os.path.join(REPO, 'klein', MAP, 'shove_%02d' % i + naam)
            uit.resize((max(1, W // 2), max(1, H // 2)), Image.NEAREST).save(k, optimize=True)
        print('shove_%02d: riem %d, band %d pixels' % (i, R.sum(), G.sum()))
        if toon:
            c = Image.new('RGBA', (W, H), (128, 128, 128, 255)); c.alpha_composite(Image.fromarray(im.astype(np.uint8)))
            o = z.copy(); o[..., 3] = (o[..., 3] > 0) * 170; d = c.copy(); d.alpha_composite(Image.fromarray(o))
            bb = Image.fromarray(im.astype(np.uint8)).getbbox()
            t = Image.new('RGBA', ((bb[2] - bb[0]) * 2 + 4, bb[3] - bb[1]), (0, 0, 0, 255))
            t.paste(c.crop(bb), (0, 0)); t.paste(d.crop(bb), (bb[2] - bb[0] + 4, 0)); tegels.append(t)
    if toon:
        w = max(t.width for t in tegels); h = max(t.height for t in tegels)
        vel = Image.new('RGBA', (w * 4, h * 4), (0, 0, 0, 255))
        for k, t in enumerate(tegels):
            vel.paste(t, ((k % 4) * w, (k // 4) * h))
        vel.save(toon)


if __name__ == '__main__':
    main()
