#!/usr/bin/env python3
"""Zet de achterste voet in de stootframes weer heel.

In attack_sp_1 tot en met attack_sp_8 (karakters/amir/aanval/speerstrike/) was de
voet waar Amir op staat kapot: de tenen zaten een stuk te hoog en de voorvoet eronder
ontbrak, met een rechte snee langs de hiel. In frame 9 en 10 is die voet wel heel,
en in frame 10 staat hij op dezelfde plek, in dezelfde stand.

Dit script haalt die voet uit frame 10 (alles onder de enkel dat aan de enkel vastzit)
en zet hem in de andere frames in de plaats van de kapotte, uitgelijnd op de enkel
(horizontaal) en op de onderkant van de hiel (verticaal). Het been zelf, de speer en de
andere voet blijven zoals ze zijn. Er wordt niets getekend: alles komt uit frame 10.

Het is een reparatie van een keer, en die is al gedaan: de frames in de repository zijn
hersteld. Draai het alleen op de oorspronkelijke, kapotte frames (uit de geschiedenis van
git); op herstelde frames schuift de voet bij elke ronde een pixel mee. Daarna de kleine
set bijwerken (die frames zijn lager dan 400 en worden alleen gekopieerd):

    python3 tools/stootvoet.py
    python3 tools/gen-klein.py

Vereist Pillow en numpy: pip install pillow numpy
"""

import os
import sys
from collections import deque

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit('Pillow of numpy ontbreekt: pip install pillow numpy')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = 'karakters/amir/aanval/speerstrike'
BRON = 10                  # het frame met de hele voet
KAPOT = range(1, 9)        # de frames met de kapotte voet
ENKEL = 263                # vanaf deze rij (in de bron, 301 hoog) telt het als voet
VLAK = (262, 320)          # de kolommen waar de achterste voet staat; rechts begint de andere voet


def laad(i):
    return np.array(Image.open(os.path.join(ROOT, MAP, 'attack_sp_%d.png' % i)).convert('RGBA'))


def enkel(a):
    """Het midden van de enkel, een rij boven de snee."""
    xs = np.nonzero(a[ENKEL - 1, VLAK[0]:VLAK[1], 3] > 128)[0] + VLAK[0]
    return (xs.min() + xs.max()) / 2, xs.min(), xs.max()


def voet(a):
    """Het masker van de voet: alles vanaf ENKEL dat via dekkende pixels aan de enkel vastzit."""
    h, w = a.shape[:2]
    _, l, r = enkel(a)
    m = np.zeros((h, w), bool)
    q = deque((ENKEL, x) for x in range(l, r + 1) if a[ENKEL, x, 3] > 0)
    for y, x in q:
        m[y, x] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if ENKEL <= ny < h and VLAK[0] - 30 <= nx < VLAK[1] and not m[ny, nx] and a[ny, nx, 3] > 0:
                m[ny, nx] = True
                q.append((ny, nx))
    return m


def hiel(a, m):
    """De onderste dekkende rij van de voet, onder de enkel."""
    _, l, r = enkel(a)
    ys = np.nonzero((m[:, l:r + 1] & (a[:, l:r + 1, 3] > 128)).any(axis=1))[0]
    return ys.max()


def main():
    b = laad(BRON)
    bm = voet(b)
    bx, _, _ = enkel(b)
    bh = hiel(b, bm)
    for i in KAPOT:
        a = laad(i)
        am = voet(a)
        ax, _, _ = enkel(a)
        dx = int(round(ax - bx))
        dy = hiel(a, am) - bh
        uit = a.copy()
        uit[am] = 0                                   # de kapotte voet eruit
        ys, xs = np.nonzero(bm)
        for y, x in zip(ys, xs):                      # en die van frame 10 erin, eroverheen gelegd
            ty, tx = y + dy, x + dx
            if not (0 <= ty < uit.shape[0] and 0 <= tx < uit.shape[1]):
                continue
            s = b[y, x].astype(float) / 255
            d = uit[ty, tx].astype(float) / 255
            ao = s[3] + d[3] * (1 - s[3])
            if ao <= 0:
                continue
            rgb = (s[:3] * s[3] + d[:3] * d[3] * (1 - s[3])) / ao
            uit[ty, tx] = np.round(np.append(rgb, ao) * 255).astype(np.uint8)
        pad = os.path.join(ROOT, MAP, 'attack_sp_%d.png' % i)
        Image.fromarray(uit, 'RGBA').save(pad, optimize=True)
        print('attack_sp_%d: voet uit frame %d, verschoven %+d, %+d' % (i, BRON, dx, dy))


if __name__ == '__main__':
    main()
