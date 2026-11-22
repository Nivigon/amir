#!/usr/bin/env python3
"""Bakt de Mkuki-skin van Amir nog een keer, nu met de Pathfinder Spear in zijn handen (MKUKI_PF in het spel).

Precies zoals tools/mkuki_spel_bak.py: per frame het Mkuki-lijf zonder speer (branch claude/mkuki), de speer op de plek,
hoek en lengte uit de Mkuki animeer tool (karakters/amir/mkuki_spel/bron/tool.json) en de vuist erbovenop. Alleen de
speerplaatjes komen uit design/speer/pathfinder/hand/ (tools/pathfinder_speer.py maakt ze, op dezelfde maten als de
gewone). Ook de zonekaarten voor de outfits worden zo opnieuw gebakken, want de Pathfinder dekt net andere pixels af.

  python3 tools/mkuki_pathfinder_bak.py <mkuki-checkout> [export.json]

Schrijft karakters/amir/mkuki_pf/<pad> en <pad>_zones.png, en de helft in klein/karakters/amir/mkuki_pf/.
Daarna tools/gen-offline-manifest.py.
"""
import json, os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkuki_spel_bak as B
import mkuki_spel_zones as Z

UIT = os.path.join(B.REPO, 'karakters/amir/mkuki_pf')
KLEIN = os.path.join(B.REPO, 'klein/karakters/amir/mkuki_pf')
HAND = os.path.join(B.REPO, 'design/speer/pathfinder/hand')


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    mk = os.path.join(sys.argv[1], 'karakters/amir/mkuki')
    D = json.load(open(os.path.join(B.BRON, 'tool.json')))
    frames, am = D['init'], D.get('angleMasks') or {}
    if len(sys.argv) > 2:                                     # zelfde samenvoeging als mkuki_spel_bak.py
        ex = json.load(open(sys.argv[2]))
        for a, lst in ex.get('frames', {}).items():
            for i, f in enumerate(lst):
                if f and a in frames and i < len(frames[a]):
                    f.setdefault('L', {})
                    for iid, L in frames[a][i]['L'].items():
                        f['L'].setdefault(iid, L)
                    frames[a][i] = f
        am = ex.get('hoekmaskers') or am
    items = {it['id']: it for it in D['items']}
    B.BRON = HAND                                             # vanaf hier: de speerplaatjes van de Pathfinder
    gedaan = []
    for a in D['anims']:
        for f in a['frames']:
            pad = D['bron'][a['id'] + '-' + str(f['i'])]
            if pad in gedaan:
                continue
            gedaan.append(pad)
            lijf = Image.open(os.path.join(mk, pad)).convert('RGBA')
            W, H = lijf.size
            vp = os.path.join(mk, pad[:-4] + '_vuist.png')
            heeft_v = f.get('v') and os.path.exists(vp)
            fr = frames[a['id']][f['i']]
            im = B.bak(lijf, Image.open(vp).convert('RGBA') if heeft_v else None, fr, items, am, W, H)
            zl = Z.zone_lijf(lijf, os.path.join(mk, pad[:-4] + '_zones.png'))
            zv = Z.zone_lijf(Image.open(vp).convert('RGBA'), vp[:-4] + '_zones.png') if heeft_v else None
            z = Z.lees(B.bak(zl, zv, fr, items, am, W, H))
            for basis, k in ((UIT, 1), (KLEIN, 2)):
                doel = os.path.join(basis, pad)
                os.makedirs(os.path.dirname(doel), exist_ok=True)
                klein = (max(1, W // k), max(1, H // k))
                (im if k == 1 else im.resize(klein, Image.LANCZOS)).save(doel, optimize=True)
                (z if k == 1 else z.resize(klein, Image.NEAREST)).save(doel[:-4] + '_zones.png', optimize=True)
        print(a['id'], len(a['frames']))
    json.dump(sorted(gedaan), open(os.path.join(UIT, 'lijst.json'), 'w'), indent=0)
    print(len(gedaan), 'frames gebakken')


if __name__ == '__main__':
    main()
