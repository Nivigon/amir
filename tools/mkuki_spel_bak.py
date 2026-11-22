#!/usr/bin/env python3
"""Bakt de Mkuki-skin van Amir voor het spel (Test 88, `skin: 'mkuki'`).

Per frame: het Mkuki-lijf zonder speer (branch claude/mkuki, karakters/amir/mkuki/), de speer zoals de Mkuki
animeer tool hem plaatst (plek, hoek, lengte, spiegelen, voor of achter, de maskers) en de vuistlaag erbovenop.
Zelfde volgorde als compose() in de tool. Het resultaat heeft dezelfde naam en canvasmaat als het origineel,
zodat het spel er niets voor hoeft om te rekenen.

  python3 tools/mkuki_spel_bak.py <mkuki-checkout> [export.json]

<mkuki-checkout>  een checkout van de branch claude/mkuki (daar staan de lijven en vuisten)
export.json       optioneel: "Kopieer alle instellingen" uit de tool; zonder dit de beginstand
                  (karakters/amir/mkuki_spel/bron/tool.json)

Schrijft karakters/amir/mkuki_spel/<pad> en klein/karakters/amir/mkuki_spel/<pad> (de helft), en
karakters/amir/mkuki_spel/lijst.json (de paden, voor MKUKI_SKIN in het spel).
"""
import json, math, os, sys
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
UIT = os.path.join(REPO, 'karakters/amir/mkuki_spel')
BRON = os.path.join(UIT, 'bron')


def punten_lijn(draw, pts, breedte, kleur):
    r = breedte / 2
    if len(pts) == 1:
        x, y = pts[0]; draw.ellipse([x - r, y - r, x + r, y + r], fill=kleur); return
    draw.line(pts, fill=kleur, width=max(1, round(breedte)))
    for x, y in pts:                                   # ronde koppen en hoeken, zoals lineCap/lineJoin round
        draw.ellipse([x - r, y - r, x + r, y + r], fill=kleur)


def masker(maat, strokes, soort, kaart, eenheid):
    """Een masker van een soort (weg, voor, achter); gum haalt elke soort weer weg, in volgorde."""
    m = Image.new('L', maat, 0)
    d = ImageDraw.Draw(m)
    for st in strokes or []:
        if st['t'] != soort and st['t'] != 'gum':
            continue
        punten_lijn(d, [kaart(p) for p in st['p']], st['s'] * eenheid, 0 if st['t'] == 'gum' else 255)
    return m


def min_alpha(im, m):
    """destination-out: haal het masker uit de alfa."""
    a = im.getchannel('A')
    a = Image.composite(Image.new('L', im.size, 0), a, m)
    im.putalpha(a)


def bak(lijf, vuist, fr, items, hoekmaskers, W, H):
    uit = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    delen = []
    for iid, L in (fr.get('L') or {}).items():
        if not L or not L.get('on'):
            continue
        e = items[iid]['img']['basis'].get(L['angle']) or next(iter(items[iid]['img']['basis'].values()))
        sim = Image.open(os.path.join(BRON, os.path.basename(e['src']))).convert('RGBA')
        w = L['w'] * W; h = w * e['aspect']
        px = L['cx'] * W; py = L['cy'] * H
        rot = math.radians(L['rot'])
        s = sim.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
        if L.get('flip'):
            s = s.transpose(Image.FLIP_LEFT_RIGHT)
        op = L.get('op', 1)
        if op < 1:
            s.putalpha(s.getchannel('A').point(lambda v: int(v * op)))
        r = s.rotate(-L['rot'], resample=Image.BICUBIC, expand=True)
        vol = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vol.paste(r, (round(px - r.width / 2), round(py - r.height / 2)))   # leeg canvas: gewoon erin, alfa en al
        def kaart(p, w=w, h=h, px=px, py=py, rot=rot, fl=L.get('flip')):
            lx = -w / 2 + p[0] * w; ly = -h / 2 + p[1] * h
            if fl: lx = -lx
            return (px + lx * math.cos(rot) - ly * math.sin(rot), py + lx * math.sin(rot) + ly * math.cos(rot))
        mkey = iid + '|basis'
        strokes = (fr.get('im') or {}).get(mkey) or hoekmaskers.get(mkey + '|' + L['angle']) or []
        min_alpha(vol, masker((W, H), strokes, 'weg', kaart, w))
        ma = masker((W, H), strokes, 'achter', kaart, w)
        achter = vol.copy(); achter.putalpha(Image.composite(achter.getchannel('A'), Image.new('L', (W, H), 0), ma))
        voor = vol.copy(); min_alpha(voor, ma)
        delen.append((L, vol, achter, voor))
    for L, vol, achter, voor in delen:
        uit.alpha_composite(vol if L.get('behind') else achter)
    bs = (fr.get('body') or {}).get('basis') or []
    bk = lambda p: (p[0] * W, p[1] * H)
    lijf = lijf.copy()
    min_alpha(lijf, masker((W, H), bs, 'weg', bk, W))
    uit.alpha_composite(lijf)
    for L, vol, achter, voor in delen:
        if not L.get('behind'):
            uit.alpha_composite(voor)
    mv = masker((W, H), bs, 'voor', bk, W)
    if mv.getbbox():
        v = lijf.copy(); v.putalpha(Image.composite(v.getchannel('A'), Image.new('L', (W, H), 0), mv)); uit.alpha_composite(v)
    if vuist is not None:
        uit.alpha_composite(vuist)
    return uit


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    mk = os.path.join(sys.argv[1], 'karakters/amir/mkuki')
    D = json.load(open(os.path.join(BRON, 'tool.json')))
    frames, am = D['init'], D.get('angleMasks') or {}
    if len(sys.argv) > 2:
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
    lijst = []
    for a in D['anims']:
        for f in a['frames']:
            pad = D['bron'][a['id'] + '-' + str(f['i'])]
            if pad in lijst:
                continue
            lijf = Image.open(os.path.join(mk, pad)).convert('RGBA')
            W, H = lijf.size
            assert (W, H) == (a['canvasW'], a['canvasH']), (pad, lijf.size)
            vp = os.path.join(mk, pad[:-4] + '_vuist.png')
            vuist = Image.open(vp).convert('RGBA') if f.get('v') and os.path.exists(vp) else None
            im = bak(lijf, vuist, frames[a['id']][f['i']], items, am, W, H)
            for basis, k in ((UIT, 1), (os.path.join(REPO, 'klein/karakters/amir/mkuki_spel'), 2)):
                doel = os.path.join(basis, pad)
                os.makedirs(os.path.dirname(doel), exist_ok=True)
                (im if k == 1 else im.resize((max(1, W // k), max(1, H // k)), Image.LANCZOS)).save(doel, optimize=True)
            lijst.append(pad)
        print(a['id'], len(a['frames']))
    json.dump(sorted(lijst), open(os.path.join(UIT, 'lijst.json'), 'w'), indent=0)
    print(len(lijst), 'frames gebakken')


if __name__ == '__main__':
    main()
