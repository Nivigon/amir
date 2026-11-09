#!/usr/bin/env python3
"""Knipt de takel voor de gevels (een accent, zie "accenten" in notities/stad.md) uit design/stad/bron/takel_grok.png.

De Grok-plaat (1296x1536, doorzichtige achtergrond): links een strook muur, daaruit een ruwe stam met een schuine tak eronder,
aan het eind een katrol, en aan het touw een mand. We maken er twee stukken van:
  takel_arm.png   de stam, de tak, de katrol en het losse touw dat om de tak geknoopt is (de muurstrook links gaat eraf:
                  de stam steekt in het spel uit de zijkant van het huis)
  takel_mand.png  de twee touwen onder de katrol en de mand: dat stuk slingert in de wind om het punt bovenaan (DRAAI)

Het script print de maten voor STAD_TAKEL.

    python3 tools/takel_knip.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAD = os.path.join(ROOT, 'design', 'stad')
BRON = os.path.join(STAD, 'bron', 'takel_grok.png')
MUUR = 192                    # tot hier is het de muurstrook; vanaf hier de stam
MAND = (900, 530, 1262, 1110)  # het slingerende stuk: de touwen onder de katrol en de mand
DRAAI = (1120, 530)           # daar hangt het slingerende stuk aan (net onder de katrol, tussen de twee touwen)
STAM = 272                    # het midden van de stam (hoogte in de plaat): dat komt op de bovenste balkenrij van het huis


def main():
    a = np.asarray(Image.open(BRON).convert('RGBA')).copy()
    a[a[..., 3] < 24, 3] = 0                                # bijna onzichtbare spikkels weg, anders klopt de omtrek niet
    x0, y0, x1, y1 = MAND
    mand = Image.fromarray(a[y0:y1, x0:x1].copy())
    a[y0:y1, x0:x1, 3] = 0                                   # uit de arm halen
    arm = Image.fromarray(a[:, MUUR:])
    ab = arm.getbbox(); arm = arm.crop(ab)
    mb = mand.getbbox(); mand = mand.crop(mb)
    arm.save(os.path.join(STAD, 'takel_arm.png'), optimize=True)
    mand.save(os.path.join(STAD, 'takel_mand.png'), optimize=True)
    # alles in px van de plaat, met de muur (MUUR) als x 0 en de bovenkant van de arm als y 0
    ay = ab[1]
    print(f"  arm: {{ w: {arm.width}, h: {arm.height}, x: {ab[0]}, stam: {STAM - ay} }},")
    print(f"  mand: {{ w: {mand.width}, h: {mand.height}, x: {x0 + mb[0] - MUUR}, y: {y0 + mb[1] - ay} }},")
    print(f"  draai: [{DRAAI[0] - MUUR}, {DRAAI[1] - ay}],")


if __name__ == '__main__':
    main()
