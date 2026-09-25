#!/usr/bin/env python3
"""Maakt de gekleurde slangen uit de twee originele spritesets.

    python3 tools/slang_kleur.py           # allebei opnieuw genereren
    python3 tools/slang_kleur.py zand      # alleen de zandslang

Uit enemies/slang1/ (geel met groene zadels) komt enemies/slang1_zand/: een
zandslang in de kleur van de savannebodem, bleek zand met roestbruine zadels.
Uit enemies/slang2/ (zwart met felrode zadels) komt enemies/slang2_roet/: dezelfde
slang met leisteengrijze zadels, dus zwart op zwart in plaats van rood.

De tekening zelf blijft staan. Per kleurvlak wordt alleen de tint en de
verzadiging vervangen en de helderheid over een nieuw bereik uitgesmeerd, dus
de schubben, de schaduwen en de contour blijven precies zoals ze getekend zijn.

Twee dingen blijven met opzet hun eigen kleur houden:
- het amberen oog van de zandslang (anders wordt hij bleek en kijkt hij dood);
- het vlees in de muil van de zwarte (tong en keel blijven rozerood).

De originelen in enemies/slang1/ en enemies/slang2/ blijven staan: die zijn de
bron. Verandert er een frame, draai dit script dan opnieuw, en daarna
tools/gen-offline-manifest.py.

Nodig: pillow en numpy (pip install pillow numpy).
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = [f"{groep}_{n}.png" for groep in ("idle", "move", "attack") for n in range(1, 9)]


# ---------------------------------------------------------------- kleurruimte
def naar_hsv(rgb):
    """rgb 0..255 -> tint in graden, verzadiging 0..1, helderheid 0..1"""
    r, g, b = rgb[..., 0] / 255.0, rgb[..., 1] / 255.0, rgb[..., 2] / 255.0
    mx, mn = np.max(rgb, axis=-1) / 255.0, np.min(rgb, axis=-1) / 255.0
    d = mx - mn
    h = np.zeros_like(mx)
    raak = d > 1e-6
    i = raak & (mx == r)
    h[i] = ((g - b)[i] / d[i]) % 6
    i = raak & (mx == g) & (mx != r)
    h[i] = ((b - r)[i] / d[i]) + 2
    i = raak & (mx == b) & (mx != r) & (mx != g)
    h[i] = ((r - g)[i] / d[i]) + 4
    return h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx


def naar_rgb(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - np.abs((h / 60) % 2 - 1))
    m = v - c
    nul = np.zeros_like(h)
    deel = (h // 60).astype(int)
    keuze = [deel == k for k in range(6)]
    r = np.select(keuze, [c, x, nul, nul, x, c])
    g = np.select(keuze, [x, c, c, x, nul, nul])
    b = np.select(keuze, [nul, nul, x, c, c, x])
    return np.clip(np.stack([r + m, g + m, b + m], axis=-1) * 255, 0, 255)


def hertint(rgb, masker, tint, verz, laag, hoog, gamma=1.0):
    """Zet een kleurvlak om: nieuwe tint en verzadiging, helderheid uitgesmeerd
    over laag..hoog. Het verloop binnen het vlak blijft, dus de schubben ook."""
    h, s, v = naar_hsv(rgb)
    if not masker.any():
        return rgb
    onder, boven = np.percentile(v[masker], 2), np.percentile(v[masker], 98)
    genormeerd = np.clip((v - onder) / max(boven - onder, 1e-6), 0, 1) ** gamma
    nieuw = naar_rgb(np.full(h.shape, float(tint)),
                     np.full(s.shape, float(verz)),
                     laag + genormeerd * (hoog - laag))
    uit = rgb.copy()
    uit[masker] = nieuw[masker]
    return uit


# ---------------------------------------------------------------- vormpjes
def groei(masker, r=1):
    uit = masker.copy()
    for _ in range(r):
        o = uit.copy()
        o[1:] |= uit[:-1]
        o[:-1] |= uit[1:]
        o[:, 1:] |= uit[:, :-1]
        o[:, :-1] |= uit[:, 1:]
        uit = o
    return uit


def vlakken(masker):
    """samenhangende vlakken nummeren, inclusief de schuine buren"""
    nummer = np.zeros(masker.shape, int)
    hoogte, breedte = masker.shape
    n = 0
    for y in range(hoogte):
        for x in range(breedte):
            if masker[y, x] and nummer[y, x] == 0:
                n += 1
                stapel = [(y, x)]
                nummer[y, x] = n
                while stapel:
                    cy, cx = stapel.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < hoogte and 0 <= nx < breedte and masker[ny, nx] and nummer[ny, nx] == 0:
                                nummer[ny, nx] = n
                                stapel.append((ny, nx))
    return nummer, n


# ---------------------------------------------------------------- de zandslang
def iris(rgb, zichtbaar, geel):
    """Het oog opzoeken: de pupil is een kleine donkere spleet die in het geel
    ligt, en de iris is het gele rondje eromheen tot aan de zwarte oogrand.
    Zonder dit wordt het oog net zo bleek als de rest van de kop."""
    _, _, v = naar_hsv(rgb)
    donker = zichtbaar & (v < 0.22)
    nummer, n = vlakken(donker)
    pupil, beste = None, 0.0
    for i in range(1, n + 1):
        m = nummer == i
        aantal = int(m.sum())
        if aantal < 4 or aantal > 120:            # te klein is ruis, te groot is de contour
            continue
        rand = groei(m, 2) & ~m
        score = (rand & geel).sum() / max(rand.sum(), 1)   # ligt hij midden in het geel?
        if score > 0.55 and aantal * score > beste:
            pupil, beste = m, aantal * score
    if pupil is None:
        return np.zeros(geel.shape, bool)
    ys, xs = np.where(pupil)
    hoog = ys.max() - ys.min() + 1
    mx, my = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
    straal = min(10.0, max(4.0, 0.55 * hoog))
    Y, X = np.mgrid[0:geel.shape[0], 0:geel.shape[1]]
    rondje = ((X - mx) ** 2 + (Y - my) ** 2) <= straal * straal
    # vanaf de pupil naar buiten lopen, maar alleen door helder geel: de zwarte
    # oogrand houdt het tegen, dus de kopschubben erachter blijven buiten beeld
    door = rondje & geel & (v > 0.35)
    gevonden = groei(pupil, 1) & door
    rij = deque(zip(*np.where(gevonden)))
    while rij:
        y, x = rij.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < geel.shape[0] and 0 <= nx < geel.shape[1] and door[ny, nx] and not gevonden[ny, nx]:
                gevonden[ny, nx] = True
                rij.append((ny, nx))
    return (groei(gevonden, 1) & geel & rondje) | (pupil & rondje)


def zandslang(beeld):
    arr = np.array(beeld.convert("RGBA")).astype(float)
    rgb = arr[..., :3]
    h, s, _ = naar_hsv(rgb)
    zichtbaar = arr[..., 3] > 128
    geel = zichtbaar & (s > 0.25) & (h >= 25) & (h < 72)     # het lijf
    groen = zichtbaar & (s > 0.25) & (h >= 72) & (h < 150)   # de zadels
    oog = iris(rgb, zichtbaar, geel)
    rgb = hertint(rgb, geel & ~oog, tint=27, verz=0.40, laag=0.52, hoog=0.97, gamma=0.95)
    rgb = hertint(rgb, groen, tint=13, verz=0.68, laag=0.30, hoog=0.58)
    arr[..., :3] = rgb
    return Image.fromarray(arr.astype(np.uint8))


# ---------------------------------------------------------------- de roetslang
def roetslang(beeld):
    arr = np.array(beeld.convert("RGBA")).astype(float)
    rgb = arr[..., :3]
    h, s, v = naar_hsv(rgb)
    zichtbaar = arr[..., 3] > 128
    rood = zichtbaar & (s > 0.45) & (v > 0.33) & ((h < 40) | (h > 330))
    # De zadels zijn zuiver rood (verzadiging bijna 1), het vlees in de muil is
    # rozig (rond 0,7). Per vlak kijken welk van de twee het is, anders krijgt
    # hij een grijze tong.
    nummer, n = vlakken(rood)
    zadels = np.zeros(rood.shape, bool)
    for i in range(1, n + 1):
        m = nummer == i
        if s[m].mean() >= 0.90:
            zadels |= m
    lijf = zichtbaar & (v <= 0.33) & ((h < 60) | (h > 300))
    rgb = hertint(rgb, zadels, tint=28, verz=0.22, laag=0.24, hoog=0.46)
    rgb = hertint(rgb, lijf, tint=25, verz=0.28, laag=0.05, hoog=0.20)
    arr[..., :3] = rgb
    return Image.fromarray(arr.astype(np.uint8))


SETS = {
    "zand": ("enemies/slang1", "enemies/slang1_zand", zandslang),
    "roet": ("enemies/slang2", "enemies/slang2_roet", roetslang),
}


def main():
    namen = sys.argv[1:] or list(SETS)
    for naam in namen:
        if naam not in SETS:
            print(f"onbekend: {naam} (kies uit {', '.join(SETS)})")
            continue
        bron, doel, maak = SETS[naam]
        os.makedirs(os.path.join(ROOT, doel), exist_ok=True)
        for frame in FRAMES:
            pad = os.path.join(ROOT, bron, frame)
            if not os.path.exists(pad):
                print(f"ontbreekt: {bron}/{frame}")
                continue
            maak(Image.open(pad)).save(os.path.join(ROOT, doel, frame))
        print(f"{doel}/: {len(FRAMES)} frames")


if __name__ == "__main__":
    main()
