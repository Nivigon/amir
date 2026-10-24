#!/usr/bin/env python3
"""De speerpunt per frame van de executie, voor EXE.boog.punt.

Leest enemies/schildbandiet/executie/executie.json, legt per frame van 'executie' de lengteas van de
speer-laag (hoofdas van de dekkende pixels) en kiest het uiteinde met de grijze punt. Print per frame de
punt in canvas-px ten opzichte van het anker en de grondlijn (zoals dx en dy in de json), zodat je de
lijst voor EXE.boog.punt (frames boog.van tot boog.tot) zo kunt overnemen.

    python3 tools/exe_speerpunt.py
"""
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies', 'schildbandiet', 'executie')

def speerpunt(laag):
    im = np.array(Image.open(os.path.join(ROOT, laag['src'])).convert('RGBA'))
    dekt = im[:, :, 3] > 80
    ys, xs = np.nonzero(dekt)
    sx, sy = laag['w'] / im.shape[1], laag['h'] / im.shape[0]     # het spel rekt het plaatje naar w bij h
    pts = np.stack([xs * sx, ys * sy], 1)
    mid = pts.mean(0)
    as_ = np.linalg.svd(pts - mid, full_matrices=False)[2][0]     # de lengteas van de speer
    proj = (pts - mid) @ as_
    r, g, b = (im[ys, xs, i].astype(int) for i in range(3))
    grijs = (abs(r - g) < 25) & (abs(g - b) < 25) & (r > 90)       # de metalen punt: licht en zonder kleur
    kant = 1 if (proj[grijs].mean() if grijs.any() else 0) > 0 else -1
    uit = pts[proj.argmax() if kant > 0 else proj.argmin()]
    return laag['dx'] + float(uit[0]), laag['dy'] + float(uit[1])

def main():
    ex = json.load(open(os.path.join(ROOT, 'executie.json')))['bewegingen']['executie']
    for i, fr in enumerate(ex['frames']):
        for l in fr:
            if l['item'] == 'speer':
                x, y = speerpunt(l)
                print('frame %2d: [%d, %d]' % (i, round(x), round(y)))
    print('snijlijn:', ex['snijlijn'])

if __name__ == '__main__':
    sys.exit(main())
