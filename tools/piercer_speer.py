#!/usr/bin/env python3
"""De Shield Piercer: de speer met de ijzeren knol, uit de winkel van Co-op.

Uit de Grok-plaat in design/speer/piercer/bron/speer.png (al uitgeknipt, op doorzichtig, punt links, in de
oorspronkelijke kleuren: grijs ijzer, bruin hout, oker en witte banden). Het script
  1. zoekt de vier vlakken (ijzer, schacht, oker banden en ringen, witte banden) op kleur, met de donkere omlijning apart;
  2. kleurt ze om (op verzoek, 23-11-2026): zwart staal met een blauwe glans voor punt en knol, een donkerbruine
     schacht, de oker banden en ringen zwart en de witte banden gebroken wit (zwart/wit);
  3. bouwt jav.png even lang als de gewone speer (624 px, punt rechts, op een doek van 624 bij 69 zoals de Pathfinder,
     de punt op y 34,5); de dop en de kop houden hun vorm, het hout rekt mee;
  4. schrijft de speer in Amirs hand per hoek, net als de Pathfinder (karakters/amir/mkuki_spel/bron/sp_<hoek>.png):
     proj, de korte hoeken k30..k90 (geknepen) en de lange l110..l180 (het hout langer). Zelfde doekmaat, dus de
     maten van de Pathfinder in los.json (pf) gelden ook voor deze.

  python3 tools/piercer_speer.py
daarna tools/gen-offline-manifest.py.
"""
import os
import numpy as np
from PIL import Image
from matplotlib import colors as mc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design/speer/piercer')
HAND = os.path.join(ROOT, 'karakters/amir/mkuki_spel/bron')
KS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
LS = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
JAV_W, JAV_H, TIP_Y = 624, 69, 34.5
SCHACHT, BRON_DIK = 19, 85        # de dikte van de schacht in jav.png, en in de bron
DOP, HOUT = 177, 557              # punt rechts: de dop tot DOP, het hout tot HOUT, daarna strepen, kraag, knol en naald

STAAL = ('#16181c', '#6d87a8')    # zwart staal en zijn blauwe glans
KLEUR = {'wood': '#4e2f1c', 'gold': '#22201f', 'cream': '#e2d8c6'}

hx = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255

def zones(im):
    a = np.array(im).astype(float)
    hsv = mc.rgb_to_hsv(a[..., :3] / 255); H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    op = a[..., 3] > 0
    lijn = op & (V < 0.2)
    ijzer = op & ~lijn & (S < 0.18) & (V < 0.62)
    room = op & ~lijn & (S < 0.3) & (V >= 0.55) & ~ijzer
    warm = op & ~lijn & ~ijzer & ~room
    from scipy import ndimage
    oker = ndimage.median_filter((warm & ((H > 0.088) | (V > 0.7))).astype(np.uint8), 5).astype(bool) & warm
    return {'iron': ijzer, 'cream': room, 'gold': oker, 'wood': warm & ~oker}, V, a

def kleur(im):
    Z, V, a = zones(im)
    rgb = a[..., :3] / 255
    med = {k: np.median(V[m]) for k, m in Z.items()}
    r = V[Z['iron']] / med['iron']
    t = np.clip((r - 0.95) / 0.35, 0, 1)[:, None]
    rgb[Z['iron']] = np.clip(hx(STAAL[0]) * np.clip(r, 0.6, 1.0)[:, None] * (1 - t) + hx(STAAL[1]) * t, 0, 1)
    for k, c in KLEUR.items():
        m = Z[k]; rgb[m] = np.clip(hx(c) * (V[m] / med[k])[:, None], 0, 1)
    return Image.fromarray(np.dstack([rgb * 255, a[..., 3]]).astype(np.uint8), 'RGBA')

def bouw(sp, totaal):
    s = SCHACHT / BRON_DIK; H = round(sp.height * s)
    st = lambda x0, x1, w=None: sp.crop((x0, 0, x1, sp.height)).resize((w or max(1, round((x1 - x0) * s)), H), Image.LANCZOS)
    a, c = st(0, DOP), st(HOUT, sp.width)
    b = st(DOP, HOUT, max(4, totaal - a.width - c.width))
    im = Image.new('RGBA', (a.width + b.width + c.width, H)); x = 0
    for d in (a, b, c): im.alpha_composite(d, (x, 0)); x += d.width
    return im

def rand(im):        # een harde donkere lijn om het silhouet en een zachte schaduw eronder, zoals de gewone speer
    a = np.array(im).astype(np.int32); m = a[..., 3] > 110
    p = np.pad(m, 1); binnen = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    uit = np.zeros_like(a); uit[m] = a[m]; uit[m, 3] = 255; uit[m & ~binnen, :3] = (30, 24, 20)
    for x in range(a.shape[1]):
        ys = np.where(m[:, x])[0]
        if len(ys) and ys[-1] + 1 < a.shape[0]: uit[ys[-1] + 1, x] = (0, 0, 0, 120)
    return Image.fromarray(uit.astype(np.uint8), 'RGBA')

def doek(im, w):
    c = Image.new('RGBA', (w, JAV_H)); c.alpha_composite(im, (w - im.width, round(TIP_Y - im.height / 2))); return c

bron = Image.open(os.path.join(MAP, 'bron/speer.png')).convert('RGBA')
sp = kleur(bron).transpose(Image.FLIP_LEFT_RIGHT)
jav = doek(rand(bouw(sp, JAV_W)), JAV_W)
jav.save(os.path.join(MAP, 'jav.png'), optimize=True)
jav.save(os.path.join(HAND, 'sp_proj.png'), optimize=True)
for k in KS:
    jav.resize((round(JAV_W * k), JAV_H), Image.LANCZOS).save(os.path.join(HAND, 'sp_k%02d.png' % round(k * 100)), optimize=True)
for f in LS:
    w = round(JAV_W * f); doek(rand(bouw(sp, w)), w).save(os.path.join(HAND, 'sp_l%03d.png' % round(f * 100)), optimize=True)
print('jav.png', jav.size, 'en', 1 + len(KS) + len(LS), 'hoeken in de hand')
