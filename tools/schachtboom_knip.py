#!/usr/bin/env python3
"""Maakt de schachtboom van het regenwoud (SCHACHTBOOM) uit de Grok-platen in design/regenwoud/schachtboom/bron/.

Bron: boom_grok.png    de reuzenboom met de holte in zijn voet, doorsnede op magenta (Grok 9e970b14, 1792x1008,
                       uit vier schermafdruk-tegels op schaal 1)
      schacht_grok.png het gat door de mosgrond, op magenta (Grok ddafaaee, een tegel van 1536x702, vanaf x 300 y 306)
Uit:  boom.png    de boom alleen boven de grond: alles onder de mosrand (y 434) valt weg, er staat geen stam onder de grond
      deksel.png  wortels en mos net onder de mosrand, over het gat: van afstand dekt dit het gat af, dichtbij vervaagt het
      schacht.png het donkere gat door de grond, met de wanden, de mosrand en de worteltjes

    python3 tools/schachtboom_knip.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist Pillow, numpy en scipy.
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'regenwoud', 'schachtboom')
MOS = 434                       # de bovenkant van de mosrand in boom_grok.png
SCHX = (300, 565)               # de holte in de voet van de boom (bronpixels)
RECHTS = 900                    # zover rechts lopen de wortels over de grond


def magenta_weg(im):
    """De magenta lucht (vast aan de rand) weg, met een zachte rand; magenta in de randpixels naar donker bruin."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lucht = (r > 120) & (g < 95) & (b > 60) & (r - g > 90) & (b - g > 40)
    lab, _ = nd.label(lucht)
    rand = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    lucht = np.isin(lab, list(rand))
    d = nd.distance_transform_edt(~lucht)
    alfa = np.clip(d / 2.0, 0, 1)
    m = d < 3
    a[m, 0] = np.minimum(a[m, 0], a[m, 1] * 1.1 + 10)
    a[m, 2] = np.minimum(a[m, 2], a[m, 1] * 0.9 + 5)
    return np.dstack([a, alfa * 255])


def bewaar(a, naam):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(MAP, naam), optimize=True)
    print(naam, a.shape[1], 'x', a.shape[0])


def main():
    boom = magenta_weg(Image.open(os.path.join(MAP, 'bron', 'boom_grok.png')))
    H = boom.shape[0]
    yy = np.arange(H)[:, None]
    # de boom: onder de mosrand weg (zacht over 10 px), en de linkerkant (daar loopt de plaat af) zacht uit
    b = boom.copy()
    b[..., 3] *= np.clip((MOS + 14 - yy) / 10, 0, 1)
    xx = np.arange(b.shape[1])[None, :]
    b[..., 3] *= np.clip(xx / 60, 0, 1)
    b[..., 3] *= np.clip((RECHTS - xx) / 70, 0, 1)   # rechts van de wortels ligt in de plaat alleen nog grond: weg
    ys = np.where(b[..., 3].max(axis=1) > 8)[0]; xs = np.where(b[..., 3].max(axis=0) > 8)[0]
    print('boom: bovenkant y', ys.min(), 'rechts x', xs.max())
    bewaar(b[:MOS + 16, :xs.max() + 4], 'boom.png')
    # het deksel: een strook wortels en mos onder de mosrand, rond de holte, zacht naar alle kanten
    l, r = SCHX[0] - 30, SCHX[1] + 30
    d = boom[MOS - 4:MOS + 126, l:r].copy()
    m = np.zeros(d.shape[:2], np.float32); m[8:-30, 26:-26] = 1
    m = nd.gaussian_filter(m, 12)
    d[..., 3] *= np.clip(m * 1.4, 0, 1)
    bewaar(d, 'deksel.png')
    # de schacht: het gat met de wanden, de zijkanten en de onderkant zacht uit
    t = magenta_weg(Image.open(os.path.join(MAP, 'bron', 'schacht_grok.png')))
    s = t[236:668, 440:750].copy()
    h, w = s.shape[:2]
    f = np.ones((h, w), np.float32)
    for i in range(28): f[:, i] *= i / 28; f[:, w - 1 - i] *= i / 28
    for i in range(40): f[h - 1 - i, :] *= i / 40
    s[..., 3] *= f
    bewaar(s, 'schacht.png')
    print('deksel: links op bron-x', l, 'boven op bron-y', MOS - 4)


if __name__ == '__main__':
    main()
