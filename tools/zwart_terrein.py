#!/usr/bin/env python3
"""Maakt de zwarte varianten van de solide terreinstukken voor de nieuwe stijl.

Elk stuk wordt egaal zwart gemaakt: de vulling wordt zwart en alleen de vorm
(de alfa) blijft. Geen randlicht of richeltextuur: gewoon een zwart silhouet.
De achtergrond-steen (rots_vulling) blijft juist zichtbaar en wordt dus niet
omgekleurd.

Verandert een bron, draai dit opnieuw, en daarna gen-klein.py en
gen-offline-manifest.py.
"""
import numpy as np
from PIL import Image


def zwart(src, out):
    im = Image.open(src).convert('RGBA')
    arr = np.asarray(im).astype(np.uint8)
    a = arr[..., 3]
    rgb = np.zeros((a.shape[0], a.shape[1], 3), np.uint8)   # egaal zwart
    res = np.concatenate([rgb, a[..., None]], -1)
    Image.fromarray(res, 'RGBA').save(out)
    print('ok', out, im.size)


JOBS = [
    ('design/grondrand.png',              'design/zwart/grondrand.png'),
    ('design/grondrand_rots.png',         'design/zwart/grondrand_rots.png'),
    ('design/klimmen/klif_bovenrand.png', 'design/zwart/klif_bovenrand.png'),
    ('design/grot/plafond_strook.png',    'design/zwart/plafond_strook.png'),
    ('design/grot/wand_rand.png',         'design/zwart/wand_rand.png'),
    ('design/grot/wand_richel.png',       'design/zwart/wand_richel.png'),
]

if __name__ == '__main__':
    import os
    os.makedirs('design/zwart', exist_ok=True)
    for s, o in JOBS:
        zwart(s, o)
