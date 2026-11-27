#!/usr/bin/env python3
"""De losse slangenkoppen voor de onthoofding (KOP, zie notities/slangen.md).

    python3 tools/slang_kop.py

Bron: enemies/slang_kop/bron/kop_{zij,schuin,voor,rug}.png, de vier koppen uit het Grok-blad (post
422e6582-1aea-4db3-9e6c-47163666f01f), gekeyd van magenta, in de kleuren van de zandslang, met een fel groene
nekstomp (#00FF00, zo kwam het langs de moderatie van Grok).

Uit elke bron komen drie kleuren, net als de slangen zelf (tools/slang_kleur.py):
- enemies/slang_kop/groen/  de zandslang (de bron zoals hij is)
- enemies/slang_kop/zwart/  de zwarte slang: bijna zwart lijf, leisteengrijze zadels
- enemies/slang_kop/knock/  de knockslang: jade lijf, violette zadels
En overal wordt de groene stomp donkerrood vlees met een lichtere kern.

Per pixel: het lijf (licht zand) en de zadels (roestbruin) krijgen de kleur van de soort met hun eigen helderheid
erin, zodat de schubben en de schaduw blijven. Contour, oog, muil en tanden blijven zoals ze zijn.
Daarna tools/gen-offline-manifest.py.

Nodig: pillow en numpy.
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies', 'slang_kop', 'bron')
KOPPEN = ['zij', 'schuin', 'voor', 'rug']
# per soort: (lijf, zadel) als rgb; None = laat staan
SOORTEN = {
    'groen': None,
    'zwart': ((34, 31, 28), (112, 104, 98)),
    'knock': ((112, 206, 176), (84, 52, 116)),
}
# de gemiddelde helderheid van lijf en zadel in de bron (zand), om de schaduw relatief mee te nemen
BRON_V = (0.88, 0.55)


def hsv(a):
    r, g, b = a[..., 0] / 255, a[..., 1] / 255, a[..., 2] / 255
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    i = m & (mx == r); h[i] = ((g - b)[i] / d[i]) % 6
    i = m & (mx == g) & (mx != r); h[i] = (b - r)[i] / d[i] + 2
    i = m & (mx == b) & (mx != r) & (mx != g); h[i] = (r - g)[i] / d[i] + 4
    return h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx


def stomp(a):
    """de groene nekstomp wordt vlees: donkerrood, lichter naar het midden"""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    gr = ((g - np.maximum(r, b)) / 255 > 0.2) & (a[..., 3] > 0)
    v = g / 255
    a[gr, 0] = 62 + 118 * v[gr]
    a[gr, 1] = 8 + 22 * v[gr]
    a[gr, 2] = 12 + 22 * v[gr]
    # de magenta zweem op de rand die het keyen liet zitten
    sp = np.maximum(0, np.minimum(a[..., 0], a[..., 2]) - a[..., 1]) * (a[..., 3] < 250)
    a[..., 0] -= sp * 0.8
    a[..., 2] -= sp * 0.8
    return gr


def kleur(a, doel, geen):
    h, s, v = hsv(a)
    huid = (a[..., 3] > 0) & ~geen & (v > 0.16) & (h >= 8) & (h <= 42) & ~((s < 0.15) & (v > 0.85))
    zadel = np.clip((s - 0.42) / 0.15, 0, 1) * np.clip((0.8 - v) / 0.15, 0, 1)
    lijf, zad = np.array(doel[0], float), np.array(doel[1], float)
    rel = np.where(zadel > 0.5, v / BRON_V[1], v / BRON_V[0])
    nieuw = (lijf * (1 - zadel[..., None]) + zad * zadel[..., None]) * np.clip(rel, 0.25, 1.25)[..., None]
    a[huid, :3] = np.clip(nieuw[huid], 0, 255)


def main():
    for soort, doel in SOORTEN.items():
        uit = os.path.join(ROOT, 'enemies', 'slang_kop', soort)
        os.makedirs(uit, exist_ok=True)
        for k in KOPPEN:
            a = np.array(Image.open(os.path.join(BRON, f'kop_{k}.png')).convert('RGBA')).astype(float)
            gr = stomp(a)
            if doel:
                kleur(a, doel, gr)
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
            # 256 kleuren met alfa: een kwart van de grootte, en op het scherm niet te zien
            im.quantize(256, method=Image.Quantize.FASTOCTREE).save(os.path.join(uit, f'kop_{k}.png'), optimize=True)
        print('klaar', soort)


if __name__ == '__main__':
    main()
