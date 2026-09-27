#!/usr/bin/env python3
"""Zet de meegestuurde tribeplaatjes (JPG met een grijze achtergrond) om naar
transparante PNG's in design/tribes/.

De achtergrond is vlak grijs zonder kleur; hout, vacht en schild zijn warm. Er wordt
vanaf de rand gevuld over pixels die grijs zijn en dicht bij de randkleur liggen, zodat
de grijze speerpunten (lichter dan de achtergrond) blijven staan. Daarna bijgesneden op
de inhoud en verkleind naar MAAT: op het scherm zijn ze nooit groter dan 200 px, dus dit
is scherp genoeg voor een scherm met dubbele pixeldichtheid.

De bronnen zijn de JPG's zoals ze in de root van de repo zijn geupload (commit e05702c,
"Add files via upload"); na het omzetten zijn ze daar weggehaald. Wil je het opnieuw
draaien, zet ze dan terug in de root, of geef een map mee:

    python3 tools/tribe_logos.py [map met de jpg's]
"""
import os
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)

PLAATJES = {
    'speartribe.jpg': 'design/tribes/mkuki/logo.png',
    'liontribe.jpg': 'design/tribes/bhubesi/logo.png',
    'jakkaltribe.jpg': 'design/tribes/impungushe/logo.png',
    'quickrecovery.jpg': 'design/tribes/mkuki/abilities/1_quick_recovery.png',
    'thornkiller.jpg': 'design/tribes/mkuki/abilities/2_thorn_breaker.png',
    'lowsweep.jpg': 'design/tribes/mkuki/abilities/3_low_sweep.png',
}
MAAT = 400
GRIJS = 16      # max - min van r, g, b: daaronder telt een pixel als kleurloos
TOL = 28        # zover mag de helderheid van de randkleur afwijken


def knip(bron, doel):
    im = Image.open(bron).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    hel = a.mean(axis=2)
    kleur = a.max(axis=2) - a.min(axis=2)
    rand = np.concatenate([hel[0], hel[-1], hel[:, 0], hel[:, -1]])
    bg = float(np.median(rand))
    kan = (kleur < GRIJS) & (np.abs(hel - bg) < TOL)
    weg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if kan[y, x] and not weg[y, x]:
                weg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if kan[y, x] and not weg[y, x]:
                weg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and kan[ny, nx] and not weg[ny, nx]:
                weg[ny, nx] = True; q.append((ny, nx))
    alfa = Image.fromarray(np.where(weg, 0, 255).astype(np.uint8))
    # een pixel krimpen en zacht maken, anders blijft er een grijze rand staan
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.copy(); rgba.putalpha(alfa)
    box = alfa.point(lambda v: 255 if v > 8 else 0).getbbox()
    rgba = rgba.crop(box)
    z = max(rgba.size)
    vak = Image.new('RGBA', (z, z), (0, 0, 0, 0))
    vak.paste(rgba, ((z - rgba.size[0]) // 2, (z - rgba.size[1]) // 2))
    vak = vak.resize((MAAT, MAAT), Image.LANCZOS)
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    vak.save(doel, optimize=True)
    print(doel, 'achtergrond', round(bg), 'bijgesneden', box)


if __name__ == '__main__':
    import sys
    map_ = sys.argv[1] if len(sys.argv) > 1 else ROOT
    for bron, doel in PLAATJES.items():
        knip(os.path.join(map_, bron), os.path.join(ROOT, doel))
