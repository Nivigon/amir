#!/usr/bin/env python3
"""Maakt de bruine rotstextuur voor de golvende rand uit de bron.

De bron (tools/bron/rots_bruin.jpg, uit Grok; staat buiten design/ zodat hij niet in de
offline-download komt) is links-rechts naadloos maar boven-onder niet: boven is hij donkerder
dan onder, en de splijtvlakken lopen schuin, dus elke blend over die naad geeft een wazige strook
(geprobeerd, met een brede band en per frequentie; allebei zichtbaar). Daarom wordt hij alleen
verkleind naar 1024 breed, en tekent het spel hem verticaal VERANKERD aan de rand van de massa
(de bovenkant van de grond, de onderkant van een plafond), nooit verticaal herhaald. Een massa
is in beeld nooit hoger dan een tegel, dus dat is genoeg. De grijze (rots_grijs.png) is in beide
richtingen naadloos en blijft zoals hij is.

Verandert de bron, draai dit opnieuw, en daarna gen-offline-manifest.py.
"""
import numpy as np
from PIL import Image

BRON = 'tools/bron/rots_bruin.jpg'
UIT = 'design/golf/rots_bruin.jpg'
BREED = 1024


def meet(a):
    return abs(a[:, 0] - a[:, -1]).mean(), abs(a[0] - a[-1]).mean(), abs(a[:, 1] - a[:, 2]).mean()


if __name__ == '__main__':
    im = Image.open(BRON).convert('RGB')
    im = im.resize((BREED, round(im.height * BREED / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    print('naad links-rechts %.1f, boven-onder %.1f (binnenin %.1f): links-rechts is naadloos, boven-onder niet' % meet(a))
    im.save(UIT, quality=90)
    print('geschreven:', UIT, im.size)
