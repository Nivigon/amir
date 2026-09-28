#!/usr/bin/env python3
"""Waar de speer uit de speerval in de borst van de baviaan zit, per frame.

De speerval raakt hem van voren (hij rent op Amir af, en Amir staat bij het zegel voor de klif). De speer
blijft dan in zijn borst zitten, door het drama heen tot hij als lijk ligt (BAV_VALSPEER in het spel). Daarvoor
moet per frame bekend zijn waar die plek op zijn borst is. Dit script volgt een stukje vacht van frame tot
frame (het kleinste kwadratisch verschil in een zoekvenster), vanaf een punt dat met de hand is gekozen, en
print de tabel die in BAV_VALSPEER.anker hoort.

Alleen de reeksen waarin de speer hem kan raken (run, hap, brul, idle_grom: dan bevriest hij op dat frame)
en die van het drama erna (idle_grom, brul, dood). De sprong niet: daar schiet zijn lijf zo over het canvas
dat het volgen de weg kwijtraakt, en het spel zet de speer dan waar hij hem raakte. Coordinaten in
bronpixels van het eigen canvas van elke reeks, zoals de frames zijn aangeleverd.

    python3 tools/baviaan_speer_anker.py
"""
import os
import numpy as np
from PIL import Image

MAP = os.path.join(os.path.dirname(__file__), '..', 'enemies', 'baviaan')
# reeks: aantal frames, en een of meer beginpunten (frame, x, y) die met de hand gekozen zijn; vanaf elk
# beginpunt wordt gevolgd tot het volgende, zodat een grote sprong in de houding er niet tussen valt
REEKSEN = {
    'run':       (17, [(5, 210, 365)]),
    'hap':       (26, [(0, 230, 340)]),
    'idle_grom': (39, [(0, 140, 291)]),
    'brul':      (24, [(0, 255, 470), (4, 205, 305), (6, 149, 290)]),
    'dood':      (22, [(0, 300, 303)]),
}
R, ZOEK = 24, 30


def grijs(reeks, i):
    a = np.asarray(Image.open(os.path.join(MAP, reeks, f'{reeks}_{i:02d}.png')).convert('RGBA'), dtype=float)
    al = a[..., 3] / 255
    return (a[..., 0] * .3 + a[..., 1] * .5 + a[..., 2] * .2) * al + (1 - al) * 204


def stap(reeks, van, naar, xy):
    a, b = grijs(reeks, van), grijs(reeks, naar)
    x, y = xy
    T = a[y - R:y + R, x - R:x + R]
    best = None
    for dy in range(-ZOEK, ZOEK + 1):
        for dx in range(-ZOEK, ZOEK + 1):
            P = b[y + dy - R:y + dy + R, x + dx - R:x + dx + R]
            if P.shape != T.shape:
                continue
            s = ((P - T) ** 2).mean()
            if best is None or s < best[0]:
                best = (s, x + dx, y + dy)
    return best[1], best[2]


def volg(reeks, n, starts):
    pos = {}
    starts = sorted(starts)
    for k, (f0, x, y) in enumerate(starts):
        pos[f0] = (x, y)
        tot = starts[k + 1][0] if k + 1 < len(starts) else n       # vooruit tot het volgende beginpunt
        for f in range(f0 + 1, tot):
            pos[f] = stap(reeks, f - 1, f, pos[f - 1])
        if k == 0:                                                   # en terug tot frame 0
            for f in range(f0 - 1, -1, -1):
                pos[f] = stap(reeks, f + 1, f, pos[f + 1])
    return [pos[i] for i in range(n)]


if __name__ == '__main__':
    regels = []
    for reeks, (n, starts) in REEKSEN.items():
        p = volg(reeks, n, starts)
        regels.append(f"    {reeks}: [{', '.join(f'{x},{y}' for x, y in p)}]")
    print('  anker: {   // uit tools/baviaan_speer_anker.py: x, y per frame, achter elkaar')
    print(',\n'.join(regels))
    print('  },')
