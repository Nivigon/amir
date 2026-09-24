#!/usr/bin/env python3
"""Maakt de winterversies van de achtergrondpanelen (bestandsnaam met _sneeuw erachter).

    python3 tools/sneeuw_bg.py              # alle twaalf panelen
    python3 tools/sneeuw_bg.py midden_4     # alleen dat paneel

Nodig: pillow en numpy (pip install pillow numpy).

Twee lagen, twee recepten:
- design/bg/laag1 (verre bergen): een sneeuwgrens. Boven in het paneel liggen de
  toppen wit, naar beneden toe loopt de sneeuw uit; zonkanten (licht) houden meer
  sneeuw dan schaduwkanten (donker), zodat de rotsribbels erdoorheen blijven staan.
- design/bg/laag2 (heuvelrij met acacia's): sneeuw op de ruggen en kruinen (per kolom
  vanaf de bovenrand een laag die met ruis uitdunt) en een dek over de hele vlakte,
  met de grondtextuur als reliëf en kale plekken waar de wind hem wegneemt. Donkere
  details (stammen, stenen, struiken, schaduw) steken erdoorheen.

Beide worden meteen koud gezet (kleur eruit, iets lichter, blauwige schaduwen), zodat
het paneel ook goed staat in browsers zonder canvas-filters (Safari op iOS).
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sneeuw import blur, noise2d, smooth1d, median1d  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SNOW = np.array([0.965, 0.975, 1.0])
SHADE = np.array([0.78, 0.84, 0.94])       # sneeuw in de schaduw: blauwig


def load(src):
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(float) / 255.0
    rgb, alpha = a[..., :3], a[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    return rgb, alpha, lum


def cold(rgb, lum):
    """kleur eruit, iets lichter, koele tint: de winterse rots en grond"""
    gray = lum[..., None]
    out = rgb * 0.18 + gray * 0.82
    out = out * np.array([0.90, 0.95, 1.06])[None, None, :]
    out = 0.12 + out * 0.95                        # iets lichter, nooit pikzwart
    return np.clip(out, 0, 1)


def finish(rgb, alpha, lum, cover, seed, dst):
    """cover 0..1 per pixel: zoveel sneeuw ligt er. Reliëf uit de oorspronkelijke helderheid."""
    H, W = lum.shape
    relief = noise2d((H, W), max(6, W // 60), seed + 11)
    lit = np.clip((lum - 0.25) / 0.5, 0, 1)        # zonkant 1, schaduwkant 0
    snow_c = SHADE[None, None, :] + (SNOW - SHADE)[None, None, :] * (0.35 + 0.65 * lit)[..., None]
    snow_c = snow_c * (0.95 + 0.05 * relief)[..., None]
    base = cold(rgb, lum)
    out = base * (1 - cover[..., None]) + snow_c * cover[..., None]
    res = np.concatenate([np.clip(out, 0, 1), alpha[..., None]], -1)
    Image.fromarray((res * 255).round().astype(np.uint8), "RGBA").save(dst, optimize=True)
    print("geschreven:", os.path.relpath(dst, ROOT))


def top_of(alpha):
    opaque = alpha > 0.5
    H = alpha.shape[0]
    has = opaque.any(0)
    return np.where(has, opaque.argmax(0), H).astype(float), opaque


# ---------------------------------------------------------------- verre bergen
def mountain_snow(src, dst, depth, seed):
    rgb, alpha, lum = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    top, opaque = top_of(alpha)
    top_s = smooth1d(median1d(top, W / 60), W / 40)
    # hoogte in het paneel: 1 op de kam, 0 op 'depth' van de hoogte eronder
    span = np.maximum((H - top_s) * depth, 4)
    hgt = np.clip(1 - (ys - top_s[None, :]) / span[None, :], 0, 1)
    n = noise2d((H, W), max(12, W // 24), seed) * 0.6 + noise2d((H, W), max(4, W // 90), seed + 1) * 0.4
    line = np.clip((hgt - 0.35 + (n - 0.5) * 0.5) / 0.35, 0, 1)        # de sneeuwgrens, rafelig
    lit = np.clip((lum - 0.22) / 0.45, 0, 1)
    cover = line * (0.35 + 0.65 * lit) * opaque
    cover = np.maximum(cover, (ys < (top_s + 0.06 * H)[None, :]) * opaque * 0.85 * (0.5 + 0.5 * lit))   # de kam zelf altijd wit
    cover = blur(cover, 1.2) * opaque
    finish(rgb, alpha, lum, np.clip(cover, 0, 1), seed, dst)


# ---------------------------------------------------------------- heuvelrij
def hill_snow(src, dst, ridge, dust, seed):
    rgb, alpha, lum = load(src)
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    top, opaque = top_of(alpha)
    # laag op de rug: dikte met ruis, per kolom vanaf de bovenrand (bomen incluis: sneeuw op de kruinen)
    n1 = noise2d((1, W), max(8, W // 20), seed)[0]
    n2 = noise2d((1, W), max(3, W // 120), seed + 3)[0]
    thick = ridge * H * (0.65 + 0.7 * n1 + 0.3 * (n2 - 0.5))
    band = np.clip(1 - (ys - top[None, :]) / np.maximum(thick, 2)[None, :], 0, 1) ** 0.7
    # de vlakte zelf ligt onder een dek: de grondtextuur blijft als reliëf zichtbaar, met kale
    # plekken waar de wind de sneeuw wegneemt, en dikker op de lichte (zon)kant
    n3 = noise2d((H, W), max(10, W // 30), seed + 5) * 0.65 + noise2d((H, W), max(4, W // 100), seed + 6) * 0.35
    lit = np.clip((lum - 0.28) / 0.40, 0, 1)
    field = dust * (0.55 + 0.45 * n3) * (0.7 + 0.3 * lit)
    dark = np.clip((0.27 - lum) / 0.10, 0, 1)                             # stammen, stenen, struiken, schaduw: steken erdoorheen
    cover = np.maximum(band * (0.6 + 0.4 * lit), field) * (1 - dark) * opaque
    cover = blur(cover, 1.0) * opaque
    finish(rgb, alpha, lum, np.clip(cover, 0, 1), seed, dst)


# ---------------------------------------------------------------- de panelen
MOUNTAINS = {
    "verre_bergen_1_kilimanjaro": dict(depth=0.55, seed=21),
    "verre_bergen_2_ruggen":      dict(depth=0.50, seed=22),
    "verre_bergen_3_tafelberg":   dict(depth=0.45, seed=23),
    "verre_bergen_4_breuklijn":   dict(depth=0.45, seed=24),
    "verre_bergen_5_dubbeltop":   dict(depth=0.55, seed=25),
    "verre_bergen_6_kegels":      dict(depth=0.50, seed=26),
}
HILLS = {
    # dust = hoe dik het dek op de vlakte ligt (0..1)
    "midden_1": dict(ridge=0.16, dust=0.82, seed=31),
    "midden_2": dict(ridge=0.14, dust=0.82, seed=32),
    "midden_3": dict(ridge=0.18, dust=0.78, seed=33),
    "midden_4": dict(ridge=0.15, dust=0.82, seed=34),
    "midden_5": dict(ridge=0.14, dust=0.82, seed=35),
    "midden_6": dict(ridge=0.14, dust=0.78, seed=36),
}


def main(names):
    for name in names or list(MOUNTAINS) + list(HILLS):
        if name in MOUNTAINS:
            src = os.path.join(ROOT, "design/bg/laag1", name + ".png")
            mountain_snow(src, src[:-4] + "_sneeuw.png", **MOUNTAINS[name])
        elif name in HILLS:
            src = os.path.join(ROOT, "design/bg/laag2", name + ".png")
            hill_snow(src, src[:-4] + "_sneeuw.png", **HILLS[name])
        else:
            sys.exit("onbekend paneel: %s" % name)


if __name__ == "__main__":
    main(sys.argv[1:])
