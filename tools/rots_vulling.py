#!/usr/bin/env python3
"""Maakt design/grot/rots_vulling.png: de steenvulling die boven de plafondlijn ligt.

De grotset heeft wel een plafondband (plafond_strook.png) maar geen vlak steen om die
band aan vast te hangen; grot.json noemt dat vlak ook al ("anker: bovenkant tegen de
bovenrand van het scherm of tegen een rotsvulling"), maar het bestand ontbreekt.

Het staat wel al in de band zelf: rij 0 tot 433 van plafond_strook is massief steen, en
dat stuk tegelt horizontaal al naadloos, want de hele strook doet dat. Daarom knippen we
precies dat stuk eruit. De vulling is zo van hetzelfde plaatje gemaakt als de tanden die
eraan hangen: dezelfde korrel, dezelfde kleur, en in het spel op dezelfde schaal getekend.

Twee bewerkingen zijn nodig om het ook verticaal te kunnen herhalen:

  1. De strook loopt van donker bovenin naar licht onderin. Zomaar onder elkaar gezet
     geeft dat lichte en donkere banden over de rots. Daarom halen we die verloop eruit:
     elke rij wordt op het gemiddelde van het hele stuk gezet, met een brede vervaging
     zodat alleen het verloop verdwijnt en de brokken blijven.
  2. De onder- en bovenrand sluiten niet op elkaar aan. Daarom nemen we het stuk een
     stukje te hoog en kruisvervagen we de overlap, de gewone manier om een tegel
     naadloos te maken. Het blijft een rij-voor-rij bewerking, dus horizontaal blijft
     de naad die de tekenaar al gemaakt had intact.

    python3 tools/rots_vulling.py
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py
"""

import os
import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit('Pillow ontbreekt: pip install pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'design/grot/plafond_strook.png')
UIT = os.path.join(ROOT, 'design/grot/rots_vulling.png')
VAN, TOT = 16, 433     # het massieve deel van de strook (de bovenste rijen zijn contour)
OVERLAP = 96           # zoveel rijen kruisvervagen we voor de naad boven-onder


def rijgemiddelden(im):
    """Het gemiddelde per rij, breed vervaagd: alleen het verloop, niet de brokken."""
    smal = im.resize((1, im.height), Image.LANCZOS)
    smal = smal.resize((1, im.height), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))
    return [smal.getpixel((0, y)) for y in range(im.height)]


def vlak(im):
    """Het verticale licht-donkerverloop eruit, zodat het stuk onder zichzelf past."""
    rijen = rijgemiddelden(im)
    doel = [sum(r[k] for r in rijen) / len(rijen) for k in range(3)]
    uit = Image.new('RGB', im.size)
    for y in range(im.height):
        rij = im.crop((0, y, im.width, y + 1))
        f = [doel[k] / max(1.0, rijen[y][k]) for k in range(3)]
        uit.paste(rij.point([min(255, round(v * f[0])) for v in range(256)]
                            + [min(255, round(v * f[1])) for v in range(256)]
                            + [min(255, round(v * f[2])) for v in range(256)]), (0, y))
    return uit


def naadloos(im, overlap):
    """De onderste rijen over de bovenste heen vervagen: dan sluit onder weer op boven aan."""
    h = im.height - overlap
    uit = im.crop((0, 0, im.width, h))
    staart = im.crop((0, h, im.width, h + overlap))
    kop = uit.crop((0, 0, im.width, overlap))
    for y in range(overlap):
        f = y / (overlap - 1.0)                      # boven helemaal staart, onder helemaal kop
        rij = Image.blend(staart.crop((0, y, im.width, y + 1)),
                          kop.crop((0, y, im.width, y + 1)), f)
        uit.paste(rij, (0, y))
    return uit


def main():
    bron = Image.open(BRON).convert('RGB').crop((0, VAN, Image.open(BRON).width, TOT))
    beeld = naadloos(vlak(bron), OVERLAP)
    beeld.save(UIT, optimize=True)
    print('geschreven:', os.path.relpath(UIT, ROOT), beeld.size)
    px = beeld.load()
    w, h = beeld.size
    d = lambda a, b: sum(abs(a[i] - b[i]) for i in range(3)) / 3
    print('naad boven-onder', round(sum(d(px[x, 0], px[x, h - 1]) for x in range(w)) / w, 2),
          ' links-rechts', round(sum(d(px[0, y], px[w - 1, y]) for y in range(h)) / h, 2),
          ' (twee gewone buurrijen:', round(sum(d(px[x, 10], px[x, 11]) for x in range(w)) / w, 2), ')')


if __name__ == '__main__':
    main()
