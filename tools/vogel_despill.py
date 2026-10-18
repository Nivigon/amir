#!/usr/bin/env python3
"""Haalt de magenta-gloed uit de vogel-sprites (despill).

De aangeleverde vogel-frames zijn uit een magenta achtergrond geknipt en houden op de randen,
en vooral op de veerpunten, nog magenta vast; over de savanne las dat als een roze gloed. Dit
leest de ongewijzigde bron in enemies/vogel/bron/<set>/ en schrijft de speelversie naar
enemies/vogel/<set>/, met de magenta eruit.

Hoeveel magenta een pixel vasthoudt is min(rood, blauw) min groen: de chroma-key tilt rood en
blauw samen op, groen niet. Dat trek je er weer uit (rood en blauw omlaag naar groen), zodat de
hue naar neutraal grijs zakt. De alpha blijft staan: zo blijven de dunne veerpunten solide in
plaats van dun en rafelig te worden (alpha laten zakken deed dat wel), en blijven de silhouetten,
hitboxen en ankers exact gelijk.

Wat ongemoeid blijft, want daar is min(rood, blauw) min groen niet positief: het rode oog en de
oranje snavel (blauw laag), de tan poten, en de bedoelde groen- en blauwkleurige veerpunten op de
vleugels (groen- of blauw-dominant). Alleen de magenta-franje zakt naar neutraal.

Dezelfde ingreep als de eindstap in tools/kooiman_kleur.py. Verandert een bronframe, draai dit
opnieuw, en daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/vogel/bron')
UIT  = os.path.join(ROOT, 'enemies/vogel')
SETS = ('fly', 'dive')


def despill(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mag = np.clip(np.minimum(r, b) - g, 0, None)
    arr[..., 0] = r - mag
    arr[..., 2] = b - mag
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main():
    n = 0
    for setnaam in SETS:
        for f in sorted(glob.glob(os.path.join(BRON, setnaam, '*.png'))):
            dst = os.path.join(UIT, setnaam, os.path.basename(f))
            despill(Image.open(f)).save(dst)
            n += 1
    if not n:
        sys.exit('geen bronframes gevonden in ' + BRON)
    print(f'{n} vogel-frames ontmagentad (despill, alpha ongemoeid)')


if __name__ == '__main__':
    main()
