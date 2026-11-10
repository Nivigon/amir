# De finale van Murghtaan: poot_op (staan -> driepoot), mank (een manke stap, lus), omkijken (over de schouder)
# en dood_echt (strompelen, neerglijden, omrollen, bek op een kier), op het canvas van murg_sets.py (640x320,
# grondlijn 300, het midden van het staande frame op x 400, staand 176 hoog). Elke clip wordt met schaal en
# verschuiving op maximale overlap op de vorige gelegd. Daarna: murg_kleur.py voor fase 1 en bezeten.
# Gebruik: python3 murg_finale.py <map met clipmappen po h1 ta h2 omrol eind, frames f_001.png ...> <uitmap>
import numpy as np, cv2, json, os, sys
from PIL import Image, ImageDraw
from scipy import ndimage
sys.argv_ = sys.argv
D, OUT = sys.argv[1], sys.argv[2]
W, H, GY, CX, STAAN = 640, 320, 300, 400, 176
def key(rgb):
    a = rgb.astype(np.float32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    k = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    al = 1 - np.clip((k - 0.18) / 0.30, 0, 1)
    over = np.clip(np.minimum(r, b) - g, 0, None) * (al < 0.98)
    c = a.copy(); c[..., 0] -= over; c[..., 2] -= over
    lab, n = ndimage.label(al > 0.3)                      # alleen het lijf, losse vlekjes weg
    if n > 1:
        sz = ndimage.sum(al > 0.3, lab, range(1, n + 1)); hou = ndimage.binary_dilation(lab == np.argmax(sz) + 1, iterations=3)
        al = al * hou
    return np.dstack([np.clip(c, 0, 255), al * 255]).astype(np.uint8)
def lees(clip, i): return key(np.array(Image.open(f'{D}/{clip}/f_{i:03d}.png').convert('RGB')))
def warp(f, M): return cv2.warpAffine(f, np.float32(M), (W, H), flags=cv2.INTER_AREA, borderValue=(0, 0, 0, 0))
def bb(a):
    ys, xs = np.nonzero(a[..., 3] > 128); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def leg(f, ref, s0):
    # schaal s en verschuiving zodat f zo goed mogelijk op ref (canvas) valt
    R = (ref[..., 3] > 128).astype(np.float32); best = None
    rb = bb(ref)
    for s in np.arange(s0 * 0.85, s0 * 1.18, 0.01):
        g = cv2.resize((f[..., 3] > 128).astype(np.float32), None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        ys, xs = np.nonzero(g > 0.5)
        dx0 = (rb[0] + rb[2]) / 2 - (xs.min() + xs.max()) / 2; dy0 = rb[3] - ys.max()
        for dy in range(int(dy0) - 16, int(dy0) + 17, 2):
            for dx in range(int(dx0) - 40, int(dx0) + 41, 2):
                gt = cv2.warpAffine(g, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H))
                v = (gt * R).sum() / max(np.maximum(gt, R).sum(), 1)
                if best is None or v > best[0]: best = (v, s, dx, dy)
    v, s, dx, dy = best
    return [[s, 0, dx], [0, s, dy]], v
def ogen_glint(f):
    # een oog met een glimmertje (tijdens het omrollen) wordt een zwarte oogkas
    f = f.copy(); lum = f[..., :3].astype(float).mean(-1); al = f[..., 3]
    ys, xs = np.nonzero(al > 128); x0 = xs.min(); head = np.zeros(al.shape, bool); head[:, x0:x0 + int(0.16 * (xs.max() - x0))] = True
    nb = ndimage.uniform_filter(lum, 7); gl = head & (lum > 200) & (nb < 100) & (al > 200)
    lab, n = ndimage.label(ndimage.binary_dilation(gl, iterations=1)); HH, WW = al.shape; yy, xx = np.mgrid[:HH, :WW]
    for j in range(1, n + 1):
        ys2, xs2 = np.nonzero(lab == j)
        if len(xs2) > 14: continue
        e = ((xx - xs2.mean()) ** 2 + (yy - ys2.mean()) ** 2) < 7.5 ** 2
        m = e & ((lum < 120) | (lab == j)) & (al > 200); f[m, :3] = [18, 12, 12]
    return f
def ogen_vast(f, plekken):
    f = f.copy(); HH, WW = f.shape[:2]; yy, xx = np.mgrid[:HH, :WW]; lum = f[..., :3].astype(int).mean(-1)
    for cx, cy, rx, ry in plekken:
        m = (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1) & (lum < 110) & (f[..., 3] > 200); f[m, :3] = [18, 12, 12]
    return f
def litteken(c):
    # de schuine kras over de bovenste oogkas, terug in de frames waar de kop stilligt
    lum = c[..., :3].astype(int).mean(-1); al = c[..., 3]; ys, xs = np.nonzero(al > 128); x0 = xs.min(); w = xs.max() - x0
    m = (lum < 40) & (al > 200); m[:, x0 + int(0.25 * w):] = False
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
    bl = [ndimage.center_of_mass(lab == j + 1) for j, s in enumerate(sz) if s >= 60]
    if not bl: return c
    cy, cx = min(bl, key=lambda q: q[0]); k = 1.04
    lay = Image.new('L', (W, H), 0); d = ImageDraw.Draw(lay)
    d.line([(cx - 7 * k, cy - 9 * k), (cx + 6 * k, cy + 9 * k)], fill=255, width=2)
    d.line([(cx - 1 * k, cy - 12 * k), (cx + 3 * k, cy - 6 * k)], fill=255, width=1)
    for t in (0.2, 0.75):
        px, py = cx - 7 * k + 13 * k * t, cy - 9 * k + 18 * k * t; d.line([(px - 2, py + 1), (px + 2, py - 1)], fill=255, width=1)
    L = np.array(lay) > 0; ok = L & (al > 220) & (lum > 45); c = c.copy(); c[ok, :3] = [62, 28, 22]
    return c
sets = {}
# poot_op: staan -> driepoot. Het staande frame zoals inzakken: midden op 400, voeten op 300.
f0 = lees('po', 1); b = bb(f0); S = STAAN / (b[3] - b[1])
M0 = [[S, 0, CX - S * (b[0] + b[2]) / 2], [0, S, GY - S * b[3]]]
sets['poot_op'] = [warp(lees('po', i), M0) for i in range(1, 56, 3)]
DRIE = sets['poot_op'][-1]
Mm, v = leg(lees('h1', 1), DRIE, S); print('mank', v)
sets['mank'] = [warp(lees('h1', i), Mm) for i in [1, 4, 7, 10, 13, 16] + list(range(74, 143, 6))]
Mo, v = leg(lees('ta', 65), DRIE, S); print('omkijken', v)
sets['omkijken'] = [warp(lees('ta', i), Mo) for i in range(65, 146, 4)]
Mh, v = leg(lees('h2', 1), DRIE, S); print('hop2', v)
dood = []
for i in [1, 7, 13, 19, 25, 31, 37] + [91, 94, 97, 100, 103, 106, 108]:
    f = lees('h2', i)
    if i >= 91: f = np.roll(f, 22, axis=1)             # in de clip krabbelde hij tussendoor op; dat stuk is eruit
    dood.append(warp(f, Mh))
Mr, v = leg(lees('omrol', 1), dood[-1], Mh[0][0] * 1.15); print('omrol', v)
for i in [9, 17, 25, 33, 41, 49, 57]:
    f = lees('omrol', i)
    f = ogen_vast(f, [(176, 283, 8, 14), (160, 307, 9, 6)]) if i >= 57 else ogen_glint(f)
    dood.append(warp(f, Mr))
Me, v = leg(lees('eind', 1), warp(ogen_vast(lees('omrol', 145), [(176, 283, 8, 14), (160, 307, 9, 6)]), Mr), Mr[0][0] * 1.3); print('eind', v)
for i in [17, 25, 33, 41, 49]: dood.append(warp(lees('eind', i), Me))
dood = [litteken(c) if n >= 20 else c for n, c in enumerate(dood)]
sets['dood_echt'] = dood
meta = {}
for naam, fr in sets.items():
    os.makedirs(f'{OUT}/{naam}', exist_ok=True)
    for n, c in enumerate(fr): Image.fromarray(c, 'RGBA').save(f'{OUT}/{naam}/{naam}_{n:02d}.png', optimize=True)
    meta[naam] = {'frames': len(fr), 'bbox': [bb(c) for c in fr]}
    print(naam, len(fr), meta[naam]['bbox'][0], meta[naam]['bbox'][-1])
json.dump(meta, open(f'{OUT}/sets.json', 'w'))
