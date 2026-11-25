#!/usr/bin/env python3
"""De schouder-idle, de overgang en de draai naar de Animeer tool Amir stokken, zodat de stokken daar bij te stellen zijn.

Per frame: het lijf zonder de Grok-stok (het groen uit stok_idle_maak.py / stok_idle_extra.py eruit, en waar de stok voor het
lijf lag het lijf dichtgeschilderd), en de twee stokken als items met hun plaats, hoek en een achter-masker waar het lijf
(de vuist, het hoofd) in de clip over de stok lag. Het spelcanvas (511x384, anker 298, grond 379) is het Animeer-canvas
(594x301, anker 297, grond 297) plus (1, 82): dezelfde schaal.

  python3 tools/stok_idle_tool.py <map van stok_idle_maak.py> <uitmap>
Uit: <uitmap>/f/<anim>_NN.png en <uitmap>/d.json (anims en init voor const D van de tool).
Anims: idle_schouder (de idle), idle_in (de overgang), idle_draai (de draai).
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
import cv2

AW, AH = 594, 301
DXY = (1, 82)                                     # spel = tool + DXY
LENGTE = 148.3                                    # de Grok-stok in spelpixels (stok_idle_variant.py)
OUD_W = 0.1936 * AW; OUD_GRIP = (0.81 - 0.5) * OUD_W
GRIP_EIND = (1643 - 1315) * 155 / 1536            # van het midden van de grip tot het uiteinde, de gebakken stok
B = 'karakters/amir/stokken/'


def lijf(fr, gr):
    a = np.array(fr).astype(np.float32)
    al = a[..., 3] / 255
    zone = ndimage.binary_dilation(gr > 0.12, iterations=3)       # de stok met zijn donkere omlijning
    rest = (al > 0.5) & ~zone
    # het lijf dat onder de stok lag: in de zone, met lijf aan twee tegenovergestelde kanten (binnen 16 px, in 8 richtingen)
    dicht = np.zeros_like(zone)
    for hoek in np.arange(0, 180, 22.5):
        dx, dy = math.cos(math.radians(hoek)), math.sin(math.radians(hoek))
        plus = np.zeros_like(zone); min_ = np.zeros_like(zone)
        for d in range(1, 17):
            sx, sy = int(round(dx * d)), int(round(dy * d))
            plus |= np.roll(np.roll(rest, -sy, 0), -sx, 1); min_ |= np.roll(np.roll(rest, sy, 0), sx, 1)
        dicht |= plus & min_
    dicht &= zone
    rgb = a[..., :3].astype(np.uint8).copy()
    rgb = cv2.inpaint(rgb, (zone & (al > 0.05)).astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA)
    alfa = np.where(zone, np.where(dicht, 255, 0), al * 255)
    lab, n = ndimage.label(alfa > 60)                              # losse snippers van de oude stok weg
    if n > 1:
        sz = ndimage.sum(alfa > 60, lab, range(1, n + 1))
        alfa[np.isin(lab, [k + 1 for k, s in enumerate(sz) if s < 60])] = 0
    return Image.fromarray(np.dstack([rgb, alfa]).astype(np.uint8))


def items(fr, gr, lijnen):
    """lijnen: per stok [tipx, tipy, eindx, eindy, (lengte)], spelcoordinaten. Geeft L en im voor de tool."""
    a = np.array(fr).astype(float); al = a[..., 3] / 255
    st = []
    for ln in lijnen:
        T = np.array(ln[:2]); E0 = np.array(ln[2:4])
        u = (E0 - T) / max(np.hypot(*(E0 - T)), 1e-6)
        E = E0 if len(ln) > 4 and ln[4] >= 0.85 * LENGTE else T + u * LENGTE
        st.append((T, E, u))
    st.sort(key=lambda s: -max(s[0][0], s[1][0]))           # de achterste (verst naar rechts) eerst
    L, im = {}, {}
    for sid, (T, E, u) in zip(('stok_achter', 'stok_voor'), st):
        G = E - u * GRIP_EIND; C = G - u * OUD_GRIP
        rot = math.degrees(math.atan2(u[1], u[0]))
        L[sid] = {'on': True, 'angle': 'zij', 'cx': round((C[0] - DXY[0]) / AW, 4), 'cy': round((C[1] - DXY[1]) / AH, 4),
                  'w': 0.1936, 'rot': round(rot, 1), 'flip': False, 'behind': False, 'op': 1, 'locked': False}
        # waar in de clip het lijf over de stok lag: daar achter het lijf (vuist, hoofd)
        n = int(np.hypot(*(E - T)) // 2) + 1; seg, run = [], None
        for k in range(n + 1):
            P = T + (E - T) * k / n; x, y = int(round(P[0])), int(round(P[1]))
            over = 0 <= y < al.shape[0] and 0 <= x < al.shape[1] and al[y, x] > 0.5 and gr[y, x] < 0.15
            d = float((P - C) @ u)
            if over: run = [run[0] if run else d, d]
            elif run: seg.append(run); run = None
        if run: seg.append(run)
        sts = [{'t': 'achter', 's': 0.13, 'p': [[round(0.5 + s0 / OUD_W, 4), 0.5], [round(0.5 + s1 / OUD_W, 4), 0.5]]}
               for s0, s1 in seg if s1 - s0 >= 3]
        if sts: im[sid + '|basis'] = sts
    return L, im


def main():
    bron, uit = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(uit, 'f'), exist_ok=True)
    R = B + 'bron/idle/'
    lijnIdle = json.load(open(os.path.join(bron, 'punt.json')))['lijnen']
    staven = json.load(open(R + 'staven_extra.json'))
    sets = [('idle_schouder', 'Staan (schouders, idle)', 18, 200,
             lambda i: (B + f'idle/idle_{i:02d}.png', os.path.join(bron, 'uit', f'idle_{i:02d}_stok.png'), lijnIdle[i])),
            ('idle_in', 'Naar de schouders (overgang)', 21, 71,
             lambda i: (B + f'idle_in/idle_in_{i:02d}.png', R + f'uit_idle_in/idle_in_{i:02d}_stok.png', staven['idle_in'][i])),
            ('idle_draai', 'Draai (Y)', 43, 83,
             lambda i: (B + f'idle_draai/idle_draai_{i:02d}.png', R + f'uit_idle_draai/idle_draai_{i:02d}_stok.png', staven['idle_draai'][i]))]
    anims, init = [], {}
    for aid, naam, n, ms, bronF in sets:
        frames, ini = [], []
        for i in range(n):
            pb, pm, ln = bronF(i)
            fr = Image.open(pb).convert('RGBA'); gr = np.array(Image.open(pm)).astype(float) / 255
            if aid == 'idle_schouder':                       # de idle-lijnen: vaste lengte vanaf de grip
                ln = [[*l[:2], *l[2:4]] for l in ln]
            body = lijf(fr, gr)
            t = Image.new('RGBA', (AW, AH)); t.alpha_composite(body, (-DXY[0], -DXY[1]) if False else (0, 0), (DXY[0], DXY[1]))
            t.save(os.path.join(uit, 'f', f'{aid}_{i:02d}.png'), optimize=True)
            L, im = items(fr, gr, ln)
            ini.append({'L': L, 'body': {'basis': []}, 'im': im})
            frames.append({'src': f'f/{aid}_{i:02d}.png', 'orig': i, 'ms': ms})
        anims.append({'id': aid, 'name': naam, 'frames': frames}); init[aid] = ini
        print(aid, n)
    json.dump({'anims': anims, 'init': init}, open(os.path.join(uit, 'd.json'), 'w'))


if __name__ == '__main__':
    main()
