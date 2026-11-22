"""Tau niveau 1 (jonge leeuw) op de stokken-Amir: bron, Grok-invoer, terugzetten, afwerken, zones en omkleuren.

Sets (het spel tekent met de stokken):
  staan   karakters/amir/stokken/staan/staan_00.png        (stokken erin gebakken)
  rennen  karakters/amir/stokken/rennen/rennen_NN.png      (12, stokken erin gebakken)
  jump    karakters/amir/beweging/jump/jump/amirjumpN*.png (7, geen stokken: het spel tekent ze niet in de sprong)
  rol     karakters/amir/beweging/rol/zonder/rol_N.png     (28, geen stokken)

Hulpkleuren (Grok): kap + vacht groen #00C040, broek blauw #2050FF, krassen geel #FFE000.
Zones in de zonekaart: 1 vacht/kap (0,255,0), 2 broek (0,0,255), 3 krassen (255,255,0), 4 tanden (255,255,255), 5 ogen (255,128,0).

python3 tau.py bouw NAAM SET I      -> werk/NAAM.png (Grok-invoer) + .json
python3 tau.py terug NAAM           -> werk/NAAM.npy (uitgelijnd op het eigen canvas), print IoU, NAAM_vergelijk.png
python3 tau.py klaar NAAM [--voeten] [--draai]  -> werk/klaar/SET_I.npz (hulp, zones), print zonetelling
"""
import sys, os, json, glob
import numpy as np
from PIL import Image
from scipy import ndimage as nd
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
ROOT = os.path.dirname(os.path.dirname(HIER))
import raster, uitlijn
from stokweg import stok_maskers

A = os.path.join(ROOT, 'karakters/amir/')
JUMP = ['amirjump0staand', 'amirjump1hurk', 'amirjump2afzet', 'amirjump3stijgen', 'amirjump4top', 'amirjump5vallen', 'amirjump6landing']
WERK = '/home/claude/werk/'
REF = WERK + 'een/ref_hulp_mag.png'
REF_RAW = WERK + 'een/ref_hulp_raw.png'
HULP = {1: (0, 192, 64), 2: (32, 80, 255), 3: (255, 224, 0)}
KAART = {1: (0, 255, 0), 2: (0, 0, 255), 3: (255, 255, 0), 4: (255, 255, 255), 5: (255, 128, 0)}
# Tau-kleuren (uit het origineel: vacht 218,180,139; broek 88,67,105; krassen in vachtkleur, iets lichter)
TAU = {1: (218, 180, 139), 2: (88, 67, 105), 3: (226, 196, 150)}
WIT = {1: (236, 232, 224), 2: (70, 74, 96), 3: (240, 238, 232)}          # witte leeuw, broek leisteen
ZWART = {1: (48, 44, 46), 2: (40, 34, 44), 3: (214, 170, 60)}           # zwarte leeuw met goud
VREF = {1: 0.71, 2: 0.74, 3: 0.95}


def pad(set_, i):
    if set_ in ('staan', 'rennen'):
        return A + 'stokken/%s/%s_%02d.png' % (set_, set_, i)
    if set_ == 'jump':
        return A + 'beweging/jump/jump/%s.png' % JUMP[i]
    if set_ == 'rol':
        return A + 'beweging/rol/zonder/rol_%d.png' % i
    raise ValueError(set_)


def uitpad(set_, i, extra=''):
    p = pad(set_, i).replace(A, A + 'tau1/')
    return p[:-4] + extra + '.png'


def bron(set_, i):
    """(origineel, stokmaskers, lijf zonder stokken): het lijf is wat Grok krijgt en waarop we uitlijnen."""
    if set_ not in ('staan', 'rennen'):
        o = raster.laad(pad(set_, i))
        return o, [], o.copy()
    fr, ms, _ = stok_maskers(set_, i)
    if set_ == 'staan':
        # het echte lijf zonder stokken uit de Animeer tool (594x301, anker 297, grond 297) op het spelcanvas
        l = raster.laad(A + 'stokken/bron/lijf/staan_00.png')
        out = np.zeros_like(fr); h, w = l.shape[:2]
        dx, dy = 298 - 297, 379 - 297
        out[dy:dy + h, dx:dx + w] = l[:min(h, fr.shape[0] - dy), :min(w, fr.shape[1] - dx)]
        return fr, ms, out
    weg = np.zeros(fr.shape[:2], bool)
    for m in ms:
        weg |= m
    weg = nd.binary_dilation(weg, iterations=2)
    b = fr.copy(); b[weg, 3] = 0
    # halfdoorzichtige randjes en sliertjes van de stok weg
    b[b[..., 3] < 140, 3] = 0
    lijf = b[..., 3] > 100
    kern = nd.binary_opening(lijf, iterations=2)
    lab, n = nd.label(kern)
    if n:
        sz = nd.sum(kern, lab, range(1, n + 1))
        kern = np.isin(lab, [k + 1 for k in range(n) if sz[k] > 0.02 * sz.max()])
    lijf = lijf & nd.binary_dilation(kern, iterations=2)
    # gaten waar de stok over het lijf liep dichten met de dichtstbijzijnde lijfkleur
    dicht = nd.binary_closing(lijf, structure=np.ones((3, 3)), iterations=6) & weg & ~lijf
    out = np.zeros_like(b)
    out[lijf] = b[lijf]
    if dicht.any():
        _, (iy, ix) = nd.distance_transform_edt(~lijf, return_indices=True)
        out[dicht] = b[iy[dicht], ix[dicht]]; out[dicht, 3] = 255
    return fr, ms, out


def bouw(naam, set_, i, draai=False, refgroot=520):
    _, _, a = bron(set_, i)
    if draai:
        a = a[::-1, ::-1].copy()
    ref = Image.open(REF); s = refgroot / ref.height; ref = ref.resize((int(ref.width * s), refgroot), Image.LANCZOS)
    ys, xs = np.where(a[..., 3] > 30); x0, y0 = int(xs.min()), int(ys.min())
    c = a[y0:ys.max() + 1, x0:xs.max() + 1]
    s = min(980 / c.shape[0], 1050 / c.shape[1])
    im = Image.fromarray(c).resize((int(c.shape[1] * s), int(c.shape[0] * s)), Image.LANCZOS)
    C = Image.new('RGB', (1650, 1100), (255, 0, 255))
    C.paste(ref, (0, 0))
    px = 1050 - im.width // 2; py = 60 + (980 - im.height) // 2
    C.paste(Image.fromarray(raster.op_magenta(np.asarray(im))), (px, py))
    C.save(WERK + naam + '.png')
    json.dump({'set': set_, 'i': i, 'draai': draai, 's': s, 'px': px, 'py': py}, open(WERK + naam + '.json', 'w'))


def haal(naam, sleutel, breed=None):
    """Het laatst bewaarde schermbeeld met dit stukje in de naam als NAAM_grok.png."""
    f = sorted(glob.glob('/tmp/claude-tool-results/*/*' + sleutel + '*'))[-1]
    im = Image.open(f).convert('RGB')
    if breed:
        im = im.resize((breed, round(im.height * breed / im.width)), Image.LANCZOS)
    im.save(WERK + naam + '_grok.png')


def terug(naam, bereik=40, schaal=(0.88, 1.12, 13)):
    m = json.load(open(WERK + naam + '.json'))
    g = np.asarray(Image.open(WERK + naam + '_grok.png').convert('RGB'))
    k = raster.key(g)
    al = k[..., 3] > 60
    lab, n = nd.label(al)
    sz = nd.sum(al, lab, range(1, n + 1))
    kand = [i + 1 for i in np.argsort(-sz)[:3] if sz[i] > 0.15 * sz.max()]
    cm = nd.center_of_mass(al, lab, kand)
    kand = [kid for kid, (cy, cx) in zip(kand, cm) if not (cx < 0.25 * al.shape[1] and cy < 0.5 * al.shape[0])] or kand
    _, _, o = bron(m['set'], m['i'])
    if m['draai']:
        o = o[::-1, ::-1].copy()
    H, W = o.shape[:2]
    oy, ox = np.where(o[..., 3] > 60)
    oh, ow = oy.max() - oy.min() + 1, ox.max() - ox.min() + 1
    res = None
    for kid in kand:
        kk = k.copy(); kk[~nd.binary_dilation(lab == kid, iterations=3)] = 0
        ys, xs = np.where(kk[..., 3] > 60)
        fig = kk[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        for f in np.linspace(*schaal):
            nh = int(round(oh * f)); nw = int(round(fig.shape[1] * nh / fig.shape[0]))
            im = np.asarray(Image.fromarray(fig).resize((nw, nh), Image.LANCZOS))
            doek = np.zeros_like(o)
            cy = int(oy.min() + oh / 2 - nh / 2); cx = int(ox.min() + ow / 2 - nw / 2)
            y0, x0 = max(0, cy), max(0, cx); y1, x1 = min(H, cy + nh), min(W, cx + nw)
            doek[y0:y1, x0:x1] = im[y0 - cy:y1 - cy, x0 - cx:x1 - cx]
            b, dx, dy, v = uitlijn.lijn_uit(doek, o, bereik)
            if res is None or v > res[3]:
                res = (b, dx, dy, v, f)
    b, dx, dy, v, f = res
    mm = o[..., 3] > 128
    if m['draai']:
        b = b[::-1, ::-1].copy(); mm = mm[::-1, ::-1]
    np.save(WERK + naam + '.npy', b)
    m['iou'] = round(float(v), 3); json.dump(m, open(WERK + naam + '.json', 'w'))
    print(naam, m['set'], m['i'], 'dx', dx, 'dy', dy, 'schaal', round(f, 3), 'IoU', round(v, 3))
    r = mm ^ nd.binary_erosion(mm); c = b.copy(); c[r] = [255, 0, 255, 255]
    ys, xs = np.where(c[..., 3] > 0)
    c = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    oc = raster.laad(pad(m['set'], m['i']))[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    duo = np.hstack([oc, c])
    Image.fromarray(duo).resize((duo.shape[1] * 2, duo.shape[0] * 2), Image.NEAREST).save(WERK + naam + '_vergelijk.png')
    return v


def hsv(rgb):
    r, g, b = [rgb[..., i].astype(float) / 255 for i in range(3)]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    d = mx - mn; h = np.zeros_like(mx); m = d > 1e-6
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6; h[gm] = (b - r)[gm] / d[gm] + 2; h[bm] = (r - g)[bm] / d[bm] + 4
    return h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx


def zones(a, draai=False):
    """Zonekaart uit een frame in hulpkleuren. draai: frame staat ondersteboven (boven/onder omkeren voor ogen/krassen)."""
    if draai:
        return zones(a[::-1, ::-1])[::-1, ::-1]
    H, S, V = hsv(a[..., :3]); al = a[..., 3] > 40
    z = np.zeros(H.shape, np.uint8)
    z[al & (H >= 80) & (H < 170) & (S > 0.35) & (V > 0.15)] = 1
    z[al & (H >= 195) & (H < 255) & (S > 0.45) & (V > 0.25)] = 2
    geel = al & (H >= 40) & (H < 75) & (S > 0.45) & (V > 0.55)
    oranje = al & (H >= 12) & (H < 45) & (S > 0.45) & (V > 0.5)
    # krassen: geel binnen (of tegen) de broek; ogen: amber/geel boven de broek, tegen of in de kap
    broek = nd.binary_dilation(z == 2, iterations=3)
    z[geel & broek] = 3
    kap = nd.binary_dilation(z == 1, iterations=14)
    ybroek = np.where(z == 2)[0].min() if (z == 2).any() else a.shape[0]
    yy = np.mgrid[0:a.shape[0], 0:a.shape[1]][0]
    z[(geel | oranje) & ~broek & kap & (yy < ybroek)] = 5
    # tanden: licht en kleurloos, tegen de kap aan, boven de broek
    tand = al & (S < 0.3) & (V > 0.72) & nd.binary_dilation(z == 1, iterations=4) & (yy < ybroek)
    z[tand & (z == 0)] = 4
    for k in range(1, 6):
        m = z == k
        lab, n = nd.label(m)
        if n:
            sz = nd.sum(m, lab, range(1, n + 1))
            klein = np.isin(lab, [i + 1 for i in range(n) if sz[i] < (3 if k >= 3 else 8)])
            z[klein] = 0
    return z


def kleur(a, z, pal):
    """Omkleuren: doelkleur * (V / Vref) per pixel in zones 1-3; tanden en ogen blijven."""
    H, S, V = hsv(a[..., :3])
    out = a.copy().astype(float)
    for k, c in pal.items():
        m = z == k
        if not m.any():
            continue
        f = np.clip(V[m] / VREF[k], 0, 1.35)[:, None]
        out[m, :3] = np.clip(np.array(c, float)[None] * f, 0, 255)
    # randpixels van een zone (antialias tegen de zwarte lijn): mee, zodat er geen groene/blauwe zoom blijft
    rest = (z == 0) & (a[..., 3] > 0)
    Hh, Ss, Vv = H, S, V
    zoom = rest & (((Hh >= 80) & (Hh < 170)) | ((Hh >= 195) & (Hh < 255))) & (Ss > 0.2)
    if zoom.any():
        _, (iy, ix) = nd.distance_transform_edt(z == 0, return_indices=True)
        bz = z[iy, ix]
        for k, c in pal.items():
            m = zoom & (bz == k)
            f = np.clip(V[m] / VREF[k], 0, 1.2)[:, None]
            out[m, :3] = np.array(c, float)[None] * f
        # wat geen zone naast zich heeft: grijs maken
        m = zoom & (bz == 0)
        out[m, :3] = V[m, None] * 255 * 0.5
    return out.astype(np.uint8)


def kaart(z, a):
    out = np.zeros(z.shape + (4,), np.uint8)
    out[..., 3] = a[..., 3]
    for k, c in KAART.items():
        out[z == k, :3] = c
    out[(z == 0) & (a[..., 3] > 0), :3] = (0, 0, 0)
    return out


def afwerk(naam, voeten=False):
    m = json.load(open(WERK + naam + '.json'))
    b = np.load(WERK + naam + '.npy')
    o = raster.laad(pad(m['set'], m['i']))
    _, _, ol = bron(m['set'], m['i'])
    out = b.copy()
    # magenta-rand: pixels met nog een paarse zweem aan de rand
    H, S, V = hsv(out[..., :3])
    rand = (out[..., 3] > 0) & ~nd.binary_erosion(out[..., 3] > 128, iterations=2)
    paars = rand & (H > 285) & (H < 335) & (S > 0.25)
    out[paars, 3] = 0
    if voeten:
        # onder de laagste broekrij per kolom het originele lijf (voeten)
        z = zones(out, m['draai'])
        bl = z == 2
        if bl.any():
            yy = np.mgrid[0:bl.shape[0], 0:bl.shape[1]][0]
            laag = nd.maximum_filter((bl * (yy + 1)).astype(int), size=(1, 25)).max(0)
            zone = (laag[None, :] > 0) & (yy > laag[None, :] + 2)
            weg = zone & (out[..., 3] > 0)
            out[weg] = 0
            zet = zone & (ol[..., 3] > 0)
            out[zet] = ol[zet]
    # losse eilanden weg
    al = out[..., 3] > 40
    lab, n = nd.label(al)
    if n > 1:
        sz = nd.sum(al, lab, range(1, n + 1))
        out[np.isin(lab, [i + 1 for i in range(n) if sz[i] < 0.03 * sz.max()])] = 0
    out[~nd.binary_dilation(out[..., 3] > 40, iterations=1)] = 0
    z = zones(out, m['draai'])
    os.makedirs(WERK + 'klaar', exist_ok=True)
    np.savez_compressed(WERK + 'klaar/%s_%d.npz' % (m['set'], m['i']), hulp=out, zones=z)
    print('klaar', m['set'], m['i'], {k: int((z == k).sum()) for k in range(1, 6)})
    return out, z


def met_stokken(set_, i, beeld):
    """De stokken uit het originele frame er weer overheen (alleen waar ze in het origineel te zien waren)."""
    if set_ not in ('staan', 'rennen'):
        return beeld
    fr, ms, _ = stok_maskers(set_, i)
    out = beeld.copy()
    for w in ms:
        w2 = w & (fr[..., 3] > 0)
        o = Image.fromarray(np.where(w2[..., None], fr, 0).astype(np.uint8))
        base = Image.fromarray(out); base.alpha_composite(o); out = np.asarray(base).copy()
    return out


def schrijf(set_, i):
    d = np.load(WERK + 'klaar/%s_%d.npz' % (set_, i))
    hulp, z = d['hulp'], d['zones']
    tau = kleur(hulp, z, TAU)
    os.makedirs(os.path.dirname(uitpad(set_, i)), exist_ok=True)
    if set_ in ('staan', 'rennen'):
        lijfdir = os.path.join(os.path.dirname(uitpad(set_, i)), 'lijf')
        os.makedirs(lijfdir, exist_ok=True)
        Image.fromarray(tau).save(os.path.join(lijfdir, os.path.basename(uitpad(set_, i))))
        Image.fromarray(kaart(z, hulp)).save(os.path.join(lijfdir, os.path.basename(uitpad(set_, i, '_zones'))))
        Image.fromarray(hulp).save(os.path.join(lijfdir, os.path.basename(uitpad(set_, i, '_hulp'))))
    else:
        Image.fromarray(hulp).save(uitpad(set_, i, '_hulp'))
    Image.fromarray(met_stokken(set_, i, tau)).save(uitpad(set_, i))
    Image.fromarray(kaart(z, hulp)).save(uitpad(set_, i, '_zones'))
    return tau


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'bouw':
        bouw(sys.argv[2], sys.argv[3], int(sys.argv[4]), draai='--draai' in sys.argv)
    elif c == 'haal':
        haal(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif c == 'terug':
        terug(sys.argv[2], int(os.environ.get('BEREIK', 40)))
    elif c == 'klaar':
        afwerk(sys.argv[2], voeten='--voeten' in sys.argv)
    elif c == 'schrijf':
        schrijf(sys.argv[2], int(sys.argv[3]))
