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
    """Robuust: grootste figuur (niet het voorbeeld), schaal en plek zoeken op IoU met het origineel."""
    m = json.load(open(naam + '.json'))
    g = Image.open(naam + '_grok.png').convert('RGB')
    k = raster.key(np.asarray(g))
    al = k[..., 3] > 60
    lab, n = nd.label(al)
    sz = nd.sum(al, lab, range(1, n + 1))
    kandidaten = [i + 1 for i in np.argsort(-sz)[:3] if sz[i] > 0.15 * sz.max()]
    k0 = k.copy()
    o = raster.laad(m['pad'])
    from speer_meet import override
    if m['speer']:
        o, _ = raster.zonder_speer(o, override(m['pad']))
    if m['draai']:
        o = o[::-1, ::-1].copy()
    vacht = nd.binary_dilation(afwerk._vacht(o) & (o[..., 3] > 40), iterations=3)
    o2 = o.copy(); o2[vacht, 3] = 0
    H, W = o.shape[:2]
    oy, ox = np.where(o2[..., 3] > 60)
    oh, ow = oy.max() - oy.min() + 1, ox.max() - ox.min() + 1
    res = None
    for kid in kandidaten:
      kk = k0.copy(); kk[~nd.binary_dilation(lab == kid, iterations=3)] = 0
      ys, xs = np.where(kk[..., 3] > 60)
      fig = kk[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
      for f in np.linspace(0.9, 1.1, 9):
          nh = int(round(oh * f)); nw = int(round(fig.shape[1] * nh / fig.shape[0]))
          im = np.asarray(Image.fromarray(fig).resize((nw, nh), Image.LANCZOS))
          doek = np.zeros_like(o)
          cy = int(oy.min() + oh / 2 - nh / 2); cx = int(ox.min() + ow / 2 - nw / 2)
          y0, x0 = max(0, cy), max(0, cx); y1, x1 = min(H, cy + nh), min(W, cx + nw)
          doek[y0:y1, x0:x1] = im[y0 - cy:y1 - cy, x0 - cx:x1 - cx]
          b, dx, dy, v = uitlijn.lijn_uit(doek, o2, 40)
          if res is None or v > res[3]:
              res = (b, dx, dy, v, f)
    b, dx, dy, v, f = res
    if m['draai']:
        b = b[::-1, ::-1].copy()
        mm = (o2[..., 3] > 128)[::-1, ::-1]
    else:
        mm = o2[..., 3] > 128
    np.save(naam + '.npy', b)
    print(os.path.basename(m['pad']), dx, dy, round(f, 3), round(v, 3))
    r = mm ^ nd.binary_erosion(mm); c = b.copy(); c[r] = [255, 255, 255, 255]
    ys, xs = np.where((c[..., 3] > 0))
    Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).resize(((xs.max() - xs.min() + 1) * 2, (ys.max() - ys.min() + 1) * 2), Image.NEAREST).save(naam + '_vergelijk.png')
    return v


if __name__ == '__main__':
    if sys.argv[1] == 'bouw':
        bouw(sys.argv[2], sys.argv[3])
    else:
        terug(sys.argv[2])
