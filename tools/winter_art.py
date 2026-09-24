#!/usr/bin/env python3
"""Maakt de winterart voor episode Winter World.

    python3 tools/winter_art.py            # alles
    python3 tools/winter_art.py panter     # of: hyena, grond, gras

Nodig: pillow en numpy (pip install pillow numpy).

- panter: alle frames van de zwarte panter worden wit (enemies/panter_wit/...).
  De tekening blijft, alleen de toonschaal draait om: zwart wordt wit, schaduw
  wordt lichtgrijs, de rozetten schemeren als grijze vlekken door.
- hyena: alle frames van de hyena worden wit-grijs (enemies/hyena_wit/...).
  Vacht wit, vlekken donkergrijs, ogen en bek blijven.
- grond: design/grondrand_sneeuw.png. Sneeuw op het loopvlak, een sneeuwrand
  over de afbrokkelende rand, en de rotswand eronder grijs. Naadloos in de breedte.
- gras: design/drygrass_sneeuw.png. Bevroren droog gras: bleek, met rijp op de sprieten.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sneeuw import blur, box, dilate, noise2d, smooth1d, median1d, shift_down, shift_up, find_rim, load, to_img, from_img  # noqa: E402


def save(out, alpha, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    res = np.concatenate([np.clip(out, 0, 1), alpha[..., None]], -1)
    Image.fromarray((res * 255).round().astype(np.uint8), "RGBA").save(dst)


def hsv_parts(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    return mx, mn, sat


# ---------------------------------------------------------------- witte panter
def white_panther(src, dst, low=0.47, high=0.965, warm=0.6, rosette=0.85):
    rgb, alpha, lum, opaque, dark = load(src)
    mx, mn, sat = hsv_parts(rgb)
    eyes = opaque & (sat > 0.45) & (mx > 0.25) & (rgb[..., 1] >= rgb[..., 2])
    teeth = opaque & (lum > 0.6) & (sat < 0.25)
    keep = eyes | teeth
    v = lum[opaque & ~keep]
    if v.size < 10:
        save(rgb, alpha, dst); return
    lo, hi = np.percentile(v, [1, 95])
    st = np.clip((lum - lo) / max(hi - lo, 1e-3), 0, 1)
    st = np.sqrt(st)                                   # schaduwen wat lichter, matter
    fill = np.where(opaque, st, np.median(st[opaque]))
    base = blur(fill, 6)
    st = np.clip(base + (st - base) * rosette, 0, 1)   # rozetten (lichte ringen) iets dempen
    new = low + (high - low) * st
    edge = blur((~opaque).astype(float), 2.5) * opaque
    new = new - 0.18 * np.clip(edge * 3, 0, 1)         # dun grijs randje, anders valt hij weg tegen sneeuw
    tint = np.array([1.0, 1.0 - 0.02 * warm, 1.0 - 0.06 * warm])
    out = np.clip(new[..., None] * tint[None, None, :], 0, 1)
    out = np.where(keep[..., None], rgb, out)
    save(out, alpha, dst)


# ---------------------------------------------------------------- witte hyena
def white_hyena(src, dst):
    rgb, alpha, lum, opaque, dark = load(src)
    mx, mn, sat = hsv_parts(rgb)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # ogen: geel en verzadigd; bek: rood/roze. Die blijven zoals ze zijn.
    # het oog is fel geel: groen bijna zo sterk als rood. Tan vacht (g ongeveer 0,7 x r) valt erbuiten.
    eyes = opaque & (sat > 0.6) & (mx > 0.6) & (g > r * 0.8) & (r > b * 2.5)
    # de bek is echt rood/roze: veel meer rood dan groen. Bruine vachtschaduw (r ongeveer 1,2 x g) valt erbuiten.
    mouth = opaque & (sat > 0.4) & (r > 0.35) & (r > g * 1.9) & (r > b * 1.4)
    keep = eyes | mouth
    # vacht: verzadiging bijna weg, helderheid omhoog met behoud van donkere vlekken en contour
    v = mx
    v2 = 1.0 - (1.0 - v) ** 2.1
    grey = np.stack([v2, v2, v2], -1)
    cool = np.array([0.97, 0.985, 1.0])
    col = grey * cool[None, None, :]
    # heel licht wat van de oorspronkelijke kleur laten staan (warmte in de vacht)
    rest = np.where(sat[..., None] > 1e-3, rgb / np.maximum(mx, 1e-3)[..., None], 1.0)
    col = col * (0.88 + 0.12 * rest)
    out = np.where(keep[..., None], rgb, col)
    save(np.clip(out, 0, 1), alpha, dst)


# ---------------------------------------------------------------- wintergrond
def noise_x_periodic(shape, scale, seed):
    """zachte ruis die in de breedte naadloos rondloopt: som van cosinussen met hele golfgetallen"""
    rng = np.random.default_rng(seed)
    H, W = shape
    ys = np.arange(H)[:, None] / max(1, scale)
    xs = np.arange(W)[None, :]
    out = np.zeros((H, W))
    kmax = max(2, int(W / scale))
    for k in range(1, kmax + 1):
        for j in range(0, 3):
            amp = 1.0 / (k + 1) / (j + 1)
            out += amp * np.cos(2 * np.pi * k * xs / W + rng.uniform(0, 2 * np.pi)) \
                       * np.cos(2 * np.pi * j * ys / 6.0 + rng.uniform(0, 2 * np.pi))
    out = (out - out.min()) / max(out.max() - out.min(), 1e-6)
    return out


def snow_ground(src, dst, rim_win=(140, 180), cover=0.10, fringe=0.06, seed=4):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    rim = find_rim(lum, opaque, *rim_win)
    rim = np.full(W, float(np.median(rim)))             # de rand ligt praktisch recht: één rij, dan blijft hij naadloos
    top = np.where(opaque.any(0), opaque.argmax(0), H).astype(float)

    field = 0.7 * noise_x_periodic((H, W), W // 8, seed) + 0.3 * noise_x_periodic((H, W), W // 40, seed + 1)
    plane = (ys >= top[None, :]) & (ys < rim[None, :]) & opaque & (field > cover)
    plane |= (ys >= (rim - 0.06 * H)[None, :]) & (ys < rim[None, :]) & opaque
    n1 = noise_x_periodic((1, W), W // 25, seed + 3)[0]
    n2 = noise_x_periodic((1, W), W // 90, seed + 4)[0]
    f = np.maximum(fringe * H * (0.6 + 0.8 * n1) + fringe * H * 0.5 * (n2 - 0.5), fringe * H * 0.35)
    fr = (ys >= rim[None, :]) & (ys < (rim + f)[None, :]) & opaque
    m = blur((plane | fr).astype(float), 2.0) > 0.5
    m &= opaque

    # de wand eronder grijs: verzadiging weg, iets koeler, iets lichter (hoog in de bergen)
    mx, mn, sat = hsv_parts(rgb)
    grey = 0.25 * rgb[..., 0] + 0.6 * rgb[..., 1] + 0.15 * rgb[..., 2]
    wall = np.stack([grey * 0.98, grey * 1.0, grey * 1.06], -1) * 1.08
    base = np.clip(wall, 0, 1)

    mf = m.astype(float)
    outline = np.zeros((H, W), bool)
    for k in range(1, 3):
        outline |= shift_down(m, k) & ~m
    outline &= opaque
    s = max(4, int(H * 0.03))
    lower = np.zeros((H, W), bool)
    for k in range(1, s + 1):
        lower |= m & ~shift_up(m, k)
    shade = blur(lower.astype(float), s * 0.5) * mf
    relief = noise_x_periodic((H, W), W // 60, seed + 5)
    white = np.array([0.97, 0.98, 1.0]); shade_c = np.array([0.72, 0.80, 0.93]); line_c = np.array([0.20, 0.22, 0.30])
    col = white[None, None, :] * (0.92 + 0.08 * relief)[..., None]
    col = col * (1 - shade[..., None] * 0.6) + shade_c[None, None, :] * (shade[..., None] * 0.6)
    out = np.where(m[..., None], col, base)
    out = np.where(outline[..., None], line_c[None, None, :] * 0.6 + out * 0.4, out)
    save(out, alpha, dst)


# ---------------------------------------------------------------- bevroren gras
def frost_grass(src, dst, seed=2):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    mx, mn, sat = hsv_parts(rgb)
    # bleek: verzadiging grotendeels weg, lichter, koel
    grey = 0.3 * rgb[..., 0] + 0.55 * rgb[..., 1] + 0.15 * rgb[..., 2]
    pale = np.stack([grey * 1.0, grey * 1.02, grey * 1.08], -1)
    col = np.clip(rgb * 0.25 + pale * 0.75, 0, 1)
    col = np.clip(col * 1.18, 0, 1)
    col = np.where(dark[..., None], rgb * 0.9 + 0.05, col)     # contouren blijven donker
    # rijp: de bovenkant van elke spriet (eerste paar dekkende pixels van boven per kolom)
    ys = np.arange(H)[:, None]
    run = np.zeros(W); depth = np.zeros((H, W))
    for y in range(H):
        run = np.where(opaque[y], run + 1, 0); depth[y] = run
    n = noise2d((H, W), 5, seed)
    rim = opaque & (depth <= 2 + 3 * n) & ~dark
    rim_f = blur(rim.astype(float), 0.8)
    frost = np.array([0.97, 0.98, 1.0])
    out = col * (1 - rim_f[..., None]) + frost[None, None, :] * rim_f[..., None]
    save(out, alpha, dst)


# ---------------------------------------------------------------- aansturing
PAN_SETS = {'walk': 14, 'turn': 24, 'prowl': 16, 'pounce': 20, 'run': 9}
HY_SETS = {'loop': 20, 'dreigen': 22, 'ren_lijf': 12, 'ren_kop': 27}


def do_panther():
    src_root = os.path.join(ROOT, 'enemies', 'blackpanther')
    dst_root = os.path.join(ROOT, 'enemies', 'panter_wit')
    n = 0
    for k, cnt in PAN_SETS.items():
        for i in range(cnt):
            f = '%s_%02d.png' % (k, i)
            white_panther(os.path.join(src_root, 'blackpanther', k, f), os.path.join(dst_root, 'panter_wit', k, f)); n += 1
    for i in range(14):
        f = 'claw_%02d.png' % i
        white_panther(os.path.join(src_root, 'lowstrike', f), os.path.join(dst_root, 'lowstrike', f)); n += 1
    print('panter: %d frames -> enemies/panter_wit' % n)


def do_hyena():
    src_root = os.path.join(ROOT, 'enemies', 'hyena')
    dst_root = os.path.join(ROOT, 'enemies', 'hyena_wit')
    n = 0
    for k, cnt in HY_SETS.items():
        for i in range(cnt):
            f = '%s_%02d.png' % (k, i)
            white_hyena(os.path.join(src_root, k, f), os.path.join(dst_root, k, f)); n += 1
    print('hyena: %d frames -> enemies/hyena_wit' % n)


def do_ground():
    snow_ground(os.path.join(ROOT, 'design', 'grondrand.png'), os.path.join(ROOT, 'design', 'grondrand_sneeuw.png'))
    print('grond: design/grondrand_sneeuw.png')


def do_grass():
    frost_grass(os.path.join(ROOT, 'design', 'drygrass.png'), os.path.join(ROOT, 'design', 'drygrass_sneeuw.png'))
    print('gras: design/drygrass_sneeuw.png')


JOBS = {'panter': do_panther, 'hyena': do_hyena, 'grond': do_ground, 'gras': do_grass}

if __name__ == '__main__':
    names = sys.argv[1:] or list(JOBS)
    for nm in names:
        if nm not in JOBS:
            sys.exit('onbekend: %s (kies uit %s)' % (nm, ', '.join(JOBS)))
        JOBS[nm]()
