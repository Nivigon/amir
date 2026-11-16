#!/usr/bin/env python3
"""De stokken van Amir opnieuw bakken: de stok uit Grok op de lijf-frames uit de Animeer tool.

Bron (in karakters/amir/stokken/bron/):
  lijf/<set>_NN.png   het lijf zonder stokken, uit de Animeer tool Amir stokken (594x301, anker 297, grond 297;
                      de vechtsets kijken daar naar rechts)
  stok_grok.jpg       de stok op magenta, met de grip en de slippen in een egale kleur (geel uit Grok)
plaatsing.json        de export van de Animeer tool: per frame waar stok_voor en stok_achter liggen, de maskers
                      van het lijf (voor/weg) en van de stok (achter/weg)

Uit:
  <set>/<set>_NN.png  de speelframes (440x328, anker 256, grond 323), met de stok erin maar zonder slippen
  slip.png            de twee slippen, los: het spel hangt ze aan de knoop en laat ze naslepen (STOK.slip)
  en op het scherm de regel `slipPunt` voor STOK in de HTML: per frame de knoop van elke stok en of hij achter Amir valt

Gebruik:  python3 tools/stok_bak.py [--kleur 170,108,40] [--lengte 155] [--dikte 1.15] [--slip 0.75]
          python3 tools/stok_bak.py --alleen stapslag
          --alleen bakt alleen die sets, op het canvas dat nu in STOK staat (--canvas W,H,ANKER,GROUND); de rest blijft
          staan. Nodig sinds de ren met stokken niet meer uit plaatsing.json komt (samengesteld, zie notities/stokken.md)
Daarna:   python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'karakters', 'amir', 'stokken')
AW, AH = 594, 301                 # het canvas van de Animeer tool
SW, SH = 440, 328                 # het oude canvas van het spel; het nieuwe groeit mee met de stok (zie onderaan)
P = 80                            # marge om het Animeer-canvas tijdens het samenstellen: de stok steekt erbuiten
DX, DY = -41, 26                  # Animeer naar spel: anker 297 -> 256, grond 297 -> 323 (nagemeten op het lijf)
GESPIEGELD = ('slag', 'stapslag', 'slag2', 'draaislag', 'draaiterug', 'blok')   # die kijken in de Animeer tool naar rechts
DRAAITERUG = [13, 11, 9, 6, 3, 1]  # draaiterug is draaislag achterstevoren, op deze frames (nagemeten)
# de stok in stok_grok.jpg: de schacht en de slippen, in pixels van dat beeld
STOK_BOX = (107, 517, 1643, 650)  # links, boven, rechts, onder (de onderkant snijdt de slippen eraf, de knoop blijft)
SLIP_BOX = (1370, 650, 1590, 995)
KNOOP_X = 1475                    # waar de slippen aan de knoop hangen
GRIP_X = 1315                     # het midden van de grip, die in de vuist komt
OUD_W = 0.1936 * AW               # de oude stok (i/stok.png, 370x40) zoals de Animeer tool hem plaatste
OUD_H = OUD_W * 40 / 370
OUD_GRIP = (0.81 - 0.5) * OUD_W   # het midden van de oude grip, gerekend vanaf het midden van de stok


def sleutel(im):
    """Magenta eruit (de clean key op verhouding), met despill."""
    a = np.array(im.convert('RGB')).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    al = np.clip((0.75 - m) / 0.30, 0, 1)
    ex = np.clip(np.minimum(r, b) - g, 0, None) * (1 - al)
    return np.stack([r - ex, g, b - ex], -1), al, (r, g, b)


def stok_maken(kleur):
    rgb, al, (r, g, b) = sleutel(Image.open(os.path.join(DIR, 'bron', 'stok_grok.jpg')))
    geel = (r > 120) & (g > 90) & (b < 110) & (g > b + 60) & (al > 0.3)
    L = (r + g) / 510
    k = np.clip(L / np.percentile(L[geel], 90), 0, 1.25)
    rgb[geel] = np.clip(np.array(kleur, float) * k[geel, None], 0, 255)
    return Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8))


def draai(v, deg, flip):
    x, y = v
    if flip: x = -x
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (x * c - y * s, x * s + y * c)


def masker(strokes, soort, mp, eenheid):
    """Penseelstreken van de Animeer tool (strokePath: ronde kop, breedte s * eenheid)."""
    m = Image.new('L', (AW + 2 * P, AH + 2 * P), 0)
    d = ImageDraw.Draw(m)
    for st in strokes or []:
        if st['t'] != soort and st['t'] != 'gum': continue
        f = 0 if st['t'] == 'gum' else 255
        lw = st['s'] * eenheid
        pts = [mp(p) for p in st['p']]
        if len(pts) > 1: d.line(pts, fill=f, width=max(1, round(lw)))
        for x, y in pts: d.ellipse((x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2), fill=f)
    return np.array(m).astype(int)


def alfa_keer(im, m):
    a = np.array(im.getchannel('A')).astype(int)
    im = im.copy(); im.putalpha(Image.fromarray((a * m // 255).astype(np.uint8))); return im


def olijf_weg(im):
    """Resten uit de Grok-clips: olijfgroen van de groene stokken op de handen terug naar huidskleur,
    en de paarsroze vlekjes (de vlek uit de clip) weg."""
    a = np.array(im).astype(float)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    roze = (r > 140) & (b > 110) & (g < np.minimum(r, b) - 30)
    a[roze, 3] = 0
    m = (g >= r * 0.8) & (b < g * 0.6) & (al > 0)
    lum = (r + g + b)[m] / 3
    huid = np.array([1.45, 0.9, 0.65])             # verhouding van zijn bruine huid
    a[m, :3] = np.clip(lum[:, None] * huid, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kleur', default='170,108,40', help='de grip en de slippen (gebrand oker)')
    ap.add_argument('--lengte', type=float, default=155, help='lengte van de stok in Animeer-pixels')
    ap.add_argument('--dikte', type=float, default=1.15, help='de stok zoveel dikker dan in verhouding')
    ap.add_argument('--slip', type=float, default=0.75, help='de slippen zoveel kleiner')
    ap.add_argument('--alleen', default='', help='alleen deze sets bakken, met komma\'s (de rest blijft staan)')
    ap.add_argument('--canvas', default='511,384,298,379', help='met --alleen: W,H,ANKER,GROUND van STOK')
    o = ap.parse_args()
    alleen = [z for z in o.alleen.split(',') if z]
    kleur = [int(v) for v in o.kleur.split(',')]
    PL = json.load(open(os.path.join(DIR, 'plaatsing.json')))

    vol = stok_maken(kleur)
    va = np.array(vol)
    sa = va.copy(); sa[STOK_BOX[3]:, :, 3] = 0
    stok = Image.fromarray(sa).crop(STOK_BOX)
    pa = va.copy(); pa[:SLIP_BOX[1], :, 3] = 0
    slip = Image.fromarray(pa).crop(SLIP_BOX)
    s = o.lengte / stok.width
    stok = stok.resize((round(stok.width * s), round(stok.height * s * o.dikte)), Image.LANCZOS)
    ss = s * o.slip
    slip = slip.resize((round(slip.width * ss), round(slip.height * ss)), Image.LANCZOS)
    slip.save(os.path.join(DIR, 'slip.png'))
    ncx, ncy = (STOK_BOX[0] + STOK_BOX[2]) / 2, (STOK_BOX[1] + STOK_BOX[3]) / 2
    grip = (GRIP_X - ncx) * s
    knoop = ((KNOOP_X - ncx) * s, (STOK_BOX[3] - ncy) * s * o.dikte)

    def item(L, ims, sid):
        flip, deg = L.get('flip', False), L['rot']
        oc = (L['cx'] * AW + P, L['cy'] * AH + P)
        g = draai((OUD_GRIP, 0), deg, flip); gp = (oc[0] + g[0], oc[1] + g[1])   # de grip blijft in de vuist
        v = draai((grip, 0), deg, flip); nc = (gp[0] - v[0], gp[1] - v[1])
        im = stok.transpose(Image.FLIP_LEFT_RIGHT) if flip else stok
        r = im.rotate(-deg, expand=True, resample=Image.BICUBIC)
        full = Image.new('RGBA', (AW + 2 * P, AH + 2 * P))
        full.alpha_composite(r, (round(nc[0] - r.width / 2), round(nc[1] - r.height / 2)))
        kv = draai(knoop, deg, flip)
        sts = (ims or {}).get(sid + '|basis') or []
        def mp(p):
            q = draai((-OUD_W / 2 + p[0] * OUD_W, -OUD_H / 2 + p[1] * OUD_H), deg, flip)
            return (oc[0] + q[0], oc[1] + q[1])
        full = alfa_keer(full, 255 - masker(sts, 'weg', mp, OUD_W))
        ma = masker(sts, 'achter', mp, OUD_W)
        return full, alfa_keer(full, ma), alfa_keer(full, 255 - ma), (nc[0] + kv[0], nc[1] + kv[1])

    punten, beelden = {}, []
    for zet, frames in PL['frames'].items():
        if alleen and zet not in alleen: continue
        punten[zet] = []
        os.makedirs(os.path.join(DIR, zet), exist_ok=True)
        for i, fr in enumerate(frames):
            bron = f'draaislag_{DRAAITERUG[i]:02d}' if zet == 'draaiterug' else f'{zet}_{i:02d}'
            # (de stapslag heeft root motion: STOK.root in de HTML, uit plaatsing.json 'root' per frame)
            lijf = olijf_weg(Image.open(os.path.join(DIR, 'bron', 'lijf', bron + '.png')).convert('RGBA'))
            delen = []
            for sid in ('stok_achter', 'stok_voor'):
                L = fr['L'].get(sid)
                if L and L.get('on', True): delen.append((L,) + item(L, fr.get('im'), sid))
            bs = (fr.get('body') or {}).get('basis') or []
            bmp = lambda p: (p[0] * AW + P, p[1] * AH + P)
            pl = Image.new('RGBA', (AW + 2 * P, AH + 2 * P)); pl.alpha_composite(lijf, (P, P)); lijf = pl
            lijf = alfa_keer(lijf, 255 - masker(bs, 'weg', bmp, AW))
            mv = masker(bs, 'voor', bmp, AW)
            uit = Image.new('RGBA', (AW + 2 * P, AH + 2 * P))
            for L, full, back, front, kp in delen: uit.alpha_composite(full if L.get('behind') else back)
            uit.alpha_composite(lijf)
            for L, full, back, front, kp in delen:
                if not L.get('behind'): uit.alpha_composite(front)
            uit.alpha_composite(alfa_keer(lijf, mv))
            spieg = zet in GESPIEGELD
            if spieg: uit = uit.transpose(Image.FLIP_LEFT_RIGHT)
            rij = []
            for L, full, back, front, kp in delen:
                x = (AW + 2 * P - 1 - kp[0]) if spieg else kp[0]
                rij += [x + DX - P, kp[1] + DY - P, 1 if L.get('behind') else 0]
            beelden.append((zet, i, uit, rij))
    # het speelcanvas: het oude, plus wat de stok of een slip erbuiten nodig heeft (links, boven, rechts)
    x0, y0, x1 = 0, 0, SW
    for zet, i, uit, rij in beelden:
        bb = uit.getbbox()
        if bb:
            x0 = min(x0, bb[0] + DX - P); y0 = min(y0, bb[1] + DY - P); x1 = max(x1, bb[2] + DX - P)
        for j in range(0, len(rij), 3):
            x0 = min(x0, rij[j] - slip.width); x1 = max(x1, rij[j] + slip.width)
    LX, TY = -math.floor(x0) + 2 if x0 < 0 else 0, -math.floor(y0) + 2 if y0 < 0 else 0
    NW, NH = math.ceil(x1) + LX + (2 if x1 > SW else 0), SH + TY
    if alleen:                                    # het canvas blijft wat het is
        cw, ch, ca, cg = [int(v) for v in o.canvas.split(',')]
        if (NW, NH) != (cw, ch) and (NW > cw or NH > ch or LX > ca - 256 or TY > cg - 323):
            print(f'LET OP: deze sets hebben {NW}x{NH} (links {LX}, boven {TY}) nodig, het canvas is {cw}x{ch}: er valt iets buiten')
        NW, NH, LX, TY = cw, ch, ca - 256, cg - 323
    for zet, i, uit, rij in beelden:
        spel = Image.new('RGBA', (NW, NH))
        sx, sy = P - DX - LX, P - DY - TY            # kan negatief worden als het canvas groter is dan de marge
        spel.alpha_composite(uit, dest=(max(0, -sx), max(0, -sy)), source=(max(0, sx), max(0, sy)))
        spel.save(os.path.join(DIR, zet, f'{zet}_{i:02d}.png'))
        punten[zet].append([round(v + (LX if j % 3 == 0 else TY if j % 3 == 1 else 0), 1) if j % 3 < 2 else v
                            for j, v in enumerate(rij)])
    print(f"  W: {NW}, H: {NH}, ANKER: {256 + LX}, GROUND: {323 + TY},")
    sw, sh = slip.size
    print(f"  slip: {{ w: {sw}, h: {sh}, piv: {round((KNOOP_X - SLIP_BOX[0]) * ss, 1)},")
    print("    // per frame per stok: x en y van de knoop in de speelframes, en 1 als de stok achter Amir valt (tools/stok_bak.py)")
    print("    punt: {")
    for zet, rijen in punten.items():
        print(f"      {zet}: {json.dumps(rijen, separators=(',', ':'))},")
    print("    } },")


if __name__ == '__main__':
    main()
