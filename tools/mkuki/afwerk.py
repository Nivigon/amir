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


def benen_orig(kleed, orig, info):
    """Onder de heup de benen uit het origineel (oude broek omgezet naar de blauwe hulpkleur), alleen de schort van Grok.
    Voor poses waar Grok de benen niet volgt (gekruiste benen in de ren)."""
    z = kleur.zones(kleed)
    if not (z == 3).any() or not (z == 2).any():
        return kleed
    H, W = z.shape
    yy, xx = np.mgrid[0:H, 0:W]
    heup = int(np.percentile(np.where(z == 3)[0], 70))
    o = orig.copy()
    if info is not None:
        o[nd.binary_dilation(info['masker'], iterations=1), 3] = 0
    br = _broek_oud(o) & (o[..., 3] > 40)
    Vo = o[..., :3].max(-1).astype(float) / 255
    med = np.median(Vo[br]) if br.any() else 0.35
    f = np.clip(Vo / med * kleur.VREF[1], 0, 1)[..., None]
    hulp = np.array([32, 80, 255], float)
    o2 = o.astype(float)
    br &= Vo > 0.2
    o2[..., :3][br] = (hulp * f)[br]
    o2 = o2.astype(np.uint8)
    onder = yy > heup
    oal = o[..., 3] > 40
    # benen in het origineel: de broek plus de huid eronder (kuiten, voeten), niet een hand op heuphoogte
    benen_o = br & onder
    rest = oal & ~br & onder
    lab, n = nd.label(rest)
    cy_b = np.where(br)[0].mean() if br.any() else heup
    for i in range(1, n + 1):
        m = lab == i
        if (nd.binary_dilation(m, iterations=2) & br).any() and np.where(m)[0].mean() > cy_b:
            benen_o |= m
    benen_o = nd.binary_closing(benen_o, iterations=1) & oal
    # benen in Grok: hetzelfde idee (blauw plus huid eronder), de schort niet
    gal = kleed[..., 3] > 40
    blauw = (z == 1) & onder
    rest = gal & onder & ~blauw & ~nd.binary_dilation(z == 2, iterations=1)
    lab, n = nd.label(rest)
    benen_g = blauw.copy()
    cy_g = np.where(blauw)[0].mean() if blauw.any() else heup
    for i in range(1, n + 1):
        m = lab == i
        if (nd.binary_dilation(m, iterations=2) & blauw).any() and np.where(m)[0].mean() > cy_g:
            benen_g |= m
    out = kleed.copy()
    weg = nd.binary_dilation(benen_g, iterations=1) & ~nd.binary_dilation(z == 2, iterations=1)
    out[weg] = 0
    out[benen_o] = o2[benen_o]
    # vlak onder de heup: zachte overgang, Grok blijft boven
    schort = nd.binary_dilation(z == 2, iterations=2) & gal & onder
    out[schort] = kleed[schort]
    boven = ~onder
    out[boven] = kleed[boven]
    # gaatjes tussen de schort en de originele benen dicht met Grok
    gat = gal & onder & (out[..., 3] < 40) & nd.binary_dilation(out[..., 3] > 40, iterations=1) & ~nd.binary_dilation(benen_g, iterations=1)
    out[gat] = kleed[gat]
    return out


def afwerk(kleed, orig, info, hoofd=True, voeten=True, hoofd_lijn=None, benen=False):
    if benen:
        kleed = benen_orig(kleed, orig, info)
        voeten = False
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
        if (z == 3).any():
            yn = min(yn, int(np.percentile(np.where(z == 3)[0], 5)) - 10)
        zone = yy < yn
        # alleen rond het hoofd: kolommen van het originele hoofd (plus marge)
        hk = np.where((oal & zone & ~_vacht(orig)).any(0))[0]
        if len(hk):
            zone &= (xx >= hk.min() - 3) & (xx <= hk.max() + 3)
        weg = zone & ~oal & (z == 0)
        out[weg] = 0
        donker = orig[..., :3].astype(int).sum(-1) < 300
        zet = zone & keep & (z == 0) & (~bijvacht | (kleed[..., 3] > 128)) & (donker | ~bijvacht)
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
        # de vuist komt uit het originele frame, zodat de speer er altijd precies doorheen loopt
        r = max(12, 0.06 * info['lengte'])
        for hx, hy in info['handen']:
            disc = (xx - hx) ** 2 + (yy - hy) ** 2 < r * r
            rand = ((xx - hx) ** 2 + (yy - hy) ** 2 < (r + 3) ** 2) & ~disc
            org = disc & oal & ~info['masker']
            # Grok-pixels in de schijf weg, behalve waar ze aan de rand doorlopen (pols, manchet)
            out[disc & ~org & ~nd.binary_dilation(rand & (out[..., 3] > 0), iterations=1)] = 0
            out[org] = orig[org]
            vuist[org] = orig[org]
    z = kleur.zones(out)
    vz = kleur.zones(vuist) if vuist[..., 3].any() else np.zeros(z.shape, np.uint8)
    return {'lijf': out, 'vuist': vuist, 'zones': z, 'vuist_zones': vz}
