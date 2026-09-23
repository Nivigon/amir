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
ASSET_DIRS = ('design', 'enemies', 'karakters', 'klein', 'music', 'sounds')

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
    # docs-mappen zijn leesvoer bij de assets: readme's en previews, niets voor het spel
    if '/docs/' in rel:
        return True
    if '_magenta' in name or '_preview' in name:
        return True
    if 'sheet' in name and rel not in SHEETS_IN_USE:
        return True
    return False


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

    payload = {
        'version': digest.hexdigest()[:12],
        'bytes': sum(size for _, size in assets),
        'assets': [rel for rel, _ in assets],
    }

    out = os.path.join(ROOT, 'offline-assets.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=0, ensure_ascii=False)
        fh.write('\n')

    print(f"{len(assets)} bestanden, {payload['bytes'] / 1048576:.1f} MB, versie {payload['version']}")
    print(f'geschreven naar {out}')


if __name__ == '__main__':
    main()
