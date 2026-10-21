#!/usr/bin/env python3
"""Maakt de zwarte varianten van de solide terreinstukken voor de nieuwe stijl.

Elk stuk wordt per pixel omgekleurd (zoals winter en de put): de vulling wordt
zwart, alleen de helderste richels en de buitencontour houden een zwak randlicht,
zodat de vorm en de tandjes leesbaar blijven. De achtergrond-steen (rots_vulling)
blijft juist zichtbaar en wordt dus niet omgekleurd.

Verandert een bron, draai dit opnieuw, en daarna gen-klein.py en
gen-offline-manifest.py.
"""
import numpy as np
from PIL import Image, ImageFilter

# randlicht (rim) sterkte, hoeveel helderste richels overleven, en de warmte ervan
RIM_PX = 9        # dikte van de buitencontour in bronpixels
HI_LO = 0.72      # alleen helderheid boven deze drempel overleeft als richel
HI_MAX = 0.50     # hoe sterk die richels nog zijn (0..1)
RIM_MAX = 0.62    # hoe sterk de buitencontour is
WARM = (1.06, 1.0, 0.92)  # lichte warme bias in de rand


def zwart(src, out):
    im = Image.open(src).convert('RGBA')
    arr = np.asarray(im).astype(np.float32)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    L = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    hi = np.clip((L - HI_LO) / (1 - HI_LO), 0, 1) ** 1.3 * HI_MAX
    er = np.asarray(Image.fromarray(a.astype(np.uint8)).filter(
        ImageFilter.MinFilter(RIM_PX))).astype(np.float32)
    edge = np.clip((a - er) / 255.0, 0, 1)
    val = np.maximum(hi, edge * RIM_MAX)
    rgb = np.stack([np.clip(val * 255 * WARM[0], 0, 255),
                    np.clip(val * 255 * WARM[1], 0, 255),
                    np.clip(val * 255 * WARM[2], 0, 255)], -1)
    res = np.concatenate([rgb, a[..., None]], -1).astype(np.uint8)
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
