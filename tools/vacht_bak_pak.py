#!/usr/bin/env python3
# Pakt de maskers van tools/vacht_bak.js kleiner in: elk masker heeft hooguit een paar honderd verschillende kleuren, dus een
# PNG met een palet (exact, elke kleur zijn eigen index) is zes keer kleiner dan de RGBA uit de browser. Het spel leest
# hetzelfde terug. Roept vacht_bak.js zelf aan het eind aan; met paden als argument alleen die bestanden.
import sys, os, glob
import numpy as np
from PIL import Image

def pak(f):
    a = np.asarray(Image.open(f).convert('RGB'))
    plat = a.reshape(-1, 3)
    kleuren, idx = np.unique(plat, axis=0, return_inverse=True)
    if len(kleuren) > 256:
        Image.fromarray(a).save(f, optimize=True)
        return
    p = Image.fromarray(idx.reshape(a.shape[:2]).astype(np.uint8), 'P')
    p.putpalette(kleuren.astype(np.uint8).flatten().tolist())
    p.save(f, optimize=True)
    assert (np.asarray(Image.open(f).convert('RGB')) == a).all(), f

if __name__ == '__main__':
    wortel = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'karakters', 'amir_vacht')
    lijst = sys.argv[1:] or glob.glob(os.path.join(wortel, '**', '*.png'), recursive=True)
    for f in lijst: pak(f)
    print('%d maskers met een palet' % len(lijst))
