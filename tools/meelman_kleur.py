#!/usr/bin/env python3
"""Kleurt de meelman-sprites om naar het bandietpalet, zodat hij bij de bende hoort.

Zelfde aanpak als tools/kooiman_kleur.py en tools/slang_kleur.py (`hertint`): de tekening
zelf blijft staan. Per kleurvlak wordt alleen de tint en de verzadiging vervangen en de
helderheid over een nieuw bereik uitgesmeerd, dus de inktlijnen, de plooien en de schaduwen
blijven precies zoals ze getekend zijn. Dat is het verschil met een helderheidsverloop dat de
pixels vervangt: daar vervagen de lijnen van.

De aangeleverde frames (blauwe tuniek, groene broek, roze mondmasker, roodbruine riem) staan
ongewijzigd in enemies/meelman/bron/<set>/. Dit leest die bron en schrijft de speelversie naar
enemies/meelman/<set>/, zodat de meelman in dezelfde kleuren loopt als de bandiet en de kooiman:

  tuniek      -> marineblauw (de bandietjas, #201f3c)
  broek       -> kaki-olijf  (de bandietbroek, #534b39)
  mondmasker  -> donker doek bij de jas (een gemaskerde rover)
  de roodbruine riem, de huid, het haar en de sandalen blijven ongemoeid (de riem leest als de
    rode sjerp van de bandiet)

De masker-grenzen worden per vlak op tint en verzadiging gezocht (de zwarte contour en de huid,
met lage verzadiging of een warme tint, vallen er vanzelf buiten). Er wordt niet in de lijnen
uitgelopen. De tan meelzakken staan los in items/meelzak/ (dat is meel, die blijven tan) en
worden hier niet aangeraakt.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, glob
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/meelman/bron')
UIT  = os.path.join(ROOT, 'enemies/meelman')
SETS = ('idle', 'opricht', 'worp', 'ren', 'drag')


# ---------------------------------------------------------------- kleurruimte (uit kooiman_kleur.py)
def naar_hsv(rgb):
    r, g, b = rgb[..., 0] / 255.0, rgb[..., 1] / 255.0, rgb[..., 2] / 255.0
    mx, mn = np.max(rgb, axis=-1) / 255.0, np.min(rgb, axis=-1) / 255.0
    d = mx - mn
    h = np.zeros_like(mx)
    raak = d > 1e-6
    i = raak & (mx == r)
    h[i] = ((g - b)[i] / d[i]) % 6
    i = raak & (mx == g) & (mx != r)
    h[i] = ((b - r)[i] / d[i]) + 2
    i = raak & (mx == b) & (mx != r) & (mx != g)
    h[i] = ((r - g)[i] / d[i]) + 4
    return h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx


def naar_rgb(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - np.abs((h / 60) % 2 - 1))
    m = v - c
    nul = np.zeros_like(h)
    deel = (h // 60).astype(int)
    keuze = [deel == k for k in range(6)]
    r = np.select(keuze, [c, x, nul, nul, x, c])
    g = np.select(keuze, [x, c, c, x, nul, nul])
    b = np.select(keuze, [nul, nul, x, c, c, x])
    return np.clip(np.stack([r + m, g + m, b + m], axis=-1) * 255, 0, 255)


def hertint(rgb, masker, tint, verz, laag, hoog, gamma=1.0):
    """Nieuwe tint en verzadiging, helderheid uitgesmeerd over laag..hoog. Het verloop
    binnen het vlak (de plooien, de schaduwen, de lijnen eromheen) blijft."""
    h, s, v = naar_hsv(rgb)
    if not masker.any():
        return rgb
    onder, boven = np.percentile(v[masker], 2), np.percentile(v[masker], 98)
    genormeerd = np.clip((v - onder) / max(boven - onder, 1e-6), 0, 1) ** gamma
    nieuw = naar_rgb(np.full(h.shape, float(tint)),
                     np.full(s.shape, float(verz)),
                     laag + genormeerd * (hoog - laag))
    uit = rgb.copy()
    uit[masker] = nieuw[masker]
    return uit


def maak(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    rgb = arr[..., :3]
    al = arr[..., 3]
    h, s, v = naar_hsv(rgb)
    op = al > 128

    # de tuniek (blauw, sterk verzadigd)
    tuniek = op & (s > 0.30) & (h >= 185) & (h < 240)
    # de broek (groen)
    broek  = op & (s > 0.18) & (h >= 85) & (h < 145)
    # het mondmasker (roze/mauve); de blauwe tuniek (hue < 240) en de roodbruine riem (hue < 30)
    # vallen er vanzelf buiten
    masker = op & (s > 0.12) & (h >= 245) & (h < 345)

    rgb = hertint(rgb, tuniek, tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas #201f3c
    rgb = hertint(rgb, broek,  tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek #534b39
    rgb = hertint(rgb, masker, tint=236, verz=0.18, laag=0.05, hoog=0.20)   # donker doeken mondmasker, bij de jas
    arr[..., :3] = rgb

    # magenta-ontspilling, als losse eindstap. De aangeleverde frames zijn uit een magenta
    # achtergrond geknipt en houden op de randen (en in het haar) nog wat magenta vast; over de
    # savanne las dat als een roze gloed. Hoeveel magenta: min(rood, blauw) min groen. Dat trek je
    # er weer uit, zodat de hue naar neutraal zakt. De hue-maskers hierboven zijn al omgezet, dus
    # dit raakt vooral de randspikkels. De marineblauwe jas (rood is gelijk aan groen) en de huid
    # (groen hoger dan het minimum van rood en blauw) blijven ongemoeid.
    rr, gg, bb = arr[..., 0], arr[..., 1], arr[..., 2]
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    arr[..., 0] = rr - mag
    arr[..., 2] = bb - mag
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main():
    if not os.path.isdir(BRON):
        raise SystemExit('bron ontbreekt: ' + BRON + ' (kopieer de aangeleverde frames daarheen)')
    n = 0
    for setnaam in SETS:
        for f in sorted(glob.glob(os.path.join(BRON, setnaam, '*.png'))):
            dst = os.path.join(UIT, setnaam, os.path.basename(f))
            maak(Image.open(f)).save(dst)
            n += 1
    print('%d frames omgekleurd naar het bandietpalet in enemies/meelman/' % n)


if __name__ == '__main__':
    main()
