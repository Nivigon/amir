#!/usr/bin/env python3
"""Kleurt de kruisboogbandiet om naar het bandietpalet.

Zelfde aanpak als tools/schildman_kleur.py en tools/kooiman_kleur.py: de tekening zelf blijft
staan. Per kleurvlak wordt alleen de tint en de verzadiging vervangen en de helderheid over een
nieuw bereik uitgesmeerd, dus de inktlijnen, de plooien en de schaduwen blijven precies zoals
ze getekend zijn.

De aangeleverde frames (rood haar, oranje hemd, gele sjerp, felblauwe broek, witte sandalen)
staan ongewijzigd in enemies/kruisboog/bron/, met dezelfde mappen als de speelversie. Dit leest
die bron en schrijft de speelversie naar enemies/kruisboog/, zodat hij in dezelfde kleuren loopt
als de bandiet, de kooiman en de schildbandiet:

  hemd           -> marineblauw (de bandietjas, #201f3c)
  broek          -> kaki-olijf (de bandietbroek, #534b39)
  sjerp          -> het rood van de bandietsjerp
  haar, wenkbrauwen -> bijna zwart (geen fel rood meer boven het gezicht)
  sandalen       -> leerbruin, zoals de sandalen van de kooiman
  de huid, de ogen en de kruisboog blijven ongemoeid
  daarna de magenta-ontspilling van de kooiman (de roze randjes van de chroma-key)

Komt er een nieuwe export, zet hem dan gewoon in de speelmap en draai dit script: een frame dat
daar nog in de oude kleuren staat wordt eerst naar bron/ gekopieerd (zo blijven de oude kleuren
bewaard) en dan omgekleurd. Aan het eind kijkt het na dat er geen frame in de oude kleuren meer
in de speelmap staat.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-offline-manifest.py

Vereist Pillow en numpy.
"""
import os, sys, glob, shutil
sys.dont_write_bytecode = True   # geen __pycache__ in tools/ door de import hieronder
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kooiman_kleur import naar_hsv, hertint

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/kruisboog/bron')
UIT  = os.path.join(ROOT, 'enemies/kruisboog')
MAPPEN = ('loop', 'mik', 'omlaag')
VOET_Y = 380       # canvas-y: daaronder staan alleen de voeten (grondlijn 443), dus daar is wit de sandaal
OUD_DREMPEL = 20   # zoveel pixels in een van de oude kleuren en het is een nieuw, nog niet gekleurd frame


def groei(masker, n=2):
    """Het masker n pixels breder, alle kanten op."""
    uit = masker.copy()
    for _ in range(n):
        m = uit.copy()
        m[1:] |= uit[:-1]; m[:-1] |= uit[1:]; m[:, 1:] |= uit[:, :-1]; m[:, :-1] |= uit[:, 1:]
        uit = m
    return uit


def maak(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    rgb = arr[..., :3]
    al = arr[..., 3]
    h, s, v = naar_hsv(rgb)
    op = al > 128
    y = np.arange(arr.shape[0])[:, None] * np.ones((1, arr.shape[1]))

    # het haar en de wenkbrauwen: fel rood. De huid zit op hue 14-20 en de donkerrode contour heeft
    # een lage helderheid, dus die vallen er allebei buiten.
    rood   = op & ((h < 12) | (h >= 340)) & (s > 0.55) & (v > 0.30)
    oranje = op & (h >= 12) & (h < 34) & (s > 0.78) & (v > 0.50)    # het hemd (de huid is minder fel)
    geel   = op & (h >= 34) & (h < 70) & (s > 0.45)                 # de sjerp
    blauw  = op & (h >= 175) & (h < 255) & (s > 0.30)               # de broek
    wit    = op & (y > VOET_Y) & (s < 0.25) & (v > 0.40)            # de sandalen
    # de overgangspixels langs het hemd en de sjerp (half oranje of geel, half contour) vallen net buiten
    # de strenge maskers en bleven als spikkels staan; vlak naast het vlak mag het losser
    oranje |= groei(oranje) & op & (h >= 10) & (h < 36) & (s > 0.55) & (v > 0.28)
    geel   |= groei(geel) & op & (h >= 28) & (h < 70) & (s > 0.35) & (v > 0.25)

    rgb = hertint(rgb, rood,   tint=20,  verz=0.30, laag=0.06, hoog=0.20)   # haar: bijna zwart
    rgb = hertint(rgb, oranje, tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas #201f3c
    rgb = hertint(rgb, geel,   tint=356, verz=0.78, laag=0.18, hoog=0.42)   # bandietsjerp
    rgb = hertint(rgb, blauw,  tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek #534b39
    rgb = hertint(rgb, wit,    tint=18,  verz=0.55, laag=0.16, hoog=0.38)   # sandalen: leerbruin

    # magenta-ontspilling (zie kooiman_kleur.py): min(rood, blauw) min groen eruit, alpha blijft
    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    rgb[..., 0] = rr - mag
    rgb[..., 2] = bb - mag
    arr[..., :3] = rgb
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def oude_kleuren(beeld):
    """Telt de pixels in het aangeleverde palet: het felblauwe broek, het oranje hemd, het rode haar.
    Het bandietpalet zelf (donker marineblauw, kaki, donker sjerprood) valt er buiten, dus een
    gekleurd frame telt nul en een vers aangeleverd frame duizenden."""
    arr = np.array(beeld.convert('RGBA')).astype(float)
    h, s, v = naar_hsv(arr[..., :3])
    op = arr[..., 3] > 128
    blauw  = (h >= 190) & (h < 225) & (s > 0.6) & (v > 0.45)
    oranje = (h >= 14) & (h < 30) & (s > 0.85) & (v > 0.65)
    rood   = ((h < 10) | (h >= 345)) & (s > 0.7) & (v > 0.5)
    return int((op & (blauw | oranje | rood)).sum())


def speelframes():
    for map_ in MAPPEN:
        yield from sorted(glob.glob(os.path.join(UIT, map_, '*.png')))


def main():
    # 1. staan er in de speelmap frames in de oude kleuren (een nieuwe export), dan eerst naar bron/
    nieuw = 0
    for f in speelframes():
        if oude_kleuren(Image.open(f)) > OUD_DREMPEL:
            doel = os.path.join(BRON, os.path.relpath(f, UIT))
            os.makedirs(os.path.dirname(doel), exist_ok=True)
            shutil.copy2(f, doel)
            nieuw += 1
    # 2. alles in bron/ opnieuw naar het bandietpalet, in de speelmap
    n = 0
    for f in sorted(glob.glob(os.path.join(BRON, '**', '*.png'), recursive=True)):
        doel = os.path.join(UIT, os.path.relpath(f, BRON))
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        maak(Image.open(f)).save(doel)
        n += 1
    if not n:
        sys.exit('geen bronframes gevonden in ' + BRON)
    # 3. controle: geen enkel speelframe mag nog in de oude kleuren staan
    over = [os.path.relpath(f, UIT) for f in speelframes() if oude_kleuren(Image.open(f)) > OUD_DREMPEL]
    print(f'{nieuw} nieuwe frames naar bron/ gezet (oude kleuren bewaard)')
    print(f'{n} frames omgekleurd naar het bandietpalet (hertint, lijnen blijven)')
    if over:
        sys.exit('FOUT: nog in de oude kleuren: ' + ', '.join(over[:10]))


if __name__ == '__main__':
    main()
