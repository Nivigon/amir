#!/usr/bin/env python3
"""De rotsen met richels van de savanne (KOPJE in de HTML): knippen uit de Grok-platen.

Bron (design/savanne/rotsen/bron/):
- rotsvormen.png: drie rotsen naast elkaar op wit (Grok 4f43b1c2): het kopje, de tafelrots en de gespleten rots.
- wandrichel.png: een rotswand met een diepe richel ervoor (Grok 82f58dbf). Alleen de richel wordt gebruikt:
  het bovenvlak heeft de diepte van de galerij, zodat Amir erin staat zoals op de galerij.

Uit (design/savanne/rotsen/):
- kopje.png, tafelrots.png, spleetrots.png: wit weg, warm gemaakt zoals de andere rotsen (rots_warm.py).
- richel_eind.png, richel_midden.png, richel_eind_r.png: de richel in drie stukken. Het spel legt ze aan elkaar tot
  elke lengte: het eind, het midden zo vaak als nodig (met een zachte overgang die al in de plaat zit, de eerste
  OV px lopen van doorzichtig naar vol) en het gespiegelde eind. Bovenop een lichte rand op het loopvlak.
Daarna: python3 tools/gen-offline-manifest.py
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'design/savanne/rotsen')
src = open(os.path.join(ROOT, 'tools/rots_warm.py')).read().split('\nfor basis')[0]
rw = {'__file__': os.path.join(ROOT, 'tools/rots_warm.py')}; exec(src, rw)   # alleen de functie warm(), zonder de lus

def witweg(im):
    a = np.array(im.convert('RGB')).astype(int); bgc = (255 - a).max(axis=2) <= 20
    lab, n = ndimage.label(bgc); sz = ndimage.sum(bgc, lab, range(1, n + 1)); bg = np.zeros_like(bgc)
    for i, s in enumerate(sz):
        if s >= 300: bg |= lab == i + 1
    return ~bg

OV = 60
im = Image.open(os.path.join(D, 'bron/rotsvormen.png')).convert('RGB')
fg = witweg(im); ol, on = ndimage.label(fg); sz = ndimage.sum(fg, ol, range(1, on + 1)); objs = ndimage.find_objects(ol)
groot = sorted((objs[i][1].start, i + 1) for i, s in enumerate(sz) if s > 20000)
for naam, (_, i) in zip(['kopje', 'tafelrots', 'spleetrots'], groot):
    m = Image.fromarray(((ol == i) * 255).astype('uint8')).filter(ImageFilter.MinFilter(3))
    p = im.convert('RGBA'); p.putalpha(m); p = p.crop(m.getbbox())
    tmp = os.path.join(D, naam + '_tmp.png'); p.save(tmp)
    rw['warm'](tmp, os.path.join(D, naam + '.png'), rand=True); os.remove(tmp)

w = Image.open(os.path.join(D, 'bron/wandrichel.png')).convert('RGB')
m = Image.fromarray((witweg(w) * 255).astype('uint8')).filter(ImageFilter.MinFilter(3))
w = w.convert('RGBA'); w.putalpha(m); w = w.crop(m.getbbox())
tmp = os.path.join(D, 'wand_tmp.png'); w.save(tmp); rw['warm'](tmp, tmp, rand=False)
S = Image.open(tmp).crop((0, 428, 1757, 543)); os.remove(tmp)    # bovenvlak en voorkant van de richel, zonder de wand
a = np.array(S).astype(float); h = a.shape[0]
rng = np.random.default_rng(3)
rand = (h - 6 + np.convolve(rng.normal(0, 3, a.shape[1]), np.ones(25) / 25, 'same')).astype(int)
for x in range(a.shape[1]): a[rand[x]:, x, 3] = 0                   # een grillige onderkant
for y in range(2, 40):                                               # de lichte rand op het loopvlak
    t = max(0, 1 - (y - 2) / 38) ** 1.2 * 0.36
    a[y, :, :3] = a[y, :, :3] * (1 - t) + np.array([236, 214, 178]) * t
S = Image.fromarray(a.clip(0, 255).astype('uint8'))
def fade(img):
    b = np.array(img).astype(float); f = np.ones(b.shape[1]); f[:OV] = np.linspace(0, 1, OV); b[..., 3] *= f[None, :]
    return Image.fromarray(b.astype('uint8'))
E_ = S.crop((0, 0, 260, h))
E_.save(os.path.join(D, 'richel_eind.png'))
fade(S.crop((500, 0, 1100, h))).save(os.path.join(D, 'richel_midden.png'))
fade(ImageOps.mirror(E_)).save(os.path.join(D, 'richel_eind_r.png'))
for f in sorted(os.listdir(D)):
    if f.endswith('.png'): print(f, Image.open(os.path.join(D, f)).size)
