# handplaats.py werkmap/sN schaal dx dy : grok-figuur met de hand op het origineel zetten (onderkant figuur op onderkant origineel)
import sys, json, os
sys.path.insert(0, 'tools/mkuki')
import numpy as np, raster, afwerk
from PIL import Image
from scipy import ndimage as nd
naam = sys.argv[1]; f = float(sys.argv[2]); ddx = int(sys.argv[3]); ddy = int(sys.argv[4])
m = json.load(open(naam + '.json'))
k = raster.key(np.asarray(Image.open(naam + '_grok.png').convert('RGB')))
al = k[..., 3] > 60
lab, n = nd.label(al); sz = nd.sum(al, lab, range(1, n + 1))
kand = [i + 1 for i in np.argsort(-sz)[:3]]
cm = nd.center_of_mass(al, lab, kand)
kid = [c for c, (cy, cx) in zip(kand, cm) if cx > 0.17 * al.shape[1]][0]
kk = k.copy(); kk[~nd.binary_dilation(lab == kid, iterations=3)] = 0
ys, xs = np.where(kk[..., 3] > 60); fig = kk[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
o = raster.laad(m['pad'])
from speer_meet import override
if m['speer']: o, _ = raster.zonder_speer(o, override(m['pad']))
oy, ox = np.where(o[..., 3] > 128)
H, W = o.shape[:2]
oh = oy.max() - oy.min() + 1
nh = int(round(oh * f)); nw = int(round(fig.shape[1] * nh / fig.shape[0]))
im = np.asarray(Image.fromarray(fig).resize((nw, nh), Image.LANCZOS))
cy = oy.max() + 1 - nh + ddy; cx = int(np.median(ox)) - nw // 2 + ddx
b = np.zeros_like(o)
y0, x0 = max(0, cy), max(0, cx); y1, x1 = min(H, cy + nh), min(W, cx + nw)
b[y0:y1, x0:x1] = im[y0 - cy:y1 - cy, x0 - cx:x1 - cx]
np.save(naam + '.npy', b)
a = b[..., 3] > 128; c = o[..., 3] > 128
print('iou', round((a & c).sum() / (a | c).sum(), 3), 'onderkant', oy.max(), H)
