#!/usr/bin/env python3
"""Knipt de winkelspullen uit het derde Grok-vel (in de spelstijl, met de speer en de kalebas als voorbeeld) (design/stad/binnen/bron/spullen_vel3.png).

Het vel heeft acht spullen in twee rijen van vier op wit. Wit wordt weggeknipt met een flood-fill
vanaf de rand over bijna-wit (licht materiaal binnenin blijft staan), daarna per vak bijsnijden en
op halve maat opslaan als design/stad/binnen/spul_<naam>.png, net zo groot als de spullen van het eerste vel.

    python3 tools/spul_knip.py
"""
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / 'design/stad/binnen'
BRON = DIR / 'bron/spullen_vel3.png'

# links naar rechts, boven naar onder
NAMEN = [['kruiden', 'zak', 'kan', 'flesje'], ['touw', 'lamp', 'trommel', 'dadels']]
SCHAAL = 0.5
WIT = 232          # helderder dan dit en weinig kleur telt als achtergrond
KLEUR = 18         # hooguit zoveel verschil tussen de kanalen
GAT = 25           # ingesloten wit groter dan dit (pixels) is een gat, kleiner is glimlicht
MIN_BLOK = 3000    # kleinere blokken zijn spikkels


def achtergrond(a):
    """Bool-masker van de achtergrond: bijna-wit dat met de rand verbonden is."""
    rgb = a[:, :, :3].astype(int)
    wit = (rgb.min(axis=2) > WIT) & ((rgb.max(axis=2) - rgb.min(axis=2)) < KLEUR)
    h, w = wit.shape
    bg = np.zeros_like(wit)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if wit[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if wit[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and wit[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))
    return bg


def main():
    from scipy import ndimage
    a = np.array(Image.open(BRON).convert('RGBA'))
    rgb = a[:, :, :3].astype(int)
    wit = (rgb.min(axis=2) > WIT) & ((rgb.max(axis=2) - rgb.min(axis=2)) < KLEUR)
    bg = achtergrond(a)
    # ingesloten wit (het gat in een hengsel) is ook achtergrond, als het groot genoeg is om geen glimlicht te zijn
    lab, n = ndimage.label(wit & ~bg)
    maat = np.bincount(lab.ravel())
    groot = np.nonzero(maat > GAT)[0]
    bg |= np.isin(lab, groot[groot > 0])
    alfa = np.where(bg, 0, 255).astype(np.uint8)
    # zachte rand: een pixel naast de achtergrond half doorzichtig, naar hoe wit hij is
    rand = np.zeros_like(bg)
    rand[1:, :] |= bg[:-1, :]; rand[:-1, :] |= bg[1:, :]; rand[:, 1:] |= bg[:, :-1]; rand[:, :-1] |= bg[:, 1:]
    rand &= ~bg
    alfa[rand] = np.clip((255 - rgb.min(axis=2)[rand]) * 3, 90, 255)
    a[:, :, 3] = alfa
    # de spullen zijn de grote losse blokken; spikkels in het wit vallen af
    lab, n = ndimage.label(alfa > 0)
    tel = np.bincount(lab.ravel())
    blokken = [(i, s) for i, s in enumerate(ndimage.find_objects(lab), 1) if tel[i] > MIN_BLOK]
    H = a.shape[0]
    blokken.sort(key=lambda b: (b[1][0].start > H / 2, b[1][1].start))   # boven eerst, dan van links naar rechts
    namen = [n for rij in NAMEN for n in rij]
    if len(blokken) != len(namen):
        raise SystemExit(f'FOUT: {len(blokken)} blokken gevonden, {len(namen)} verwacht')
    for naam, (i, (sy, sx)) in zip(namen, blokken):
        stuk = a[sy, sx].copy()
        stuk[lab[sy, sx] != i, 3] = 0   # alleen dit blok, niet een stukje van de buurman dat in het kader valt
        uit = Image.fromarray(stuk)
        uit = uit.resize((round(uit.width * SCHAAL), round(uit.height * SCHAAL)), Image.LANCZOS)
        pad = DIR / f'spul_{naam}.png'
        uit.save(pad)
        print(pad.relative_to(ROOT), uit.size)


if __name__ == '__main__':
    main()
