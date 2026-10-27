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
  de huid                    -> warmbruin (HUID_TINT), met het lokale contrast versterkt (HUID_CONTRAST),
                                zodat de mond, de neus en de frons leesbaar blijven
  de ogen en de kruisboog blijven ongemoeid

Elk vlak neemt ook zijn randje mee (RAND): de anti-aliaspixels langs het haar, de tuniek, de sjerp, de
broek en het schouderstuk staan in de bron nog in de felle kleur, maar net buiten de drempels. Zonder
dat bleven er rode randen om het haar en blauwe om de broek staan.

Daarna:
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kooiman_kleur import naar_hsv, naar_rgb, hertint
from slang_kleur import groei

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kruisboog/bron')
UIT  = os.path.join(ROOT, 'enemies/kruisboog')
GROND = 442          # de grondlijn op het canvas (metadata.json): de sandalen staan vlak erboven
RAND = 3             # zo ver (px) buiten een kleurvlak zoekt het naar zijn randje
HUID_TINT = 18       # de huid van rood (tint 13 in de bron) naar warmbruin, dichter bij de schildman (21)
HUID_HELDER = 1.0    # de gemiddelde helderheid van de huid: zo donker als de bron
HUID_CONTRAST = 2.0  # het verschil met de buurt zoveel keer sterker: de lijnen in het gezicht
HUID_VERZ, HUID_VERZ_TOT = 0.76, 0.86   # tot hier vol huid, vanaf hier niet meer (het hout)


def vervaag(x, r):
    """Twee keer een kastvervaging met straal r (bijna een gauss), met numpy."""
    for _ in range(2):
        for as_ in (0, 1):
            p = np.pad(x, [(r, r) if a == as_ else (0, 0) for a in (0, 1)], mode='edge')
            c = np.cumsum(p, axis=as_)
            c = np.concatenate([np.zeros_like(np.take(c, [0], axis=as_)), c], axis=as_)
            n = x.shape[as_]
            x = (np.take(c, range(2 * r + 1, 2 * r + 1 + n), axis=as_)
                 - np.take(c, range(0, n), axis=as_)) / (2 * r + 1)
    return x


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

    # de randjes: dezelfde tint, maar donkerder of minder verzadigd, en vlak naast het vlak
    haar     |= op & groei(haar, RAND) & ((h < 8) | (h > 340)) & (s > 0.45) & (v > 0.18)
    tuniek   |= op & groei(tuniek, RAND) & (h >= 12) & (h < 28) & (s > 0.7) & (v > 0.35)
    sjerp    |= op & groei(sjerp, RAND) & (h >= 25) & (h < 65) & (s > 0.35)
    broek    |= op & groei(broek, RAND) & (h >= 180) & (h < 255) & (s > 0.15)
    schouder |= op & groei(schouder, RAND) & (h >= 60) & (h < 170) & (s > 0.2)
    sandaal  |= op & groei(sandaal, RAND) & (rij > GROND - 75) & (s < 0.5) & (v > 0.4) & ((h > 35) | (s < 0.3))

    huid = op & ((h < 25) | (h > 345)) & (v < 0.62) & ~(haar | tuniek | sjerp)
    # het hout van de kruisboog heeft bijna dezelfde tint als de huid, maar is verzadigder (0,8 tot 0,9
    # tegen 0,6 tot 0,75): dus vol huid onder HUID_VERZ, en geleidelijk minder tot HUID_VERZ_TOT
    w = np.clip((HUID_VERZ_TOT - s) / (HUID_VERZ_TOT - HUID_VERZ), 0, 1) * huid

    rgb = hertint(rgb, tuniek,   tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas
    rgb = hertint(rgb, broek,    tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek
    rgb = hertint(rgb, sjerp,    tint=354, verz=0.78, laag=0.25, hoog=0.62)   # rode sjerp, fel als bij de schildman
    rgb = hertint(rgb, haar,     tint=30,  verz=0.15, laag=0.04, hoog=0.16)   # zwart haar
    rgb = hertint(rgb, sandaal,  tint=28,  verz=0.50, laag=0.18, hoog=0.42)   # bruine sandalen
    rgb = hertint(rgb, schouder, tint=215, verz=0.12, laag=0.16, hoog=0.48)   # donker ijzer

    # de huid: warmbruin, en het verschil met het gemiddelde in de buurt versterkt. Vroeger werd de huid
    # in zijn geheel donkerder gemaakt, en dan zakten de mond, de neus en de frons weg in de huid
    H, S, V = naar_hsv(rgb)
    buurt = vervaag(np.where(huid, V, 0), 4) / np.maximum(vervaag(huid.astype(float), 4), 1e-3)
    nieuw = naar_rgb(H + HUID_TINT - 13, S * 0.95,
                     np.clip(buurt * HUID_HELDER + (V - buurt) * HUID_CONTRAST, 0, 1))
    rgb = rgb * (1 - w[..., None]) + nieuw * w[..., None]
    # de donkerste lijnen op de huid zijn in de bron fel verzadigd rood (verzadiging bijna 1) en vallen
    # daardoor buiten de huid hierboven: die krijgen alleen de bruine tint, hun helderheid blijft
    H, S, V = naar_hsv(rgb)
    lijn = op & ((H < 19) | (H > 340)) & (V < 0.36) & (S > 0.5) & ~(haar | tuniek | sjerp)
    nieuw = naar_rgb(np.maximum(np.where(H > 340, H - 360, H), HUID_TINT - 3), np.minimum(S, 0.85), V)
    rgb[lijn] = nieuw[lijn]
    # de achterste voet is in de bron olijfgeel geschaduwd (tint 20 tot 45): onderaan, en niet de sandaal,
    # wordt dat ook huid
    voet = op & (rij > GROND - 90) & (h >= 19) & (h < 45) & (s > 0.4) & (v < 0.55) & ~sandaal
    nieuw = naar_rgb(np.full(h.shape, float(HUID_TINT)), np.minimum(s, 0.7), v * 0.85)
    rgb[voet] = nieuw[voet]

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
