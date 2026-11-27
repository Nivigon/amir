"""Knipt de drie graanschuren van het savannedorp uit de Grok-plaat (ae35351f).

Bron: design/savanne/graanschuren/bron/grok_ae35351f.png (2448x816, wit).
Uit:  design/savanne/graanschuren/graanschuur_{rond,ladder,mand}.png

Wit dat aan de rand vastzit is achtergrond, en een wit gat van 300 px of meer ook
(tussen de poten van de vlonder). Daarna de rand een pixel ingeknabbeld.
Draaien na een nieuwe plaat, daarna tools/gen-offline-manifest.py.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HIER = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HIER, '..', 'design', 'savanne', 'graanschuren')
BRON = os.path.join(MAP, 'bron', 'grok_ae35351f.png')
NAMEN = ['rond', 'ladder', 'mand']   # van links naar rechts

im = Image.open(BRON).convert('RGB')
a = np.asarray(im).astype(int)
wit = (a.min(axis=2) > 225) & (a.max(axis=2) - a.min(axis=2) < 18)
lab, n = ndimage.label(wit)
weg = np.zeros_like(wit)
groot = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
for i, g in enumerate(groot, 1):
    if i in rand or g >= 300:
        weg |= lab == i
alpha = np.where(weg, 0, 255).astype(np.uint8)
alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)))

# losse voorwerpen: kolommen zonder dekking scheiden ze
vol = (alpha > 0).sum(axis=0) > 3
stukken, k = ndimage.label(vol)
delen = sorted(ndimage.find_objects(stukken), key=lambda s: -(s[0].stop - s[0].start))[:3]
delen = sorted(delen, key=lambda s: s[0].start)
rgba = np.dstack([a.astype(np.uint8), alpha])
for naam, (sx,) in zip(NAMEN, delen):
    stuk = rgba[:, sx.start:sx.stop]
    rijen = np.where(stuk[:, :, 3].max(axis=1) > 0)[0]
    stuk = stuk[rijen[0]:rijen[-1] + 1]
    uit = os.path.join(MAP, f'graanschuur_{naam}.png')
    Image.fromarray(stuk).save(uit)
    h, w = stuk.shape[:2]
    print(f'{naam}: {w}x{h}  r={w / h:.2f}')
