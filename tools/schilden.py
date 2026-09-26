#!/usr/bin/env python3
"""De drie kapotte schilden uit schilden_hires.zip op spelmaat zetten.

Het spel tekent een schild ongeveer 109 px hoog bij een Amir van 237 px (0,46 Amir,
zie schilden.json in de zip). Op een groot scherm is dat hooguit zo'n 250 px, dus 440
bronrijen is ruim. De ingegraven versies (scheef, onderrand = grondlijn) gaan naar
design/schilden/; de hele, rechte versies laten we voorlopig in de zip.

Vereist Pillow: pip install pillow
"""
import io
import os
import sys
import zipfile

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow ontbreekt: pip install pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, 'schilden_hires.zip')
UIT = os.path.join(ROOT, 'design', 'schilden')
HOOG = 440
NAMEN = ['schild_1_gespleten', 'schild_2_klauwen', 'schild_3_verbrand']

os.makedirs(UIT, exist_ok=True)
with zipfile.ZipFile(ZIP) as z:
    for n in NAMEN:
        im = Image.open(io.BytesIO(z.read('schilden_hires/' + n + '.png'))).convert('RGBA')
        w = round(im.width * HOOG / im.height)
        im.resize((w, HOOG), Image.LANCZOS).save(os.path.join(UIT, n + '.png'), optimize=True)
        print(n, w, 'x', HOOG)
