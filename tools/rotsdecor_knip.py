#!/usr/bin/env python3
"""Knipt de rotsdecor in design/rotsdecor/ uit de platen in design/rotsdecor/bron/.

Elke plaat is een rij losse rotsstukken uit Grok, op wit of op magenta. Dit script haalt
de achtergrond weg (alleen wat met de rand van de plaat verbonden is, zodat er nooit een
gat in een steen valt), rekent de roze of witte zweem uit de rand, en knipt elk stuk los.
Stukjes die dicht bij elkaar liggen (een puinhoopje) blijven een stuk.

Per plaat komt er <plaat>_01.png, _02.png enzovoort, van links naar rechts, strak
bijgesneden met een paar pixels marge.

    python3 tools/rotsdecor_knip.py

Daarna: python3 tools/gen-offline-manifest.py

Vereist Pillow, numpy en scipy.
"""
import glob, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'rotsdecor')
BRON = os.path.join(MAP, 'bron')

GROEPEER = 14      # pixels: stukjes binnen deze afstand horen bij elkaar
MIN_OPP = 400      # kleinere vlekjes zijn ruis
MARGE = 3


def met_rand_verbonden(masker):
    lab, _ = nd.label(masker)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(rand))


def soort_achtergrond(im):
    hoeken = [im[2, 2], im[2, -3], im[-3, 2], im[-3, -3]]
    r, g, b = np.mean(hoeken, axis=0)
    return 'magenta' if (r - g > 60 and b - g > 40) else 'wit'


def knip(pad):
    naam = os.path.splitext(os.path.basename(pad))[0]
    im = np.asarray(Image.open(pad).convert('RGB')).astype(np.float32)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    soort = soort_achtergrond(im)
    if soort == 'magenta':
        # hoe ver rood en blauw boven groen uitsteken; de rots is grijsbruin, r ~ g ~ b
        m = np.minimum(r - g, b - g)
        weg = met_rand_verbonden(m > 35)
        zacht = np.clip((m - 8) / 30.0, 0, 1)
    else:
        mn = np.minimum(np.minimum(r, g), b)
        weg = met_rand_verbonden(mn > 225)
        zacht = np.clip((mn - 150) / 90.0, 0, 1)

    alfa = np.where(weg, 0.0, 1.0)
    rand = nd.binary_dilation(weg, iterations=2) & ~weg
    alfa[rand] = 1.0 - zacht[rand]

    uit = im.copy()
    if soort == 'magenta':
        zoom = nd.binary_dilation(weg, iterations=4) & ~weg
        uit[..., 0] = np.where(zoom, np.minimum(r, g + 18), r)
        uit[..., 2] = np.where(zoom, np.minimum(b, g + 6), b)
    else:
        a = alfa[..., None]
        los = (im - 255.0 * (1 - a)) / np.maximum(a, 0.05)
        half = rand & (alfa > 0) & (alfa < 1)
        uit = np.where(half[..., None], np.clip(los, 0, 255), uit)

    voor = alfa > 0.05
    lab, n = nd.label(nd.binary_dilation(voor, iterations=GROEPEER))
    stukken = []
    for i in range(1, n + 1):
        sel = (lab == i) & voor
        if sel.sum() < MIN_OPP:
            continue
        ys, xs = np.where(sel)
        stukken.append((xs.min(), ys.min(), xs.max(), ys.max(), sel))
    stukken.sort(key=lambda s: s[0])

    for oud in glob.glob(os.path.join(MAP, naam + '_[0-9][0-9].png')):
        os.remove(oud)
    rgba = np.dstack([uit, alfa * 255]).clip(0, 255).astype(np.uint8)
    h, w = alfa.shape
    for k, (x0, y0, x1, y1, sel) in enumerate(stukken, 1):
        x0, y0 = max(0, x0 - MARGE), max(0, y0 - MARGE)
        x1, y1 = min(w - 1, x1 + MARGE), min(h - 1, y1 + MARGE)
        stuk = rgba[y0:y1 + 1, x0:x1 + 1].copy()
        # alleen dit stuk, niets van de buren
        stuk[..., 3] = np.where(sel[y0:y1 + 1, x0:x1 + 1], stuk[..., 3], 0)
        Image.fromarray(stuk).save(os.path.join(MAP, f'{naam}_{k:02d}.png'), optimize=True)
    print(f'{naam}: {len(stukken)} stukken ({soort})')


def main():
    platen = sorted(glob.glob(os.path.join(BRON, '*.jpg')) + glob.glob(os.path.join(BRON, '*.png')))
    if not platen:
        sys.exit('geen platen in ' + BRON)
    for p in platen:
        knip(p)


if __name__ == '__main__':
    main()
