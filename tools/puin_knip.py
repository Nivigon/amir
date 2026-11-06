#!/usr/bin/env python3
"""Knipt de brokken uit design/stad/plein_brokken.png los naar design/stad/puin/puin_01..14.png.

Het spel gebruikt de plaat zelf voor het puin van Nyundo (BRU_SCHADE.brokken); de losse stukken zijn
voor de Maker (Kapotte vloer, familie Puin, de PROPS puin_01..14). De rechthoeken zijn die uit
BRU_SCHADE.brokken.r; elk stuk wordt daarna nog strak op zijn pixels bijgesneden.

    python3 tools/puin_knip.py
    python3 tools/gen-offline-manifest.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = [[0, 0, 110, 73], [114, 0, 89, 65], [207, 0, 37, 30], [248, 0, 77, 67], [329, 0, 28, 23], [361, 0, 110, 70],
     [475, 0, 68, 66], [547, 0, 74, 61], [625, 0, 89, 64], [718, 0, 51, 58], [773, 0, 26, 26], [803, 0, 59, 57],
     [866, 0, 63, 58], [933, 0, 60, 55]]

bron = Image.open(os.path.join(ROOT, 'design/stad/plein_brokken.png')).convert('RGBA')
uit = os.path.join(ROOT, 'design/stad/puin')
os.makedirs(uit, exist_ok=True)
for i, (x, y, w, h) in enumerate(R, 1):
    stuk = bron.crop((x, y, x + w, y + h))
    stuk = stuk.crop(stuk.getbbox())
    stuk.save(os.path.join(uit, 'puin_%02d.png' % i), optimize=True)
    print('puin_%02d.png' % i, stuk.size)
