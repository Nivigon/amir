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
    al0 = rgba[..., 3] > 100
    ys0 = np.where(al0.any(1))[0]
    xs0 = np.where(al0.any(0))[0]
    hfig = max((ys0.max() - ys0.min()), 0.75 * (xs0.max() - xs0.min())) if len(ys0) else 0
    if hfig > 380 and not (override or {}).get('geenschaal'):
        from PIL import Image
        f = 290.0 / hfig
        H0, W0 = rgba.shape[:2]
        klein = np.asarray(Image.fromarray(rgba).resize((max(1, int(W0 * f)), max(1, int(H0 * f))), Image.LANCZOS))
        ov = None
        if override:
            ov = dict(override)
            for k in ('tip', 'kont'):
                if k in ov: ov[k] = [ov[k][0] * f, ov[k][1] * f]
            if 'handen' in ov: ov['handen'] = [[x * f, y * f] for x, y in ov['handen']]
        r = _meet(klein, ov)
        if r is None:
            return None
        up = lambda m: np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((W0, H0), Image.NEAREST)) > 127
        r['masker'] = nd.binary_dilation(up(r['masker']), iterations=max(1, int(round(0.8 / f)))) & al0
        r['band'] = up(r['band'])
        for k in ('tip', 'kont'):
            r[k] = [round(r[k][0] / f, 1), round(r[k][1] / f, 1)]
        r['lengte'] = round(r['lengte'] / f, 1)
        r['handen'] = [[round(x / f, 1), round(y / f, 1)] for x, y in r['handen']]
        r['handstuk'] = [[int(a / f), int(b / f)] for a, b in r['handstuk']]
        return r
    return _meet(rgba, override)


def _meet(rgba, override=None):
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
    # zichtbaarheid langs de lijn: waar de schacht te zien is en waar iets ervoor zit (hand, lijf)
    nrm = np.array([-d[1], d[0]])
    n = int(lengte) + 1
    zicht = np.zeros(n, bool)
    for i in range(n):
        q = tip + d * i
        x, y = int(round(q[0])), int(round(q[1]))
        if not (0 <= x < W and 0 <= y < H):
            continue
        if not al[y, x]:
            continue
        c = bruin[y, x] or grijs[y, x] or rood[y, x]
        zij = [False, False]
        for k, sg in enumerate((1, -1)):
            for j in range(2, 8):
                xx, yy = int(round(q[0] + sg * nrm[0] * j)), int(round(q[1] + sg * nrm[1] * j))
                if not (0 <= xx < W and 0 <= yy < H) or donker[yy, xx]:
                    zij[k] = True; break
        zicht[i] = c and zij[0] and zij[1]
    kop = int(lengte * 0.2)
    zicht[:kop] = True
    # gaatjes van 1-3 punten dicht (ruis), echte bedekking blijft
    zicht = nd.binary_closing(zicht, structure=np.ones(5)) | zicht
    bedekt = []
    lab, nb = nd.label(~zicht)
    for j in range(1, nb + 1):
        idx = np.where(lab == j)[0]
        if idx[0] == 0 or idx[-1] >= n - 1 or len(idx) < 5:
            continue
        bedekt.append([int(idx[0]), int(idx[-1])])
    # handen: stukken waar het silhouet dwars op de schacht breder is dan de schacht (een vuist eromheen)
    breedte = np.zeros(n)
    for i in range(n):
        q = tip + d * i; w = 1
        for sg in (1, -1):
            j = 0
            while j < 60:
                x, y = np.round(q + sg * nrm * (j + 1)).astype(int)
                if not (0 <= x < W and 0 <= y < H) or not al[y, x]:
                    break
                j += 1
            w += j
        breedte[i] = w
    basis = np.percentile(breedte[int(0.3 * n):int(0.9 * n)], 25)
    wijd = breedte > max(11, basis * 1.7)
    wijd[:int(0.3 * n)] = False; wijd[int(0.93 * n):] = False
    wijd = nd.binary_closing(wijd, structure=np.ones(5))
    handen = []; handstuk = []
    lab, nb = nd.label(wijd)
    for j in range(1, nb + 1):
        idx = np.where(lab == j)[0]
        if len(idx) < 8 or len(idx) > 0.22 * n:
            continue
        # een vuist is huid naast de schacht; een been (broek) of de vacht is het niet
        huid = 0; tel = 0
        a3 = rgba[..., :3].astype(int)
        for i in idx:
            for sg in (1, -1):
                for j in (6, 8, 10):
                    x, y = np.round(tip + d * i + sg * nrm * j).astype(int)
                    if 0 <= x < W and 0 <= y < H and al[y, x]:
                        r_, g_, b_ = a3[y, x]
                        tel += 1
                        if r_ >= g_ >= b_ - 3 and r_ - b_ > 8 and r_ + g_ + b_ < 330:
                            huid += 1
        if tel == 0 or huid / tel < 0.5:
            continue
        m = idx[0] + min(11, (idx[-1] - idx[0]) / 2)  # de vuist zit aan de kant van de punt, daarna de onderarm
        handen.append([round(float(tip[0] + d[0] * m), 1), round(float(tip[1] + d[1] * m), 1)])
        handstuk.append([int(idx[0]), int(idx[-1])])
    if override and 'handen' in override:
        handen = override['handen']
    # masker: band langs de lijn, alleen waar de speer zichtbaar is
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx - tip[0]) * d[0] + (yy - tip[1]) * d[1]
    s = np.abs((xx - tip[0]) * (-d[1]) + (yy - tip[1]) * d[0])
    breed = (override or {}).get('breed', 6.5)
    ti = np.clip(np.round(t).astype(int), 0, n - 1)
    zbreed = nd.binary_erosion(zicht, structure=np.ones(3)) | (np.arange(n) < kop)
    vrij = np.ones(n, bool)
    if override and 'handstuk' in override:
        handstuk = override['handstuk']
    for a0, a1 in handstuk:
        vrij[max(0, a0 + 2):a1 - 1] = False
    band = (t > -3) & (t < lengte + 3) & (s < breed) & (vrij[ti] | (t < 0) | (t > lengte))
    bandvol = (t > -3) & (t < lengte + 3) & (s < breed)
    # kop en lint: grijs en rood vlak bij de punt (binnen 22% van de lengte)
    dicht = (t > -6) & (t < lengte * 0.32 + 6) & (s < 36)
    # de metalen kop: de grijze vlek die de band raakt, dicht bij de punt
    labg, ng = nd.label(grijs & dicht)
    raakg = nd.binary_dilation(band, iterations=2)
    idg = np.unique(labg[raakg & (labg > 0)])
    kopblob = np.isin(labg, idg[idg > 0])
    masker = (band | kopblob) & al
    # in de vuist: wat er van de schacht tussen de vingers door te zien is (lichter bruin dan de huid) ook weg
    a3 = rgba[..., :3].astype(int)
    licht = (a3.sum(-1) > 225) & (a3[..., 0] - a3[..., 2] > 26) & (a3[..., 0] >= a3[..., 1])
    extra = bandvol & ~band & licht & (s < breed - 1.5) & al
    labx, nx = nd.label(extra)
    for i in range(1, nx + 1):
        if (labx == i).sum() >= 10:
            masker |= labx == i
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
    return {'tip': [round(float(tip[0]), 1), round(float(tip[1]), 1)], 'handen': handen, 'handstuk': handstuk,
            'band': bandvol & al,
            'kont': [round(float(kont[0]), 1), round(float(kont[1]), 1)],
            'hoek': round(hoek, 1), 'lengte': round(lengte, 1), 'masker': masker}


if __name__ == '__main__':
    from PIL import Image
    im = np.asarray(Image.open(sys.argv[1]).convert('RGBA'))
    r = meet(im)
    print({k: v for k, v in r.items() if k != 'masker'})


OVF = __import__('os').path.join(__import__('os').path.dirname(__file__), 'overrides.json')


def rel(pad):
    pad = __import__('os').path.abspath(pad)
    return pad.split('karakters/amir/', 1)[1] if 'karakters/amir/' in pad else pad


def override(pad):
    import os
    if not os.path.exists(OVF):
        return None
    return json.load(open(OVF)).get(rel(pad))


def meet_pad(pad, rgba=None):
    from PIL import Image
    if rgba is None:
        rgba = np.asarray(Image.open(pad).convert('RGBA'))
    return meet(rgba, override(pad))


def set_lengte(paden, drempel=0.93):
    """Zelfde speer in een set: frames waar de meting te kort uitvalt krijgen de mediane lengte (kont verlengd)."""
    import os
    from PIL import Image
    ov = json.load(open(OVF)) if os.path.exists(OVF) else {}
    rs = {}
    for p in paden:
        o = ov.get(rel(p), {})
        if 'tip' in o:
            continue
        rs[p] = meet(np.asarray(Image.open(p).convert('RGBA')), o or None)
    if not rs:
        return
    med = float(np.median([r['lengte'] for r in rs.values()]))
    for p, r in rs.items():
        if r['lengte'] < drempel * med:
            t = np.array(r['tip']); k = np.array(r['kont']); d = (k - t) / np.linalg.norm(k - t)
            k2 = t + d * med
            o = ov.setdefault(rel(p), {})
            o['tip'] = r['tip']; o['kont'] = [round(float(k2[0]), 1), round(float(k2[1]), 1)]
            print('lengte', rel(p), r['lengte'], '->', round(med, 1))
    json.dump(ov, open(OVF, 'w'), indent=1)
