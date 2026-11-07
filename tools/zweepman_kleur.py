#!/usr/bin/env python3
"""Kleurt de zweepman om naar het bandietpalet.

Zelfde aanpak als tools/schildman_kleur.py (hertint uit tools/kooiman_kleur.py): de tekening zelf
blijft staan. Per kleurvlak wordt alleen de tint en de verzadiging vervangen en de helderheid over
een nieuw bereik uitgesmeerd, dus de inktlijnen, de plooien en de schaduwen blijven.

De aangeleverde lagen (blauw vest, teal broek, oranje sjerp, rode baard) staan ongewijzigd in
enemies/zweepman/bron/lagen/. Dit leest die bron en schrijft de speelversie naar
enemies/zweepman/lagen/, zodat hij in dezelfde kleuren loopt als de bandiet:

  vest            -> marineblauw (de bandietjas, #201f3c)
  broek           -> kaki-olijf (de bandietbroek, #534b39)
  sjerp           -> rood, zoals de sjerp van de bandiet en de kooiman
  baard en wenkbrauwen -> zwart
  de huid, de laarzen, de polsbanden, de oorring en de ketting blijven ongemoeid
  de opgerolde zweep (de lagen *_z.png, al in leerkleur) blijft buiten dit script
  daarna de magenta-ontspilling van de kooiman (de roze randjes van de chroma-key)

De sjerp en de oorring liggen dicht bij elkaar in tint; de sjerp is een groot vlak, de oorring en de
hanger zijn klein en liggen niet tegen de broek, dus alleen vlakken vanaf SJERP_MIN pixels
die tegen de broek aan liggen worden rood, en van daaruit groeit het
masker in het mattere oranje langs de randen (in fase 2 is de sjerp smal en minder fel).

Het bandietpalet is de standaard. Komt er een nieuwe export, zet hem dan gewoon in de speelmap en
draai dit script: een frame dat daar nog in de oude kleuren staat wordt eerst naar bron/ gekopieerd
(zo blijven de oude kleuren bewaard) en dan omgekleurd. Aan het eind kijkt het na dat er geen frame
in de oude kleuren meer in de speelmap staat.

Daarna:
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
BRON = os.path.join(ROOT, 'enemies/zweepman/bron')
UIT  = os.path.join(ROOT, 'enemies/zweepman')
MAP  = 'lagen'
SJERP_TINT = 24   # het mattere oranje van de sjerp begint hier; de huid zit er net onder (rond 22, s 0,7); de sjerp is
                  # in fase 2 roder (vanaf 14) maar veel verzadigder (s boven 0,84)
SJERP_MIN = 60     # kleinere oranje vlakken zijn goud (oorring, hanger) of licht op de huid
SJERP_BUUR = 4     # de sjerp ligt altijd tegen de broek; een vlak verder daarvandaan (de oorring, een
                   # opgeheven vuist, het hoofd onder de zweep) is geen sjerp
OUD_DREMPEL = 300  # zoveel pixels fel blauw of teal en het is een nieuw, nog niet gekleurd frame


def grote_vlakken(masker, minimum, buur=None):
    """Alleen de samenhangende vlakken (met schuine buren) van minstens `minimum` pixels, en met `buur`
    erbij alleen die tot op SJERP_BUUR px tegen `buur` aan liggen."""
    if buur is not None:
        buur = groei_binnen(buur, np.ones_like(buur), SJERP_BUUR)
    uit = np.zeros_like(masker)
    gezien = np.zeros_like(masker)
    hoog, breed = masker.shape
    for y0, x0 in np.argwhere(masker):
        if gezien[y0, x0]:
            continue
        stapel, vlak = [(y0, x0)], []
        gezien[y0, x0] = True
        while stapel:
            y, x = stapel.pop()
            vlak.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < hoog and 0 <= nx < breed and masker[ny, nx] and not gezien[ny, nx]:
                        gezien[ny, nx] = True
                        stapel.append((ny, nx))
        if len(vlak) >= minimum:
            ys, xs = list(zip(*vlak))
            if buur is None or buur[list(ys), list(xs)].sum() >= 10:
                uit[list(ys), list(xs)] = True
    return uit


def groei_binnen(zaad, ruim, stappen=60):
    """Groeit `zaad` uit (ook schuin) zolang het binnen `ruim` blijft."""
    uit = zaad & ruim
    for _ in range(stappen):
        o = uit.copy()
        o[1:] |= uit[:-1]; o[:-1] |= uit[1:]
        o[:, 1:] |= uit[:, :-1]; o[:, :-1] |= uit[:, 1:]
        o[1:, 1:] |= uit[:-1, :-1]; o[:-1, :-1] |= uit[1:, 1:]
        o[1:, :-1] |= uit[:-1, 1:]; o[:-1, 1:] |= uit[1:, :-1]
        o &= ruim
        if (o == uit).all():
            break
        uit = o
    return uit


def maak(beeld):
    arr = np.array(beeld.convert('RGBA')).astype(float)
    rgb = arr[..., :3]
    h, s, v = naar_hsv(rgb)
    op = arr[..., 3] > 128

    vest  = op & (s > 0.30) & (h >= 203) & (h < 250)
    broek = op & (s > 0.30) & (h >= 165) & (h < 203)
    # de felle kern van de sjerp, en van daaruit het mattere oranje eromheen (in fase 2 is hij minder fel)
    kern = grote_vlakken(op & (h >= 14) & (h < 46) & (s > 0.84) & (v > 0.30), SJERP_MIN, broek)
    sjerp = groei_binnen(kern, op & (h < 46) & (v > 0.22)
                         & (((h >= SJERP_TINT) & (s > 0.72)) | ((h >= 14) & (s > 0.84))))
    # de baard vanuit zijn verzadigde kern; een rozige arm of hoofd in een snelle slag (s rond 0,65) niet
    rood = op & ((h < 12) | (h > 340)) & (v > 0.38)
    baard = groei_binnen(rood & (s > 0.78), rood & (s > 0.60), 2)

    rgb = hertint(rgb, vest,  tint=242, verz=0.46, laag=0.09, hoog=0.30)   # bandietjas #201f3c
    rgb = hertint(rgb, broek, tint=41,  verz=0.28, laag=0.22, hoog=0.46)   # bandietbroek #534b39
    rgb = hertint(rgb, sjerp, tint=356, verz=0.76, laag=0.26, hoog=0.58)   # rode sjerp
    rgb = hertint(rgb, baard, tint=20,  verz=0.20, laag=0.06, hoog=0.20)   # zwarte baard

    # magenta-ontspilling (zie kooiman_kleur.py): min(rood, blauw) min groen eruit, alpha blijft
    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = np.clip(np.minimum(rr, bb) - gg, 0, None)
    rgb[..., 0] = rr - mag
    rgb[..., 2] = bb - mag
    arr[..., :3] = rgb
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def oude_kleuren(beeld):
    """Telt de pixels in het aangeleverde palet: het felle blauwe vest en de teal broek. Het
    bandietpalet (donker marineblauw, kaki) valt erbuiten, dus een gekleurd frame telt bijna nul."""
    arr = np.array(beeld.convert('RGBA')).astype(float)
    h, s, v = naar_hsv(arr[..., :3])
    op = arr[..., 3] > 128
    return int((op & (h >= 175) & (h < 235) & (s > 0.70) & (v > 0.25)).sum())


def speelframes():
    for f in sorted(glob.glob(os.path.join(UIT, MAP, '*.png'))):
        if not f.endswith('_z.png'):
            yield f


def main():
    nieuw = 0
    for f in speelframes():
        if oude_kleuren(Image.open(f)) > OUD_DREMPEL:
            doel = os.path.join(BRON, os.path.relpath(f, UIT))
            os.makedirs(os.path.dirname(doel), exist_ok=True)
            shutil.copy2(f, doel)
            nieuw += 1
    n = 0
    for f in sorted(glob.glob(os.path.join(BRON, MAP, '*.png'))):
        maak(Image.open(f)).save(os.path.join(UIT, os.path.relpath(f, BRON)))
        n += 1
    if not n:
        sys.exit('geen bronframes gevonden in ' + BRON)
    over = [os.path.relpath(f, UIT) for f in speelframes() if oude_kleuren(Image.open(f)) > OUD_DREMPEL]
    print(f'{nieuw} nieuwe frames naar bron/ gezet (oude kleuren bewaard)')
    print(f'{n} frames omgekleurd naar het bandietpalet (hertint, lijnen blijven)')
    if over:
        sys.exit('FOUT: nog in de oude kleuren: ' + ', '.join(over[:10]))


if __name__ == '__main__':
    main()
