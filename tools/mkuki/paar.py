"""Een frame alleen, groot, met de omgekleurde referentie klein linksboven als kostuumvoorbeeld.

python3 paar.py bouw werk/naam pad      -> werk/naam.png + .json
python3 paar.py terug werk/naam [pad]   -> werk/naam.npy (uitgelijnd op het eigen canvas), print IoU
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster, uitlijn, afwerk
from PIL import Image
from scipy import ndimage as nd
REF = '/home/claude/werk/een/ref_hulp.png'


def bouw(naam, pad):
    a = raster.laad(pad)
    from speer_meet import override
    if '_ns' not in os.path.basename(pad) and 'idle_ns' not in pad and '/zonder/' not in pad and '/jump/jump/' not in pad and '/bukken/bukken/' not in pad and 'sluipen_' + '' not in pad[-14:-6]:
        pass
    sp = json.load(open(naam + '.spec')) if os.path.exists(naam + '.spec') else {}
    if sp.get('speer'):
        a, _ = raster.zonder_speer(a, override(pad))
    if sp.get('draai'):
        a = a[::-1, ::-1].copy()
    ref = Image.open(REF); s = 520 / ref.height; ref = ref.resize((int(ref.width * s), 520), Image.LANCZOS)
    ys, xs = np.where(a[..., 3] > 30); x0, y0 = int(xs.min()), int(ys.min())
    c = a[y0:ys.max() + 1, x0:xs.max() + 1]
    s = min(980 / c.shape[0], 1050 / c.shape[1])
    im = Image.fromarray(c).resize((int(c.shape[1] * s), int(c.shape[0] * s)), Image.LANCZOS)
    C = Image.new('RGB', (1650, 1100), (255, 0, 255))
    C.paste(Image.fromarray(raster.op_magenta(np.asarray(ref))), (40, 40))
    px = 1050 - im.width // 2; py = 60 + (980 - im.height) // 2
    C.paste(Image.fromarray(raster.op_magenta(np.asarray(im))), (px, py))
    C.save(naam + '.png')
    json.dump({'pad': pad, 's': s, 'px': px, 'py': py, 'x0': x0, 'y0': y0, 'w': im.width, 'h': im.height,
               'speer': sp.get('speer', False), 'draai': sp.get('draai', False)}, open(naam + '.json', 'w'))


def terug(naam):
    m = json.load(open(naam + '.json'))
    g = Image.open(naam + '_grok.png').convert('RGB').resize((1650, 1100), Image.LANCZOS)
    k = raster.key(np.asarray(g))
    k[:600, :520] = 0  # het voorbeeld weg
    o = raster.laad(m['pad'])
    from speer_meet import override
    if m['speer']:
        o, _ = raster.zonder_speer(o, override(m['pad']))
    if m['draai']:
        o = o[::-1, ::-1].copy()
    H, W = o.shape[:2]
    s = m['s']
    big = Image.fromarray(k).resize((int(round(1650 / s)), int(round(1100 / s))), Image.LANCZOS)
    a = np.asarray(big)
    sx = m['x0'] - int(round(m['px'] / s)); sy = m['y0'] - int(round(m['py'] / s))
    doek = np.zeros_like(o); ah, aw = a.shape[:2]
    ys0 = max(0, sy); xs0 = max(0, sx); ys1 = min(H, sy + ah); xs1 = min(W, sx + aw)
    doek[ys0:ys1, xs0:xs1] = a[ys0 - sy:ys1 - sy, xs0 - sx:xs1 - sx]
    # alleen de grootste figuur houden
    al = doek[..., 3] > 60; lab, n = nd.label(al)
    if n > 1:
        sz = nd.sum(al, lab, range(1, n + 1)); keep = nd.binary_dilation(lab == np.argmax(sz) + 1, iterations=2)
        doek[~keep] = 0
    vacht = nd.binary_dilation(afwerk._vacht(o) & (o[..., 3] > 40), iterations=3)
    o2 = o.copy(); o2[vacht, 3] = 0
    b, dx, dy, v = uitlijn.lijn_uit(doek, o2, 30)
    if m['draai']:
        b = b[::-1, ::-1].copy()
    np.save(naam + '.npy', b)
    print(os.path.basename(m['pad']), dx, dy, round(v, 3))
    oo = raster.laad(m['pad'])
    mm = o2[..., 3] > 128
    if m['draai']:
        mm = mm[::-1, ::-1]
    r = mm ^ nd.binary_erosion(mm); c = b.copy(); c[r] = [255, 255, 255, 255]
    ys, xs = np.where((c[..., 3] > 0) | (oo[..., 3] > 0))
    Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).resize(((xs.max() - xs.min() + 1) * 2, (ys.max() - ys.min() + 1) * 2), Image.NEAREST).save(naam + '_vergelijk.png')
    return v


if __name__ == '__main__':
    if sys.argv[1] == 'bouw':
        bouw(sys.argv[2], sys.argv[3])
    else:
        terug(sys.argv[2])
