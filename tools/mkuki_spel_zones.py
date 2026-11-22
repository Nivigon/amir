#!/usr/bin/env python3
"""Zonekaarten bij de Mkuki-skin van Amir (de outfits, MK_OUTFIT in het spel).

Per gebakken frame van tools/mkuki_spel_bak.py een kaart <pad>_zones.png met per pixel het kledingstuk:
  1 broek #0000FF, 2 schort #FFFF00, 3 riem #FF0000, 4 schuine band #00FF00, 5 kralen #00FFFF, 6 armbanden #FF8000
De rest (huid, speer, achtergrond) is doorzichtig. Het spel kleurt daarmee een outfit om: per zone een doelkleur maal de
helderheid van het frame (licht en schaduw blijven).

Gebakken op precies dezelfde manier als het frame zelf: dezelfde speer, maskers en vuist, maar met het lijf in de
zonekleuren. Wat de speer of een masker afdekt valt zo vanzelf weg.

  python3 tools/mkuki_spel_zones.py <mkuki-checkout> [export.json] [--check]

--check vergelijkt eerst het opnieuw gebakken frame met dat in de repo (dan weet je dat de lijven kloppen).
Schrijft karakters/amir/mkuki_spel/<pad>_zones.png en de helft in klein/.
"""
import json, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkuki_spel_bak as B

KAART = {1: (0, 0, 255), 2: (255, 255, 0), 3: (255, 0, 0), 4: (0, 255, 0), 5: (0, 255, 255), 6: (255, 128, 0)}


def zone_lijf(lijf, zp):
    """Het lijf in zonekleuren: zone waar de kaart een kleur heeft, zwart waar het lijf geen zone is."""
    a = np.array(lijf.getchannel('A'))
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., 3] = a
    if os.path.exists(zp):
        z = np.array(Image.open(zp).convert('RGBA'))
        m = z[..., 3] > 0
        out[..., :3][m] = z[..., :3][m]
    return Image.fromarray(out)


def lees(uit):
    """Terug naar een zonekaart: alleen pixels die precies een zonekleur hebben (randen met de speer vallen weg)."""
    p = np.array(uit)
    z = np.zeros(p.shape[:2] + (4,), np.uint8)
    for k, c in KAART.items():
        m = np.all(p[..., :3] == c, axis=-1) & (p[..., 3] > 0)
        z[m, :3] = c
        z[m, 3] = 255
    return Image.fromarray(z)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__); sys.exit(1)
    check = '--check' in sys.argv
    mk = os.path.join(args[0], 'karakters/amir/mkuki')
    D = json.load(open(os.path.join(B.BRON, 'tool.json')))
    frames, am = D['init'], D.get('angleMasks') or {}
    if len(args) > 1:
        ex = json.load(open(args[1]))
        for a, lst in ex.get('frames', {}).items():
            for i, f in enumerate(lst):
                if f and a in frames and i < len(frames[a]):
                    f.setdefault('L', {})
                    for iid, L in frames[a][i]['L'].items():
                        f['L'].setdefault(iid, L)
                    frames[a][i] = f
        am = ex.get('hoekmaskers') or am
    items = {it['id']: it for it in D['items']}
    gedaan, slecht = set(), []
    for a in D['anims']:
        for f in a['frames']:
            pad = D['bron'][a['id'] + '-' + str(f['i'])]
            if pad in gedaan:
                continue
            gedaan.add(pad)
            lijf = Image.open(os.path.join(mk, pad)).convert('RGBA')
            W, H = lijf.size
            vp = os.path.join(mk, pad[:-4] + '_vuist.png')
            heeft_v = f.get('v') and os.path.exists(vp)
            fr = frames[a['id']][f['i']]
            if check:
                echt = B.bak(lijf, Image.open(vp).convert('RGBA') if heeft_v else None, fr, items, am, W, H)
                repo = Image.open(os.path.join(B.UIT, pad)).convert('RGBA')
                d = np.abs(np.array(echt, int) - np.array(repo, int)).max()
                if d > 2:
                    slecht.append((pad, int(d)))
            zl = zone_lijf(lijf, os.path.join(mk, pad[:-4] + '_zones.png'))
            zv = zone_lijf(Image.open(vp).convert('RGBA'), vp[:-4] + '_zones.png') if heeft_v else None
            z = lees(B.bak(zl, zv, fr, items, am, W, H))
            for basis, k in ((B.UIT, 1), (os.path.join(B.REPO, 'klein/karakters/amir/mkuki_spel'), 2)):
                doel = os.path.join(basis, pad[:-4] + '_zones.png')
                os.makedirs(os.path.dirname(doel), exist_ok=True)
                zz = z if k == 1 else z.resize((max(1, W // k), max(1, H // k)), Image.NEAREST)
                zz.save(doel, optimize=True)
        print(a['id'], len(a['frames']))
    print(len(gedaan), 'zonekaarten')
    if check:
        print('afwijkend van de repo:', len(slecht), slecht[:20])


if __name__ == '__main__':
    main()
