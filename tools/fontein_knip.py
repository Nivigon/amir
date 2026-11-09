#!/usr/bin/env python3
"""Maakt de fontein voor het plein uit de Grok-plaat in design/stad/bron/.

Bron: fontein.webp, een droge fontein van leem (bassin, zuil, schaal) op een doorzichtige achtergrond.
Uit:  design/stad/fontein.png, bijgesneden, met de witte randpixels van Grok in de kleur van het leem ernaast.

Het water tekent het spel er zelf in (zie "de fontein" in notities/water.md); de maten waar dat komt
(de binnenkant van het bassin, de zuil, de schaal) staan in STAD.plein.fontein, in pixels van fontein.png.

    python3 tools/fontein_knip.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist Pillow, numpy en scipy.
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'design', 'stad', 'bron', 'fontein.webp')
UIT = os.path.join(ROOT, 'design', 'stad', 'fontein.png')
WIT = 205                         # zo licht (in elk kanaal) is wit dat aan de achtergrond vastzit
RAND = 2                          # zo breed (px) is de strook langs de rand die de kleur van binnen krijgt

bron = np.array(Image.open(BRON).convert('RGBA')).astype(float)
rgb, alpha = bron[..., :3], bron[..., 3]
leeg = alpha < 8
# Grok liet aan de rechterkant een strook wit staan: wit dat aan de lege achtergrond vastzit gaat ook weg
wit = rgb.min(axis=-1) > WIT
lab, _ = nd.label(wit | leeg)
leeg = leeg | np.isin(lab, np.unique(lab[leeg]))
buurt = nd.binary_dilation(leeg, iterations=RAND)
rand = (~leeg) & ((alpha < 255) | buurt)
kern = (~leeg) & ~rand
_, (iy, ix) = nd.distance_transform_edt(~kern, return_indices=True)
rgb = np.where(rand[..., None], rgb[iy, ix], rgb)
alpha = np.where(rand & (alpha >= 255), 200, alpha)
alpha[leeg] = 0
img = Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), 'RGBA')
box = img.getbbox()
img = img.crop(box)
img.save(UIT, optimize=True)
print('fontein.png', img.size, 'bijgesneden op', box)
