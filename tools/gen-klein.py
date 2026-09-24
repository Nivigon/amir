#!/usr/bin/env python3
"""Maakt de kleine spriteset in klein/: dezelfde mappen en bestandsnamen als het
origineel, maar de grote frames op de helft. Het spel kiest bij het starten
welke set het laadt (zie "Beeld" in het startmenu): een telefoon krijgt klein,
een laptop groot. De tekencode rekent overal met vaste maten en rekt het plaatje
daarnaartoe, dus beide sets werken met dezelfde code.

Draai dit opnieuw zodra je sprites van Amir of de hyena toevoegt of vervangt,
en daarna de manifestgenerator:

    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Alleen frames hoger dan MIN_H gaan op de helft. De lopende en stilstaande frames
van Amir (594x301) zijn al kleiner dan hij op een telefoon getekend wordt; die
worden ongewijzigd gekopieerd, zodat de set compleet is en het spel nooit hoeft
terug te vallen op de grote map.

Vereist Pillow: pip install pillow
"""

import os
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow ontbreekt: pip install pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = 'klein'

# Welke families een kleine versie krijgen. Uitbreiden is een regel erbij, plus
# in de HTML het pad van die familie door KLEIN laten lopen.
FAMILIES = ('karakters/amir', 'enemies/hyena', 'enemies/hyena_wit')

FACTOR = 0.5      # zoveel kleiner, per zijde
MIN_H = 400       # alleen frames hoger dan dit gaan op de helft

# Bronmateriaal dat het spel nooit opvraagt: dezelfde regels als de manifestgenerator.
SKIP_DIRS = ('preview', 'docs')
SKIP_NAME = ('_magenta', '_preview', 'sheet', 'startframe')
KEEP_EXT = ('.png',)


def is_source_material(rel):
    parts = rel.split('/')
    if any(p in SKIP_DIRS for p in parts[:-1]):
        return True
    name = parts[-1]
    return any(s in name for s in SKIP_NAME)


def shrink(src, dst):
    im = Image.open(src)
    if im.height <= MIN_H:
        shutil.copyfile(src, dst)
        return 'kopie', im.size, im.size
    w = max(1, round(im.width * FACTOR))
    h = max(1, round(im.height * FACTOR))
    if im.mode not in ('RGBA', 'LA'):
        im = im.convert('RGBA')
    im = im.resize((w, h), Image.LANCZOS)
    im.save(dst, optimize=True)
    return 'halve', Image.open(src).size, (w, h)


def main():
    n_copy = n_small = 0
    bytes_in = bytes_out = 0
    for fam in FAMILIES:
        base = os.path.join(ROOT, fam)
        if not os.path.isdir(base):
            print('map ontbreekt:', fam)
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for name in sorted(filenames):
                if not name.lower().endswith(KEEP_EXT):
                    continue
                src = os.path.join(dirpath, name)
                rel = os.path.relpath(src, ROOT).replace(os.sep, '/')
                if is_source_material(rel):
                    continue
                dst = os.path.join(ROOT, OUT, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                what, _, _ = shrink(src, dst)
                if what == 'kopie':
                    n_copy += 1
                else:
                    n_small += 1
                bytes_in += os.path.getsize(src)
                bytes_out += os.path.getsize(dst)
    print(f'{n_small} frames op de helft, {n_copy} ongewijzigd gekopieerd')
    print(f'{bytes_in / 1048576:.1f} MB origineel, {bytes_out / 1048576:.1f} MB in {OUT}/')


if __name__ == '__main__':
    main()
