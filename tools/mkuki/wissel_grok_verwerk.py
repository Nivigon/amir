"""Grok-beeld (twee tegels) terug naar het Mkuki-frame.

python3 verwerk.py <set_n> <tegel_boven> <tegel_onder>
Tegels: beeld-x 400..1350, boven y 100..750, onder y 600..1150 (op ware grootte van 1728x1152).
"""
import sys, json
sys.path.insert(0, '/home/claude/amir/tools/mkuki')
import numpy as np
from PIL import Image
from raster import key
from scipy import ndimage as nd

naam, t1, t2 = sys.argv[1:4]
meta = json.load(open('/home/claude/g/meta.json'))[naam]
G = np.zeros((1152, 1728, 3), np.uint8); G[:] = (255, 0, 255)
a = np.asarray(Image.open(t1).convert('RGB'))[:650, :950]
b = np.asarray(Image.open(t2).convert('RGB'))[:550, :950]
G[100:100 + a.shape[0], 400:400 + a.shape[1]] = a
G[600 + 50:600 + b.shape[0], 400:400 + b.shape[1]] = b[50:]
Image.fromarray(G).save(f'/home/claude/g/{naam}_grok_vol.png')
# terug naar het invoercanvas 1650x1100
g = Image.fromarray(G).resize((1650, 1100), Image.LANCZOS)
ga = key(np.asarray(g))
oud = np.asarray(Image.open(f'/home/claude/g/in/{naam}_oud.png').convert('RGBA'))
H, W = oud.shape[:2]
bb, sc, ox, oy = meta['bb'], meta['sc'], meta['ox'], meta['oy']
# figuurvak op het invoercanvas
w = round((bb[2] - bb[0]) * sc); h = 760
oa = oud[..., 3] > 100


def plaats(ds, dx, dy):
    s = sc * ds
    x0 = ox + (w - w * ds) / 2 - dx * s; y0 = oy + (h - h * ds) / 2 - dy * s
    # canvas-pixel (cx, cy) in het frame -> invoer (x0 + (cx-bb0)*s, ...)
    cw, ch = W, H
    # eerst netjes verkleinen (LANCZOS, voorvermenigvuldigd), dan alleen verschuiven
    big = Image.fromarray(ga)
    nw, nh = round(1650 / s), round(1100 / s)
    pm = np.asarray(big).astype(float); pm[..., :3] *= pm[..., 3:4] / 255
    kl = np.dstack([np.asarray(Image.fromarray(pm[..., c].astype(np.float32), 'F').resize((nw, nh), Image.LANCZOS)) for c in range(4)])
    fx = 1650 / nw / s; fy = 1100 / nh / s
    tr = (1 / fx, 0, (x0 / s - bb[0]) / fx * 1, 0, 1 / fy, (y0 / s - bb[1]) / fy)
    uit = np.dstack([np.asarray(Image.fromarray(kl[..., c].astype(np.float32), 'F').transform((cw, ch), Image.AFFINE, tr, resample=Image.BILINEAR)) for c in range(4)])
    al = np.clip(uit[..., 3], 0, 255)
    rgb = np.where(al[..., None] > 0, uit[..., :3] * 255 / np.maximum(al[..., None], 1), 0)
    return np.dstack([np.clip(rgb, 0, 255), al]).astype(np.uint8)


beste = None
for ds in [0.97, 0.985, 1.0, 1.015, 1.03]:
    for dx in range(-6, 7, 2):
        for dy in range(-6, 7, 2):
            f = plaats(ds, dx, dy)
            m = f[..., 3] > 100
            iou = (m & oa).sum() / max((m | oa).sum(), 1)
            if beste is None or iou > beste[0]:
                beste = (iou, ds, dx, dy)
iou, ds, dx, dy = beste
for ddx in [-1, 0, 1]:
    for ddy in [-1, 0, 1]:
        f = plaats(ds, dx + ddx, dy + ddy); m = f[..., 3] > 100
        i2 = (m & oa).sum() / max((m | oa).sum(), 1)
        if i2 > beste[0]:
            beste = (i2, ds, dx + ddx, dy + ddy)
iou, ds, dx, dy = beste
f = plaats(ds, dx, dy).copy()
print(naam, 'IoU', round(iou, 3), ds, dx, dy)
# losse spikkels weg
m = f[..., 3] > 20
lab, n = nd.label(m)
if n > 1:
    sz = nd.sum(m, lab, range(1, n + 1)); k = 1 + int(np.argmax(sz))
    f[(lab != k) & (lab > 0), 3] = 0
Image.fromarray(f).save(f'/home/claude/g/{naam}_nieuw.png')
# zonekaart: per pixel de zone van de dichtstbijzijnde kleur in het oude frame (kleur + plek)
oz = np.asarray(Image.open(f'/home/claude/g/in/{naam}_zones.png').convert('RGB'))
from scipy.spatial import cKDTree
ys, xs = np.where(oa)
feat = np.c_[oud[ys, xs, :3].astype(float), xs * 0.6, ys * 0.6]
tree = cKDTree(feat)
ny, nx = np.where(f[..., 3] > 40)
q = np.c_[f[ny, nx, :3].astype(float), nx * 0.6, ny * 0.6]
_, idx = tree.query(q, k=5)
lab5 = oz[ys[idx], xs[idx]]  # (N,5,3)
code = lab5[..., 0].astype(int) * 65536 + lab5[..., 1].astype(int) * 256 + lab5[..., 2]
z = np.zeros_like(oz)
for i in range(len(ny)):
    v, c = np.unique(code[i], return_counts=True); best = v[np.argmax(c)]
    z[ny[i], nx[i]] = (best >> 16, (best >> 8) & 255, best & 255)
za = np.dstack([z, np.where(f[..., 3] > 40, 255, 0).astype(np.uint8)])
Image.fromarray(za).save(f'/home/claude/g/{naam}_nieuw_zones.png')
