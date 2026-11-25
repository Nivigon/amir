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
    for k in range(n):
        if sz[k] < 40: continue
        ys, xs = np.nonzero(lab == k + 1); P = np.stack([xs, ys], 1).astype(float); c = P.mean(0)
        if sz[k] < 0.18 * groot:                     # een stompje voorbij de vuist: dat is grip
            grip[ys, xs] = True; continue
        _, _, vt = np.linalg.svd(P - c); d = vt[0]; t = (P - c) @ d; lo, hi = t.min(), t.max()
        L = hi - lo
        # welk eind zit in de hand: het eind dat het dichtst bij de vuist van het vorige frame ligt (de hand beweegt
        # weinig, de punt veel); in het eerste frame het onderste (begin 'onder') of het bovenste eind ('boven')
        e_hi, e_lo = c + d * hi, c + d * lo
        if vorige:
            dist = lambda e: min(np.hypot(*(e - v)) for v in vorige)
            hi_hand = dist(e_hi) <= dist(e_lo)
        else:
            hi_hand = (e_hi[1] > e_lo[1]) == (begin == 'onder')
        g_sel = (t > hi - 0.27 * L) if hi_hand else (t < lo + 0.27 * L)
        grip[P[g_sel, 1].astype(int), P[g_sel, 0].astype(int)] = True
        eind = c + d * (hi if hi_hand else lo); ander = c + d * (lo if hi_hand else hi)
        kn = eind + (ander - eind) * 0.08
        punten.append((kn, L, eind))
    grip = ndimage.binary_dilation(grip, iterations=2) & (gr > 0)
    l = np.clip(g / 255, 0, 1)[..., None]
    kl = np.where(grip[..., None], GRIP, HOUT) * (0.6 + 0.8 * l)
    return rgb * (1 - gr[..., None]) + np.clip(kl, 0, 255) * gr[..., None], punten


def main():
    alles = {}
    for zet, (map_, i0, i1, begin) in CLIPS.items():
        uit = os.path.join('karakters/amir/stokken', zet); os.makedirs(uit, exist_ok=True)
        rij = []; vorige = []
        for k, i in enumerate(range(i0, i1 + 1, 2)):
            a = np.array(Image.open(f'{R}{map_}/f_{i:03d}.png').convert('RGB')).astype(float)
            rgb, al = key(a)
            rgb, punten = stokken(rgb, al, vorige, begin)
            vorige = [p[2] for p in punten] or vorige
            im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8))
            im = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)
            c = Image.new('RGBA', (W, H)); c.alpha_composite(im, (round(T[0]), round(T[1])))
            c.save(f'{uit}/{zet}_{k:02d}.png')
            # de twee langste stokken, de achterste (verst naar rechts, hij kijkt naar links) met de vlag achter
            punten = sorted(punten, key=lambda p: -p[1])[:2]
            punten = sorted(punten, key=lambda p: p[0][0])
            pt = []
            for j, (kn, _, _) in enumerate(punten):
                pt += [round(kn[0] * S + T[0], 1), round(kn[1] * S + T[1], 1), 1 if j == 1 else 0]
            if len(pt) < 6: pt = (pt + rij[-1][len(pt):]) if rij else (pt * 2)[:6]
            rij.append(pt)
        alles[zet] = rij
        print(zet, len(rij))
    json.dump(alles, open(R + 'punt_extra.json', 'w'))


if __name__ == '__main__':
    main()
