#!/usr/bin/env python3
"""Maakt de plaatjes van het speerteken in design/botten/speerteken/: het doek in
drie kleuren en het leren riempje. Alles komt uit plaatjes die al in het spel
staan, zodat het in dezelfde stijl is getekend.

    doek_zwart/  doek_vaal/  doek_rood/
        de twintig beelden van het blauwe doek van het skelet
        (design/botten/skelet/doek/), omgekleurd op helderheid: de inktlijn blijft
        donker, de plooien en de glans blijven waar ze zijn, alleen de kleur
        verandert. Bijgesneden tot wat er in de beelden staat; waar die snede in
        de speer ligt, print dit script, en dat hoort in TEKEN.doek in de HTML.

    riem.png
        de rode omwikkeling onder de punt van Amir zijn eigen speer
        (karakters/amir/idle/amirspear.png), uitgeknipt en leerbruin gekleurd.
        Alleen het rood en de inktlijn blijven staan, de speerpunt en de schacht
        eronder worden doorzichtig.

Verandert het doek of de speer van Amir, draai dit dan opnieuw, en daarna:

    python3 tools/gen-klein.py
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
BRON_DOEK = os.path.join(ROOT, 'design/botten/skelet/doek')
BRON_AMIR = os.path.join(ROOT, 'karakters/amir/idle/amirspear.png')
UIT = os.path.join(ROOT, 'design/botten/speerteken')
N = 20

# helderheid (0 tot 255) naar een kleur; dezelfde formules als in de schets
KLEUREN = {
    'zwart': lambda l: (lambda v: (v * 0.96, v * 0.94, v * 1.06))(10 + l * 0.30),
    'vaal':  lambda l: (lambda v: (v * 1.02, v * 0.97, v * 0.93))(30 + l * 0.34),
    'rood':  lambda l: (lambda v: (18 + v * 190, 8 + v * 30, 8 + v * 28))(l / 255),
}

# de omwikkeling in amirspear.png: x 280 tot 343, y 344 tot 382
RIEM = (280, 344, 343, 382)


def helder(r, g, b):
    return 0.3 * r + 0.59 * g + 0.11 * b


def klem(v):
    return max(0, min(255, int(round(v))))


def doek():
    beelden = [Image.open(os.path.join(BRON_DOEK, 'doek_%02d.png' % i)).convert('RGBA') for i in range(N)]
    w, h = beelden[0].size
    # een snede voor alle beelden samen, anders verspringt het doek tussen de beelden
    doos = None
    for im in beelden:
        b = im.getchannel('A').getbbox()
        if b is None:
            continue
        doos = b if doos is None else (min(doos[0], b[0]), min(doos[1], b[1]), max(doos[2], b[2]), max(doos[3], b[3]))
    doos = (max(0, doos[0] - 2), max(0, doos[1] - 2), min(w, doos[2] + 2), min(h, doos[3] + 2))
    for naam, kleur in KLEUREN.items():
        map_ = os.path.join(UIT, 'doek_' + naam)
        os.makedirs(map_, exist_ok=True)
        for i, im in enumerate(beelden):
            uit = im.crop(doos)
            px = uit.load()
            for y in range(uit.height):
                for x in range(uit.width):
                    r, g, b, a = px[x, y]
                    if not a:
                        continue
                    nr, ng, nb = kleur(helder(r, g, b))
                    px[x, y] = (klem(nr), klem(ng), klem(nb), a)
            uit.save(os.path.join(map_, 'doek_%02d.png' % i), optimize=True)
    print('doek: bron %d x %d, snede x %d tot %d, y %d tot %d' % (w, h, doos[0], doos[2], doos[1], doos[3]))
    print("  in de HTML: doek: { bron: [%d, %d], x: %d, y: %d, w: %d, h: %d }" %
          (w, h, doos[0], doos[1], doos[2] - doos[0], doos[3] - doos[1]))


def riem():
    im = Image.open(BRON_AMIR).convert('RGBA').crop(RIEM)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            l = helder(r, g, b)
            rood, donker = r > g + 45, l < 55
            if not a or not (rood or donker):
                px[x, y] = (0, 0, 0, 0)
                continue
            # rood naar leer: de helderheid van het rood wordt de helderheid van het bruin
            v = r / 255 if rood else l / 255 * 0.6
            px[x, y] = (klem(28 + 150 * v), klem(16 + 92 * v), klem(9 + 50 * v), a)
    im.save(os.path.join(UIT, 'riem.png'), optimize=True)
    print('riem: %d x %d' % im.size)


if __name__ == '__main__':
    os.makedirs(UIT, exist_ok=True)
    doek()
    riem()
