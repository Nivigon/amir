"""Overzichtsplaat en GIF per set (origineel naast Tau 1), en de recolours."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tau
BG = (122, 140, 118)


def bbox(paden):
    ys0 = xs0 = 10 ** 6; ys1 = xs1 = 0
    for p in paden:
        a = np.asarray(Image.open(p).convert('RGBA'))[..., 3] > 20
        ys, xs = np.where(a)
        ys0, ys1, xs0, xs1 = min(ys0, ys.min()), max(ys1, ys.max()), min(xs0, xs.min()), max(xs1, xs.max())
    return xs0 - 4, ys0 - 4, xs1 + 5, ys1 + 5


def plaat(naam, orig, tau_, uit, k=2, extra=None):
    rijen = [orig, tau_] + ([extra] if extra else [])
    box = bbox(orig + tau_)
    w, h = (box[2] - box[0]) * k, (box[3] - box[1]) * k
    n = len(orig)
    cols = min(n, 7)
    blokken = (n + cols - 1) // cols
    S = Image.new('RGB', (w * cols, h * len(rijen) * blokken + 20), BG)
    d = ImageDraw.Draw(S); d.text((4, 4), naam + ': boven origineel, onder Tau 1', fill=(0, 0, 0))
    for r, paden in enumerate(rijen):
        for j, p in enumerate(paden):
            im = Image.open(p).convert('RGBA').crop(box).resize((w, h), Image.LANCZOS)
            b, c = divmod(j, cols)
            S.paste(im, (c * w, 20 + (b * len(rijen) + r) * h), im)
    S.save(uit)


def gif(orig, tau_, uit, ms=70, k=2):
    box = bbox(orig + tau_)
    w, h = (box[2] - box[0]) * k, (box[3] - box[1]) * k
    fr = []
    for a, b in zip(orig, tau_):
        S = Image.new('RGB', (w * 2, h), BG)
        for n, p in enumerate((a, b)):
            im = Image.open(p).convert('RGBA').crop(box).resize((w, h), Image.LANCZOS)
            S.paste(im, (n * w, 0), im)
        fr.append(S)
    fr[0].save(uit, save_all=True, append_images=fr[1:], duration=ms, loop=0)
