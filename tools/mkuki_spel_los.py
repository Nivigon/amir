#!/usr/bin/env python3
"""De Mkuki-skin met een losse speer (MK_LOS in het spel).

Per frame van de skin (zelfde paden als tools/mkuki_spel_bak.py) los wat het spel zelf op elkaar tekent:
  <pad>_lijf.png    het lijf zonder speer (met het weg-masker van het lijf)
  <pad>_boven.png   wat over de speer heen komt: het stuk lijf onder het voor-masker en de vuistlaag (alleen als er iets is)
  <pad>_sm.png      de maskers van de speer in framepixels: rood = weg, groen = achter het lijf (alleen als er streken zijn)
  en van lijf en boven de zonekaart (_lijf_zones.png, _boven_zones.png) voor de outfits.
Plus karakters/amir/mkuki_spel/los.json met per frame de speer (hoek, midden, breedte, draaiing, spiegelen, achter, dekking),
en in bron/ de Pathfinder Spear in dezelfde hoeken als de gewone (pf_<hoek>.png, de schacht rekt mee zoals in de tool).

Het spel tekent dan: speer achter (of het achter-stuk), lijf, speer voor, boven. Zo kan elke speersoort in zijn handen.

  python3 tools/mkuki_spel_los.py <mkuki-checkout> [export.json]
"""
import json, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkuki_spel_bak as B
import mkuki_spel_zones as Z

KLEIN = os.path.join(B.REPO, 'klein/karakters/amir/mkuki_spel')
KS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
LS = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]


def bewaar(im, pad, achtervoegsel, nearest=False):
    W, H = im.size
    for basis, k in ((B.UIT, 1), (KLEIN, 2)):
        doel = os.path.join(basis, pad[:-4] + achtervoegsel)
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        (im if k == 1 else im.resize((max(1, W // k), max(1, H // k)), Image.NEAREST if nearest else Image.LANCZOS)).save(doel, optimize=True)


def leeg(im):
    return im.getchannel('A').getbbox() is None


def lagen(lijf, vuist, fr, items, am, W, H):
    """lijf (weg-masker eraf), boven (voor-masker van het lijf plus vuist), sm (maskers van de speer) en de speerdata."""
    bs = (fr.get('body') or {}).get('basis') or []
    bk = lambda p: (p[0] * W, p[1] * H)
    l = lijf.copy()
    B.min_alpha(l, B.masker((W, H), bs, 'weg', bk, W))
    boven = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mv = B.masker((W, H), bs, 'voor', bk, W)
    if mv.getbbox():
        v = l.copy(); v.putalpha(Image.composite(v.getchannel('A'), Image.new('L', (W, H), 0), mv)); boven.alpha_composite(v)
    if vuist is not None:
        boven.alpha_composite(vuist)
    speer, sm = None, None
    for iid, L in (fr.get('L') or {}).items():
        if not L or not L.get('on'):
            continue
        assert iid == 'amirspeer', iid
        e = items[iid]['img']['basis'].get(L['angle'])
        w = L['w'] * W; h = w * e['aspect']; px = L['cx'] * W; py = L['cy'] * H
        import math
        rot = math.radians(L['rot'])
        def kaart(p, w=w, h=h, px=px, py=py, rot=rot, fl=L.get('flip')):
            lx = -w / 2 + p[0] * w; ly = -h / 2 + p[1] * h
            if fl: lx = -lx
            return (px + lx * math.cos(rot) - ly * math.sin(rot), py + lx * math.sin(rot) + ly * math.cos(rot))
        mkey = iid + '|basis'
        strokes = (fr.get('im') or {}).get(mkey) or am.get(mkey + '|' + L['angle']) or []
        mw, ma = B.masker((W, H), strokes, 'weg', kaart, w), B.masker((W, H), strokes, 'achter', kaart, w)
        if mw.getbbox() or ma.getbbox():
            sm = Image.merge('RGBA', (mw, ma, Image.new('L', (W, H), 0), Image.new('L', (W, H), 255)))
        speer = {'a': L['angle'], 'cx': round(L['cx'], 5), 'cy': round(L['cy'], 5), 'w': round(L['w'], 5),
                 'r': round(L['rot'], 2), 'f': 1 if L.get('flip') else 0, 'b': 1 if L.get('behind') else 0,
                 'op': L.get('op', 1)}
    return l, boven, sm, speer


def pathfinder():
    """De Pathfinder in de hoeken van de gewone speer, zoals de tool (tools/mkuki/animeer/bouw.py op claude/mkuki)."""
    PF = Image.open(os.path.join(B.REPO, 'design/speer/pathfinder/jav.png')).convert('RGBA'); KN = (509.9, 41.3)
    def lang(f):
        extra = round(PF.width * (f - 1)); e1 = round(extra * 195 / 350); e2 = extra - e1
        n = Image.new('RGBA', (PF.width + extra, PF.height))
        n.paste(PF.crop((0, 0, 30, PF.height)), (0, 0))
        n.paste(PF.crop((30, 0, 225, PF.height)).resize((195 + e1, PF.height), Image.LANCZOS), (30, 0))
        n.paste(PF.crop((225, 0, 345, PF.height)), (225 + e1, 0))
        n.paste(PF.crop((345, 0, 500, PF.height)).resize((155 + e2, PF.height), Image.LANCZOS), (345 + e1, 0))
        n.paste(PF.crop((500, 0, PF.width, PF.height)), (500 + extra, 0))
        return n, KN[0] + extra
    uit = {}
    for hid, f in [('proj', 1.0)] + [('k%02d' % round(k * 100), k) for k in KS] + [('l%03d' % round(f * 100), f) for f in LS]:
        if f > 1: im, kx = lang(f)
        elif f < 1: im = PF.resize((round(PF.width * f), PF.height), Image.LANCZOS); kx = KN[0] * f
        else: im, kx = PF, KN[0]
        im.save(os.path.join(B.BRON, 'pf_%s.png' % hid), optimize=True)
        uit[hid] = {'kx': round(kx / im.width, 4), 'ky': round(KN[1] / PF.height, 4), 'asp': round(PF.height / im.width, 4)}
    return uit


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__); sys.exit(1)
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
    hoeken = {h: {'asp': e['aspect']} for h, e in items['amirspeer']['img']['basis'].items()}
    uit = {'hoeken': hoeken, 'pf': pathfinder(), 'frames': {}}
    for a in D['anims']:
        for f in a['frames']:
            pad = D['bron'][a['id'] + '-' + str(f['i'])]
            if pad in uit['frames']:
                continue
            lijf = Image.open(os.path.join(mk, pad)).convert('RGBA')
            W, H = lijf.size
            vp = os.path.join(mk, pad[:-4] + '_vuist.png')
            vuist = Image.open(vp).convert('RGBA') if f.get('v') and os.path.exists(vp) else None
            fr = frames[a['id']][f['i']]
            l, boven, sm, speer = lagen(lijf, vuist, fr, items, am, W, H)
            bewaar(l, pad, '_lijf.png')
            zl = Z.zone_lijf(lijf, os.path.join(mk, pad[:-4] + '_zones.png'))
            zv = Z.zone_lijf(vuist, vp[:-4] + '_zones.png') if vuist is not None else None
            zlijf, zboven, _, _ = lagen(zl, zv, fr, items, am, W, H)
            bewaar(Z.lees(zlijf), pad, '_lijf_zones.png', True)
            d = {'s': speer}
            if not leeg(boven):
                bewaar(boven, pad, '_boven.png'); bewaar(Z.lees(zboven), pad, '_boven_zones.png', True); d['b'] = 1
            if sm is not None:
                bewaar(sm, pad, '_sm.png', True); d['m'] = 1
            uit['frames'][pad] = d
        print(a['id'], len(a['frames']))
    json.dump(uit, open(os.path.join(B.UIT, 'los.json'), 'w'), separators=(',', ':'))
    print(len(uit['frames']), 'frames los')


if __name__ == '__main__':
    main()
