#!/usr/bin/env python3
"""Maakt design/mes/mes.png: het mes van Impungushe (talent Jackal Fang).

Er is geen getekend mes, dus het wordt uit Amir zijn eigen speer gezet
(karakters/amir/idle/amirspear.png), zodat het in dezelfde stijl is:

    het lemmet   de speerpunt met de kraag eronder
    het heft     het leerbruine riempje van het speerteken (riem.png, uit
                 tools/speerteken.py), dus draai dat script eerst als de speer verandert
    de knop      een stukje schacht onder de rode linten

De punt wijst omhoog; het spel draait hem zelf. Waar het heft zit print dit
script, en dat hoort in MES.greep in de HTML.

Verandert de speer van Amir, draai dit dan opnieuw, en daarna:

    python3 tools/gen-offline-manifest.py

Vereist Pillow: pip install pillow
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow ontbreekt: pip install pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON_AMIR = os.path.join(ROOT, 'karakters/amir/idle/amirspear.png')
BRON_RIEM = os.path.join(ROOT, 'design/botten/speerteken/riem.png')
UIT = os.path.join(ROOT, 'design/mes/mes.png')

LEMMET = (262, 70, 348, 344)     # de speerpunt tot en met de kraag, in amirspear.png
RIEM_X = 280                     # waar riem.png in amirspear.png begon (zie speerteken.py)
KNOP = (298, 560, 330, 610)      # een stukje schacht, onder de linten


def main():
    speer = Image.open(BRON_AMIR).convert('RGBA')
    riem = Image.open(BRON_RIEM).convert('RGBA')
    lemmet = speer.crop(LEMMET)
    knop = speer.crop(KNOP)
    w = lemmet.width
    h = lemmet.height + riem.height + knop.height - 6
    mes = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # eerst de knop, dan het riempje eroverheen, en het lemmet bovenop: zo vallen de naden
    # onder de omwikkeling
    y_riem = lemmet.height - 4
    y_knop = y_riem + riem.height - 2
    mes.alpha_composite(knop, (KNOP[0] - LEMMET[0], y_knop))
    mes.alpha_composite(riem, (RIEM_X - LEMMET[0], y_riem))
    mes.alpha_composite(lemmet, (0, 0))
    doos = mes.getchannel('A').getbbox()
    mes = mes.crop(doos)
    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    mes.save(UIT)
    greep = (y_riem + riem.height / 2 - doos[1]) / mes.height
    print('design/mes/mes.png: %d x %d' % mes.size)
    print('MES.greep (het midden van het heft, als deel van de hoogte): %.3f' % greep)


if __name__ == '__main__':
    main()
