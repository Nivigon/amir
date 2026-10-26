#!/usr/bin/env python3
"""Kleurt de kruisboogbandiet om naar het bandietpalet.

De frames komen uit de Animeer tool Kruisboogbandiet (met het schouderstuk erop gebakken) en staan in de
felle bronkleuren in enemies/kruisboog/bron/<set>/. Dit script schrijft de speelversie naar
enemies/kruisboog/<set>/. Zelfde aanpak als tools/schildman_kleur.py: per kleurvlak alleen een nieuwe tint
en verzadiging, de helderheid uitgesmeerd over een nieuw bereik, dus lijnen, plooien en schaduwen blijven.

  tuniek (fel oranje)        -> marineblauw, de bandietjas (#201f3c)
  broek (fel cyaan)          -> kaki-olijf, de bandietbroek (#534b39)
  sjerp (fel geel)           -> rood, zoals de sjerp van de bandiet en de kooiman
  haar en wenkbrauwen (rood) -> zwart
  sandalen (wit)             -> bruin leer
  schouderstuk (fel groen)   -> donker ijzer
  de huid                    -> een tint donkerder (HUID_DONKER)
  de ogen en de kruisboog blijven ongemoeid

Daarna:
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kooiman_kleur import naar_hsv, hertint

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kruisboog/bron')
UIT  = os.path.join(ROOT, 'enemies/kruisboog')
GROND = 442          # de grondlijn op het canvas (metadata.json): de sandalen staan vlak erboven
HUID_DONKER = 0.80   # de huid een tint donkerder: zoveel van de helderheid blijft over
HUID_VERZ, HUID_VERZ_TOT = 0.76, 0.86   # tot hier vol donkerder, vanaf hier niet meer (het hout)


def maak(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    rgb = arr[..., :3]
    h, s, v = naar_hsv(rgb)
    op = arr[..., 3] > 40
    rij = np.arange(arr.shape[0])[:, None] * np.ones((1, arr.shape[1]))

    haar     = op & ((h < 10) | (h > 345)) & (s > 0.55) & (v > 0.45)
    tuniek   = op & (h >= 10) & (h < 25) & (s > 0.6) & (v > 0.58)
    sjerp    = op & (h >= 25) & (h < 62) & (s > 0.45) & (v > 0.5)
    broek    = op & (h >= 185) & (h < 228) & (s > 0.4)
    schouder = op & (h >= 80) & (h < 160) & (s > 0.35)
    sandaal  = op & (s < 0.18) & (v > 0.65) & (rij > GROND - 75)

    rgb = hertint(rgb, tuniek,   tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas
    rgb = hertint(rgb, broek,    tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek
    rgb = hertint(rgb, sjerp,    tint=356, verz=0.70, laag=0.22, hoog=0.55)   # rode sjerp
    rgb = hertint(rgb, haar,     tint=30,  verz=0.15, laag=0.04, hoog=0.16)   # zwart haar
    rgb = hertint(rgb, sandaal,  tint=28,  verz=0.50, laag=0.18, hoog=0.42)   # bruine sandalen
    rgb = hertint(rgb, schouder, tint=215, verz=0.12, laag=0.16, hoog=0.48)   # donker ijzer

    # de huid een tint donkerder. Het hout van de kruisboog heeft bijna dezelfde tint, maar is
    # verzadigder (0,8 tot 0,9 tegen 0,6 tot 0,75 voor de huid): dus vol donkerder onder HUID_VERZ,
    # en geleidelijk minder tot HUID_VERZ_TOT, waar het hout zit.
    huid = op & ((h < 25) | (h > 345)) & (v < 0.62) & ~(haar | tuniek | sjerp)
    w = np.clip((HUID_VERZ_TOT - s) / (HUID_VERZ_TOT - HUID_VERZ), 0, 1) * huid
    rgb = rgb * (1 - w * (1 - HUID_DONKER))[..., None]

    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]          # magenta-ontspilling, zoals de kooiman
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    rgb[..., 0] = rr - mag
    rgb[..., 2] = bb - mag
    arr[..., :3] = rgb
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(BRON, '*', '*.png'))):
        doel = os.path.join(UIT, os.path.relpath(f, BRON))
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        maak(Image.open(f)).save(doel, optimize=True)
        n += 1
    print(n, 'frames gekleurd naar', os.path.relpath(UIT, ROOT))


if __name__ == '__main__':
    main()
