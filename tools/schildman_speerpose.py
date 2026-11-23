#!/usr/bin/env python3
"""De speer in de dood van de schildbandiet als pose in plaats van alleen een plaatje.

In knielen, wankel en val (executie.json) zit Amirs speer als losse laag (item 'speer'): een
plaatje van de standaardspeer, gedraaid en met het blad weggeknipt waar hij in de borst zit. Dit
script zoekt per speerplaatje waar de punt zit, onder welke hoek de speer staat en hoeveel er vanaf
de punt in het lijf verdwijnt, door de standaardspeer (speer_projectiel.png) op die plek te tekenen
en de overlap met het plaatje zo groot mogelijk te maken. Dat komt bij de laag te staan:

  tip   [x, y]  de punt, ten opzichte van het anker (272) en de grondlijn (781), grote set
  hoek  graden, de richting van de schacht naar de punt (0 = punt naar rechts, positief = omlaag)
  in    zoveel px (grote set) vanaf de punt zit in het lijf en tekent niet

Met die drie tekent de engine elke speersoort (Pathfinder, Shield Piercer, Ardhi's Reach, de
gekleurde vaantjes) op dezelfde plek (exeSpeerPose in de HTML). De standaardspeer blijft het
plaatje. De lengte van de speer volgt uit de liggende speer (speer_080): EXE_SPEER_K.

  python3 tools/schildman_speerpose.py
"""
import json, math, os
import numpy as np
from PIL import Image

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
E = os.path.join(R, 'enemies/schildbandiet/executie')
JSON = os.path.join(E, 'executie.json')
JAV = Image.open(os.path.join(R, 'amir runc/amir_sprites/design/amir/speer_projectiel.png')).convert('RGBA')
TX, TY = 623, 33                 # de punt in speer_projectiel.png (JAV.tipX, JAV.tipY)
LEN = 380.3                      # de hele speer in de lagen, grote set (gemeten op de liggende speer)
K = LEN / 624                    # schaal van speer_projectiel.png naar de lagen
BEWEGINGEN = ['knielen', 'wankel', 'val']


def tekenen(w, h, tipx, tipy, hoek, weg):
    im = JAV
    if weg > 3:
        a = np.array(im); a[:, max(0, int(round(TX - weg / K))):, 3] = 0; im = Image.fromarray(a)
    c, s = math.cos(math.radians(hoek)), math.sin(math.radians(hoek))
    a_, b_, d_, e_ = c / K, s / K, -s / K, c / K
    return im.transform((w, h), Image.AFFINE, (a_, b_, TX - a_ * tipx - b_ * tipy, d_, e_, TY - d_ * tipx - e_ * tipy),
                        resample=Image.BILINEAR)


def alfa(im):
    return np.array(im)[:, :, 3].astype(float) / 255


def iou(A, w, h, tip, hoek, weg):
    B = alfa(tekenen(w, h, tip[0], tip[1], hoek, weg))
    return np.minimum(A, B).sum() / np.maximum(A, B).sum()


def pas(src, w, h):
    A = alfa(Image.open(os.path.join(E, src)).convert('RGBA').resize((w, h)))
    ys, xs = np.nonzero(A > 0.5)
    P = np.stack([xs, ys], 1).astype(float); c = P.mean(0)
    ax = np.linalg.svd(P - c, full_matrices=False)[2][0]
    if ax[0] < 0: ax = -ax
    pr = (P - c) @ ax
    hoek0 = math.degrees(math.atan2(ax[1], ax[0])); kont = c + ax * pr.min(); zicht = pr.max() - pr.min()
    weg = max(0, LEN - zicht)
    beste = None
    for da in np.arange(-1.5, 1.51, 0.5):          # grof: hoek, lengte en dwars
        hoek = hoek0 + da; v = np.array([math.cos(math.radians(hoek)), math.sin(math.radians(hoek))]); n = np.array([-v[1], v[0]])
        for dl in range(-4, 5, 2):
            for dn in range(-4, 5, 2):
                tip = kont + v * (LEN + dl) + n * dn
                q = iou(A, w, h, tip, hoek, weg)
                if beste is None or q > beste[0]: beste = (q, list(tip), hoek)
    q, tip, hoek = beste
    for st in [(0.4, 1.0), (0.15, 0.5)]:           # fijn: stapjes zolang het beter wordt
        beter = True
        while beter:
            beter = False
            for da, dx, dy in [(st[0], 0, 0), (-st[0], 0, 0), (0, st[1], 0), (0, -st[1], 0), (0, 0, st[1]), (0, 0, -st[1])]:
                t = [tip[0] + dx, tip[1] + dy]; q2 = iou(A, w, h, t, hoek + da, weg)
                if q2 > q + 1e-4: q, tip, hoek, beter = q2, t, hoek + da, True
    return q, tip, hoek, weg


def main():
    d = json.load(open(JSON))
    gedaan = {}
    for bew in BEWEGINGEN:
        for fr in d['bewegingen'][bew]['frames']:
            for l in fr:
                if l['item'] != 'speer': continue
                if l['src'] not in gedaan:
                    gedaan[l['src']] = pas(l['src'], l['w'], l['h'])
                    q, tip, hoek, weg = gedaan[l['src']]
                    print(f"{l['src']}: overlap {q:.2f}, hoek {hoek:.1f}, in {weg:.0f}")
                q, tip, hoek, weg = gedaan[l['src']]
                l['tip'] = [round(l['dx'] + tip[0], 1), round(l['dy'] + tip[1], 1)]
                l['hoek'] = round(hoek, 2)
                l['in'] = round(weg) if weg > 3 else 0
    d['speer_lengte'] = LEN
    with open(JSON, 'w') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print('geschreven:', JSON)


if __name__ == '__main__':
    main()
