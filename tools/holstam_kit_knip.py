#!/usr/bin/env python3
"""Knipt de aankleedkit en de schorsrand van de holle stam uit de Grok-platen.

Bron (design/regenwoud/holstam/bron/):
  kit_grok_e4de8c8f.jpg   een vel met losse stukken op wit (mos, hangmos, zwammen, paddenstoelen, wortel, varens)
  rand_grok_97898eeb.jpg  twee gebroken bastranden op wit; de rechter (met hangend mos) is de rand die Tom koos

Uit: design/regenwoud/holstam/kit/<soort>_<n>.png en design/regenwoud/holstam/rand.png.
Het wit gaat zacht weg (de gloed van de teal paddenstoeltjes blijft half doorzichtig) en de randkleur wordt
ontmengd, zodat er geen witte halo om de stukken zit.

  python3 tools/holstam_kit_knip.py           knippen
  python3 tools/holstam_kit_knip.py --vel     ook een genummerd overzicht naar /tmp/kit_vel.png
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

D = 'design/regenwoud/holstam/'

# volgorde van de stukken op het vel (van links naar rechts, rij voor rij); de naam bepaalt de soort in het spel
KIT = ['mos_0', 'hangmos_0', 'hangmos_1', 'mos_1', 'mos_2',
       'mos_3', 'zwam_0', 'zwam_1', 'mos_4', 'zwam_2', 'zwam_3',
       'paddo_0', 'paddo_1', 'gloei_0', 'wortel_0', 'varen_0', 'varen_1', 'tak_0']


def zacht(rgb):
    a = rgb.astype(float)
    alpha = np.clip((255 - a.min(2) - 10) / 45.0, 0, 1)
    # alleen wat met de rand verbonden is is achtergrond: wit binnen een stuk (een glans) blijft staan
    licht = alpha < 0.02
    lab, n = ndimage.label(licht)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(rand))
    alpha[licht] = 0   # ook ingesloten wit (tussen twee stelen) is achtergrond
    alpha[bg] = 0
    alpha = np.minimum(alpha, ndimage.grey_erosion(alpha, size=(4, 4)))   # de jpeg-rand (een lichte ring) eraf
    kleur = np.where(alpha[..., None] > 0.01, (a - (1 - alpha[..., None]) * 255) / np.maximum(alpha[..., None], 0.01), 0)
    return np.dstack([np.clip(kleur, 0, 255), alpha * 255]).astype(np.uint8)


def stukken(rgba, min_px=900):
    m = ndimage.binary_dilation(rgba[..., 3] > 25, iterations=7)
    lab, n = ndimage.label(m)
    sl = ndimage.find_objects(lab)
    uit = []
    for i, s in enumerate(sl):
        if s is None:
            continue
        grootte = ((lab[s] == i + 1) & (rgba[s][..., 3] > 25)).sum()
        if grootte < min_px:
            continue
        p = rgba[s].copy()
        p[..., 3] = np.where(lab[s] == i + 1, p[..., 3], 0)
        uit.append((s[0].start, s[1].start, s, p))
    # rijen: groepeer op het midden in y
    uit.sort(key=lambda t: (t[2][0].start + t[2][0].stop) / 2)
    rijen, rij, vorig = [], [], None
    for t in uit:
        my = (t[2][0].start + t[2][0].stop) / 2
        if vorig is not None and my - vorig > 120:
            rijen.append(rij); rij = []
        rij.append(t); vorig = my
    rijen.append(rij)
    return [t for r in rijen for t in sorted(r, key=lambda t: t[1])]


def main():
    os.makedirs(D + 'kit', exist_ok=True)
    kit = zacht(np.asarray(Image.open(D + 'bron/kit_grok_e4de8c8f.jpg').convert('RGB')))
    st = stukken(kit)
    if len(st) != len(KIT):
        print('LET OP: %d stukken gevonden, %d namen' % (len(st), len(KIT)))
    for naam, (_, _, s, p) in zip(KIT, st):
        Image.fromarray(p, 'RGBA').save(D + 'kit/' + naam + '.png')
        print(naam, p.shape[1], 'x', p.shape[0])
    if '--vel' in sys.argv:
        v = Image.new('RGBA', (2128, 912), (60, 60, 60, 255)); d = ImageDraw.Draw(v)
        for i, (_, _, s, p) in enumerate(st):
            v.alpha_composite(Image.fromarray(p, 'RGBA'), (s[1].start, s[0].start))
            d.text((s[1].start, s[0].start), str(i) + ' ' + (KIT[i] if i < len(KIT) else '?'), fill=(255, 80, 80, 255))
        v.save('/tmp/kit_vel.png')
    # de schorsrand: het rechter stuk van de rand-plaat
    rand = zacht(np.asarray(Image.open(D + 'bron/rand_grok_97898eeb.jpg').convert('RGB')))
    st = sorted(stukken(rand, 20000), key=lambda t: t[1])
    p = st[-1][3]
    Image.fromarray(p, 'RGBA').save(D + 'rand.png')
    print('rand', p.shape[1], 'x', p.shape[0])


if __name__ == '__main__':
    main()
