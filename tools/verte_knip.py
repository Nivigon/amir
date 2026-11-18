#!/usr/bin/env python3
"""Knipt het decor voor de verte van de stad in design/stad/verte/ uit de Grok-platen in bron/.

Een plaat is een rij losse stukken (groepjes daken, palmen) of een enkel stuk (de moskee),
transparant of op wit. Dit script haalt een witte achtergrond weg (alleen wat met de rand
verbonden is), en knipt elk stuk los. Stukjes die dicht bij elkaar liggen (de bladeren van
een palm) blijven een stuk.

Per plaat komt er <plaat>_01.png, _02.png enzovoort, van links naar rechts, strak bijgesneden;
een plaat met maar een stuk heet gewoon <plaat>.png.

    python3 tools/verte_knip.py

Daarna: python3 tools/gen-offline-manifest.py

Vereist Pillow, numpy en scipy.
"""
import glob, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad', 'verte')
BRON = os.path.join(MAP, 'bron')

GROEPEER = 18   # pixels: stukjes binnen deze afstand horen bij elkaar
GROEPEER_PLAAT = {'palm': 2}   # de palmen staan dicht op elkaar
SCHAAL = {'moskee': 0.6, 'palm': 0.6}   # in het spel komen ze niet groter in beeld dan dit (STAD_VERTE)
MIN_OPP = 600   # kleinere vlekjes zijn ruis
MARGE = 3


def met_rand_verbonden(masker):
    lab, _ = nd.label(masker)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(rand))


def knip(pad):
    naam = os.path.splitext(os.path.basename(pad))[0]
    im = np.asarray(Image.open(pad).convert('RGBA')).astype(np.float32)
    rgb, alfa = im[..., :3], im[..., 3] / 255.0
    mn = rgb.min(-1)
    # witte achtergrond die met de rand verbonden is weg, met een zachte overgang op de rand
    weg = met_rand_verbonden((mn > 225) & (alfa > 0.5))
    rand = nd.binary_dilation(weg, iterations=2) & ~weg
    alfa = np.where(weg, 0.0, alfa)
    alfa = np.where(rand, np.minimum(alfa, 1 - np.clip((mn - 150) / 90.0, 0, 1)), alfa)

    vol = alfa > 0.1
    lab, n = nd.label(nd.binary_dilation(vol, iterations=GROEPEER_PLAAT.get(naam, GROEPEER)))
    stukken = []
    for i in range(1, n + 1):
        m = (lab == i) & vol
        if m.sum() < MIN_OPP:
            continue
        ys, xs = np.nonzero(m)
        stukken.append((xs.min(), xs.max(), ys.min(), ys.max(), lab == i))
    stukken.sort(key=lambda s: s[0])

    uit = np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8)
    for k, (x0, x1, y0, y1, m) in enumerate(stukken, 1):
        x0, y0 = max(0, x0 - MARGE), max(0, y0 - MARGE)
        x1, y1 = min(uit.shape[1], x1 + MARGE + 1), min(uit.shape[0], y1 + MARGE + 1)
        stuk = uit[y0:y1, x0:x1].copy()
        stuk[~m[y0:y1, x0:x1], 3] = 0
        im_s = Image.fromarray(stuk)
        sk = SCHAAL.get(naam, 1)
        if sk != 1:
            im_s = im_s.resize((round(im_s.width * sk), round(im_s.height * sk)), Image.LANCZOS)
        doel = naam + ('.png' if len(stukken) == 1 else '_%02d.png' % k)
        im_s.save(os.path.join(MAP, doel), optimize=True)
        print('%-16s %4d x %4d' % (doel, im_s.width, im_s.height))


for pad in sorted(glob.glob(os.path.join(BRON, '*'))):
    if pad.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        knip(pad)
