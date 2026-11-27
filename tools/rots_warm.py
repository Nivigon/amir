#!/usr/bin/env python3
"""De savannerotsen warmer maken: kei, platte rots en rotswand.

De oude platen (koel grijs, dikke zwarte omlijning) staan in design/bron/rotsen_oud/ (en klein/).
Dit script schrijft de speelversie naar design/ (en klein/design/boulder.png):
- het grijs schuift naar warm grijsbruin, hoe grijzer hoe meer (het gras blijft bijna gelijk);
- de zwarte lijnen (rand en kieren) worden warm donkerbruin;
- de buitenrand wordt 1 pixel dunner (niet bij de kleine set).
Vorm en textuur blijven precies hetzelfde, dus PLAT, CLIFF en de props hoeven niet aangepast.
Daarna: python3 tools/gen-offline-manifest.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONKER = np.array([62, 46, 34.])
LICHT = np.array([222, 200, 168.])
LIJN = np.array([88, 66, 48.])


def warm(src, uit, rand=True):
    a = np.array(Image.open(src).convert('RGBA')).astype(float)
    rgb, al = a[..., :3], a[..., 3]
    L = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255
    doel = DONKER + (LICHT - DONKER) * np.clip(L * 1.08, 0, 1)[..., None]
    sat = (rgb.max(-1) - rgb.min(-1)) / 255
    m = np.clip(0.55 - sat * 1.5, 0.15, 0.55)[..., None]
    zwart = (L < 0.22)[..., None]
    m = np.where(zwart, 0.85, m)
    doel = np.where(zwart, LIJN, doel)
    rgb = rgb * (1 - m) + doel * m
    o = Image.fromarray(np.dstack([rgb, al]).clip(0, 255).astype('uint8'))
    if rand:
        o.putalpha(o.getchannel('A').filter(ImageFilter.MinFilter(3)))
    o.save(uit)
    print(os.path.relpath(uit, ROOT), o.size)


for naam in ['boulder.png', 'flatrock.png', 'cliff.png']:
    warm(os.path.join(ROOT, 'design/bron/rotsen_oud', naam), os.path.join(ROOT, 'design', naam))
k = os.path.join(ROOT, 'klein/design/bron/rotsen_oud/boulder.png')
if os.path.exists(k):
    warm(k, os.path.join(ROOT, 'klein/design/boulder.png'), rand=False)
