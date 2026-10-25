#!/usr/bin/env python3
"""Schrijft offline-assets.json: de lijst die de service worker binnenhaalt
als je in het startmenu op "Download voor offline" drukt.

Draai dit opnieuw zodra je sprites of geluiden toevoegt, weghaalt of vervangt:

    python3 tools/gen-offline-manifest.py

De versie in het bestand is een hash over alle paden en groottes. Verandert er
iets aan de assets, dan verandert de versie, en de service worker weet dat hij
de oude cache mag weggooien.
"""

import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mappen die het spel tijdens het spelen inlaadt. klein/ is de halve spriteset
# van Amir en de hyena (tools/gen-klein.py); die hoort erbij zodat het spel ook
# offline nog van set kan wisselen.
# 'amir runc' is de oude mappenstructuur; daar staan de speerworpframes.
# items/ (de drinkkalebas, de meelzakken) en ravijn/assets/ (de wand en de stenen van het ravijn)
# zaten er lang niet in, en dan ontbraken ze offline in elk level met een ravijn of een meelman.
ASSET_DIRS = ('amir runc', 'design', 'enemies', 'items', 'karakters', 'klein', 'music', 'ravijn', 'sounds')

# Alleen deze extensies; de rest is bronmateriaal of documentatie. De json hoort
# erbij omdat het spel enemies/hyena/metadata.json tijdens het laden opvraagt.
KEEP_EXT = ('.png', '.jpg', '.jpeg', '.mp3', '.json')

# Bronmateriaal dat het spel nooit opvraagt: sprite sheets, previews en de
# magenta-werkbestanden. De drie vegetatie-sheets staan wel letterlijk in de
# HTML, dus die horen er wel bij.
SHEETS_IN_USE = (
    'design/vegetatie/boom_sheet.png',
    'design/vegetatie/drygrass_sheet.png',
    'design/vegetatie/struik_sheet.png',
)


def is_source_material(rel: str) -> bool:
    name = os.path.basename(rel)
    # De halve set spiegelt de mappen van het origineel, dus dezelfde regels gelden
    # daar. Zonder dit zou klein/design/vegetatie/drygrass_sheet.png als bronmateriaal
    # gelden en uit de lijst vallen, terwijl het spel hem op een telefoon juist gebruikt.
    kaal = rel[len('klein/'):] if rel.startswith('klein/') else rel
    # docs-mappen zijn leesvoer bij de assets: readme's en previews, niets voor het spel
    if '/docs/' in rel:
        return True
    # bron-mappen bewaren aangeleverde frames waar een script de speelversie van maakt
    # (tools/baviaan_run_fix.py); het spel laadt alleen die speelversie
    if '/bron/' in rel:
        return True
    if '_magenta' in name or '_preview' in name:
        return True
    # ravijn/assets/ heeft twee werkbestanden van de module naast de platen die het spel laadt
    if name in ('referentie_frames.png', 'grond_strip.png'):
        return True
    if 'sheet' in name and kaal not in SHEETS_IN_USE:
        return True
    return False


# De arena-set: wat de Arena modus van de sandbox nodig heeft, zodat de speler alleen dat kan
# downloaden (de knop "Alleen de Arena modus" onder Instellingen) in plaats van het hele spel.
# De basis (ARENA_MAPPEN, per voorvoegsel zonder klein/; de kleine set volgt vanzelf): Amir, het
# decor van de arena van de koning, wat de knoppen in de wizard kunnen oproepen (bloed, doornbos,
# water, kalebassen, de abilities), het gif van de slangen (dat laadt het spel altijd), alle
# geluiden en alle muziek (de speler kiest zelf een nummer). De losse bestanden in design/ horen
# er allemaal bij: het spel laadt ze bij het opstarten. Daarbovenop per soort uit SB_ARENA_SOORTEN
# zijn frames (ARENA_SOORTEN): het spel vraagt alleen de soorten die in de arena aan staan, zodat
# een speler die alleen tegen de schildman wil vechten alleen de schildman ophaalt.
#
# tools/arena-assets.js meet dit na: hij speelt de arena en meldt FOUT op elk bestand dat het
# spel opvraagt en hier niet in staat. Draai hem na een wijziging aan deze lijsten of aan de arena.
ARENA_MAPPEN = (
    'karakters/amir/', 'amir runc/', 'items/', 'ravijn/', 'sounds/', 'music/',
    # wat het spel bij het opstarten laadt, los van een level: het gif van de slangen en de dolk van de
    # bandiet. Wat het menu voor het gekozen levelkaartje alvast laadt (laadLevel, bij het opstarten de
    # nieuwste test) hoort hier niet bij: offline ontbreekt dat zonder gevolgen, het level wordt niet gespeeld
    'enemies/slang2/venom.png', 'enemies/slang1_knock/venom.png', 'enemies/bandiet/dolk/',
    'design/speer/', 'design/doornbos/', 'design/fakkel/', 'design/grot/', 'design/water/', 'design/vegetatie/',
    'design/schilden/', 'design/klimmen/', 'design/tribes/', 'design/menu/', 'design/bloed/', 'design/botten/',
    'design/mes/', 'design/zwart/', 'design/golf/', 'design/bg/',
)
# per soort (de sleutel uit SB_ARENA_SOORTEN in de HTML) de mappen met zijn frames; de bandiet met
# zijn elite en de Duinwacht (knoppen in de wizard), de kooiman met zijn vogel, de fosfor tekent
# met de frames van de zandslang
ARENA_SOORTEN = {
    'scorp': ('enemies/schorpioen1/',),
    'groen': ('enemies/slang1_zand/',),
    'zwart': ('enemies/slang2_roet/', 'enemies/slang2/'),
    'knock': ('enemies/slang1_knock/',),
    'fosfor': ('enemies/slang1_zand/',),
    'hyena1': ('enemies/hyena/',),
    'panter': ('enemies/blackpanther/',),
    'bandiet': ('enemies/bandiet/', 'enemies/bandiet_elite/', 'enemies/bandiet_duin/'),
    'schildman_makkelijk': ('enemies/schildbandiet/',),
    'schildman': ('enemies/schildbandiet/',),
    'meelman': ('enemies/meelman/',),
    'kooiman': ('enemies/kooiman/', 'enemies/vogel/'),
}
# wat binnen die mappen toch niet meegaat: het skelet en het speerteken (levels), en de
# sneeuwversies van het uitzicht (de arena is nooit winter)
ARENA_NIET = ('design/botten/skelet/', 'design/botten/speerteken/')


def kaal_pad(rel: str) -> str:
    return rel[len('klein/'):] if rel.startswith('klein/') else rel


def in_arena(rel: str) -> bool:
    kaal = kaal_pad(rel)
    if kaal.startswith(ARENA_NIET):
        return False
    if kaal.startswith('design/bg/') and '_sneeuw' in os.path.basename(kaal):
        return False
    if kaal.startswith(ARENA_MAPPEN):
        return True
    # de metadata (json) en de geluiden (mp3) van de vijanden laadt het spel bij het opstarten, allemaal
    if kaal.startswith('enemies/') and kaal.lower().endswith(('.json', '.mp3')):
        return True
    # de losse bestanden direct in design/
    return kaal.startswith('design/') and '/' not in kaal[len('design/'):]


def in_soort(rel: str, soort: str) -> bool:
    return kaal_pad(rel).startswith(ARENA_SOORTEN[soort])


def collect():
    files = []
    for top in ASSET_DIRS:
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for name in sorted(filenames):
                abspath = os.path.join(dirpath, name)
                rel = os.path.relpath(abspath, ROOT).replace(os.sep, '/')
                if not rel.lower().endswith(KEEP_EXT):
                    continue
                if is_source_material(rel):
                    continue
                files.append((rel, os.path.getsize(abspath)))
    return files


def main():
    assets = collect()

    digest = hashlib.sha256()
    for rel, size in assets:
        digest.update(f'{rel}:{size}\n'.encode())

    # Van een deel van de sprites staat er een halve versie in klein/. Een toestel
    # speelt er maar één van, dus de service worker haalt ook maar één set binnen.
    # Hier alvast uitrekenen hoeveel bytes dat per set is, zodat het startmenu de
    # juiste download kan noemen.
    klein = {rel[len('klein/'):] for rel, _ in assets if rel.startswith('klein/')}

    def in_set(rel, set_naam):
        is_klein = rel.startswith('klein/')
        if set_naam == 'groot':
            return not is_klein
        return is_klein or rel not in klein

    arena = [(rel, size) for rel, size in assets if in_arena(rel)]
    soorten = {k: [rel for rel, _ in assets if in_soort(rel, k)] for k in ARENA_SOORTEN}

    payload = {
        'version': digest.hexdigest()[:12],
        'bytes': sum(size for _, size in assets),
        'bytesSet': {
            naam: sum(size for rel, size in assets if in_set(rel, naam))
            for naam in ('klein', 'groot')
        },
        # de delen: een naam en de bestanden die erbij horen (een deel van 'assets'); de arena is de
        # basis, de service worker legt er de soorten bij die het spel noemt
        'delen': {'arena': [rel for rel, _ in arena]},
        'soorten': soorten,
        'assets': [rel for rel, _ in assets],
        # de grootte per bestand, in dezelfde volgorde als 'assets', zodat de service worker voor elke
        # keuze (set, deel, soorten) kan uitrekenen hoeveel er te halen is
        'groottes': [size for _, size in assets],
    }

    out = os.path.join(ROOT, 'offline-assets.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=0, ensure_ascii=False)
        fh.write('\n')

    b = payload['bytesSet']
    print(f"{len(assets)} bestanden, {payload['bytes'] / 1048576:.1f} MB, versie {payload['version']}")
    print(f"  download per set: klein {b['klein'] / 1048576:.1f} MB, groot {b['groot'] / 1048576:.1f} MB")
    def mb(lijst, naam):
        return sum(size for rel, size in lijst if in_set(rel, naam)) / 1048576
    print(f"  alleen de arena, de basis: {len(arena)} bestanden, klein {mb(arena, 'klein'):.1f} MB, groot {mb(arena, 'groot'):.1f} MB")
    for k, paden in soorten.items():
        lijst = [(rel, size) for rel, size in assets if rel in set(paden)]
        print(f"    + {k}: {len(lijst)} bestanden, klein {mb(lijst, 'klein'):.1f} MB, groot {mb(lijst, 'groot'):.1f} MB")
    print(f'geschreven naar {out}')


if __name__ == '__main__':
    main()
