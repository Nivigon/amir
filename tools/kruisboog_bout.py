#!/usr/bin/env python3
"""Knipt de bout van de kruisboogbandiet uit de plaat met vier pijlen.

De bron is enemies/kruisboog/bron/bout_bron.jpg: vier pijlen onder elkaar op wit, de punt naar links.
Dit script neemt de bovenste, haalt het wit eromheen weg (alleen het wit dat aan de rand vastzit, zodat
het lichte streepje tussen de veren blijft), legt de punt naar RECHTS en schrijft enemies/kruisboog/bout.png.
De schacht ligt precies op de middellijn van het plaatje: het spel tekent hem met de punt op de vliegrichting.

Daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kruisboog/bron/bout_bron.jpg')
UIT  = os.path.join(ROOT, 'enemies/kruisboog/bout.png')
STROOK = (0, 40, None, 270)   # de bovenste pijl (x0, y0, x1, y1 op de plaat)
BREED = 640                   # zo breed wordt de bout (px): ruim genoeg voor elk scherm
WIT = 228                     # lichter dan dit (in elk kanaal) en aan de rand vast: achtergrond


def main():
    im = Image.open(BRON).convert('RGB')
    x0, y0, x1, y1 = STROOK
    im = im.crop((x0, y0, x1 or im.width, y1))
    arr = np.array(im).astype(float)
    mn = arr.min(axis=2)

    # het wit dat aan de rand vastzit: vul vanuit de hoeken op een zwart-wit masker
    licht = Image.fromarray(((mn > WIT) * 255).astype(np.uint8)).copy()   # copy: anders is hij alleen-lezen
    for p in [(0, 0), (licht.width - 1, 0), (0, licht.height - 1), (licht.width - 1, licht.height - 1)]:
        if licht.getpixel(p) == 255: ImageDraw.floodfill(licht, p, 128)
    bg = np.array(licht) == 128

    # de rand zacht: twee pixels rond de achtergrond krijgen hun dekking uit hoe wit ze zijn
    rand = bg.copy()
    for _ in range(2):
        r = rand.copy()
        r[1:] |= rand[:-1]; r[:-1] |= rand[1:]; r[:, 1:] |= rand[:, :-1]; r[:, :-1] |= rand[:, 1:]
        rand = r
    a = np.ones(mn.shape)
    zacht = rand & ~bg
    a[zacht] = np.clip((255 - mn[zacht]) / 70, 0, 1)
    a[bg] = 0
    # de kleur los van het wit (ontmengen), zodat de rand niet licht oplicht
    rgb = (arr - 255 * (1 - a[..., None])) / np.maximum(a[..., None], 1e-3)
    rgba = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)

    ys, xs = np.where(a > 0.1)
    punt = xs.min()
    rij = int(round(ys[xs <= punt + 2].mean()))           # de schacht: waar de punt zit
    half = max(rij - ys.min(), ys.max() - rij) + 2        # symmetrisch om de schacht
    uit = Image.fromarray(rgba).crop((punt - 2, rij - half, xs.max() + 3, rij + half + 1))
    uit = uit.transpose(Image.FLIP_LEFT_RIGHT)            # de punt naar rechts
    uit = uit.resize((BREED, max(2, round(uit.height * BREED / uit.width))), Image.LANCZOS)
    uit.save(UIT, optimize=True)
    print('bout', uit.size, 'naar', os.path.relpath(UIT, ROOT))


if __name__ == '__main__':
    main()
