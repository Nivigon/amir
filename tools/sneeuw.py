#!/usr/bin/env python3
"""Maakt de sneeuwversies van de rotsen en klimstukken (bestandsnaam met _sneeuw erachter).

    python3 tools/sneeuw.py            # alle zes opnieuw genereren
    python3 tools/sneeuw.py boulder    # alleen die ene

Nodig: pillow en numpy (pip install pillow numpy).

Twee soorten stukken:
- losse rotsen (flatrock, boulder, cliff): een sneeuwkap op de bovenkant van het
  silhouet, tot aan de eerste contourlijn, dunner op steile flanken.
- klimstukken (design/klimmen): het loopvlak wordt bedekt, op wat kale plekken na,
  en een sneeuwrand hangt over de voorrand.

Beide krijgen dezelfde afwerking: dekkend wit met licht reliëf, een blauwe
schaduwband onderin, een donkere contour onder de sneeuw (past bij de lijntekening)
en een lichte koude tint op de rots zelf. De zwarte buitencontour blijft staan.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- hulpjes
def to_img(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L")


def from_img(im):
    return np.asarray(im).astype(float) / 255.0


def blur(arr, r):
    return from_img(to_img(arr).filter(ImageFilter.GaussianBlur(r))) if r > 0 else arr


def box(arr, wx, wy):
    return from_img(to_img(arr).filter(ImageFilter.BoxBlur((wx, wy))))


def dilate(mask, r):
    return box(mask.astype(float), r, r) > 1e-3


def noise2d(shape, scale, seed):
    """zachte ruis: klein random raster, bicubisch opgeschaald"""
    rng = np.random.default_rng(seed)
    h, w = shape
    small = rng.random((max(2, h // scale + 2), max(2, w // scale + 2)))
    return from_img(Image.fromarray((small * 255).astype(np.uint8), "L").resize((w, h), Image.BICUBIC))


def smooth1d(v, k):
    k = max(1, int(k))
    pad = np.pad(v, k, mode="edge")
    return np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="valid")


def median1d(v, k):
    k = max(1, int(k))
    pad = np.pad(v, k, mode="edge")
    return np.median(np.lib.stride_tricks.sliding_window_view(pad, 2 * k + 1), axis=1)


def shift_down(a, k):
    out = np.zeros_like(a)
    out[k:] = a[:-k]
    return out


def shift_up(a, k):
    out = np.zeros_like(a)
    out[:-k] = a[k:]
    return out


def load(src):
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(float) / 255.0
    rgb, alpha = a[..., :3], a[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    opaque = alpha > 0.5
    dark = (lum < 0.30) & opaque
    return rgb, alpha, lum, opaque, dark


def paint(rgb, alpha, opaque, outer_line, mask, seed, dst):
    """de afwerking: sneeuwkleur, schaduwband, contour eronder, koude tint op de rest"""
    H, W = mask.shape
    m = mask & opaque & ~outer_line
    mf = m.astype(float)
    outline = np.zeros((H, W), bool)
    for k in range(1, max(2, int(H * 0.004)) + 1):
        outline |= shift_down(m, k) & ~m
    outline &= opaque
    s = max(4, int(H * 0.012))
    lower = np.zeros((H, W), bool)
    for k in range(1, s + 1):
        lower |= m & ~shift_up(m, k)
    shade = blur(lower.astype(float), s * 0.5) * mf
    relief = noise2d((H, W), max(5, W // 45), seed + 5)

    white = np.array([0.97, 0.98, 1.0])
    shade_c = np.array([0.72, 0.80, 0.93])
    line_c = np.array([0.20, 0.22, 0.30])
    col = white[None, None, :] * (0.93 + 0.07 * relief)[..., None]
    col = col * (1 - shade[..., None] * 0.6) + shade_c[None, None, :] * (shade[..., None] * 0.6)
    out = np.clip(rgb * np.array([0.93, 0.96, 1.04])[None, None, :], 0, 1)   # koude tint
    out = np.where(m[..., None], col, out)
    out = np.where(outline[..., None], line_c[None, None, :] * 0.6 + out * 0.4, out)
    out = np.where(outer_line[..., None], rgb, out)                         # contour blijft
    res = np.concatenate([np.clip(out, 0, 1), alpha[..., None]], -1)
    Image.fromarray((res * 255).round().astype(np.uint8), "RGBA").save(dst)
    print("geschreven:", os.path.relpath(dst, ROOT))


# ---------------------------------------------------------------- losse rotsen
def rock_snow(src, dst, cap_min, cap_max, slope_k, seed=1):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    outer_line = dark & dilate(~opaque, max(2, int(H * 0.006)))

    has = opaque.any(0)
    top = np.where(has, opaque.argmax(0), H).astype(float)
    min_t, max_t = cap_min * H, cap_max * H
    # helling van de bovenrand: steil = weinig sneeuw
    top_s = smooth1d(median1d(top, W / 80), W / 80)
    slope_f = smooth1d(np.clip(1.0 - np.abs(np.gradient(top_s)) / slope_k, 0, 1) ** 1.6, W / 60)
    # tot de eerste contourlijn onder de minimale dikte (zo vult hij een plat bovenvlak)
    below_min = (ys > (top + min_t)[None, :]) & dark & ~outer_line
    stop = np.where(below_min.any(0), below_min.argmax(0), top + max_t)
    thick = np.clip(stop - top, min_t, max_t).astype(float)
    thick = smooth1d(median1d(thick, W / 50), W / 70)
    n1 = noise2d((1, W), max(6, W // 30), seed)[0]
    n2 = noise2d((1, W), max(3, W // 100), seed + 7)[0]
    thick = (thick * (0.8 + 0.3 * n1) + min_t * 0.5 * (n2 - 0.5)) * slope_f
    cap = (ys >= top[None, :]) & (ys < (top + thick)[None, :]) & opaque & (thick[None, :] > 2)
    cap[int(H * 0.72):] = False
    # geen kap op gras: kolommen waarvan de bovenste (niet-donkere) pixels geel/bruin zijn
    sat = (rgb.max(-1) - rgb.min(-1)) / np.maximum(rgb.max(-1), 1e-3)
    band = (ys >= top[None, :]) & (ys < (top + 10)[None, :]) & opaque & (lum > 0.35)
    colsat = np.where(band.sum(0) > 0, (sat * band).sum(0) / np.maximum(band.sum(0), 1), 0)
    cap &= ~(smooth1d((colsat > 0.32).astype(float), 3) > 0.3)[None, :]

    m = blur(cap.astype(float), max(2.0, H * 0.005)) > 0.5
    paint(rgb, alpha, opaque, outer_line, m, seed, dst)


# ---------------------------------------------------------------- klimstukken
def find_rim(lum, opaque, y0, y1):
    """per kolom: de rij met de sterkste overgang licht (loopvlak) -> donker (wand)"""
    above = box(lum, 0, 3)
    step = above - shift_up(above, 7)
    step[~opaque] = -1
    r = y0 + step[y0:y1].argmax(0)
    return smooth1d(median1d(r.astype(float), 9), 3)


def plane_snow(src, dst, rim_win, cover, fringe, top_fn=None, seed=2):
    rgb, alpha, lum, opaque, dark = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    xs = np.arange(W)
    outer_line = dark & dilate(~opaque, 3)

    rim = find_rim(lum, opaque, *rim_win)
    top = np.where(opaque.any(0), opaque.argmax(0), H).astype(float)
    if top_fn is not None:
        top = np.maximum(top, top_fn(xs).astype(float))
    top = np.minimum(top, rim - 2)

    # loopvlak: bedekt, op een paar kale plekken na
    field = 0.7 * noise2d((H, W), max(10, W // 10), seed) + 0.3 * noise2d((H, W), max(4, W // 40), seed + 1)
    plane = (ys >= top[None, :]) & (ys < rim[None, :]) & opaque & (field > cover)
    # vlak bij de voorrand altijd sneeuw, anders hangt de rand nergens aan vast
    plane |= (ys >= (rim - 0.05 * H)[None, :]) & (ys < rim[None, :]) & opaque

    # rand die over de voorkant hangt
    n1 = noise2d((1, W), max(6, W // 25), seed + 3)[0]
    n2 = noise2d((1, W), max(3, W // 90), seed + 4)[0]
    f = np.maximum(fringe * H * (0.6 + 0.8 * n1) + fringe * H * 0.5 * (n2 - 0.5), fringe * H * 0.35)
    fr = (ys >= rim[None, :]) & (ys < (rim + f)[None, :]) & opaque

    m = blur((plane | fr).astype(float), 2.5) > 0.5
    paint(rgb, alpha, opaque, outer_line, m, seed, dst)


# ---------------------------------------------------------------- de stukken
ROCKS = {
    "flatrock": dict(src="design/flatrock.png", cap_min=0.05, cap_max=0.30, slope_k=1.6),
    "boulder":  dict(src="design/boulder.png",  cap_min=0.06, cap_max=0.14, slope_k=2.8),
    "cliff":    dict(src="design/cliff.png",    cap_min=0.025, cap_max=0.06, slope_k=1.6),
}
PLANES = {
    "klif_bovenrand":  dict(src="design/klimmen/klif_bovenrand.png", rim_win=(190, 250), cover=0.14, fringe=0.03),
    "klif_richel":     dict(src="design/klimmen/klif_richel.png",    rim_win=(35, 85),   cover=0.12, fringe=0.045),
    # de vloer begint op rij 628; rechts van x=555 loopt de voet van de wand schuin omlaag
    "klif_binnenhoek": dict(src="design/klimmen/klif_binnenhoek.png", rim_win=(780, 830), cover=0.14, fringe=0.025,
                            top_fn=lambda x: np.where(x < 555, 628, 628 + (x - 555) * (795 - 628) / (815 - 555))),
}


def out_path(src):
    base, ext = os.path.splitext(src)
    return os.path.join(ROOT, base + "_sneeuw" + ext)


def main(names):
    for name in names or list(ROCKS) + list(PLANES):
        if name in ROCKS:
            p = dict(ROCKS[name]); src = os.path.join(ROOT, p.pop("src"))
            rock_snow(src, out_path(os.path.relpath(src, ROOT)), **p)
        elif name in PLANES:
            p = dict(PLANES[name]); src = os.path.join(ROOT, p.pop("src"))
            plane_snow(src, out_path(os.path.relpath(src, ROOT)), **p)
        else:
            sys.exit("onbekend stuk: %s (kies uit %s)" % (name, ", ".join(list(ROCKS) + list(PLANES))))


if __name__ == "__main__":
    main(sys.argv[1:])
