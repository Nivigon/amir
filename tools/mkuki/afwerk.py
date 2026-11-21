"""Afwerken van een aangekleed, uitgelijnd frame: gezicht en voeten terug uit het origineel, de vuistlaag, de zones.

afwerk(kleed, orig, info, hoofd=True, voeten=True) -> dict(lijf, vuist, zones, vuist_zones)
  kleed: RGBA in hulpkleuren op het eigen canvas (uitgelijnd); orig: het originele frame (met speer);
  info: de speermeting van het origineel (of None).
"""
import numpy as np
from scipy import ndimage as nd
import kleur


def _vacht(o):
    r, g, b = [o[..., i].astype(int) for i in range(3)]
    return (r > 120) & (g > 85) & (r - b > 35) & (r + g + b > 380)


def _broek_oud(o):
    r, g, b = [o[..., i].astype(int) for i in range(3)]
    return (b > r - 6) & (b > g + 12) & (b > 45)


def afwerk(kleed, orig, info, hoofd=True, voeten=True, hoofd_lijn=None):
    out = kleed.copy()
    z = kleur.zones(kleed)
    oal = orig[..., 3] > 40
    spr = np.zeros(oal.shape, bool)
    if info is not None:
        spr = nd.binary_dilation(info['masker'], iterations=1)
    keep = oal & ~_vacht(orig) & ~spr
    bijvacht = nd.binary_dilation(_vacht(orig), iterations=4)
    H, W = oal.shape
    yy, xx = np.mgrid[0:H, 0:W]
    if hoofd and (z == 5).any():
        ys = np.where(z == 5)[0]
        yn = hoofd_lijn if hoofd_lijn is not None else int(np.percentile(ys, 8))
        zone = yy < yn
        # alleen rond het hoofd: kolommen van het originele hoofd (plus marge)
        hk = np.where((oal & zone & ~_vacht(orig)).any(0))[0]
        if len(hk):
            zone &= (xx >= hk.min() - 3) & (xx <= hk.max() + 3)
        weg = zone & ~oal & (z == 0)
        out[weg] = 0
        zet = zone & keep & (z == 0) & (~bijvacht | (kleed[..., 3] > 128))
        out[zet] = orig[zet]
    if voeten and (z == 1).any():
        blauw = z == 1
        zoom = nd.maximum_filter((blauw * (yy + 1)).astype(int), size=(1, 21))
        zoom = zoom.max(0)  # laagste blauwe rij per kolom (binnen 10 px)
        zone = (zoom[None, :] > 0) & (yy > zoom[None, :] + 1)
        zone &= ~_broek_oud(orig) | ~oal
        weg = zone & ~oal & (z == 0)
        out[weg] = 0
        zet = zone & keep
        out[zet] = orig[zet]
    # losse snippers (lintresten, randjes) weg
    al = out[..., 3] > 40
    lab, n = nd.label(al)
    if n > 1:
        sz = nd.sum(al, lab, range(1, n + 1))
        for i, v in enumerate(sz):
            if v < 0.01 * sz.max():
                out[lab == i + 1] = 0
    out[~nd.binary_dilation(out[..., 3] > 40, iterations=1)] = 0
    z = kleur.zones(out)
    vuist = np.zeros_like(out)
    if info is not None and info.get('handen'):
        r = max(8, 0.045 * info['lengte'])
        for hx, hy in info['handen']:
            disc = (xx - hx) ** 2 + (yy - hy) ** 2 < r * r
            m = disc & (out[..., 3] > 0) & ~info['masker']
            vuist[m] = out[m]
    vz = kleur.zones(vuist) if vuist[..., 3].any() else np.zeros(z.shape, np.uint8)
    return {'lijf': out, 'vuist': vuist, 'zones': z, 'vuist_zones': vz}
