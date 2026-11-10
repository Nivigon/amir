# Volgt de dichte oogkas per frame met template matching vanaf een handmatig gekozen punt in frame 0.
import numpy as np, json, glob, sys, cv2
from PIL import Image
START = {'grauw': (272.5, 194), 'grauw_lus': (265, 202.5), 'sprong': (252.5, 205),
         'brul': (267.5, 190), 'brul_lus': (252.0, 156.5), 'ren': (230, 182.5)}
def grijs(p):
    a = np.array(Image.open(p)).astype(np.float32)
    g = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    return (g * (a[..., 3] / 255)).astype(np.float32)
def volg(fs, p0, R=16, S=22):
    g0 = grijs(fs[0]); x, y = p0; uit = [[x, y]]
    t0 = g0[int(y) - R:int(y) + R, int(x) - R:int(x) + R].copy(); t = t0.copy(); vorig = g0
    for f in fs[1:]:
        g = grijs(f)
        x0, y0 = int(x) - R - S, int(y) - R - S
        win = g[max(0, y0):y0 + 2 * (R + S), max(0, x0):x0 + 2 * (R + S)]
        tm = (0.5 * t + 0.5 * t0)
        res = cv2.matchTemplate(win, tm, cv2.TM_CCOEFF_NORMED)
        _, _, _, mx = cv2.minMaxLoc(res)
        x = max(0, x0) + mx[0] + R; y = max(0, y0) + mx[1] + R
        t = g[int(y) - R:int(y) + R, int(x) - R:int(x) + R].copy()
        uit.append([round(float(x), 1), round(float(y), 1)])
    return uit
if __name__ == '__main__':
    d = sys.argv[1]; res = {}
    for naam, p0 in START.items():
        fs = sorted(glob.glob(f'{d}/{naam}/*.png'))
        if not fs or p0 is None: continue
        res[naam] = volg(fs, p0)
    json.dump(res, open(d + '/ogen.json', 'w'))
