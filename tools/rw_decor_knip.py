#!/usr/bin/env python3
"""Knipt het regenwouddecor uit de Grok-vellen in design/regenwoud/decor/bron/ (elk vel: drie ontwerpen naast elkaar op wit).

Bron (schermafdrukken van de Grok-platen, schaal 0,64): varen_grok.jpg (3037b1e0, reuzenblad), kei_grok.jpg (41bb7e62),
      stronk_grok.jpg (cb316a15, boomvoet), beeld_grok.jpg (d211acc6, leeuwenschrijn), zwam_grok.jpg (ae349c54, paddenstoelen)
Uit:  design/regenwoud/decor/<naam>_1.png .. _3.png, van links naar rechts. De maten staan in PROPS (rw_<naam>_<i>).

    python3 tools/rw_decor_knip.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist Pillow, numpy en scipy.
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'regenwoud', 'decor')
NAMEN = ['varen', 'kei', 'stronk', 'beeld', 'zwam']
def knip(src, uitprefix, n=3, drempel=232, minpx=4000, gat=12):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
    lum = im.min(axis=2)
    wit = lum > drempel
    lab, k = nd.label(wit)
    rand = set(np.unique(np.r_[lab[0], lab[-1], lab[:,0], lab[:,-1]])) - {0}
    bg = np.isin(lab, list(rand))
    # ingesloten gaten: groot en heel wit
    hard = lum > 236
    lh, kh = nd.label(hard)
    groot = np.bincount(lh.ravel()); groot[0] = 0
    bg |= np.isin(lh, np.where(groot > gat)[0])
    witachtig = (lum > 226) & ((im.max(axis=2) - lum) < 22)
    bg |= witachtig & nd.binary_dilation(bg, iterations=3)
    vg = ~bg
    vg = nd.binary_opening(vg, iterations=1)
    # zachte alfa aan de rand: afstand tot achtergrond
    alfa = np.clip(nd.distance_transform_edt(vg) / 1.6, 0, 1)
    # ontwit de randpixels (despill wit): kleur = (c - (1-a')*255)/a' met a' uit witheid
    # randpixels: witte waas eruit, iets donkerder zodat de rand op een donkere grond niet licht oplicht
    randz = (alfa < 1) | (nd.distance_transform_edt(vg) < 3)
    im2 = im.copy(); im2[randz] *= 0.55
    rgba = np.dstack([im2, alfa * 255]).astype(np.uint8)
    # objecten
    lab2, k2 = nd.label(nd.binary_dilation(vg, iterations=12))
    objs = []
    for sl, i in zip(nd.find_objects(lab2), range(1, k2 + 1)):
        if (lab2[sl] == i).sum() < minpx: continue
        objs.append((sl[1].start, sl, i))
    objs.sort()
    if len(objs) < n:
        # objecten raken elkaar: splitsen op de dunste kolommen
        kol = vg.sum(axis=0).astype(float)
        xs = np.where(kol > 0)[0]; x0, x1 = xs.min(), xs.max()
        sm = np.convolve(kol, np.ones(15) / 15, 'same')
        w = x1 - x0; snedes = []
        for j in range(1, n):
            mid = x0 + w * j / n; lo, hi = int(mid - w * 0.12), int(mid + w * 0.12)
            snedes.append(lo + int(np.argmin(sm[lo:hi])))
        grenzen = [x0] + snedes + [x1 + 1]
        lab2 = np.zeros(vg.shape, int)
        for j in range(n): lab2[:, grenzen[j]:grenzen[j+1]] = j + 1
        objs = [(grenzen[j], None, j + 1) for j in range(n)]
    uit = []
    for j, (x0, sl, i) in enumerate(objs):
        m = (lab2 == i) & vg
        a = rgba.copy(); a[..., 3] = np.where(m, a[..., 3], 0)
        ys, xs = np.where(m)
        crop = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
        p = f'{uitprefix}_{j+1}.png'; Image.fromarray(crop).save(p); uit.append((p, crop.shape[1], crop.shape[0]))
    return uit


if __name__ == '__main__':
    for n in NAMEN:
        for u in knip(os.path.join(MAP, 'bron', n + '_grok.jpg'), os.path.join(MAP, n)):
            print(os.path.relpath(u[0], ROOT), u[1], 'x', u[2])
