#!/usr/bin/env python3
# De twee plaatjes van de savanne-opstapjes (zie OPSTAP en SAV_OPSTAP in de HTML), uit de grondrand en de Grok-plaat:
#
#   design/opstap/savanne_onder.png  de wand onder een trede: de rotskolommen van design/grondrand.png (rij 185 tot 297),
#                                    naadloos onder elkaar te zetten (de onderkant loopt zacht over in de bovenkant)
#   design/opstap/savanne_eind.png   het eind van een trede: zand en korstkap die natuurlijk aflopen, met keien en een
#                                    graspol, uit design/opstap/bron/savanne_rand_1.png. Op de maat en de rijen van
#                                    grondrand.png (335 hoog), vanaf tegel-x 380, met links 80 px die zacht invloeit
#
# Grok kreeg design/opstap/bron/savanne_rand_start.png als startbeeld: grondrand.png 100 px lager op een doek van
# 1000 breed, en vergrootte dat 2,176 keer. Terugschalen naar 1000 breed geeft dus de tegelmaat; het script zoekt de
# kleine verschuiving zelf (op het overgenomen stuk tegel links). Draai na dit script tools/gen-offline-manifest.py.
import os
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

GROND = D('design', 'grondrand.png')
BRON = D('design', 'opstap', 'bron', 'savanne_rand_1.png')
START = D('design', 'opstap', 'bron', 'savanne_rand_start.png')
UIT_ONDER = D('design', 'opstap', 'savanne_onder.png')
UIT_EIND = D('design', 'opstap', 'savanne_eind.png')

ONDER_VAN, ONDER_TOT, ONDER_OVER = 185, 297, 34   # rijen van de kolommen in grondrand.png, en de overvloei
START_DY = 100                                    # grondrand-rij 0 staat in het startbeeld op rij 100
EIND_X0, EIND_IN = 380, 80                        # waar het eindstuk begint (tegel-x) en hoe breed het invloeit


def onder():
    im = np.array(Image.open(GROND).convert('RGB')).astype(float)
    band = im[ONDER_VAN:ONDER_TOT]
    h0 = band.shape[0] - ONDER_OVER
    out = band[:h0].copy()
    for y in range(ONDER_OVER):                   # bovenaan vloeit de onderkant in, zodat hij naadloos herhaalt
        a = y / ONDER_OVER
        out[y] = band[h0 + y] * (1 - a) + band[y] * a
    Image.fromarray(out.round().astype(np.uint8)).save(UIT_ONDER)
    print('savanne_onder.png', out.shape[1], 'x', out.shape[0])


def wit_weg(rgb):
    # wit wegknippen: flood-fill vanaf de rand over bijna-wit, zodat licht zand binnenin blijft staan
    h, w, _ = rgb.shape
    wit = (rgb.min(axis=2) > 222) & ((rgb.max(axis=2) - rgb.min(axis=2)) < 30)
    bg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if wit[y, x]:
                bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if wit[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= yy < h and 0 <= xx < w and wit[yy, xx] and not bg[yy, xx]:
                bg[yy, xx] = True; q.append((yy, xx))
    return np.where(bg, 0, 255).astype(np.uint8)


def eind():
    start = np.array(Image.open(START).convert('RGB')).astype(int)
    bron = Image.open(BRON).convert('RGB')
    h = round(bron.height * start.shape[1] / bron.width)
    sm = np.array(bron.resize((start.shape[1], h), Image.LANCZOS)).astype(int)
    best = None                                   # de kleine verschuiving van Grok, op het overgenomen stuk tegel
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            d = np.abs(start[150:250, 100:500] - sm[150 + dy:250 + dy, 100 + dx:500 + dx]).mean()
            if best is None or d < best[0]:
                best = (d, dx, dy)
    _, dx, dy = best
    a = wit_weg(sm)
    img = Image.fromarray(np.dstack([sm.astype(np.uint8), a]), 'RGBA')
    al = img.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    img.putalpha(al)                              # een pixel krimpen en zacht maken: geen witte halo
    gh = Image.open(GROND).height
    tegel = Image.new('RGBA', (start.shape[1], gh))
    tegel.paste(img.crop((dx, START_DY + dy, start.shape[1] + dx, START_DY + dy + gh)), (0, 0))
    arr = np.array(tegel)
    xe = int(np.where(arr[:, :, 3].max(axis=0) > 0)[0].max()) + 1
    arr = arr[:, EIND_X0:xe].copy()
    ramp = np.clip(np.arange(arr.shape[1]) / EIND_IN, 0, 1)
    arr[:, :, 3] = (arr[:, :, 3] * ramp[None, :]).astype(np.uint8)
    Image.fromarray(arr).save(UIT_EIND)
    print('savanne_eind.png', arr.shape[1], 'x', arr.shape[0], '(verschuiving', dx, dy, ')')


if __name__ == '__main__':
    onder()
    eind()
