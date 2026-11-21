"""Meet de speer in een origineel Amir-frame: punt, kont, hoek, lengte, masker.

Gebruik: python3 speer_meet.py frame.png [--override json]
Als module: meet(rgba) -> dict met tip, kont, hoek (graden, 0 = naar rechts, tegen de klok), lengte, masker (bool).

Werkwijze: de metalen punt is grijs (lage verzadiging), het lint is fel rood. Vanuit de punt zoeken we de
richting waarlangs een schacht loopt (bruin midden met binnen 6 px een donkere rand of leegte aan beide kanten),
en lopen die af tot de schacht ophoudt. Het masker is een band langs die lijn plus de grijze punt en het lint.
"""
import numpy as np, sys, json
from scipy import ndimage as nd


def _kleuren(rgba):
    a = rgba[..., :3].astype(float)
    al = rgba[..., 3] > 100
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1)
    grijs = al & ((mx - mn) < 28) & (a.mean(-1) > 75) & (a.mean(-1) < 215)
    rood = al & (r > 110) & (g < 75) & (b < 80) & (r > 2.2 * g)
    bruin = al & (r > 45) & (r < 190) & (r >= g) & (g >= b - 4) & (r - b > 18)
    donker = (~al) | (a.sum(-1) < 110)
    return al, grijs, rood, bruin, donker


def _schacht_score(bruin, donker, p, d, n, stap=1.0):
    """Hoeveel punten langs p + t*d (t = 0..n) lijken op een schacht."""
    H, W = bruin.shape
    nrm = np.array([-d[1], d[0]])
    goed = 0; laatst = 0; mis = 0
    for i in range(int(n)):
        q = p + d * i * stap
        x, y = int(round(q[0])), int(round(q[1]))
        if not (0 <= x < W and 0 <= y < H):
            break
        c = bruin[y, x] or bruin[min(H-1, max(0, int(round(q[1]+nrm[1])))), min(W-1, max(0, int(round(q[0]+nrm[0]))))]
        zij = [False, False]
        for k, s in enumerate((1, -1)):
            for j in range(2, 8):
                xx, yy = int(round(q[0] + s * nrm[0] * j)), int(round(q[1] + s * nrm[1] * j))
                if not (0 <= xx < W and 0 <= yy < H) or donker[yy, xx]:
                    zij[k] = True; break
        if c and zij[0] and zij[1]:
            goed += 1; laatst = i; mis = 0
        else:
            mis += 1
            if mis > 34:
                break
    return goed, laatst


def meet(rgba, override=None):
    al, grijs, rood, bruin, donker = _kleuren(rgba)
    H, W = al.shape
    if override and 'tip' in override and 'kont' in override:
        tip = np.array(override['tip'], float); kont = np.array(override['kont'], float)
    else:
        lab, n = nd.label(grijs)
        if n == 0:
            return None
        sz = nd.sum(grijs, lab, range(1, n + 1))
        k = int(np.argmax(sz)) + 1
        ys, xs = np.where(lab == k)
        cen = np.array([xs.mean(), ys.mean()])
        best = None
        for hoek in np.arange(0, 360, 1.0):
            d = np.array([np.cos(np.radians(hoek)), -np.sin(np.radians(hoek))])
            g, l = _schacht_score(bruin, donker, cen + d * 6, d, 700)
            if best is None or g > best[0]:
                best = (g, l, hoek, d)
        g, l, hoek, d = best
        # verfijn
        for hh in np.arange(hoek - 1, hoek + 1.01, 0.2):
            dd = np.array([np.cos(np.radians(hh)), -np.sin(np.radians(hh))])
            gg, ll = _schacht_score(bruin, donker, cen + dd * 6, dd, 700)
            if gg > g:
                g, l, hoek, d = gg, ll, hh, dd
        kont = cen + d * (6 + l)
        # punt: verste grijze pixel van de kop tegen de schachtrichting in
        proj = (xs - cen[0]) * (-d[0]) + (ys - cen[1]) * (-d[1])
        tip = cen + (-d) * proj.max()
    v = kont - tip
    lengte = float(np.hypot(*v))
    d = v / max(lengte, 1e-6)
    hoek = float(np.degrees(np.arctan2(-d[1], d[0])))  # richting van punt naar kont
    # masker: band langs de lijn
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx - tip[0]) * d[0] + (yy - tip[1]) * d[1]
    s = np.abs((xx - tip[0]) * (-d[1]) + (yy - tip[1]) * d[0])
    breed = (override or {}).get('breed', 6.5)
    band = (t > -3) & (t < lengte + 3) & (s < breed)
    # kop en lint: grijs en rood vlak bij de punt (binnen 22% van de lengte)
    dicht = (t > -6) & (t < lengte * 0.24 + 6) & (s < 26)
    masker = (band | ((grijs | rood) & dicht)) & al
    # lint: alle roodachtige stukken die het masker raken, met hun donkere omlijning
    a = rgba[..., :3].astype(float)
    roodw = al & (a[..., 0] > 55) & (a[..., 0] > 1.7 * a[..., 1]) & (a[..., 0] > 1.5 * a[..., 2]) & dicht
    lab, n = nd.label(roodw | (rood & dicht))
    raak = nd.binary_dilation(masker, iterations=2)
    ids = np.unique(lab[raak & (lab > 0)])
    lint = np.isin(lab, ids[ids > 0])
    lint = nd.binary_dilation(lint, iterations=2) & (lint | (a.sum(-1) < 150)) & al
    masker = masker | lint
    masker = nd.binary_dilation(masker, iterations=1) & al
    return {'tip': [round(float(tip[0]), 1), round(float(tip[1]), 1)],
            'kont': [round(float(kont[0]), 1), round(float(kont[1]), 1)],
            'hoek': round(hoek, 1), 'lengte': round(lengte, 1), 'masker': masker}


if __name__ == '__main__':
    from PIL import Image
    im = np.asarray(Image.open(sys.argv[1]).convert('RGBA'))
    r = meet(im)
    print({k: v for k, v in r.items() if k != 'masker'})
