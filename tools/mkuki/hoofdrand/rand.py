# Hoofdrand van Mkuki-frames: vorm repareren en een nette donkere lijn zoals de goede originelen.
# Drie methodes om te vergelijken:
#   M1 'synth' : vorm uit het origineel (glad), oude randpixels weg, nieuwe lijn uit een afstandsveld (subpixel)
#   M2 'meng'  : als M1, maar de oude Mkuki-lijn blijft staan (donkerste van beide)
#   M3 'kopie' : de rand (lijn + zachte buitenrand) van het origineel overnemen, met de paarse/oranje zoom omgekleurd
import sys, os
import numpy as np
from scipy import ndimage
import cv2
sys.path.insert(0, '/home/claude/gat')
from vul import hoofdgat

LIJN = np.array([16., 4., 4.])
D_PER_KOP = 0.0105          # donkerte-integraal van de lijn als deel van de hoofdgrootte (origineel springen: 1.05-1.08%)
UP = 4                      # subpixel-factor voor het afstandsveld
DREMPEL = 0.85             # randpixels donkerder dan dit deel van de huid zijn oude lijn of waas


def buiten(leeg):
    lab, n = ndimage.label(leeg)
    ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(ids))


def lum(A):
    return (A[..., :3].astype(float) * [.3, .59, .11]).sum(-1)


def zoom_kleur(A):
    """paarse of oranje zoom van het uitknippen (geen huid, geen lijn)"""
    a = A[..., :3].astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    paars = (r - g > 12) & (b - g > 12)
    oranje = (r > 150) & (r - b > 90) & (g > 70)          # fel oranje/zandkleur, niet de huid (r~85)
    blauw = (b - r > 10) & (b > 60)
    return paars | oranje | blauw


def gebied(O, M, h, kop_set=None):
    """waar we de rand mogen aanpassen: rond de kop, naar de lucht, niet bij de kralen/hals"""
    from skimage.morphology import convex_hull_image
    o = O.astype(int); m = M.astype(int)
    ma = m[..., 3]
    marge = 3
    if kop_set:
        marge = int(round(max(3, 0.5 * (kop_set - kopmaat(h)) + 3)))
    hull = ndimage.binary_dilation(convex_hull_image(h), iterations=marge)
    rood = (m[..., 0] > 140) & (m[..., 1] < 90) & (m[..., 2] < 90) & (ma > 128)
    R = hull & ~ndimage.binary_dilation(rood, iterations=3)
    rk = rood & ndimage.binary_dilation(h, iterations=8)
    if rk.sum() > 15:
        hy, hx = ndimage.center_of_mass(h); ry, rx = np.where(rk)
        d = np.array([ry.mean() - hy, rx.mean() - hx]); d /= np.linalg.norm(d) + 1e-9
        yy, xx = np.mgrid[0:o.shape[0], 0:o.shape[1]]
        proj = (yy - hy) * d[0] + (xx - hx) * d[1]
        R2 = R & (proj < np.percentile((ry - hy) * d[0] + (rx - hx) * d[1], 2) - 2)
        if R2.sum() >= 0.4 * R.sum():
            R = R2
    return R


def kopmaat(h):
    from skimage.morphology import convex_hull_image
    ch = convex_hull_image(h)
    return max(np.ptp(np.where(ch.any(1))[0]), np.ptp(np.where(ch.any(0))[0]))


def doelvorm(O, M, R, h=None):
    """vorm binnen R: Mkuki zelf, glad (rafels weg, kleine inkepingen dicht); grotere inkepingen
    alleen dicht waar het origineel daar ook hoofd heeft"""
    oa = O[..., 3].astype(int); ma = M[..., 3].astype(int)
    So = (oa > 128) & ~zoom_kleur(O)
    Sm = ma > 128
    eo = R & Sm & ~ndimage.binary_erosion(Sm)
    do = ndimage.distance_transform_edt(~(So & ~ndimage.binary_erosion(So)))
    gem = do[eo].mean() if eo.any() else 99

    def schijf(r):
        yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; return yy ** 2 + xx ** 2 <= r * r
    p = 10
    v = np.pad(Sm, p)
    k3 = ndimage.binary_closing(v, structure=schijf(3))
    k3 = ndimage.binary_fill_holes(k3)
    k3 = ndimage.binary_opening(k3, structure=schijf(2))
    # grote inkepingen: sluiten met r=7, maar alleen waar het origineel hoofd heeft
    k7 = ndimage.binary_closing(np.pad(Sm, p), structure=schijf(7))
    groot = k7 & ~k3 & np.pad(So, p)
    S = (k3 | groot)[p:-p, p:-p]
    bron = 'mkuki+orig' if groot.any() else 'mkuki'
    if h is not None:
        # spleten tussen hoofd en een ander lichaamsdeel (arm, hand) niet dichtmaken
        hh = ndimage.binary_dilation(h, iterations=3) & Sm
        ander = Sm & ~ndimage.binary_dilation(hh, iterations=2)
        add = S & ~Sm
        lab, n = ndimage.label(add)
        for i in range(1, n + 1):
            c = lab == i
            if (ndimage.binary_dilation(c, iterations=2) & ander).sum() > 3:
                S[c] = False
    if gem < 1.0:
        # origineel en Mkuki vallen samen: volg het gladde origineel, hooguit MAXC px van Mkuki af
        MAXC = 3.0
        vo = np.pad(So, p)
        vo = ndimage.binary_closing(vo, structure=schijf(3)); vo = ndimage.binary_fill_holes(vo)
        vo = ndimage.binary_opening(vo, structure=schijf(2))[p:-p, p:-p]
        d_uit = ndimage.distance_transform_edt(~vo)[S & ~vo & R]
        d_in = ndimage.distance_transform_edt(~S)[vo & ~S & R]
        te_ver = (d_uit.max() if d_uit.size else 0) > MAXC or (d_in.max() if d_in.size else 0) > MAXC + 2
    if gem < 1.0 and not te_ver:
        add = vo & ~S & (ndimage.distance_transform_edt(~S) <= MAXC)
        if h is not None:
            lab, n = ndimage.label(add)
            for i in range(1, n + 1):
                c = lab == i
                if (ndimage.binary_dilation(c, iterations=2) & ander).sum() > 3:
                    add[c] = False
        rem = S & ~vo & (ndimage.distance_transform_edt(~vo) <= MAXC)
        S = (S | add) & ~rem
        bron = 'orig'
    S = np.where(R, S, Sm)
    return S, bron, gem


def afstandsveld(S, sigma=1.0):
    """subpixel signed distance (px, positief binnen) en dekking per pixel"""
    f = ndimage.gaussian_filter(S.astype(float), sigma)
    H, W = S.shape
    fu = cv2.resize(f, (W * UP, H * UP), interpolation=cv2.INTER_LINEAR)
    binnen = fu > 0.5
    din = ndimage.distance_transform_edt(binnen); dout = ndimage.distance_transform_edt(~binnen)
    sdf = np.where(binnen, din - 0.5, -(dout - 0.5)) / UP
    dek = binnen.reshape(H, UP, W, UP).mean(axis=(1, 3))
    d = sdf.reshape(H, UP, W, UP).mean(axis=(1, 3))
    return d, dek


def maak(O, M, methode='synth', h=None, keep=None, D=None, sigma=1.0, kop_set=None):
    if h is None:
        keep, h = hoofdgat(O, M)
        if h is None:
            return None, {}
    O = O.copy(); M = M.copy()
    R = gebied(O, M, h, kop_set)
    # alleen waar lucht in de buurt is (randen naar de achtergrond)
    lucht = buiten(M[..., 3] < 30) | buiten(O[..., 3] < 30)
    R &= ndimage.binary_dilation(lucht, iterations=6)
    S, bron, gem = doelvorm(O, M, R, h)
    d, dek = afstandsveld(S, sigma)
    kop = kopmaat(h)
    if D is None:
        D = D_PER_KOP * (kop_set if kop_set else kop)
    Wl = max(D - 0.5, 0.0)
    w = np.clip(1 - (d - Wl), 0, 1); w[d <= Wl] = 1.0; w[d < -0.5] = 1.0
    # zachte overgang aan de rand van R (geen harde knik waar de nieuwe lijn ophoudt)
    Rz = ndimage.gaussian_filter(R.astype(float), 1.2) * R
    Rz = np.clip(Rz * 1.6, 0, 1)

    m = M.astype(float)
    ma = m[..., 3]
    L = lum(M)
    huidL = np.median(L[h & ndimage.binary_erosion(h, iterations=6) & (ma > 250)])
    # 1. de kleur onder de lijn: oude randpixels (donker, zoom, halfdoorzichtig, nieuw) opnieuw uit de huid
    rand = R & (d > -1.0) & (d < Wl + 2.0)
    oud = rand & ((ma < 235) | (L < huidL * DREMPEL) | zoom_kleur(M) | (S & (ma < 128)))
    # oude (wazige) Mkuki-rand die binnen de nieuwe rand komt te liggen
    dm = ndimage.distance_transform_edt(ma > 40)
    oud |= R & S & (dm < 2.5) & (L < huidL * DREMPEL) & (d < Wl + 4.0)
    if methode == 'meng':
        oud = rand & ((ma < 235) | zoom_kleur(M) | (S & (ma < 128)))
    rgb = np.ascontiguousarray(M[..., :3][..., ::-1]).copy()
    masker = (oud | (R & (ma < 128))).astype(np.uint8) * 255
    C = cv2.inpaint(rgb, masker, 5, cv2.INPAINT_TELEA)[..., ::-1].astype(float)
    C[~(oud | (R & (ma < 128)))] = m[..., :3][~(oud | (R & (ma < 128)))]

    if methode == 'kopie':
        o = O.astype(float)
        Z = zoom_kleur(O)
        oc = o[..., :3].copy(); oc[Z] = LIJN
        nieuw = C.copy()
        band = R & (d < Wl + 2.5)
        nieuw[band] = oc[band]
        a_new = ma.copy()
        a_new[band] = np.where(Z[band], np.minimum(o[..., 3][band], 60), o[..., 3][band])
    else:
        nieuw = C * (1 - w[..., None]) + LIJN * w[..., None]
        if methode == 'meng':
            ln = (nieuw * [.3, .59, .11]).sum(-1)
            donkerder = (lum(M) < ln) & (ma > 200) & ~zoom_kleur(M)
            nieuw[donkerder] = m[..., :3][donkerder]
        a_new = dek * 255.0
        # binnen het hoofd verder dan de rand: Mkuki-dekking houden
        a_new = np.where(d > 1.5, np.maximum(a_new, ma), a_new)

    uit = m.copy()
    k = Rz[..., None]
    uit[..., :3] = m[..., :3] * (1 - k) + nieuw * k
    uit[..., 3] = ma * (1 - Rz) + a_new * Rz
    # gaatjes binnen in het hoofd (buiten R, bv. midden op de schedel)
    if keep is not None:
        binnen = keep & ~R & S
        uit[binnen, :3] = C[binnen]; uit[binnen, 3] = 255
    leeg = (uit[..., 3] < 1) & R
    uit[leeg] = 0
    out = uit.round().clip(0, 255).astype(np.uint8)
    return out, dict(bron=bron, gem=round(float(gem), 2), kop=int(kop), D=round(float(D), 2), R=R, S=S, d=d, h=h)
