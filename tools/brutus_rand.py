#!/usr/bin/env python3
"""Nyundo donker: de lichte stippelrand om zijn omtrek weghalen.

In de Grok-export zit langs de omtrek een rest van de magenta achtergrond: roodroze pixels,
vaak half doorzichtig, om en om met de donkere contour, en blauwe langs de polswindsels.
Tegen een lichte achtergrond (de muur van het plein) mengen die tot een licht streepjeslijntje
over zijn arm en schouder, vooral in de dood als hij zijn arm strekt. Dit script geeft die
pixels (en bijna witte glans) in de buitenste RAND pixels de kleur van de contour (alpha blijft gelijk).

Alleen de donkere set: daar is het haar zwart, dus rood aan de rand is altijd zo'n rest
(in de gewone set is zijn hanenkam rood en hoort rood aan de rand er wel bij).
Draai het na tools/brutus_donker.py (en brutus_spleet.py), daarna gen-klein.py en
gen-offline-manifest.py.
"""
import glob
import numpy as np
from PIL import Image, ImageFilter

MAP = 'enemies/brutus/frames_donker/'
RAND = 3                     # zo diep (px) vanaf de buitenkant telt als rand
CONTOUR = (28, 16, 16)       # de kleur van de donkere contour


def schoon(pad):
    im = Image.open(pad).convert('RGBA')
    a = np.array(im).astype(int)
    zicht = a[..., 3] > 40                                 # vanaf de zichtbare pixels gemeten
    alles = a[..., 3] > 0
    kern = np.array(Image.fromarray((zicht * 255).astype('uint8')).filter(ImageFilter.MinFilter(2 * RAND + 1))) > 0
    rand = alles & ~kern
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    rood = (r > g + 20) & (b >= g - 6)                     # de magenta-rest: rood met evenveel blauw als groen (de huid is oranjebruin, groen boven blauw)
    blauw = (b > r + 20) & (b > g + 10)                   # blauwe spikkels langs de windsels
    licht = (0.3 * r + 0.59 * g + 0.11 * b) > 150         # bijna witte glans precies op de rand
    weg = rand & (rood | blauw | licht)
    if not weg.any():
        return 0
    for i, c in enumerate(CONTOUR):
        a[..., i][weg] = c
    Image.fromarray(a.astype('uint8'), 'RGBA').save(pad)
    return int(weg.sum())


if __name__ == '__main__':
    tot = 0
    for pad in sorted(glob.glob(MAP + '*.png')):
        tot += schoon(pad)
    print(f'{tot} randpixels donker gemaakt in {MAP}')
