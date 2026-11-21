"""Uitlijnen van een aangekleed frame op het origineel (IoU-schuifzoektocht) en vergelijken."""
import numpy as np
from scipy import ndimage as nd


def iou(a, b):
    return (a & b).sum() / max((a | b).sum(), 1)


def schuif(arr, dx, dy):
    out = np.zeros_like(arr)
    H, W = arr.shape[:2]
    xs0, xs1 = max(0, -dx), min(W, W - dx); ys0, ys1 = max(0, -dy), min(H, H - dy)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = arr[ys0:ys1, xs0:xs1]
    return out


def lijn_uit(nieuw, orig, bereik=40):
    """Zoek dx, dy waarmee alpha van nieuw het best op orig valt. Geeft (verschoven, dx, dy, iou)."""
    a = nieuw[..., 3] > 128; b = orig[..., 3] > 128
    best = (iou(a, b), 0, 0)
    stap = 4
    cx, cy = 0, 0
    for st in (4, 1):
        r = bereik if st == 4 else 4
        for dy in range(cy - r, cy + r + 1, st):
            for dx in range(cx - r, cx + r + 1, st):
                v = iou(schuif(a, dx, dy), b)
                if v > best[0]:
                    best = (v, dx, dy)
        cx, cy = best[1], best[2]
    v, dx, dy = best
    return schuif(nieuw, dx, dy), dx, dy, v
