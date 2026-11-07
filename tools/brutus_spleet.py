#!/usr/bin/env python3
"""Nyundo (Brutus): de spleet tussen de steel en de bal van zijn knots dichtmaken.

In de Grok-export van de kap ligt de bal in een paar frames los van de steel, met een
spleet van een of twee pixels die half doorzichtig is. In het spel schijnt de lichte
lucht of muur daar doorheen, en dat is het witte randje boven de steel als de knots
neerkomt. Dit script zoekt per frame de grote stukken (alpha boven DREMPEL): zijn het
er twee (lijf en bal), dan vult het de pixels waar die twee elkaar op BRUG pixels na
raken, met de kleur van de dekkende buren eromheen.

Werkt op enemies/brutus/frames/ en frames_donker/ (zelfde maten), en raakt alleen
frames aan waar de bal los ligt. Draai daarna gen-klein.py en gen-offline-manifest.py.
"""
import glob
import numpy as np
from PIL import Image, ImageFilter

MAPPEN = ['enemies/brutus/frames/', 'enemies/brutus/frames_donker/']
DREMPEL = 200      # vanaf deze alpha telt een pixel als dekkend
BRUG = 6           # zo breed (px) mag de spleet tussen lijf en bal zijn
MIN_STUK = 1500    # kleinere stukken (losse spikkels) tellen niet als bal


def stukken(m):
    h, w = m.shape
    lab = np.zeros((h, w), int)
    maten = []
    for y0, x0 in zip(*np.where(m)):
        if lab[y0, x0]:
            continue
        n = len(maten) + 1
        stapel = [(y0, x0)]
        lab[y0, x0] = n
        c = 0
        while stapel:
            y, x = stapel.pop()
            c += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        stapel.append((yy, xx))
        maten.append(c)
    return lab, maten


def groei(m, r):
    im = Image.fromarray((m * 255).astype('uint8'))
    return np.array(im.filter(ImageFilter.MaxFilter(2 * r + 1))) > 0


def krimp(m, r):
    im = Image.fromarray((m * 255).astype('uint8'))
    return np.array(im.filter(ImageFilter.MinFilter(2 * r + 1))) > 0


def sluit(m, r):
    return krimp(groei(m, r), r)


def dicht(pad):
    im = Image.open(pad).convert('RGBA')
    a = np.array(im).astype(float)
    dek = a[..., 3] > DREMPEL
    lab, maten = stukken(dek)
    groot = [i + 1 for i, s in enumerate(maten) if s >= MIN_STUK]
    if len(groot) != 2:
        return 0
    s1, s2 = (lab == groot[0]), (lab == groot[1])
    # de brug: wat dichtgaat als je lijf en bal samen sluit, maar niet als je elk apart sluit
    # (dat zijn hun eigen holtes), en alleen vlak bij allebei
    gat = sluit(s1 | s2, BRUG) & ~sluit(s1, BRUG) & ~sluit(s2, BRUG)
    gat &= groei(s1, BRUG + 1) & groei(s2, BRUG + 1) & ~dek
    if not gat.any():
        return 0
    # kleur: van buiten naar binnen, telkens het gemiddelde van de al dekkende buren
    vol = dek.copy()
    over = gat.copy()
    while over.any():
        rand = over & groei(vol, 1)
        if not rand.any():
            break
        for y, x in zip(*np.where(rand)):
            y0, y1, x0, x1 = max(0, y - 1), y + 2, max(0, x - 1), x + 2
            buur = a[y0:y1, x0:x1][vol[y0:y1, x0:x1]]
            a[y, x, :3] = buur[:, :3].mean(0)
            a[y, x, 3] = 255
        vol |= rand
        over &= ~rand
    Image.fromarray(a.round().astype('uint8'), 'RGBA').save(pad)
    return int(gat.sum())


if __name__ == '__main__':
    for map_ in MAPPEN:
        for pad in sorted(glob.glob(map_ + '*.png')):
            n = dicht(pad)
            if n:
                print(f'{pad}: {n} pixels dicht')
