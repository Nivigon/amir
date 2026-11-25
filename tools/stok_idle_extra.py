#!/usr/bin/env python3
"""De overgang naar de schouder-idle en de draai met de stokken (STOK.idleIn, STOK.idleDraai), uit twee Grok-clips.

Bron (groene stokken op magenta, hetzelfde canvas als de idle-clip, dus dezelfde schaal en verschuiving als
tools/stok_idle_maak.py):
  bron/idle/grok_overgang.mp4  staan (beginbeeld) naar de schouders (eindbeeld idle-frame 0), Grok-post 42689905
  bron/idle/grok_draai.mp4     een lus op idle-frame 0: de stokken eraf, draaien langs de heupen, terug, Grok-post 7767bae7
Eerst de frames eruit:
  ffmpeg -i karakters/amir/stokken/bron/idle/grok_overgang.mp4 karakters/amir/stokken/bron/idle/ruw_in/f_%03d.png
  ffmpeg -i karakters/amir/stokken/bron/idle/grok_draai.mp4 karakters/amir/stokken/bron/idle/ruw_draai/f_%03d.png
Dan:  python3 tools/stok_idle_extra.py
Uit: karakters/amir/stokken/idle_in/ en idle_draai/ (om de twee clipframes, 12 per seconde) en in de bronmap
punt_extra.json (de knopen van de slippen voor STOK.slip.punt). Daarna de winkelstokken niet (die vallen op de gewone
terug), klein/ kopieren, vacht_bak.js en gen-offline-manifest.py.

Het groen wordt omgekleurd zoals in de idle: donker hout, en de grip (het kwart aan de kant van de vuist) oker. Welke kant
de vuist is, zie je aan het lijf: aan het eind met de meeste huid ernaast zit de hand.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

R = 'karakters/amir/stokken/bron/idle/'
S = 275 / 612
T = (37.59088186566083, 54.02124183006538)      # uit stok_idle_maak.py (de broek boven die van staan)
W, H = 511, 384
HOUT = np.array([40, 31, 27.]); GRIP = np.array([170, 108, 40.])
CLIPS = {                                         # set: (map met ruwe frames, eerste frame, laatste frame), om de twee
    'idle_in': ('ruw_in', 7, 47, 'boven'),
    'idle_draai': ('ruw_draai', 17, 101, 'onder'),
}


def key(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    bgl = (m > 0.5) & (r > 140) & (b > 100)
    lab, n = ndimage.label(bgl); sz = ndimage.sum(bgl, lab, range(1, n + 1))
    bg = np.isin(lab, [k + 1 for k, s in enumerate(sz) if s > 60])
    rand = ndimage.binary_dilation(bg, iterations=2) & ~bg
    al = np.ones(a.shape[:2]); al[bg] = 0
    soft = np.clip((0.62 - m) / 0.3, 0, 1); al[rand] = np.minimum(al[rand], soft[rand])
    ex = np.clip(np.minimum(r, b) - g, 0, None) * (1 - al)
    return np.stack([r - ex, g, b - ex], -1), al


def stokken(rgb, al, vorige, begin):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    gr = np.clip((g - np.maximum(r, b) - 4) / 45, 0, 1) * (al > 0.3)
    m = ndimage.binary_closing(gr > 0.2, iterations=2)
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
    grip = np.zeros(m.shape, bool); punten = []
    groot = max(sz) if n else 0
    # stukken van dezelfde stok (onderbroken door een vuist of het lijf) eerst samenvoegen: zelfde richting, op een lijn
    stuk = []
    for k in range(n):
        if sz[k] < 40: continue
        ys, xs = np.nonzero(lab == k + 1); P = np.stack([xs, ys], 1).astype(float); c = P.mean(0)
        d = np.linalg.svd(P - c)[2][0] if len(P) > 2 else np.array([1., 0])
        stuk.append([P, c, d, sz[k]])
    stuk.sort(key=lambda s: -s[3])
    groepen = []
    for P, c, d, s in stuk:
        for gp in groepen:
            gc, gd = gp[1], gp[2]
            hoek = abs(float(gd @ d)) if s > 120 else 1.0          # een klein stompje heeft geen betrouwbare richting
            loodrecht = abs(float((c - gc) @ np.array([-gd[1], gd[0]])))
            if hoek > 0.985 and loodrecht < 10:
                gp[0] = np.vstack([gp[0], P]); gp[3] += s; break
        else:
            groepen.append([P, c, d, s])
    stompjes = [P.mean(0) for P, c0, d0, s in groepen if s < 0.18 * groot]
    for P, c0, d0, s in groepen:
        ys, xs = P[:, 1].astype(int), P[:, 0].astype(int)
        if s < 0.18 * groot:                         # een los stompje voorbij de vuist: dat is grip
            grip[ys, xs] = True; continue
        c = P.mean(0)
        _, _, vt = np.linalg.svd(P - c); d = vt[0]; t = (P - c) @ d; lo, hi = t.min(), t.max()
        L = hi - lo
        # welk eind zit in de hand: het eind dat het dichtst bij de vuist van het vorige frame ligt (de hand beweegt
        # weinig, de punt veel); in het eerste frame het onderste (begin 'onder') of het bovenste eind ('boven')
        e_hi, e_lo = c + d * hi, c + d * lo
        # eerst de vuist zelf zoeken: langs de lijn een kort stuk huid tussen of naast het groen (een vuist is 8 tot 40 px,
        # het lijf achter de stok is langer)
        vuist = None
        ts = np.arange(lo - 25, hi + 25)
        pts = (c[None] + ts[:, None] * d[None]).round().astype(int)
        ok = (pts[:, 0] >= 0) & (pts[:, 0] < m.shape[1]) & (pts[:, 1] >= 0) & (pts[:, 1] < m.shape[0])
        if ok.all():
            px = rgb[pts[:, 1], pts[:, 0]]; a_ = al[pts[:, 1], pts[:, 0]]; gm = m[pts[:, 1], pts[:, 0]]
            huid = (a_ > 0.5) & ~gm & (px[:, 0] > px[:, 1] + 6) & (px[:, 0] < 170) & (px[:, 2] < 120)
            runs, i = [], 0
            while i < len(ts):
                if huid[i]:
                    s0 = i
                    while i < len(ts) and huid[i]: i += 1
                    runs.append((s0, i - 1))
                i += 1
            kand = [(ts[s0] + ts[s1]) / 2 for s0, s1 in runs if 8 <= s1 - s0 <= 40]
            if kand: vuist = min(kand, key=lambda v: min(abs(v - lo), abs(v - hi)))
        # een los stompje vlak bij een eind (op de lijn): daar zit de vuist, en het stompje is het uiteinde
        stomp = [(np.hypot(*(sp - e_hi)), np.hypot(*(sp - e_lo))) for sp in stompjes
                 if abs(float((sp - c) @ np.array([-d[1], d[0]]))) < 14 and min(np.hypot(*(sp - e_hi)), np.hypot(*(sp - e_lo))) < 45]
        if stomp:
            dh, dl = min(stomp, key=lambda q: min(q))
            hi_hand = dh < dl
            sp = min(stompjes, key=lambda q: min(np.hypot(*(q - e_hi)), np.hypot(*(q - e_lo))))
            if hi_hand: hi = max(hi, float((sp - c) @ d) + 6)          # de stok loopt door tot voorbij het stompje
            else: lo = min(lo, float((sp - c) @ d) - 6)
            e_hi, e_lo = c + d * hi, c + d * lo; L = hi - lo
        elif vuist is not None and abs((vuist - lo) - (hi - vuist)) > 0.1 * L:
            hi_hand = (hi - vuist) < (vuist - lo)
        elif vorige:
            dist = lambda e: min(np.hypot(*(e - v)) for v in vorige)
            hi_hand = dist(e_hi) <= dist(e_lo)
        else:
            hi_hand = (e_hi[1] > e_lo[1]) == (begin == 'onder')
        g_sel = (t > hi - 0.27 * L) if hi_hand else (t < lo + 0.27 * L)
        grip[P[g_sel, 1].astype(int), P[g_sel, 0].astype(int)] = True
        eind = c + d * (hi if hi_hand else lo); ander = c + d * (lo if hi_hand else hi)
        kn = eind + (ander - eind) * 0.08
        punten.append((kn, L, eind, ander))
    grip = ndimage.binary_dilation(grip, iterations=2) & (gr > 0)
    l = np.clip(g / 255, 0, 1)[..., None]
    kl = np.where(grip[..., None], GRIP, HOUT) * (0.6 + 0.8 * l)
    return rgb * (1 - gr[..., None]) + np.clip(kl, 0, 255) * gr[..., None], punten, gr


def voetVerschuif(beelden, ref):
    """Per beeld de verschuiving (dx, dy) waarmee de voeten op die van ref vallen (de voeten blijven staan)."""
    rv = np.array(ref.crop((240, 330, 350, 384)))[..., 3] > 128
    uit = []
    for im in beelden:
        a = np.array(im.crop((240, 330, 350, 384)))[..., 3] > 128
        best = None
        for dx in range(-12, 13):
            for dy in range(-6, 7):
                s = np.roll(np.roll(a, dx, 1), dy, 0); iou = (s & rv).sum() / max((s | rv).sum(), 1)
                if best is None or iou > best[0]: best = (iou, dx, dy)
        uit.append(best[1:])
    return uit


def main():
    alles = {}; staven = {}
    ref = Image.open('karakters/amir/stokken/idle/idle_00.png')
    for zet, (map_, i0, i1, begin) in CLIPS.items():
        uit = os.path.join('karakters/amir/stokken', zet); os.makedirs(uit, exist_ok=True)
        os.makedirs(R + 'uit_' + zet, exist_ok=True)
        beelden, maskers, rij, lijnen = [], [], [], []; vorige = []
        for k, i in enumerate(range(i0, i1 + 1, 2)):
            a = np.array(Image.open(f'{R}{map_}/f_{i:03d}.png').convert('RGB')).astype(float)
            rgb, al = key(a)
            rgb, punten, gr = stokken(rgb, al, vorige, begin)
            vorige = [p[2] for p in punten] or vorige
            im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8))
            w, h = round(im.width * S), round(im.height * S)
            c = Image.new('RGBA', (W, H)); c.alpha_composite(im.resize((w, h), Image.LANCZOS), (round(T[0]), round(T[1])))
            gm = Image.fromarray((gr * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
            cm = Image.new('L', (W, H)); cm.paste(gm, (round(T[0]), round(T[1])))
            beelden.append(c); maskers.append(cm)
            g = lambda v: (v[0] * S + T[0], v[1] * S + T[1])
            punten = sorted(punten, key=lambda p: -p[1])[:2]
            lijnen.append([[*g(p[3]), *g(p[2]), p[1] * S] for p in punten])      # per stok: tip, het eind bij de vuist, de lengte
            punten = sorted(punten, key=lambda p: p[0][0])
            pt = []
            for j, p in enumerate(punten):
                x, y = g(p[0]); pt += [x, y, 1 if j == 1 else 0]
            if len(pt) < 6: pt = (pt + rij[-1][len(pt):]) if rij else (pt * 2)[:6]
            rij.append(pt)
        # de voeten: in de overgang staan ze in de clip een paar pixels lager dan in de idle en springen ze aan het eind
        # omhoog. Schuif elk beeld zo dat de voeten blijven staan: aan het begin zoals bij staan, aan het eind zoals in
        # de idle, en daartussen geleidelijk (de draai begint en eindigt al op de idle).
        sch = voetVerschuif(beelden, ref)
        n = len(beelden)
        for k in range(n):
            wgt = 1.0 if zet != 'idle_in' else min(1.0, k / max(1, n - 5))
            dx, dy = round(sch[k][0] * wgt), round(sch[k][1] * wgt)
            if dx or dy:
                for lst in (beelden, maskers):
                    nw = Image.new(lst[k].mode, (W, H)); nw.paste(lst[k], (dx, dy)); lst[k] = nw
                rij[k] = [v + (dx if q % 3 == 0 else dy if q % 3 == 1 else 0) for q, v in enumerate(rij[k])]
                lijnen[k] = [[l[0] + dx, l[1] + dy, l[2] + dx, l[3] + dy, l[4]] for l in lijnen[k]]
            beelden[k].save(f'{uit}/{zet}_{k:02d}.png')
            maskers[k].save(f'{R}uit_{zet}/{zet}_{k:02d}_stok.png')
        alles[zet] = [[round(v, 1) for v in r] for r in rij]
        staven[zet] = [[[round(v, 1) for v in l] for l in ls] for ls in lijnen]
        print(zet, n, 'voeten', sch[0], sch[n // 2], sch[-1])
    json.dump(alles, open(R + 'punt_extra.json', 'w'))
    json.dump(staven, open(R + 'staven_extra.json', 'w'))


if __name__ == '__main__':
    main()
