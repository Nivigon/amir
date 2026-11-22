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
sys.path.insert(0, HIER); sys.path.insert(0, os.path.join(os.path.dirname(HIER)))
ROOT = os.path.dirname(os.path.dirname(HIER))
import raster, uitlijn
from stokweg import stok_maskers

A = os.path.join(ROOT, 'karakters/amir/')
JUMP = ['amirjump0staand', 'amirjump1hurk', 'amirjump2afzet', 'amirjump3stijgen', 'amirjump4top', 'amirjump5vallen', 'amirjump6landing']
WERK = '/home/claude/werk/'
REF = WERK + 'een/ref_anker_mag.png'
REF_RAW = WERK + 'een/ref_hulp_raw.png'
HULP = {1: (0, 192, 64), 2: (32, 80, 255), 3: (255, 224, 0)}
KAART = {1: (0, 255, 0), 2: (0, 0, 255), 3: (255, 255, 0), 4: (255, 255, 255), 5: (255, 128, 0)}
# Tau-kleuren (uit het origineel: vacht 218,180,139; broek 88,67,105; krassen in vachtkleur, iets lichter)
TAU = {1: (218, 180, 139), 2: (88, 67, 105), 3: (226, 196, 150)}
WIT = {1: (236, 232, 224), 2: (70, 74, 96), 3: (226, 222, 214)}          # witte leeuw, broek leisteen
ZWART = {1: (48, 44, 46), 2: (40, 34, 44), 3: (214, 170, 60)}           # zwarte leeuw met goud
VREF = {1: 0.71, 2: 0.74, 3: 0.95}


HERSTEL = {('rennen', 3): '/home/claude/werk/rennen_03_fix.png'}   # rennen_03: gat in de broek gerepareerd (Grok)


def pad(set_, i, echt=False):
    if not echt and (set_, i) in HERSTEL and os.path.exists(HERSTEL[(set_, i)]):
        return HERSTEL[(set_, i)]
    if set_ in ('staan', 'rennen'):
        return A + 'stokken/%s/%s_%02d.png' % (set_, set_, i)
    if set_ == 'jump':
        return A + 'beweging/jump/jump/%s.png' % JUMP[i]
    if set_ == 'rol':
        return A + 'beweging/rol/zonder/rol_%d.png' % i
    raise ValueError(set_)


def uitpad(set_, i, extra=''):
    p = pad(set_, i, echt=True).replace(A, A + 'tau1/')
    return p[:-4] + extra + '.png'


MET_STOK = os.environ.get('MET_STOK') == '1'


def bron(set_, i, invoer=False):
    """(origineel, stokmaskers, lijf zonder stokken): het lijf is wat Grok krijgt en waarop we uitlijnen."""
    if set_ not in ('staan', 'rennen'):
        o = raster.laad(pad(set_, i))
        return o, [], o.copy()
    fr, ms, _ = stok_maskers(set_, i)
    if invoer and MET_STOK:
        return fr, ms, fr.copy()
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
    dicht = nd.binary_closing(lijf, structure=np.ones((3, 3)), iterations=11) & weg & ~lijf
    out = np.zeros_like(b)
    out[lijf] = b[lijf]
    if dicht.any():
        _, (iy, ix) = nd.distance_transform_edt(~lijf, return_indices=True)
        out[dicht] = b[iy[dicht], ix[dicht]]; out[dicht, 3] = 255
    vol = out[..., 3] > 100
    gat = nd.binary_fill_holes(vol) & ~vol
    if gat.any():
        _, (iy, ix) = nd.distance_transform_edt(~vol, return_indices=True)
        out[gat] = out[iy[gat], ix[gat]]; out[gat, 3] = 255
    return fr, ms, out


def bouw(naam, set_, i, draai=False, refgroot=520):
    _, _, a = bron(set_, i, invoer=True)
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
    json.dump({'set': set_, 'i': i, 'draai': draai, 'metstok': MET_STOK and set_ in ('staan', 'rennen'), 's': s, 'px': px, 'py': py}, open(WERK + naam + '.json', 'w'))


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
    fo, _, o = bron(m['set'], m['i'])
    if m.get('metstok'):
        o = fo
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
    # paarse zweem (magenta-spill van Grok, vooral in de schaduw onder de kap) naar donker bruin
    pz = (z == 0) & (a[..., 3] > 0) & (H > 250) & (H < 335) & (S > 0.2)
    if pz.any():
        out[pz, :3] = np.array([0.55, 0.36, 0.30])[None] * (V[pz, None] * 255)
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
    if m.get('metstok'):
        # de stokken die Grok overtekende weg (de originele komen er in schrijf weer overheen)
        import stok_variant as sv
        fr, ms, lijf = bron(m['set'], m['i'])
        alle = np.zeros(out.shape[:2], bool)
        for w in ms:
            alle |= w
        band = nd.binary_dilation(alle, iterations=7)
        S2 = sv.stokkleur(out.astype(int))
        kern = nd.binary_erosion(lijf[..., 3] > 100, iterations=3)
        weg = band & S2 & ~kern
        out[weg] = 0
        # de vuisten uit het origineel: binnen de band, waar het origineel lijf (geen stok) is en Grok een hand tekende
        r_, g_, b_ = [fr[..., c].astype(int) for c in range(3)]
        oker = alle & (r_ > 95) & (g_ > 55) & (g_ < 120) & (b_ < 60) & (r_ - b_ > 60)
        bij = nd.binary_dilation(oker, iterations=12)
        hand = bij & (fr[..., 3] > 100) & ~alle & (out[..., 3] > 0)
        out[hand] = fr[hand]
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


# ---- de kap los: alleen kop en schouders naar Grok, de kap eruit knippen en op het origineel zetten ----
def bouw_kop(naam, set_, i, box, refgroot=420):
    o = raster.laad(pad(set_, i))
    x0, y0, x1, y1 = box
    c = o[y0:y1, x0:x1]
    s = min(940 / c.shape[0], 1000 / c.shape[1])
    im = Image.fromarray(c).resize((int(c.shape[1] * s), int(c.shape[0] * s)), Image.LANCZOS)
    ref = Image.open(REF); r = refgroot / ref.height; ref = ref.resize((int(ref.width * r), refgroot), Image.LANCZOS)
    C = Image.new('RGB', (1650, 1100), (255, 0, 255))
    C.paste(ref, (20, 20))
    px = 1100 - im.width // 2; py = 80 + (940 - im.height) // 2
    C.paste(Image.fromarray(raster.op_magenta(np.asarray(im))), (px, py))
    C.save(WERK + naam + '.png')
    json.dump({'set': set_, 'i': i, 'box': box, 's': s, 'px': px, 'py': py, 'w': im.width, 'h': im.height, 'kop': True},
              open(WERK + naam + '.json', 'w'))


def terug_kop(naam, bereik=30):
    """Grok-uitvoer (1650 breed) terug naar het crop-vak van het origineel, uitgelijnd op IoU (schaal en schuif)."""
    m = json.load(open(WERK + naam + '.json'))
    g = np.asarray(Image.open(WERK + naam + '_grok.png').convert('RGB'))
    g = np.asarray(Image.fromarray(g).resize((1650, round(g.shape[0] * 1650 / g.shape[1])), Image.LANCZOS))
    k = raster.key(g)
    o = raster.laad(pad(m['set'], m['i']))
    x0, y0, x1, y1 = m['box']
    oc = o[y0:y1, x0:x1]
    best = None
    for f in np.linspace(0.94, 1.06, 7):
        s = m['s'] * f
        # vak in Grok rond de plek van het crop, ruim
        gx0, gy0 = int(m['px'] - 60), int(m['py'] - 60)
        gx1, gy1 = int(m['px'] + m['w'] + 60), int(m['py'] + m['h'] + 60)
        st = k[max(0, gy0):gy1, max(0, gx0):gx1]
        kl = np.asarray(Image.fromarray(st).resize((round(st.shape[1] / s), round(st.shape[0] / s)), Image.LANCZOS))
        # kl op een doek in crop-coordinaten: linksboven van st hoort bij crop (gx0-px)/s
        ox, oy = round((max(0, gx0) - m['px']) / s), round((max(0, gy0) - m['py']) / s)
        doek = np.zeros_like(oc)
        H, W = oc.shape[:2]
        for yy in range(kl.shape[0]):
            ty = yy + oy
            if 0 <= ty < H:
                xs_ = np.arange(kl.shape[1]) + ox
                ok = (xs_ >= 0) & (xs_ < W)
                doek[ty, xs_[ok]] = kl[yy, ok]
        b, dx, dy, v = uitlijn.lijn_uit(doek, oc, bereik)
        if best is None or v > best[3]:
            best = (b, dx, dy, v, f)
    b, dx, dy, v, f = best
    vol = np.zeros_like(o); vol[y0:y1, x0:x1] = b
    np.save(WERK + naam + '.npy', vol)
    print(naam, 'kop IoU', round(v, 3), 'dx', dx, 'dy', dy, 'f', round(f, 3))
    return vol


VREF_ORIG = {1: 0.85, 2: 0.41}      # V van de vacht en de broek in de originele frames (gemeten op staan_00)


def orig_zones(o):
    """Vacht (beige) en broek (paars) in een origineel frame."""
    r, g, b = [o[..., c].astype(int) for c in range(3)]
    al = o[..., 3] > 40
    H, S, V = hsv(o[..., :3])
    z = np.zeros(o.shape[:2], np.uint8)
    vacht = al & (r > 110) & (g > 75) & (r - b > 30) & (S < 0.55) & (V > 0.45) & (H > 15) & (H < 45)
    broek = al & (H > 222) & (H < 305) & (S > 0.12) & (V > 0.1)
    z[vacht] = 1; z[broek] = 2
    for k in (1, 2):
        m = z == k; lab, n = nd.label(m)
        if n:
            sz = nd.sum(m, lab, range(1, n + 1))
            z[np.isin(lab, [i + 1 for i in range(n) if sz[i] < 6])] = 0
    return z


def kop_plak(naam, kopzone_extra=0):
    """Het origineel met de kap uit de Grok-kop erop. Geeft (beeld in Tau-look zonder krassen, zones)."""
    m = json.load(open(WERK + naam + '.json'))
    vol = np.load(WERK + naam + '.npy')
    o = raster.laad(pad(m['set'], m['i']))
    zk = zones(vol)
    kap = (zk == 1) | (zk == 4) | (zk == 5)
    lab, n = nd.label(kap)
    if n:
        sz = nd.sum(kap, lab, range(1, n + 1))
        kap = np.isin(lab, [i + 1 for i in range(n) if sz[i] > 0.05 * sz.max()])
    from skimage.morphology import convex_hull_image
    K = convex_hull_image(kap) | nd.binary_dilation(kap, iterations=1 + kopzone_extra)
    K &= ~nd.binary_dilation(zones(vol) == 2, iterations=2)      # Grok-broek (blauw) nooit: daar blijft het origineel
    out = o.copy()
    out[K] = vol[K]
    z = orig_zones(o)
    z[K] = 0
    zk2 = zones(vol)
    z[K & (zk2 > 0)] = zk2[K & (zk2 > 0)]
    # randjes: wat in K van het origineel overbleef buiten het Grok-silhouet weg
    out[K & (vol[..., 3] < 30)] = 0
    return out, z, K


# ---- de krassen: twee korte schuine halen op de dij van het been dichtst bij de camera ----
# per frame de dij van dat been (heup -> knie) in pixels van het frame; met de hand afgelezen op een raster
DIJ = json.load(open(os.path.join(HIER, 'dij.json'))) if os.path.exists(os.path.join(HIER, 'dij.json')) else {}
KRAS = {'t': 0.5, 'hoek': 55, 'lang': 0.5, 'min': 20, 'max': 29, 'tussen': 7.0, 'dik': 3.8, 'boog': 0.09}


def krassen(set_, i, broek, k=6):
    """Masker (H x W, float 0..1) met twee klauwkrassen zoals op de referentie (post 3e331009): lang, sikkelvormig,
    spits aan beide einden, licht gebogen, evenwijdig, schuin over de dij. Binnen de broek."""
    from PIL import ImageDraw
    key = '%s_%d' % (set_, i)
    if key not in DIJ:
        return None
    (hx, hy), (kx, ky) = DIJ[key][:2]
    H, W = broek.shape
    big = Image.new('L', (W * k, H * k), 0); d = ImageDraw.Draw(big)
    ax, ay = kx - hx, ky - hy; L = np.hypot(ax, ay); ux, uy = ax / L, ay / L
    cx, cy = hx + ax * KRAS['t'], hy + ay * KRAS['t']
    dt = nd.distance_transform_edt(broek)
    yy, xx = np.mgrid[0:H, 0:W]
    afst = np.hypot(xx - cx, yy - cy)
    sk = DIJ[key][3] if len(DIJ[key]) > 3 else 1.0
    score = np.minimum(dt, 8 * sk) - 0.3 * afst
    score[afst > (DIJ[key][2] if len(DIJ[key]) > 2 else 16)] = -99
    cy, cx = np.unravel_index(np.argmax(score), score.shape)
    sk = DIJ[key][3] if len(DIJ[key]) > 3 else 1.0
    ln0 = float(np.clip(L * KRAS['lang'], KRAS['min'] * sk, KRAS['max'] * sk)); ln = ln0
    a = np.radians(KRAS['hoek'])
    dx, dy = ux * np.cos(a) - uy * np.sin(a), ux * np.sin(a) + uy * np.cos(a)
    if dy < 0:
        dx, dy = -dx, -dy
    nx, ny = -dy, dx
    KRAS_LAATST.update({'x': int(cx), 'y': int(cy), 'hoek': round(float(np.degrees(np.arctan2(dy, dx))), 1), 'lang': round(ln, 1),
                        'tussen': KRAS['tussen'], 'dik': KRAS['dik'], 'boog': KRAS['boog']})
    for s in (-0.5, 0.5):
        mx, my = cx + nx * s * KRAS['tussen'] * sk, cy + ny * s * KRAS['tussen'] * sk
        boven, onder = [], []
        for t in np.linspace(-0.5, 0.5, 21):
            w = KRAS['dik'] * sk * (1 - (2 * abs(t)) ** 1.8) / 2
            bo = KRAS['boog'] * ln * (1 - (2 * t) ** 2)
            px, py = mx + dx * t * ln + nx * bo, my + dy * t * ln + ny * bo
            boven.append(((px + nx * w) * k, (py + ny * w) * k)); onder.append(((px - nx * w) * k, (py - ny * w) * k))
        d.polygon(boven + onder[::-1], fill=255)
    m = np.asarray(big.resize((W, H), Image.LANCZOS)).astype(float) / 255
    return m * nd.binary_erosion(broek, iterations=1)


KRAS_LAATST = {}
_kp = os.path.join(A, 'tau1', 'krassen_plaatsing.json')
KRAS_PLAATS = json.load(open(_kp)) if os.path.exists(_kp) else {}
TAU_KRAS = (208, 162, 108)   # goudbeige zoals op de referentie
PALET = {'tau': TAU, 'wit': WIT, 'zwart': ZWART}


def maak(naam, set_, i):
    """Eindframe: origineel + kap (Grok) + krassen (getekend) + stokken (origineel). Schrijft spelbeeld, zones en
    voorbeeld-recolours; geeft dict met de beelden."""
    beeld, z, K = kop_plak(naam)
    o = raster.laad(pad(set_, i))
    H, S, V = hsv(beeld[..., :3])
    # paarse zweem in de kap (schaduw onder de kap) naar donkerbruin
    pz = K & (z == 0) & (beeld[..., 3] > 0) & (H > 250) & (H < 335) & (S > 0.2)
    beeld[pz, :3] = (np.array([0.55, 0.36, 0.30])[None] * (V[pz, None] * 255)).astype(np.uint8)
    Vrel = np.zeros(z.shape)
    Vrel[(z == 1) & K] = V[(z == 1) & K] / VREF[1]
    Vrel[(z == 1) & ~K] = V[(z == 1) & ~K] / VREF_ORIG[1]
    Vrel[z == 2] = V[z == 2] / VREF_ORIG[2]
    zonder_kras = None
    m = krassen(set_, i, z == 2)
    if m is not None:
        z[m > 0.5] = 3
        Vrel[m > 0] = np.clip(V[m > 0] / VREF_ORIG[2], 0.92, 1.08)
    Vrel = np.clip(Vrel, 0, 1.3)
    uit = {}
    for pn, pal in PALET.items():
        b = beeld.copy().astype(float)
        for zk in (1, 2):
            sel = (z == zk) & (K if (pn == 'tau' and zk == 1) else True)
            if pn == 'tau' and zk == 2:
                continue                                  # de paarse broek blijft het origineel
            b[sel, :3] = np.array(pal[zk], float)[None] * Vrel[sel, None]
        if pn == 'tau':
            zonder_kras = np.clip(b, 0, 255).astype(np.uint8)
        if m is not None:
            # een donkere rand om de krassen (de gescheurde stof), zoals op de referentie
            rand = np.clip(nd.maximum_filter(m, size=3 if set_ != 'jump' else 5) - m, 0, 1) * (z == 2)
            b[rand > 0, :3] = b[rand > 0, :3] * (1 - 0.55 * rand[rand > 0, None])
            kc = np.array(TAU_KRAS if pn == 'tau' else pal[3], float)
            kl = kc[None] * Vrel[m > 0, None]
            mm = m[m > 0, None]
            b[m > 0, :3] = b[m > 0, :3] * (1 - mm) + kl * mm
            if pn == 'tau':
                pass
        b = np.clip(b, 0, 255).astype(np.uint8)
        uit[pn] = met_stokken(set_, i, b)
    # zones: waar een stok overheen ligt is geen zone
    if set_ in ('staan', 'rennen'):
        _, ms, _ = stok_maskers(set_, i)
        for w in ms:
            z[w] = 0
    zk = np.zeros(z.shape + (4,), np.uint8); zk[..., 3] = uit['tau'][..., 3]
    for k_, c in KAART.items():
        zk[z == k_, :3] = c
    uit['zones'] = zk
    p = uitpad(set_, i)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    # krassen als losse laag (Tom 02:56): het spelbeeld zonder krassen, de krassen apart
    uit['metkras'] = uit['tau']
    uit['tau'] = met_stokken(set_, i, zonder_kras)
    kd = os.path.join(os.path.dirname(p), 'krassen')
    os.makedirs(kd, exist_ok=True)
    if m is not None:
        laag = np.zeros(m.shape + (4,), np.uint8)
        kc = np.array(TAU_KRAS, float)
        laag[..., :3] = np.clip(kc[None, None] * Vrel[..., None].clip(0.92, 1.08), 0, 255).astype(np.uint8)
        rand = np.clip(nd.maximum_filter(m, size=3) - m, 0, 1)
        laag[..., :3] = (laag[..., :3] * (1 - (rand > 0)[..., None]) + np.array([40, 26, 44]) * (rand > 0)[..., None]).astype(np.uint8)
        laag[..., 3] = (np.clip(m + 0.55 * rand, 0, 1) * 255).astype(np.uint8)
        Image.fromarray(laag).save(os.path.join(kd, os.path.basename(uitpad(set_, i, '_kras'))))
        Image.fromarray(uit['metkras']).save(os.path.join(kd, os.path.basename(uitpad(set_, i, '_voorbeeld'))))
        KRAS_PLAATS['%s_%d' % (set_, i)] = KRAS_LAATST.copy()
        json.dump(KRAS_PLAATS, open(os.path.join(A, 'tau1', 'krassen_plaatsing.json'), 'w'), indent=1)
    Image.fromarray(uit['tau']).save(p)
    Image.fromarray(zk).save(uitpad(set_, i, '_zones'))
    vd = os.path.join(os.path.dirname(p), 'recolour')
    os.makedirs(vd, exist_ok=True)
    for pn in ('wit', 'zwart'):
        Image.fromarray(uit[pn]).save(os.path.join(vd, os.path.basename(uitpad(set_, i, '_' + pn))))
    return uit
