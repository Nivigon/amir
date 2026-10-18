#!/usr/bin/env python3
"""Kleurt de kooiman-sprites om naar het bandietpalet, en maakt de kooi zwart-doorschijnend.

Zelfde aanpak als tools/slang_kleur.py (`hertint`): de tekening zelf blijft staan. Per
kleurvlak wordt alleen de tint en de verzadiging vervangen en de helderheid over een nieuw
bereik uitgesmeerd, dus de inktlijnen, de plooien en de schaduwen blijven precies zoals ze
getekend zijn. Dat is het verschil met een helderheidsverloop dat de pixels vervangt: daar
vervagen de lijnen van.

De aangeleverde frames (teal hoofddoek, blauw gewaad, groene broek, grijze kooivulling) staan
ongewijzigd in enemies/kooiman/bron/<set>/. Dit leest die bron en schrijft de speelversie naar
enemies/kooiman/<set>/, zodat de kooiman in dezelfde kleuren loopt als de bandiet:

  hoofddoek en gewaad -> marineblauw (de bandietjas, #201f3c)
  broek               -> kaki-olijf (de bandietbroek, #534b39)
  de rode sjerp, de huid en de sandalen blijven ongemoeid
  de kooivulling      -> van (32,32,38) op 50% alpha naar puur zwart (0,0,0) op 50% alpha
  de gele glinsteringen in de tralies (restant van de oude gele kooi) -> neutraal taupe

De masker-grenzen worden per vlak op tint en verzadiging gezocht (de zwarte contour, met lage
verzadiging, valt er vanzelf buiten en blijft dus zwart). Er wordt niet in de lijnen uitgelopen.
In de bron is de broek nog groen, dus het geel is alleen de kooi, geen kleding.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kooiman/bron')
UIT  = os.path.join(ROOT, 'enemies/kooiman')
SETS = ('drag', 'smash', 'recovery', 'stomp', 'hatch', 'stomp_out', 'dood', 'parry')


# ---------------------------------------------------------------- kleurruimte (uit slang_kleur.py)
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

    # de hoofddoek (teal) en het gewaad (blauw) zijn samen één marineblauw vlak
    blauw = op & (s > 0.25) & (h >= 160) & (h < 258)
    # de broek (groen in de bron)
    groen = op & (s > 0.20) & (h >= 78) & (h < 150)
    # het geel/tan van de tralies en de rand van de kooi (de oude gele kooi zat hier nog in). De huid
    # en de sandalen zijn roodbruin op hue < 34; het tan van de kooi loopt van ongeveer 34 tot 74, dus
    # daar scheidt het. Vroeger stond de ondergrens op 40, waardoor de warme kooirand (hue 34-40) bleef
    # staan en de kooi nog geel oogde; nu valt die er ook onder, terwijl de hand en het gezicht (lager
    # in hue) ongemoeid blijven.
    geel = op & (h >= 34) & (h < 80) & (s > 0.20)

    rgb = hertint(rgb, blauw, tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas #201f3c
    rgb = hertint(rgb, groen, tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek #534b39
    rgb = hertint(rgb, geel,  tint=40,  verz=0.05, laag=0.16, hoog=0.36)   # geel weg: neutrale, iets donkerder taupe tralie
    arr[..., :3] = rgb

    # de kooivulling: semi-transparant en donker -> puur zwart, en iets minder doorschijnend (tussen de
    # spijlen wat donkerder), zodat je nog net vaag doorheen kijkt maar niet ziet wat erin zit. De alpha
    # gaat van zo'n 40-65% naar zo'n 55-80%, met de weef-variatie erin behouden.
    rgba = arr
    fill = (al > 100) & (al < 165) & (rgb.max(-1) < 80)
    rgba[..., 0][fill] = 0; rgba[..., 1][fill] = 0; rgba[..., 2][fill] = 0
    rgba[..., 3][fill] = np.minimum(205.0, al[fill] * 1.3)

    # magenta-ontspilling, als losse eindstap. De aangeleverde frames zijn uit een magenta
    # achtergrond geknipt en houden op de randen, en in de handvat-ring van de kooi, nog magenta
    # vast; over de savanne las dat als een roze gloed. Hoeveel magenta: min(rood, blauw) min groen
    # (de chroma-key tilt rood en blauw samen op). Dat trek je er weer uit, zodat de hue naar
    # neutraal grijs zakt. De hue-maskers hierboven slaan magenta (hue rond 300) juist over, dus dit
    # staat er los achteraan. De alpha blijft staan: de ring is een echt, bijna-ondoorzichtig object,
    # alpha laten zakken zou hem dun en kapot maken. De marineblauwe jas (rood is gelijk aan groen)
    # en de huid (groen hoger dan het minimum van rood en blauw) blijven ongemoeid; de rode sjerp
    # verliest alleen zijn paarse randspikkels en blijft helder rood.
    rr, gg, bb = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    rgba[..., 0] = rr - mag
    rgba[..., 2] = bb - mag
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8))


def main():
    n = 0
    for setnaam in SETS:
        for f in sorted(glob.glob(os.path.join(BRON, setnaam, '*.png'))):
            dst = os.path.join(UIT, setnaam, os.path.basename(f))
            maak(Image.open(f)).save(dst)
            n += 1
    if not n:
        sys.exit('geen bronframes gevonden in ' + BRON)
    print(f'{n} frames omgekleurd naar het bandietpalet (hertint, lijnen blijven), kooi zwart op 50% alpha')


if __name__ == '__main__':
    main()
