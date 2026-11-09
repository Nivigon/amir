#!/usr/bin/env python3
"""De stadsvoorgrond: knipt de losse stukken uit design/stad/voetdecor.png naar design/stad/voorgrond/.

Het spel maakt ze zelf donker en onscherp (vgPlaatje), dus hier alleen knippen, op de rand van wat
er staat. Draai daarna tools/gen-offline-manifest.py.
"""
import os
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
STAD = os.path.join(HIER, '..', 'design', 'stad')
UIT = os.path.join(STAD, 'voorgrond')
# de kolommen in voetdecor.png (links, boven, rechts, onder): elk stuk staat los
STUKKEN = {
    'potten': (331, 440, 573, 600),
    'stenen': (603, 420, 800, 600),
    'kruik':  (1117, 370, 1254, 600),
    'mand':   (1311, 380, 1457, 600),
}

def main():
    os.makedirs(UIT, exist_ok=True)
    bron = Image.open(os.path.join(STAD, 'voetdecor.png')).convert('RGBA')
    for naam, vak in STUKKEN.items():
        stuk = bron.crop(vak)
        stuk = stuk.crop(stuk.getbbox())
        stuk.save(os.path.join(UIT, naam + '.png'), optimize=True)
        print(naam, stuk.size)

if __name__ == '__main__':
    main()
