# Verwerkt de Grok-clips van Murghtaan tot sprite-sets op een gemeenschappelijk canvas.
import numpy as np, cv2, json, os, sys
from PIL import Image
from scipy import ndimage
W, H, GY = 640, 320, 300           # canvas, grondlijn
CX = 400                          # waar het midden van het eerste frame komt
OUT = sys.argv[1]
SETS = [
  # naam, map, frames, schaal, zoomfix
  ('grauw', '1552b30e', list(range(1, 52, 2)), 0.714, True),
  ('grauw_lus', '1552b30e', list(range(55, 146, 6)), 0.714, True),
  ('sprong', 'h2', list(range(1, 38, 2)) + list(range(40, 59, 3)), 1.0, False),
  ('brul', 'c', list(range(1, 50, 2)), 0.78, False),
  ('brul_lus', 'c', list(range(50, 92, 4)), 0.78, False),
]
def key(rgb):
    a = rgb.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    k = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    al = 1 - np.clip((k - 0.18) / 0.30, 0, 1)
    # ingesloten kleine magenta vlekken (binnen de bek) worden donkerrood en blijven
    bg = al < 0.5
    lab, n = ndimage.label(bg)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    sz = ndimage.sum(bg, lab, range(1, n + 1))
    fy, fx = np.nonzero(~bg); kopgrens = fx.min() + 0.28 * (fx.max() - fx.min())
    for i in range(1, n + 1):
        if i not in rand and sz[i - 1] < 900:
            cy, cx = ndimage.center_of_mass(lab == i)
            if cx > kopgrens: continue
            m = lab == i
            a[m] = [92, 18, 24]; al[m] = 1
    # despill: het magenta-overschot (min(r,b) boven g) eraf, zonder te delen (dat gaf groene randen)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    over = np.clip(np.minimum(r, b) - g, 0, None) * (al < 0.98)
    c = a.copy(); c[..., 0] -= over; c[..., 2] -= over
    # Grok kleurt de verre poot in de vlucht soms groen of blauw: een hyena heeft geen groen of blauw,
    # dus die pixels worden donkerbruin op dezelfde helderheid
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    mx = np.maximum(np.maximum(r, g), b); sat = (mx - np.minimum(np.minimum(r, g), b)) / np.maximum(mx, 1)
    mn = np.minimum(np.minimum(r, g), b)
    tint = np.where(mx == r, 60 * (g - b) / np.maximum(mx - mn, 1), np.where(mx == g, 120 + 60 * (b - r) / np.maximum(mx - mn, 1), 240 + 60 * (r - g) / np.maximum(mx - mn, 1)))
    fout = (tint > 42) & (tint < 270) & (sat > 0.25) & (Y < 210) & (al > 0.05)   # de vacht zit rond 30 graden, oranje op 29
    c[fout] = np.stack([Y[fout] * 1.18, Y[fout] * 0.98, Y[fout] * 0.78], -1)
    c = np.clip(c, 0, 255)
    return np.dstack([c, al * 255]).astype(np.uint8)
def zoomfix(frames):
    # schaal per frame zodat het achterlijf op het eerste frame blijft (Grok zoomt langzaam in)
    ref = frames[0]
    out = []
    for f in frames:
        g0 = (ref[..., 3] > 128).astype(np.float32); g1 = (f[..., 3] > 128).astype(np.float32)
        h, w = g0.shape; roi = np.zeros_like(g0); roi[:, int(w * 0.5):] = 1
        best = (0, 1, 0, 0)
        for s in np.arange(0.94, 1.011, 0.005):
            M = np.float32([[s, 0, 0], [0, s, 0]])
            # schaal rond de grond-achterpoot: verschuiving zoeken
            gs = cv2.warpAffine(g1, M, (w, h))
            for dx in range(-14, 15, 2):
                for dy in range(-14, 15, 2):
                    T = np.float32([[1, 0, dx], [0, 1, dy]])
                    gt = cv2.warpAffine(gs, T, (w, h))
                    iou = ((gt * g0 * roi).sum()) / max(((np.maximum(gt, g0)) * roi).sum(), 1)
                    if iou > best[0]: best = (iou, s, dx, dy)
        _, s, dx, dy = best
        M = np.float32([[s, 0, dx], [0, s, dy]])
        out.append(cv2.warpAffine(f, M, (w, h), flags=cv2.INTER_LINEAR))
    return out
meta = {'canvas': {'w': W, 'h': H, 'ground_y': GY}, 'kijkrichting': 'links', 'sets': {}}
cache = {}
for naam, d, fr, sch, zf in SETS:
    frames = [key(np.array(Image.open(f'{d}/{i:03d}.png').convert('RGB'))) for i in fr]
    if zf:
        if d not in cache:
            # referentie is frame 1 van de clip, voor alle sets uit deze clip
            cache[d] = key(np.array(Image.open(f'{d}/001.png').convert('RGB')))
        frames = zoomfix([cache[d]] + frames)[1:]
    # schalen
    frames = [cv2.resize(f, None, fx=sch, fy=sch, interpolation=cv2.INTER_AREA) for f in frames]
    # een offset per clip: eerste frame van de clip bepaalt grond en midden
    ref = cache.get(d)
    f0 = cv2.resize(ref, None, fx=sch, fy=sch, interpolation=cv2.INTER_AREA) if ref is not None else frames[0]
    if d not in cache:
        cache[d] = frames[0] if False else None
    ys, xs = np.nonzero(f0[..., 3] > 128)
    ox = CX - (xs.min() + xs.max()) / 2; oy = GY - ys.max()
    os.makedirs(f'{OUT}/{naam}', exist_ok=True)
    nose = []
    for i, f in enumerate(frames):
        T = np.float32([[1, 0, ox], [0, 1, oy]])
        c = cv2.warpAffine(f, T, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        Image.fromarray(c, 'RGBA').save(f'{OUT}/{naam}/{naam}_{i:02d}.png', optimize=True)
        ys, xs = np.nonzero(c[..., 3] > 128)
        nose.append([int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())])
    meta['sets'][naam] = {'frames': len(frames), 'bbox': nose}
    print(naam, len(frames), nose[0], nose[-1])
json.dump(meta, open(f'{OUT}/sets.json', 'w'))
