#!/usr/bin/env python3
"""Knipt de deurgordijnen uit de Grok-platen in design/stad/gordijn/bron/ (zie notities/gordijnen.md).

Elke plaat heeft drie gordijnen naast elkaar op wit. Het script haalt het wit weg (ook de witte
stukjes tussen de stok en het doek, niet alleen wat aan de rand vastzit), knipt de drie los en
rekt het middenstuk van het doek 1,14 keer in de hoogte (de stok en de rafels houden hun maat),
zodat het gordijn de verhouding van het deurgat krijgt. Daarna gen-klein.py en gen-offline-manifest.py.

    python3 tools/gordijn_knip.py
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

HIER = os.path.join(os.path.dirname(__file__), '..', 'design', 'stad', 'gordijn')
PLATEN = [
    ('gordijn_streep_grok.jpg', [None, 'indigo_streep', None]),   # de middelste van de drie
    ('gordijn_patroon_grok.png', ['adire', 'bogolan', 'rood_oker']),
    ('gordijn_effen_grok.png', ['geel', 'olijf', 'terracotta']),
]
REK = 1.14                 # zoveel langer wordt het doek
MIDDEN = (0.10, 0.86)      # het stuk dat meerekt, als deel van de hoogte (onder de stok tot boven de rafels)


def knip(pad, namen):
    im = np.array(Image.open(pad).convert('RGB')).astype(float)
    d = 255 - im.min(axis=2)                       # afstand tot wit
    sat = im.max(axis=2) - im.min(axis=2)
    wit = (d < 22) & (sat < 14)
    fg = ndimage.binary_opening(~wit, iterations=1)
    alfa = fg.astype(float)
    rand = fg & ~ndimage.binary_erosion(fg, iterations=2)
    alfa[rand] = np.clip(d[rand] / 40, 0.35, 1)     # zachte rand, geen witte halo
    kol = np.where(fg.any(axis=0))[0]
    groepen = np.split(kol, np.where(np.diff(kol) > 20)[0] + 1)
    for g, naam in zip(groepen, namen):
        if not naam:
            continue
        x0, x1 = g[0], g[-1] + 1
        rij = np.where(fg[:, x0:x1].any(axis=1))[0]
        y0, y1 = rij[0], rij[-1] + 1
        rgba = np.dstack([im[y0:y1, x0:x1], alfa[y0:y1, x0:x1] * 255]).astype(np.uint8)
        g_im = Image.fromarray(rgba, 'RGBA')
        W, H = g_im.size
        a, b = int(H * MIDDEN[0]), int(H * MIDDEN[1])
        boven = g_im.crop((0, 0, W, a))
        mid = g_im.crop((0, a, W, b)).resize((W, int((b - a) * REK)), Image.LANCZOS)
        onder = g_im.crop((0, b, W, H))
        uit = Image.new('RGBA', (W, boven.height + mid.height + onder.height))
        uit.paste(boven, (0, 0)); uit.paste(mid, (0, a)); uit.paste(onder, (0, a + mid.height))
        uit.save(os.path.join(HIER, naam + '.png'))
        print(naam, uit.size)


for bestand, namen in PLATEN:
    knip(os.path.join(HIER, 'bron', bestand), namen)
