#!/usr/bin/env python3
"""Maakt de kleine spriteset in klein/: dezelfde mappen en bestandsnamen als het
origineel, maar op de helft (of een eigen factor per doel, zie DOELEN). Het spel
kiest bij het starten welke set het laadt (zie "Beeld" in het startmenu): een
telefoon krijgt klein, een laptop groot.
De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met
dezelfde code.

Draai dit opnieuw zodra je sprites toevoegt of vervangt, en daarna de
manifestgenerator:

    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py

Welke plaatjes meedoen staat hieronder in DOELEN, en dat is met opzet een korte
lijst. Een plaatje halveren mag alleen als het op een telefoon nog steeds groter
is dan het stukje scherm waar het op terechtkomt. Dat is per familie gemeten door
drawImage af te luisteren in een echt level op een telefoonscherm (852x393, waar
het spel op 1,5 canvaspixel per schermpixel tekent) en de bronmaat te delen door
de getekende maat in apparaatpixels. Die factor staat achter elk doel.

Alles onder de ongeveer 2x is bewust NIET opgenomen, want dan levert halveren een
plaatje op dat kleiner is dan het scherm vraagt, en dat zie je meteen:

    de boom (1,0x) en de struik (1,2x) staan al vrijwel precies op maat
    het doornbos (0,9x) is zelfs al krap
    de dorpshutten (ongeveer 1,8x) en de voorgrondhut (1,2x) vallen af
    de klif (1,9x) en de grondrand (2,0x) zitten op de grens
    Amir zelf (1,7x) en de dorpelinge (1,9x) ook

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

FACTOR = 0.5           # zoveel kleiner, per zijde (de standaard; een doel kan een eigen factor hebben)
MIN_H_STANDAARD = 400  # frames lager dan dit blijven zoals ze zijn

# Elk doel is een map of een los bestand, met de gemeten overmaat erachter. Het
# tweede getal is de hoogtedrempel: frames die lager zijn worden ongewijzigd
# gekopieerd, zodat de set compleet blijft en het spel nooit hoeft terug te vallen.
# Een optioneel derde getal is de factor voor dat doel (standaard FACTOR, 0,5): voor een
# familie die ook op de helft nog ruim te groot is. Het spel moet dan weten hoeveel keer
# kleiner het plaatje is: zet die familie in KLEIN_BRON in de HTML (het script print
# die lijst aan het eind), anders tekent hij het op de halve maat in plaats van de hele.
DOELEN = [
    # (pad, drempel) of (pad, drempel, factor)
    ('karakters/amir', 400),            # de sprong-, buk- en zwaaiframes (647 hoog); de
                                        # loop- en staframes zijn 301 hoog en blijven heel
    ('enemies/hyena', 400),             # 2,3x
    ('enemies/hyena_wit', 400),
    ('enemies/blackpanther', 400),      # 2,5x   veruit de grootste post: 97 frames, twee vachten
    ('enemies/panter_wit', 400),
    ('enemies/schorpioen1', 400),       # 3,5x
                                        # op een canvas van 1150x981; de figuur zelf is 800 hoog
                                        # en wordt op Amir zijn hoogte getekend
    ('enemies/bandiet', 400),           # 95 frames op een canvas van 461x504; de figuur is 351
                                        # hoog en wordt op iets boven Amir zijn hoogte getekend
    ('enemies/bandiet_elite', 400),     # de elite-garde (omgekleurd uit bandiet), zelfde maat en canvas
    ('enemies/bandiet_duin', 400),      # de Duinwacht (omgekleurd uit bandiet), zelfde maat en canvas
    ('enemies/schildbandiet/lagen', 60),  # de schildbandiet (lagen.json): de figuur is 340 hoog op een canvas van
                                        # 544x860, maar elk stuk is bijgesneden tot zijn eigen randen (het schild
                                        # 266 hoog, een lijf rond 330), dus onder de gewone drempel; even veilig te
                                        # halveren als complete frames, want het is dezelfde tekening op dezelfde
                                        # schaal. dx, dy, w en h in de json blijven ongewijzigd, het spel rekt het
                                        # halve plaatje naar die maat
    ('enemies/schildbandiet/executie/lagen', 60),  # de dood en de executie (executie.json): knielen, wankel, val en de
                                        # special execution, ook bijgesneden lagen (Amir rond 190 tot 265 hoog, een
                                        # lijf rond 330, een wond 123), dus dezelfde lage drempel
    ('enemies/kruisboog', 400),         # 107 frames op een canvas van 530x505; de figuur is 307 hoog. Op een
                                        # telefoon gemeten (Test 55) 2,0x tot 3,5x, dus op de helft nog 1,0x of meer.
                                        # Zonder halve set was hij daar met 126 MB uitgepakt de grootste post van het
                                        # level (meer dan de schildbandiet en Amir samen). De tekencode rekt elk frame
                                        # naar KRB.w en KRB.h (canvaspixels), dus het halve frame komt op dezelfde maat
                                        # en plek; bron/ blijft erbuiten
    ('enemies/kooiman', 400),           # 81 frames op een canvas van 726x648; de gebukte figuur is 301
                                        # hoog en wordt op ongeveer Amir zijn hoogte getekend
    ('enemies/meelman', 400),           # 3,3x: idle 3,26, oprichten 3,26, worp 3,29, ren 3,44, slepen 3,19 (Test 42);
                                        # 115 frames op een canvas van 744x469; bron/ blijft erbuiten. De tekencode
                                        # rekt elk frame naar MEEL.w en MEEL.h (canvaspixels), dus het halve frame
                                        # komt op dezelfde maat en plek
    ('enemies/vogel', 400),             # de secretarisvogel uit de kooi: 50 frames op 536x405,
                                        # klein getekend (ongeveer Amir-grootte met wings)
    ('enemies/baviaan', 400),           # 2,5x in het gevecht, 2,25x in de afzet, val en landing (daar maakt
                                        # BAV_GROEI hem 1,12 keer groter), 4,0x aan de rotswand (hang_idle).
                                        # 385 frames op canvassen van 493x592 tot 900x800; bron/ blijft erbuiten.
                                        # De tekencode rekent in bronpixels via bronW en bronH, dus het halve
                                        # frame komt op dezelfde maat en plek
    ('enemies/goudaapje', 400, 0.25),   # op een kwart: gemeten op het origineel 5,5x, 4,9x in de afzet en landing,
                                        # 9,8x aan de wand (dezelfde frames als de baviaan, omgekleurd, maar veel
                                        # kleiner getekend). Op de helft bleef dat 2,45x of meer, dus nog een keer
                                        # gehalveerd: een kwart zit op 1,4x, 1,2x in de afzet en landing (het krapst)
                                        # en 2,5x aan de wand. De tekencode rekent in bronpixels via bronW en bronH,
                                        # met de factor uit KLEIN_BRON, dus het kwartframe komt op dezelfde maat en plek.
                                        # De grote set (laptop) blijft heel: daar gemeten (Baboon 4, Formaat 25) 1,61x op
                                        # 1440x900 met devicePixelRatio 2 (afzet en landing; de rest 1,81x, aan de wand
                                        # 3,22x) en 2,69x op 1920x1080 met 1 (de rest 3,01x, aan de wand 5,36x). Krapst
                                        # 1,61x, onder de 2x, dus halveren zou daar zachter worden dan het scherm vraagt
    ('karakters/dorpeling1', 400),      # 2,5x
    ('amir runc/amir_sprites/design/amir', 400),    # de speerworp (814 hoog); het
                                        # projectiel is 67 hoog en wordt ongewijzigd gekopieerd
    ('design/vegetatie/drygrass_sheet.png', 400),
    ('design/drygrass.png', 400),       # 4,7x
    ('design/drygrass_sneeuw.png', 400),
    ('design/boulder.png', 400),        # 2,6x
    ('design/boulder_sneeuw.png', 400),
    ('design/villeaghut.png', 400),     # 2,3x  staat altijd als ver decor, dus op 60 procent
    ('design/villeaghut_sneeuw.png', 400),
    ('design/botten', 60),              # 6,4x  losse botten, allemaal klein
    ('design/grot', 60),                # 7,3x  de grotset: het plafond, de hoekstukken en
                                        # de wandtegels zijn met afstand de grootste bronnen
                                        # van het spel, en ze worden tot een tiende getekend.
                                        # De keien zijn klein maar zitten er nog altijd ruim
                                        # vier keer boven, vandaar dezelfde lage drempel als
                                        # bij de botten. De tekencode rekent met de maten uit
                                        # grot.json en rekt elk stuk naar die maat, dus de
                                        # ankerpunten blijven op hun plek staan.
]

# Bronmateriaal dat het spel nooit opvraagt. Een bestand dat hierboven bij naam
# staat wordt altijd verwerkt, ook als het "sheet" heet.
SKIP_DIRS = ('preview', 'docs', 'bron')   # bron bewaart aangeleverde frames; de speelversie staat ernaast
SKIP_NAME = ('_magenta', '_preview', 'sheet', 'startframe')
KEEP_EXT = ('.png',)


def is_source_material(rel):
    parts = rel.split('/')
    if any(p in SKIP_DIRS for p in parts[:-1]):
        return True
    return any(s in parts[-1] for s in SKIP_NAME)


def bestanden(pad):
    """Alle png's onder een doel: een los bestand, of alles in een map."""
    vol = os.path.join(ROOT, pad)
    if os.path.isfile(vol):
        yield pad, True            # bij naam genoemd: altijd meenemen
        return
    if not os.path.isdir(vol):
        print('bestaat niet, overgeslagen:', pad)
        return
    for dirpath, dirnames, filenames in os.walk(vol):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.lower().endswith(KEEP_EXT):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, '/')
            if is_source_material(rel):
                continue
            yield rel, False


def verwerk(rel, drempel, factor=FACTOR):
    src = os.path.join(ROOT, rel)
    dst = os.path.join(ROOT, OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src)
    if im.height <= drempel:
        shutil.copyfile(src, dst)
        return False
    w = max(1, round(im.width * factor))
    h = max(1, round(im.height * factor))
    if im.mode not in ('RGBA', 'LA'):
        im = im.convert('RGBA')
    im.resize((w, h), Image.LANCZOS).save(dst, optimize=True)
    return True


def main():
    klein = kopie = 0
    bytes_in = bytes_uit = 0
    gezien = set()
    for doel in DOELEN:
        pad, drempel = doel[0], doel[1]
        factor = doel[2] if len(doel) > 2 else FACTOR
        for rel, genoemd in bestanden(pad):
            if rel in gezien:
                continue
            gezien.add(rel)
            if verwerk(rel, drempel, factor):
                klein += 1
            else:
                kopie += 1
            bytes_in += os.path.getsize(os.path.join(ROOT, rel))
            bytes_uit += os.path.getsize(os.path.join(ROOT, OUT, rel))

    # Plaatjes die er eerder in stonden en nu niet meer bij een doel horen: weg,
    # anders blijft het spel een verouderde kleine versie laden.
    weg = 0
    basis = os.path.join(ROOT, OUT)
    for dirpath, dirnames, filenames in os.walk(basis, topdown=False):
        for name in filenames:
            abspad = os.path.join(dirpath, name)
            rel = os.path.relpath(abspad, basis).replace(os.sep, '/')
            if rel not in gezien:
                os.remove(abspad)
                weg += 1
        if not os.listdir(dirpath) and dirpath != basis:
            os.rmdir(dirpath)

    print(f'{klein} frames verkleind, {kopie} ongewijzigd gekopieerd'
          + (f', {weg} verouderde verwijderd' if weg else ''))
    print(f'{bytes_in / 1048576:.1f} MB origineel, {bytes_uit / 1048576:.1f} MB in {OUT}/')

    # In de HTML staat dezelfde lijst onder KLEIN_FAM. Die bepaalt voor welke paden
    # het spel de kleine map probeert; staat er iets niet bij, dan blijft die familie
    # stilletjes de grote versie laden. Hier afdrukken, zodat je kunt vergelijken.
    print('\nKLEIN_FAM in amir-king-of-africa.html hoort te zijn:')
    for doel in DOELEN:
        pad = doel[0]
        vol = os.path.join(ROOT, pad)
        print(f"  '{pad}/'," if os.path.isdir(vol) else f"  '{pad}',")

    # De doelen met een eigen factor: het spel leest hoeveel keer kleiner het plaatje is
    # uit KLEIN_BRON (bronW en bronH rekenen daarmee terug naar de maat van het origineel).
    # Een doel met de standaardfactor hoort er niet in, dat is de standaard (2).
    print('\nKLEIN_BRON in amir-king-of-africa.html hoort te zijn:')
    for doel in DOELEN:
        if len(doel) > 2 and doel[2] != FACTOR:
            pad = doel[0]
            vol = os.path.join(ROOT, pad)
            print(f"  '{pad}{'/' if os.path.isdir(vol) else ''}': {round(1 / doel[2])},")


if __name__ == '__main__':
    main()
