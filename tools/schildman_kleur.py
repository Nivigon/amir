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

Het bandietpalet is de standaard. Komt er een nieuwe export (nieuwe frames of nieuwe versies van
bestaande), zet hem dan gewoon in de speelmap en draai dit script: een frame dat daar nog in de
oude kleuren staat wordt eerst naar bron/ gekopieerd (zo blijven de oude kleuren bewaard) en dan
omgekleurd. Aan het eind kijkt het na dat er geen frame in de oude kleuren meer in de speelmap staat.

Verandert een bronframe, draai dit opnieuw, en daarna:
    python3 tools/gen-klein.py
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
BRON = os.path.join(ROOT, 'enemies/schildbandiet/bron')
UIT  = os.path.join(ROOT, 'enemies/schildbandiet')
# de mappen met frames van de schildbandiet; ook een nieuwe submap hieronder (een nieuwe export) gaat mee
MAPPEN = ('lagen', 'executie')
# zoveel pixels in een van de oude kleuren (fel blauw, groen, paars) en het is een nieuw, nog niet gekleurd frame
OUD_DREMPEL = 20   # de speelversie telt 0; een vers schild (roze randjes) al zo'n 50


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


def oude_kleuren(beeld):
    """Telt de pixels in het aangeleverde palet: het felle blauwe gewaad, de groene broek, de paarse
    cape. Het bandietpalet zelf (donker marineblauw, kaki) valt er buiten, dus een gekleurd frame
    telt nul en een vers aangeleverd frame honderden of duizenden."""
    arr = np.array(beeld.convert('RGBA')).astype(float)
    h, s, v = naar_hsv(arr[..., :3])
    op = arr[..., 3] > 128
    blauw = (h >= 190) & (h < 235) & (s > 0.45) & (v > 0.40)
    groen = (h >= 70) & (h < 160) & (s > 0.35) & (v > 0.25)
    paars = (h >= 262) & (h < 320) & (s > 0.35) & (v > 0.30)
    return int((op & (blauw | groen | paars)).sum())


def speelframes():
    for map_ in MAPPEN:
        for f in sorted(glob.glob(os.path.join(UIT, map_, '**', '*.png'), recursive=True)):
            if not os.path.basename(f).startswith('amir_'):
                yield f


def main():
    # 1. nieuw aangeleverde frames: staan ze in de speelmap nog in de oude kleuren (een nieuwe export uit
    #    de Animeer tool, nieuw of over een bestaand frame heen), dan is dat het nieuwe origineel: eerst
    #    naar bron/, zodat de oude kleuren bewaard blijven
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
        if os.path.basename(f).startswith('amir_'):
            continue
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
