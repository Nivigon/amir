#!/usr/bin/env python3
"""Maakt het vaantje in de steek kleiner.

In attack_sp_4 tot en met attack_sp_7 (karakters/amir/aanval/speerstrike/) wappert het
lint aan de speer ver uit: in de tussenframes (4 tot en met 6) als een veeg van 100 tot
150 pixels breed, in frame 7 (de speer helemaal uitgestoken) 86 bij 80. Het gewone
vaantje is zo'n 40 bij 33. Met de blauwe speer uit het skelet viel dat op als een groot
blauw doek dat opeens verschijnt.

Per frame:

1. het lint zoeken, op dezelfde manier als vaanMaak in de HTML (zie VAAN daar): fel en
   verzadigd rood, alleen stukken die samenhangen, en dan uitgroeien over roodachtige
   buren. Daarbij komt de donkere omlijning, de zachte rand en de gele glans;
2. het hele vak waar het lint stond leegmaken, behalve een strook aan de kant van de hand
   (MARGE): zo gaan ook de vaartstreepjes weg, maar blijft de hand heel;
3. de schacht door het gat heen trekken, van de punt tot waar de schacht weer zichtbaar is;
4. het lint verkleind terugzetten (SCHAAL), rond het punt waar het aan de speer vastzit:
   de linkerkant, bij de punt;
5. losse stipjes die in het oude lintvak zijn blijven staan weghalen.

Het lint wordt daarbij vooral platter gemaakt, strak naar achteren in de wind, zodat het
niet meer als een groot doek uitwappert: zo'n 55 bij 15 in frame 4 tot en met 6, 48 bij 24 in
frame 7 (daar blijft de haak). Frame 7 is ook de speer in de bek van de baviaan (BAV_SPEER).

Het rode lint blijft rood; het spel kleurt het blauw bij het tekenen (vaanBlauw vindt het
platte lint nog helemaal, nagekeken).

Frame 8 (de speer helemaal uitgestoken) is geen brede veeg maar een naar beneden hangend
dubbel lint. Dat werd eerst overgeslagen en bleef groter dan het platte lint van frame 7,
wat midden in de steek opviel (vooral op een telefoon, waar het spel trager loopt en dat
frame langer in beeld staat). plat_frame8 drukt dat hangende lint verticaal plat.

Het script is idempotent: frames die al verkleind zijn slaat het over (de veeg-frames op
hun lintbreedte, frame 8 op zijn linthoogte), dus herhaald draaien kan geen kwaad. De
veeg-frames 4 tot en met 7 zijn een eerdere eenmalige aanpassing; draai die op de
oorspronkelijke frames uit de geschiedenis van git. Daarna de kleine set bijwerken (die
frames zijn lager dan 400 en worden alleen gekopieerd):

    python3 tools/steekvaan.py
    python3 tools/gen-klein.py

Vereist Pillow en numpy: pip install pillow numpy
"""

import os
import sys
from collections import deque

try:
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit('Pillow of numpy ontbreekt: pip install pillow numpy')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = 'karakters/amir/aanval/speerstrike'

# per frame: (breedte, hoogte) van het lint, en hoeveel pixels aan de kant van de hand
# niet leeggemaakt worden (in frame 4 en 5 ligt de hand tegen het lint aan)
SCHAAL = {
    4: ((0.51, 0.29), 25),
    5: ((0.36, 0.25), 25),
    6: ((0.32, 0.24), 25),
    7: ((0.50, 0.30), -4),
}
TE_KLEIN = 70              # een lint dat al smaller is dan dit is al verkleind

# Frame 8 (de speer helemaal uitgestoken) is geen brede veeg maar een naar beneden hangend
# dubbel lint; de veeg-logica hierboven past er niet op. Het werd daardoor bij de eerste fix
# overgeslagen en bleef groter dan het platte lint van frame 7, wat midden in de steek opviel
# (op een telefoon loopt het spel trager, dus dat frame staat er langer). plat_frame8 drukt dat
# hangende lint verticaal plat zodat het even klein is als frame 7.
FRAME8 = 8
FRAME8_SY = 0.5            # het hangdeel half zo lang
FRAME8_HOOG = 28          # staat het lint hoger dan dit, dan is het nog niet platgedrukt (guard)

# dezelfde drempels als VAAN in de HTML
ZEKER = dict(v=115, s=0.55, t=(-20, 25), oranje=8, oranjeS=0.72)
ROOD = dict(v=50, s=0.3, t=(-45, 32))
MIN_STUK, BIJ, STAP = 25, 12, 8

SCHACHT = (110, 74, 48)    # bruin, zoals de schacht in frame 7 en 8
SCHACHT_RAND = (42, 26, 16)
STIPJE = 40                # losse stukjes kleiner dan dit in het oude lintvak gaan weg


def tint(a):
    r, g, b = (a[..., i].astype(float) for i in range(3))
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    d = np.where(mx > mn, mx - mn, 1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    t = (g - b) / d * 60
    rood_max = (mx == r) & (mx > mn) & (a[..., 3] > 0)
    return r, g, b, mx, sat, t, rood_max


def buren(m):
    """Waar een van de vier buren in m ligt."""
    o = np.zeros_like(m)
    o[1:] |= m[:-1]; o[:-1] |= m[1:]
    o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
    return o


def stukken(m):
    """Samenhangende stukken (acht buren), als lijsten van (y, x)."""
    h, w = m.shape
    gezien = np.zeros_like(m)
    for y0, x0 in zip(*np.nonzero(m)):
        if gezien[y0, x0]:
            continue
        stuk, rij = [], deque([(y0, x0)])
        gezien[y0, x0] = True
        while rij:
            y, x = rij.popleft()
            stuk.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not gezien[yy, xx]:
                        gezien[yy, xx] = True
                        rij.append((yy, xx))
        yield stuk


def lint(a):
    """Het lint, zoals vaanMaak het vindt."""
    r, g, b, mx, sat, t, rm = tint(a)
    zs = np.where(t > ZEKER['oranje'], ZEKER['oranjeS'], ZEKER['s'])
    zeker = rm & (mx >= ZEKER['v']) & (sat > zs) & (t >= ZEKER['t'][0]) & (t <= ZEKER['t'][1])
    rood = rm & (mx >= ROOD['v']) & (sat > ROOD['s']) & (t >= ROOD['t'][0]) & (t <= ROOD['t'][1])
    m = np.zeros_like(zeker)
    for stuk in stukken(zeker):
        if len(stuk) >= MIN_STUK:
            for y, x in stuk:
                m[y, x] = True
    dicht = m.copy()
    for _ in range(BIJ):
        dicht |= buren(dicht)
    m |= zeker & dicht
    for _ in range(STAP):
        m |= buren(m) & rood
    return m


def rand_erbij(a, m):
    """De omlijning, de zachte rand en de gele glans van het lint horen erbij."""
    r, g, b, mx, sat, t, _ = tint(a)
    donker = mx < 60
    zacht = a[..., 3] < 200
    geel = (g > 90) & (sat > 0.35) & (r >= b) & (g >= b) & (mx > 100) & (g > r * 0.6)
    mag = (a[..., 3] > 0) & (donker | zacht | geel)
    for _ in range(7):
        m = m | (buren(m) & mag)
    return m


def midden(a, m, x, y, r):
    """Het midden en de dikte van wat er in kolom x rond rij y staat (buiten het lint)."""
    h = a.shape[0]
    ys = [yy for yy in range(max(0, y - r), min(h, y + r + 1)) if a[yy, x, 3] > 128 and not m[yy, x]]
    return (sum(ys) / len(ys), len(ys)) if ys else None


def pas_aan(pad, nr):
    (sx, sy), marge = SCHAAL[nr]
    im = Image.open(pad).convert('RGBA')
    a = np.array(im)
    h, w = a.shape[:2]
    m = lint(a)
    ys, xs = np.nonzero(m)
    if not len(xs):
        sys.exit(f'{pad}: geen lint gevonden')
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if x1 - x0 < TE_KLEIN:
        print(f'{os.path.relpath(pad, ROOT)}: lint is {x1 - x0} breed, al verkleind, overgeslagen')
        return
    m = rand_erbij(a, m)
    m[max(0, y0 - 3):min(h, y1 + 4), x0:x1 - marge + 1] = True

    # de schacht: links bij de punt, rechts waar hij weer te zien is
    my = (y0 + y1) // 2
    xl, links = x0 - 2, None
    while links is None and xl > 0:
        links = midden(a, m, xl, my, 30)
        if links is None:
            xl -= 1
    xr, rechts = x1 + 3, None
    while rechts is None and xr < w - 1:
        rechts = midden(a, m, xr, round(links[0]), 10)
        if rechts is None:
            xr += 1
    dik = max(4, min(7, rechts[1]))

    # het lint los, en de rest zonder lint
    vaan = a.copy(); vaan[~m] = 0
    rest = a.copy(); rest[m] = 0

    # schacht getekend op vier keer de maat en dan verkleind, voor een zachte rand
    k = 4
    s = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    for kleur, dd in ((SCHACHT_RAND, dik + 2), (SCHACHT, dik)):
        p0, p1 = (xl * k, links[0] * k), (xr * k, rechts[0] * k)
        d.line([p0, p1], fill=kleur + (255,), width=dd * k)
        for px, py in (p0, p1):
            rr = dd * k / 2
            d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=kleur + (255,))
    uit = s.resize((w, h), Image.LANCZOS)
    uit.alpha_composite(Image.fromarray(rest))

    # het lint verkleind, rond waar het aan de speer vastzit
    ax, ay = x0, links[0]
    vy, vx = np.nonzero(vaan[..., 3])
    bx0, bx1, by0, by1 = vx.min(), vx.max() + 1, vy.min(), vy.max() + 1
    stuk = Image.fromarray(vaan).crop((bx0, by0, bx1, by1))
    nw, nh = max(1, round((bx1 - bx0) * sx)), max(1, round((by1 - by0) * sy))
    stuk = stuk.resize((nw, nh), Image.LANCZOS)
    plek = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    plek.paste(stuk, (round(ax + (bx0 - ax) * sx), round(ay + (by0 - ay) * sy)))
    uit.alpha_composite(plek)

    # losse stipjes die in het oude lintvak zijn blijven staan
    b = np.array(uit)
    vak = np.zeros((h, w), bool)
    vak[max(0, y0 - 3):min(h, y1 + 4), max(0, x0 - 2):min(w, x1 + 3)] = True
    weg = 0
    for stuk in stukken(b[..., 3] > 20):
        if len(stuk) < STIPJE and all(vak[y, x] for y, x in stuk):
            for y, x in stuk:
                b[max(0, y - 1):y + 2, max(0, x - 1):x + 2, 3] = 0
            weg += 1
    Image.fromarray(b).save(pad, optimize=True)
    print(f'{os.path.relpath(pad, ROOT)}: lint {x1 - x0 + 1} bij {y1 - y0 + 1} -> '
          f'{nw} bij {nh}, schacht {xl}..{xr}, {weg} stipjes weg')


def plat_frame8(pad):
    """Frame 8: het naar beneden hangende lint verticaal platdrukken, zodat het even klein is
    als frame 7. Anker is de bovenkant (bij de schacht), zodat het aan de speer vast blijft."""
    im = Image.open(pad).convert('RGBA')
    a = np.array(im)
    m = rand_erbij(a, lint(a))
    ys, xs = np.nonzero(m)
    if not len(xs):
        print(f'{os.path.relpath(pad, ROOT)}: geen lint gevonden'); return
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if y1 - y0 + 1 <= FRAME8_HOOG:
        print(f'{os.path.relpath(pad, ROOT)}: lint is {y1 - y0 + 1} hoog, al platgedrukt, overgeslagen')
        return

    # het losse lint en de rest zonder lint
    vaan = a.copy(); vaan[~m] = 0
    rest = a.copy(); rest[m] = 0

    crop = Image.fromarray(vaan).crop((x0, y0, x1 + 1, y1 + 1))
    nh = max(1, round(crop.height * FRAME8_SY))
    small = crop.resize((crop.width, nh), Image.LANCZOS)
    out = Image.fromarray(rest)
    out.alpha_composite(small, (x0, y0))

    # losse stipjes die in het oude lintvak zijn blijven staan weghalen (zie pas_aan)
    b = np.array(out)
    h, w = b.shape[:2]
    vak = np.zeros((h, w), bool)
    vak[max(0, y0 - 3):min(h, y1 + 4), max(0, x0 - 2):min(w, x1 + 3)] = True
    weg = 0
    for stuk in stukken(b[..., 3] > 20):
        if len(stuk) < STIPJE and all(vak[y, x] for y, x in stuk):
            for y, x in stuk:
                b[max(0, y - 1):y + 2, max(0, x - 1):x + 2, 3] = 0
            weg += 1
    Image.fromarray(b).save(pad, optimize=True)
    print(f'{os.path.relpath(pad, ROOT)}: lint {x1 - x0 + 1} bij {y1 - y0 + 1} -> '
          f'{x1 - x0 + 1} bij {nh}, {weg} stipjes weg')


def main():
    for nr in SCHAAL:
        pas_aan(os.path.join(ROOT, MAP, f'attack_sp_{nr}.png'), nr)
    plat_frame8(os.path.join(ROOT, MAP, f'attack_sp_{FRAME8}.png'))


if __name__ == '__main__':
    main()
