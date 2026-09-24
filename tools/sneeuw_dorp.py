#!/usr/bin/env python3
"""Maakt de sneeuwversies van de hutten, de boom en de struik (bestandsnaam met _sneeuw erachter).

    python3 tools/sneeuw_dorp.py                  # alles opnieuw genereren
    python3 tools/sneeuw_dorp.py hut_round_arch   # alleen die ene

Nodig: pillow en numpy (pip install pillow numpy).

Drie lagen sneeuw, boven op elkaar:
- dak: bij een hut is per plaatje de onderrand van het rieten dak opgegeven (een
  lijn door een paar punten). Alles daarboven wordt een sneeuwdek, op de puntige
  rietfranje na, die onder een rafelige sneeuwrand uitsteekt. De rietlagen
  schemeren als zachte schaduwbanden door het dek heen.
- kappen: elk stuk plaatje waar de lucht recht boven zit (potranden, de dwarsbalk
  van de put, stenen, bladkluiten van de boom en de struik) krijgt een sneeuwkap,
  dik op vlakke stukken, dun op steile.
- grond: in de grondstrook (onder een opgegeven rij) wordt de kale aarde een
  sneeuwlaag en krijgt het gras dezelfde bevroren, bleke look als drygrass_sneeuw.

Alles wat geen sneeuw krijgt, krijgt een koude tint; de zwarte contouren blijven.
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sneeuw import blur, box, dilate, noise2d, smooth1d, median1d, shift_down, shift_up, load  # noqa: E402

WHITE = np.array([0.97, 0.98, 1.0])
SHADE = np.array([0.72, 0.80, 0.93])
LINE = np.array([0.20, 0.22, 0.30])
FROST = np.array([0.97, 0.98, 1.0])


def save(out, alpha, dst):
    res = np.concatenate([np.clip(out, 0, 1), alpha[..., None]], -1)
    Image.fromarray((res * 255).round().astype(np.uint8), "RGBA").save(dst)
    print("geschreven:", os.path.relpath(dst, ROOT))


def polyline(points, W):
    """y per kolom, lineair tussen de opgegeven (x, y)-punten, buiten de punten vlak"""
    xs, ys = zip(*points)
    return np.interp(np.arange(W), xs, ys)


def long_lines(dark, n):
    """donkere pixels die op een lijn van n pixels liggen (horizontaal, verticaal of diagonaal)"""
    d = dark.astype(float)
    H, W = d.shape
    best = np.zeros((H, W))
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        acc = np.zeros((H, W))
        for k in range(-(n // 2), n // 2 + 1):
            acc += np.roll(np.roll(d, k * dy, axis=0), k * dx, axis=1)
        best = np.maximum(best, acc / n)
    return dark & (best > 0.8)


def hsv_parts(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    return mx, mn, sat


# ---------------------------------------------------------------- kappen op alles met lucht erboven
def local_caps(opaque, dark, outer_line, H, W, tmax, slope_k, seed, skip=None):
    """sneeuw onder elke 'plaatselijke bovenkant': een dekkende pixel met een doorzichtige erboven"""
    tops = opaque & ~shift_down(opaque, 1)
    tops[0] = opaque[0]
    if skip is not None:
        tops &= ~skip
    # helling van zo'n bovenrand: vergelijk met de bovenranden 4 kolommen verderop
    ys = np.arange(H)[:, None]
    yidx = np.where(tops, ys, np.nan)
    near = box(tops.astype(float), 0, 6) > 0        # binnen 6 rijen zit ook een top
    lft = np.roll(near, 4, axis=1); rgt = np.roll(near, -4, axis=1)
    flat = tops & lft & rgt                          # buren op ongeveer dezelfde hoogte: vlak genoeg
    # dikte: vlak = dik, steil = niets. Met wat ruis langs de rand.
    n1 = noise2d((H, W), max(6, W // 40), seed)
    thick = tmax * (0.55 + 0.9 * n1)
    thick = np.where(flat, thick, 0)
    # vul omlaag vanaf elke top, tot de dikte op is of we een contour of de lucht raken
    m = np.zeros((H, W), bool)
    budget = np.zeros(W)
    for y in range(H):
        budget = np.where(tops[y], thick[y], budget - 1)
        budget = np.where(~opaque[y], 0, budget)
        m[y] = budget > 0
    m &= ~outer_line
    # losse spikkels weg, randen zacht
    m = blur(m.astype(float), max(1.5, H * 0.003)) > 0.5
    del yidx
    return m


# ---------------------------------------------------------------- de afwerking
def finish(rgb, alpha, lum, opaque, outer_line, snow, roof_tone, ground_snow, frost, seed):
    H, W = snow.shape
    snow = snow & opaque & ~outer_line
    ground_snow = ground_snow & opaque & ~outer_line & ~snow
    m = snow | ground_snow
    mf = m.astype(float)
    # donkere contour vlak onder de sneeuw
    outline = np.zeros((H, W), bool)
    for k in range(1, max(2, int(H * 0.004)) + 1):
        outline |= shift_down(m, k) & ~m
    outline &= opaque
    # blauwe schaduwband onderin elke sneeuwvlek
    s = max(4, int(H * 0.012))
    lower = np.zeros((H, W), bool)
    for k in range(1, s + 1):
        lower |= m & ~shift_up(m, k)
    shade = blur(lower.astype(float), s * 0.5) * mf
    relief = noise2d((H, W), max(5, W // 45), seed + 5)
    col = WHITE[None, None, :] * (0.93 + 0.07 * relief)[..., None]
    # de rietlagen schemeren door: zachte schaduwbanden in het dek
    if roof_tone is not None:
        col = col * (1 - roof_tone[..., None] * 0.55) + SHADE[None, None, :] * (roof_tone[..., None] * 0.55)
    col = col * (1 - shade[..., None] * 0.6) + SHADE[None, None, :] * (shade[..., None] * 0.6)

    # de rest: koud licht, wat bleker
    grey = 0.3 * rgb[..., 0] + 0.55 * rgb[..., 1] + 0.15 * rgb[..., 2]
    cold = rgb * 0.85 + grey[..., None] * 0.15
    cold = np.clip(cold * np.array([0.90, 0.94, 1.06])[None, None, :], 0, 1)
    # bevroren gras: bleek en koel, met rijp op de bovenkant van de sprieten
    pale = np.stack([grey * 1.0, grey * 1.02, grey * 1.08], -1)
    frosty = np.clip((rgb * 0.25 + pale * 0.75) * 1.18, 0, 1)
    out = np.where(frost[..., None], frosty, cold)
    out = np.where((frost & (lum < 0.30))[..., None], rgb * 0.9 + 0.05, out)

    out = np.where(m[..., None], col, out)
    out = np.where(outline[..., None], LINE[None, None, :] * 0.6 + out * 0.4, out)
    out = np.where(outer_line[..., None], rgb, out)
    return out


# ---------------------------------------------------------------- een hut
def hut_snow(src, dst, roof=None, ground_y=None, frost_y=None, gap=0.035, cap=0.02, seed=1, no_cap=None):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    outer_line = dark & dilate(~opaque, max(2, int(H * 0.005)))
    mx, mn, sat = hsv_parts(rgb)
    top = np.where(opaque.any(0), opaque.argmax(0), H).astype(float)

    snow = np.zeros((H, W), bool)
    roof_tone = None
    if roof is not None:
        bot = polyline(roof, W)
        # rafelige onderrand: de rietfranje steekt eronder uit
        n1 = noise2d((1, W), max(6, W // 28), seed + 1)[0]
        n2 = noise2d((1, W), max(3, W // 90), seed + 2)[0]
        edge = bot - gap * H * (0.5 + 1.0 * n1) - gap * H * 0.5 * (n2 - 0.5)
        edge = smooth1d(edge, 2)
        roofm = (ys >= top[None, :]) & (ys < edge[None, :]) & opaque
        roofm = blur(roofm.astype(float), 2.0) > 0.5
        snow |= roofm
        # de toon van het riet eronder, zacht: de lagen worden schaduwbanden
        t = blur(lum, max(2, H * 0.006))
        v = t[roofm]
        lo, hi = np.percentile(v, [5, 90]) if v.size else (0, 1)
        tone = 1 - np.clip((t - lo) / max(hi - lo, 1e-3), 0, 1)
        tone = blur(tone, 1.5) * roofm
        # de lange lijnen tussen de lagen: zachte schaduwlijnen in het dek
        hl = np.clip(box(dark.astype(float), 8, 0) - 0.35, 0, 1) * 2.5
        hl = blur(np.clip(hl, 0, 1), 1.2)
        tone = np.clip(tone * 0.35 + hl * 0.9, 0, 1) * roofm
        roof_tone = tone

    skip = None
    if no_cap is not None:
        skip = np.zeros((H, W), bool)
        for (x0, y0, x1, y1) in no_cap:
            skip[y0:y1, x0:x1] = True
    snow |= local_caps(opaque, dark, outer_line, H, W, tmax=cap * H, slope_k=1.5, seed=seed + 3, skip=skip)

    ground_snow = np.zeros((H, W), bool)
    frost = np.zeros((H, W), bool)
    if ground_y is not None:
        if frost_y is None:
            frost_y = ground_y
        # de grondstrook begint op ground_y (de voet van de muur), met een golvende rand
        wave = ground_y + 10 * (noise2d((1, W), max(8, W // 12), seed + 9)[0] - 0.5)
        band = (ys >= wave[None, :]) & opaque
        hue_t = (rgb[..., 1] - rgb[..., 2]) / np.maximum(rgb[..., 0] - rgb[..., 2], 1e-3)   # 0 = rood, 1 = geel
        # De aarde is gestippeld, dus 'donker' alleen zegt niets. Lange contourlijnen (sprieten,
        # stenen, potten) wel: een donkere pixel op een lijn van 9 in een van vier richtingen.
        lines = long_lines(dark, 9)
        busy = box(lines.astype(float), 5, 5) > 0.04            # rond de lijnen: gras, stenen
        greyish = blur((opaque & (sat < 0.33) & ~dark).astype(float), 3) > 0.4    # stenen
        reddish = blur(((hue_t < 0.43) & (sat > 0.4) & ~dark).astype(float), 3) > 0.3   # potten
        dirt = band & ~busy & ~greyish & ~reddish & (lum > 0.15)
        ground_snow = blur(dirt.astype(float), 4) > 0.45
        ground_snow &= band & ~greyish & ~reddish & ~(box(lines.astype(float), 2, 2) > 0.2)
        ground_snow = blur(ground_snow.astype(float), 1.5) > 0.5
        # bevroren gras: ook de sprieten die boven de grondstrook uitsteken. Gras zit vol
        # lange lijnen dicht op elkaar, de muur erboven niet.
        dense = box(lines.astype(float), 4, 4) > 0.09
        grass = (ys >= frost_y) & opaque & (sat > 0.3) & ~ground_snow & ~dark & ~greyish & ~reddish
        grass &= blur(dense.astype(float), 3) > 0.25
        grass |= band & (sat > 0.3) & ~ground_snow & ~dark
        frost = blur(grass.astype(float), 1.5) > 0.4
    out = finish(rgb, alpha, lum, opaque, outer_line, snow, roof_tone, ground_snow, frost, seed)
    save(out, alpha, dst)


# ---------------------------------------------------------------- boom en struik
def plant_snow(src, dst, cap=0.03, frost_leaves=True, ground_y=None, seed=7):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    outer_line = dark & dilate(~opaque, max(2, int(H * 0.004)))
    mx, mn, sat = hsv_parts(rgb)
    snow = local_caps(opaque, dark, outer_line, H, W, tmax=cap * H, slope_k=1.5, seed=seed)
    frost = np.zeros((H, W), bool)
    if frost_leaves:
        # blad: het verzadigde deel (groen of okergeel), takken en stam zijn grauwbruin
        leaf = opaque & (sat > 0.28) & (rgb[..., 1] >= rgb[..., 2]) & ~dark
        frost = blur(leaf.astype(float), 1.5) > 0.4
        if ground_y is not None:
            frost |= (ys >= ground_y) & opaque & ~dark & (sat > 0.2)
    ground_snow = np.zeros((H, W), bool)
    out = finish(rgb, alpha, lum, opaque, outer_line, snow, None, ground_snow, frost, seed)
    save(out, alpha, dst)


# ---------------------------------------------------------------- de stukken
HUTS = {
    # roof: de onderrand van het rieten dak, als lijn door (x, y)-punten
    "villeaghut":          dict(src="design/villeaghut.png", ground_y=690, frost_y=540,
                                roof=[(0, 400), (60, 435), (200, 440), (440, 450), (700, 445), (840, 435), (895, 400)]),
    "hut_round_arch":      dict(src="design/village/hut_round_arch.png", ground_y=700, frost_y=540,
                                roof=[(0, 380), (60, 445), (250, 462), (450, 470), (650, 465), (840, 445), (905, 380)]),
    "hut_round_door_left": dict(src="design/village/hut_round_door_left.png", ground_y=705, frost_y=540,
                                roof=[(0, 360), (90, 415), (250, 428), (430, 438), (620, 428), (780, 415), (859, 360)]),
    "hut_round_back":      dict(src="design/village/hut_round_back.png", ground_y=765, frost_y=590,
                                roof=[(0, 400), (60, 470), (250, 490), (470, 498), (700, 490), (880, 470), (931, 400)]),
    "hut_rect_porch":      dict(src="design/village/hut_rect_porch.png", ground_y=655, frost_y=500,
                                roof=[(0, 280), (60, 315), (250, 320), (400, 285), (700, 275), (1000, 300), (1258, 350)],
                                no_cap=[(0, 0, 1259, 40)]),
    "hut_rect_back":       dict(src="design/village/hut_rect_back.png", ground_y=640, frost_y=500,
                                roof=[(0, 260), (100, 315), (400, 300), (700, 285), (900, 300), (1157, 320)]),
    "cooking_shelter":     dict(src="design/village/cooking_shelter.png", ground_y=480, frost_y=360,
                                roof=[(0, 150), (60, 170), (200, 165), (500, 160), (800, 165), (950, 170), (1023, 150)]),
    "well":                dict(src="design/village/well.png", ground_y=680, frost_y=490, roof=None, cap=0.03),
}
PLANTS = {
    "tree":   dict(src="design/tree.png",   cap=0.035, ground_y=None),
    "struik": dict(src="design/struik.png", cap=0.025, ground_y=540),
}


def out_path(src):
    base, ext = os.path.splitext(src)
    return os.path.join(ROOT, base + "_sneeuw" + ext)


def main(names):
    for name in names or list(HUTS) + list(PLANTS):
        if name in HUTS:
            p = dict(HUTS[name]); src = os.path.join(ROOT, p.pop("src"))
            hut_snow(src, out_path(os.path.relpath(src, ROOT)), **p)
        elif name in PLANTS:
            p = dict(PLANTS[name]); src = os.path.join(ROOT, p.pop("src"))
            plant_snow(src, out_path(os.path.relpath(src, ROOT)), **p)
        else:
            sys.exit("onbekend stuk: %s (kies uit %s)" % (name, ", ".join(list(HUTS) + list(PLANTS))))


if __name__ == "__main__":
    main(sys.argv[1:])
