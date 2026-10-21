#!/usr/bin/env python3
# De losse kooi-plaat voor de duw-lus (enemies/kooiman/kooi/kooi.png) wordt hier uit de
# aangeleverde bron (enemies/kooiman/bron/kooi/kooi.png) gemaakt. De bron heeft grijze spaken
# maar een MASSIEF GELE vulling tussen de spaken; dat past niet bij de ingebakken kooien van de
# man (die zijn grijs met een doorschijnend donker interieur). Dit script haalt het geel eruit en
# maakt er hetzelfde interieur van als in sprites.json staat (cage_interior: dark 32,32,38 at ~50%
# alpha): grijs met wat doorzichtigheid tussen de spaken, zodat je er doorheen kijkt. De grijze
# spaken, de rand en het hengsel blijven zoals ze zijn.
#
# Verandert de bron, draai dit opnieuw, en daarna gen-klein.py en gen-offline-manifest.py.
from PIL import Image
import os

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(HIER, 'enemies/kooiman/bron/kooi/kooi.png')
UIT  = os.path.join(HIER, 'enemies/kooiman/kooi/kooi.png')

INTERIEUR = (32, 32, 38)   # de donkere interieurkleur uit sprites.json
ALFA      = 128            # ~50%: doorschijnend tussen de spaken


def is_geel(r, g, b):
    # geel: rood en groen hoog, blauw duidelijk lager. De grijze spaken (r=g=b) en de donkere
    # randjes vallen hier buiten en blijven dus staan.
    return r > 110 and g > 90 and (r - b) > 55 and (g - b) > 45


def main():
    im = Image.open(BRON).convert('RGBA')
    px = im.load()
    W, H = im.size
    n = 0
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a < 10:
                continue
            if is_geel(r, g, b):
                px[x, y] = (INTERIEUR[0], INTERIEUR[1], INTERIEUR[2], ALFA)
                n += 1
    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    im.save(UIT)
    print('geschreven: %s (%d gele pixels naar doorschijnend donkergrijs)' % (UIT, n))


if __name__ == '__main__':
    main()
