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


def lijn_uit(nieuw, orig, bereik=40, geen=None):
    """Zoek dx, dy waarmee alpha van nieuw het best op orig valt. Geeft (verschoven, dx, dy, iou)."""
    a = nieuw[..., 3] > 128; b = orig[..., 3] > 128
    if geen is not None:
        a = a & ~geen
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


def lijn_uit_delen(nieuw, orig, bereik=40):
    """Eerst het hele frame, dan het bovenlijf (boven de riem) apart, voor als Grok het lijf iets rechter zet."""
    import kleur
    b, dx, dy, v = lijn_uit(nieuw, orig, bereik)
    z = kleur.zones(b)
    if not (z == 3).any():
        return b, dx, dy, v
    riem = int(np.median(np.where(z == 3)[0]))
    H = b.shape[0]
    boven = np.zeros(H, bool); boven[:riem] = True
    bt = b.copy(); bt[~boven] = 0
    ot = orig.copy(); ot[~boven] = 0
    t2, ddx, ddy, vt = lijn_uit(bt, ot, 14)
    if (ddx, ddy) == (0, 0):
        return b, dx, dy, v
    uit = b.copy()
    uit[:riem] = 0
    m = t2[..., 3] > 0
    uit[m] = t2[m]
    # naad bij de riem: wat onder de riem uit b komt houden, gaatjes vullen
    gat = (uit[..., 3] == 0) & (b[..., 3] > 0) & (np.arange(H)[:, None] >= riem - 6) & (np.arange(H)[:, None] <= riem + 6)
    uit[gat] = b[gat]
    v2 = iou(uit[..., 3] > 128, orig[..., 3] > 128)
    if v2 <= v:
        return b, dx, dy, v
    return uit, dx, dy, v2
