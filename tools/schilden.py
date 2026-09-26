#!/usr/bin/env python3
"""De drie kapotte schilden uit schilden_hires.zip op spelmaat zetten.

Het spel tekent een schild ongeveer 109 px hoog bij een Amir van 237 px (0,46 Amir,
zie schilden.json in de zip). Op een groot scherm is dat hooguit zo'n 250 px, dus 440
bronrijen is ruim. De ingegraven versies (scheef, onderrand = grondlijn) gaan naar
design/schilden/; de hele, rechte versies laten we voorlopig in de zip.

Bij het klauwenschild is het donkere X-motief bij het vrijstaand maken met de
achtergrond weggeknipt: die vlakken zijn doorzichtig en dan zie je de grond door het
schild. Wat binnen de omtrek ligt en toch leeg is, krijgt daarom donkerbruine verf
(VERF). De ruimte tussen de klauwscheuren is aan de bovenrand ingesloten en wordt dus
ook donker; op spelmaat valt dat niet op.

Vereist Pillow: pip install pillow
"""
import io
import os
import sys
import zipfile

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit('Pillow ontbreekt: pip install pillow')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, 'schilden_hires.zip')
UIT = os.path.join(ROOT, 'design', 'schilden')
HOOG = 440
NAMEN = ['schild_1_gespleten', 'schild_2_klauwen', 'schild_3_verbrand']
VULLEN = ['schild_2_klauwen']
VERF = (52, 30, 20, 255)


def vul_motief(im):
    """Ingesloten lege vlakken binnen het schild dichtverven, onder het plaatje."""
    w, h = im.size
    vast = im.getchannel('A').point(lambda v: 255 if v > 100 else 0)
    # de onderrand is recht afgesneden: dicht tussen de buitenste vaste pixels,
    # anders loopt de vulling van buiten onderlangs het schild in
    xs = [x for x in range(w) if vast.getpixel((x, h - 1))]
    if xs:
        ImageDraw.Draw(vast).line([(xs[0], h - 1), (xs[-1], h - 1)], fill=255)
    ImageDraw.floodfill(vast, (0, 0), 128)                 # alles wat met buiten verbonden is
    motief = vast.point(lambda v: 255 if v == 0 else 0)    # leeg en ingesloten
    motief = motief.filter(ImageFilter.MaxFilter(5))       # tot onder de rafelige randen
    uit = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    uit.paste(VERF, (0, 0), motief)
    uit.alpha_composite(im)
    return uit

os.makedirs(UIT, exist_ok=True)
with zipfile.ZipFile(ZIP) as z:
    for n in NAMEN:
        im = Image.open(io.BytesIO(z.read('schilden_hires/' + n + '.png'))).convert('RGBA')
        if n in VULLEN:
            im = vul_motief(im)
        w = round(im.width * HOOG / im.height)
        im.resize((w, HOOG), Image.LANCZOS).save(os.path.join(UIT, n + '.png'), optimize=True)
        print(n, w, 'x', HOOG)
