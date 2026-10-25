#!/usr/bin/env python3
"""Kleurt de schildbandiet om naar het bandietpalet.

Zelfde aanpak als tools/kooiman_kleur.py (en die leent hertint uit tools/slang_kleur.py): de
tekening zelf blijft staan. Per kleurvlak wordt alleen de tint en de verzadiging vervangen en
de helderheid over een nieuw bereik uitgesmeerd, dus de inktlijnen, de plooien en de schaduwen
blijven precies zoals ze getekend zijn.

De aangeleverde frames (blauw gewaad, groene broek, paarse cape) staan ongewijzigd in
enemies/schildbandiet/bron/, met dezelfde mappen als de speelversie. Die zijn handig om later
opnieuw in een ander palet te kleuren (zoals de elite-garde of de duinbandiet). Dit leest die
bron en schrijft de speelversie naar enemies/schildbandiet/, zodat hij in dezelfde kleuren
loopt als de bandiet:

  gewaad  -> marineblauw (de bandietjas, #201f3c)
  broek   -> kaki-olijf (de bandietbroek, #534b39)
  cape    -> een donkerder marineblauw, zodat hij nog los van het gewaad leest
  de rode sjerp, de huid, de schoenen, de baard, het schild en de speer blijven ongemoeid
  daarna de magenta-ontspilling van de kooiman (de roze randjes van de chroma-key)

De lagen van Amir in executie/lagen (amir_*.png) staan niet in bron/ en worden niet aangeraakt.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
sys.dont_write_bytecode = True   # geen __pycache__ in tools/ door de import hieronder
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kooiman_kleur import naar_hsv, hertint

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/schildbandiet/bron')
UIT  = os.path.join(ROOT, 'enemies/schildbandiet')
MAPPEN = ('lagen/lijf', 'lagen/schild', 'executie/lagen')


def maak(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    rgb = arr[..., :3]
    al = arr[..., 3]
    h, s, v = naar_hsv(rgb)
    op = al > 128

    blauw = op & (s > 0.25) & (h >= 160) & (h < 258)    # het gewaad
    groen = op & (s > 0.20) & (h >= 70) & (h < 160)     # de broek
    paars = op & (s > 0.20) & (h >= 258) & (h < 335)    # de cape (en de magenta randjes erlangs)

    rgb = hertint(rgb, blauw, tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas #201f3c
    rgb = hertint(rgb, groen, tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek #534b39
    rgb = hertint(rgb, paars, tint=238, verz=0.40, laag=0.05, hoog=0.21)   # cape: donkerder marine

    # magenta-ontspilling (zie kooiman_kleur.py): min(rood, blauw) min groen eruit, alpha blijft
    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    rgb[..., 0] = rr - mag
    rgb[..., 2] = bb - mag
    arr[..., :3] = rgb
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main():
    n = 0
    for map_ in MAPPEN:
        for f in sorted(glob.glob(os.path.join(BRON, map_, '*.png'))):
            if os.path.basename(f).startswith('amir_'):
                continue
            maak(Image.open(f)).save(os.path.join(UIT, map_, os.path.basename(f)))
            n += 1
    if not n:
        sys.exit('geen bronframes gevonden in ' + BRON)
    print(f'{n} frames omgekleurd naar het bandietpalet (hertint, lijnen blijven)')


if __name__ == '__main__':
    main()
