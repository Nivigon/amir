#!/usr/bin/env python3
"""Maakt design/stad/binnen/deur_recht.png: de deur naar buiten, van binnen gezien.

Buiten is het deurgat van een huis recht, met een houten latei erboven (gevel.png). Binnen stond daar de ronde
boogdeur (deur.png), en dat klopte niet. Dit script maakt uit de boogdeur een rechte deur: de lemen rand blijft,
de boog wordt dichtgezet met leem, de opening loopt recht omhoog tot onder een latei, en die latei is dezelfde
balk als boven het deurgat buiten (STAD_DEUR.latei in gevel.png). De boogdeur zelf blijft de binnenpoort naar
een volgende kamer.

    python3 tools/binnen_deur_recht.py
"""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / 'design/stad/binnen'

# in bronpx van deur.png (772 x 892)
OPEN_L, OPEN_R = 156, 612      # de binnenkant van de stijlen
BOOG_TOP = 64                  # tot hier reikt de boog (met wat marge)
VOLLE_BREEDTE = 300            # vanaf hier is de opening op volle breedte
RECHT_TOP = 215                # de nieuwe bovenkant van de rechte opening
LEEM_VAN, LEEM_TOT = 22, 64    # een strook leem boven de boog, om de boog mee dicht te zetten
LATEI = (337, 1058, 275, 28)   # de latei in gevel.png (STAD_DEUR.latei)


def main():
    a = np.array(Image.open(BIN / 'deur.png').convert('RGBA'))
    b = a.copy()
    # 1. de boog dichtzetten met leem van boven de boog (rij voor rij herhaald)
    # stukken uit die strook onder elkaar, om en om gespiegeld, met een zachte overgang ertussen: zo komt er geen naad
    bron = a[LEEM_VAN:LEEM_TOT, OPEN_L:OPEN_R].astype(float)
    T, O = LEEM_TOT - LEEM_VAN, 14
    vul = np.zeros((RECHT_TOP - BOOG_TOP + T, OPEN_R - OPEN_L, 4))
    gewicht = np.zeros(vul.shape[:2] + (1,))
    y, i = 0, 0
    while y < RECHT_TOP - BOOG_TOP:
        stuk = bron[:, ::-1] if i % 2 else bron
        w = np.ones((T, 1, 1))
        w[:O, 0, 0] = np.linspace(0.05, 1, O)
        w[-O:, 0, 0] = np.linspace(1, 0.05, O)
        vul[y:y + T] += stuk * w
        gewicht[y:y + T] += w[:, :, 0:1].reshape(T, 1, 1)
        y += T - O
        i += 1
    vul = (vul / np.maximum(gewicht, 1e-6))[:RECHT_TOP - BOOG_TOP]
    # bovenaan zacht overlopen in de rand die er al was
    for k in range(O):
        f = (k + 1) / (O + 1)
        vul[k] = vul[k] * f + a[BOOG_TOP + k, OPEN_L:OPEN_R] * (1 - f)
    b[BOOG_TOP:RECHT_TOP, OPEN_L:OPEN_R] = vul.astype(np.uint8)

    # 2. de opening recht omhoog: de rij waar de opening op volle breedte is, naar boven doorgetrokken
    for y in range(RECHT_TOP, VOLLE_BREEDTE):
        b[y, OPEN_L:OPEN_R] = a[VOLLE_BREEDTE, OPEN_L:OPEN_R]
    # een zachte schaduw onder de latei, de opening in
    for y in range(RECHT_TOP, RECHT_TOP + 60):
        f = 0.45 * (1 - (y - RECHT_TOP) / 60)
        b[y, OPEN_L:OPEN_R, :3] = (b[y, OPEN_L:OPEN_R, :3] * (1 - f)).astype(np.uint8)
    img = Image.fromarray(b)
    # 3. de latei van buiten erover, iets breder dan de opening
    g = Image.open(ROOT / 'design/stad/gevel.png').convert('RGBA')
    x, y, w, h = LATEI
    lat = g.crop((x, y, x + w, y + h))
    breed = int((OPEN_R - OPEN_L) * 1.16)
    lat = lat.resize((breed, int(h * breed / w)), Image.LANCZOS)
    lx = (OPEN_L + OPEN_R) // 2 - breed // 2
    img.alpha_composite(lat, (lx, RECHT_TOP - lat.height + 6))
    img.save(BIN / 'deur_recht.png', optimize=True)
    print('geschreven:', BIN / 'deur_recht.png', img.size)


if __name__ == '__main__':
    main()
