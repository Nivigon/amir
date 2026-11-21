#!/usr/bin/env python3
"""Knipt de inrichting van de winkel (voorstel B) uit het Grok-vel design/stad/binnen/bron/winkel_b.jpg.

Het vel heeft acht onderdelen op wit in drie rijen: de leemtoonbank; de wandplank op pinnen, de mat, de
kruidenbos, de kruik; een open zak, een dichte zak, een stapel manden. Wit gaat eruit zoals in spul_knip.py
(flood-fill vanaf de rand, plus ingesloten wit dat groot genoeg is), elk onderdeel apart bijgesneden.

    python3 tools/winkel_b_knip.py
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

import spul_knip as sk

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / 'design/stad/binnen'
BRON = DIR / 'bron/winkel_b.jpg'

# per rij van links naar rechts: (bestandsnaam, schaal)
RIJEN = [[('toonbank_leem', 1.0)],
         [('plank_pin', 0.6), ('wand_mat', 0.6), ('wand_kruiden', 0.6), ('kruik_groot', 0.6)],
         [('zak_open', 0.6), ('zak_dicht', 0.6), ('manden', 0.6)]]


def main():
    a = np.array(Image.open(BRON).convert('RGBA'))
    rgb = a[:, :, :3].astype(int)
    wit = (rgb.min(axis=2) > sk.WIT) & ((rgb.max(axis=2) - rgb.min(axis=2)) < sk.KLEUR)
    bg = sk.achtergrond(a)
    lab, _ = ndimage.label(wit & ~bg)
    maat = np.bincount(lab.ravel())
    groot = np.nonzero(maat > sk.GAT)[0]
    bg |= np.isin(lab, groot[groot > 0])
    alfa = np.where(bg, 0, 255).astype(np.uint8)
    rand = np.zeros_like(bg)
    rand[1:, :] |= bg[:-1, :]; rand[:-1, :] |= bg[1:, :]; rand[:, 1:] |= bg[:, :-1]; rand[:, :-1] |= bg[:, 1:]
    rand &= ~bg
    alfa[rand] = np.clip((255 - rgb.min(axis=2)[rand]) * 3, 90, 255)
    a[:, :, 3] = alfa
    lab, _ = ndimage.label(alfa > 0)
    tel = np.bincount(lab.ravel())
    blokken = [(i, s) for i, s in enumerate(ndimage.find_objects(lab), 1) if tel[i] > sk.MIN_BLOK]
    # in rijen: een blok hoort bij de rij van zijn midden (de toonbank boven, dan twee rijen)
    H = a.shape[0]
    grens = [H * 0.33, H * 0.62]
    def rij(s):
        m = (s[0].start + s[0].stop) / 2
        return 0 if m < grens[0] else (1 if m < grens[1] else 2)
    for r, namen in enumerate(RIJEN):
        hier = sorted([b for b in blokken if rij(b[1]) == r], key=lambda b: b[1][1].start)
        if len(hier) != len(namen):
            raise SystemExit(f'FOUT: rij {r} heeft {len(hier)} blokken, {len(namen)} verwacht')
        for (naam, schaal), (i, (sy, sx)) in zip(namen, hier):
            stuk = a[sy, sx].copy()
            stuk[lab[sy, sx] != i, 3] = 0
            uit = Image.fromarray(stuk)
            uit = uit.resize((round(uit.width * schaal), round(uit.height * schaal)), Image.LANCZOS)
            pad = DIR / f'{naam}.png'
            uit.save(pad)
            print(pad.relative_to(ROOT), uit.size)


if __name__ == '__main__':
    main()
