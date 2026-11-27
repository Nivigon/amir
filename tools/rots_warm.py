#!/usr/bin/env python3
"""De rotsen warmer maken, met bruine lijnen in plaats van zwart.

De oude platen (koel grijs, dikke zwarte omlijning) staan in design/bron/rotsen_oud/ en
klein/design/bron/rotsen_oud/, met hetzelfde pad als in het spel. Dit script schrijft van elk
de speelversie terug naar design/ (en klein/design/):
- het grijs schuift naar warm grijsbruin, hoe grijzer hoe meer (het gras blijft bijna gelijk);
- de zwarte lijnen (rand en kieren) worden warm donkerbruin;
- bij losse stukken (kei, platte rots, rotswand, rotsdecor, grotkeien) wordt de buitenrand
  1 pixel dunner; niet bij tegels (die moeten naadloos blijven) en niet in de kleine set;
- bij een .jpg op wit (de runerotsen, witKnip) blijft het wit wit.
Vorm, textuur en maten blijven gelijk, dus geen getal in de code verandert.

Een plaat erbij: zet het origineel in bron/rotsen_oud/ op hetzelfde pad en draai dit script.
Maakt een ander script een plaat opnieuw (rotsdecor_knip.py, rots_vulling.py), kopieer die
nieuwe plaat dan eerst naar bron/rotsen_oud/ en draai dit script daarna.
Daarna: python3 tools/gen-offline-manifest.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONKER = np.array([62, 46, 34.])
LICHT = np.array([222, 200, 168.])
LIJN = np.array([88, 66, 48.])
# tegels: naadloos, dus de rand niet aanraken
TEGELS = {'plafond_strook.png', 'rots_vulling.png', 'wand_rand.png', 'wand_richel.png',
          'hoek_plafond_wand.png', 'rotstextuur.png'}


def warm(src, uit, rand=True, wit=False):
    im = Image.open(src)
    jpg = im.mode != 'RGBA'
    a = np.array(im.convert('RGBA')).astype(float)
    rgb, al = a[..., :3], a[..., 3]
    L = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255
    doel = DONKER + (LICHT - DONKER) * np.clip(L * 1.08, 0, 1)[..., None]
    sat = (rgb.max(-1) - rgb.min(-1)) / 255
    m = np.clip(0.55 - sat * 1.5, 0.15, 0.55)
    zwart = L < 0.22
    m = np.where(zwart, 0.85, m)
    if wit:   # de witte achtergrond van een jpg laten staan, anders keyt witKnip hem niet meer weg
        m = m * np.clip((0.90 - L) / 0.08, 0, 1)
    doel = np.where(zwart[..., None], LIJN, doel)
    rgb = rgb * (1 - m[..., None]) + doel * m[..., None]
    out = np.dstack([rgb, al]).clip(0, 255).astype('uint8')
    if jpg:
        Image.fromarray(out[..., :3]).save(uit, quality=95)
    else:
        o = Image.fromarray(out)
        if rand:
            o.putalpha(o.getchannel('A').filter(ImageFilter.MinFilter(3)))
        o.save(uit)
    print(os.path.relpath(uit, ROOT))


for basis, klein in [('design', False), ('klein/design', True)]:
    bron = os.path.join(ROOT, basis, 'bron/rotsen_oud')
    for d, _, fs in os.walk(bron):
        for f in sorted(fs):
            if not f.endswith(('.png', '.jpg')):
                continue
            rel = os.path.relpath(os.path.join(d, f), bron)
            warm(os.path.join(d, f), os.path.join(ROOT, basis, rel),
                 rand=not klein and f not in TEGELS, wit=f.endswith('.jpg'))
