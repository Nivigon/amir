"""Splits een Mkuki-renframe in: voorbeen, achterbeen, voorarm, achterarm, romp.

Geodetische afstand binnen het silhouet vanaf zaadpunten (voeten, vuisten, borst, hoofd),
elk pixel gaat naar het dichtstbijzijnde zaad.
"""
import numpy as np
from PIL import Image
from skimage.graph import MCP_Geometric

VB, AB, VA, AA, ROMP = 1, 2, 3, 4, 5
W_ROMP = 1.0


def laad(pad):
    return np.array(Image.open(pad).convert('RGBA'))


def zonemasker(z, rgb):
    return (z[..., 0] == rgb[0]) & (z[..., 1] == rgb[1]) & (z[..., 2] == rgb[2])


def geo(mask, seeds):
    cost = np.where(mask, 1.0, np.inf)
    m = MCP_Geometric(cost)
    d, _ = m.find_costs(seeds)
    return d


def splits(im, z, zaden=None):
    al = im[..., 3] > 20
    H, W = al.shape
    Y, X = np.mgrid[:H, :W]
    riem = zonemasker(z, (255, 0, 0))
    ry0, ry1 = np.where(riem)[0].min(), np.where(riem)[0].max()
    ys, xs = np.where(al)
    top = ys.min()
    if zaden is None:
        zaden = {}
    # voeten: voorste en achterste pixel onder de heup
    onder = al & (Y > ry1 + 10)
    oy, ox = np.where(onder)
    i = np.argmin(ox); vb = zaden.get('vb', (oy[i], ox[i]))
    i = np.argmax(ox); ab = zaden.get('ab', (oy[i], ox[i]))
    # vuisten: voorste pixel tussen hoofd en riem; achterste pixel in die band
    band = al & (Y > top + 65) & (Y < ry1 + 15)
    by, bx = np.where(band)
    i = np.argmin(bx); va = zaden.get('va', (by[i], bx[i]))
    i = np.argmax(bx); aa = zaden.get('aa', (by[i], bx[i]))
    # romp: midden van de riem en borst
    rx = np.median(np.where(riem)[1])
    borst = zaden.get('borst', (int((top + 45 + ry0) / 2), int(rx)))
    riemp = (int((ry0 + ry1) / 2), int(rx))
    hoofd = (top + 15, int(np.median(xs[ys < top + 30])))
    S = {VB: [vb], AB: [ab], VA: [va], AA: [aa], ROMP: [borst, riemp, hoofd]}
    from scipy import ndimage as nd
    schort = zonemasker(z, (255, 255, 0))
    oranje = zonemasker(z, (255, 128, 0))
    cl, n = nd.label(nd.binary_dilation(oranje, iterations=1))
    comps = sorted([np.argwhere(cl == i) for i in range(1, n + 1) if (cl == i).sum() > 8], key=lambda c: c[:, 1].mean())
    if len(comps) >= 4:
        voor, achter = comps[:2], comps[2:]
    else:
        # minder banden zichtbaar: links van de riem is voor
        voor = [c for c in comps if c[:, 1].mean() < rx]; achter = [c for c in comps if c[:, 1].mean() >= rx]
    # pols = de band het verst van de borst; daarbij de vuist zelf
    def pols(cs):
        if not cs: return None
        return max(cs, key=lambda c: np.hypot(c[:, 0].mean() - borst[0], c[:, 1].mean() - borst[1]))
    pv, pa = pols(voor), pols(achter)
    vpts = ([tuple(p) for p in pv[::2]] if pv is not None else []) + [va]
    apts = ([tuple(p) for p in pa[::2]] if pa is not None else []) + [aa]
    S[VA] = vpts; S[AA] = apts
    vrij = al & ~schort & ~riem
    D = np.stack([geo(vrij, [vb]), geo(vrij, [ab]), geo(vrij, vpts), geo(vrij, apts),
                  W_ROMP * geo(vrij, [p for p in S[ROMP] if vrij[p]])])
    keys = np.array([VB, AB, VA, AA, ROMP])
    lab = keys[np.argmin(D, 0)]
    # op de broek kan geen arm liggen: daar alleen voorbeen tegen achterbeen
    broek = zonemasker(z, (0, 0, 255)) & vrij
    lab[broek] = np.where(D[0][broek] <= D[1][broek], VB, AB)
    lab[~vrij] = ROMP
    lab[np.isinf(D.min(0))] = ROMP
    lab[~al] = 0
    return lab, S
