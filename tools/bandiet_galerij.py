# Bandiet galerijsprong: afzet, zweef, landing, opkijk uit twee Grok-clips.
# Clip 1 (sprong) begon op idle_in_00 (397x563 canvas), 2x opgeschaald naar figuur 720 px op 1500x1050, Grok 1136x800.
# Clip 2 (landing) begon op clip1 frame 58 (zweef), geschaald 1500/1136 en verschoven (95, -17) op 1500x1050, Grok 1168x784.
import os, sys, json, subprocess, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage

C1, C2, IDLE, OUT = sys.argv[1:5]
GROND, H = 555, 563

def frames(mp4):
    d = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, os.path.join(d, '%03d.png')], check=True)
    n = len(os.listdir(d))
    return [np.array(Image.open(os.path.join(d, f'{i:03d}.png')).convert('RGB')).astype(np.float32) for i in range(1, n + 1)]

def key(rgb):
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    k = np.minimum(R, B) - G
    bg = np.median(np.concatenate([rgb[:20].reshape(-1, 3), rgb[:, :20].reshape(-1, 3)]), 0)
    kbg = min(bg[0], bg[2]) - bg[1]
    a = np.clip((0.92 * kbg - k) / (0.30 * kbg), 0, 1)
    m = a > 0.5
    lab, n = ndimage.label(m)
    if n:
        s = ndimage.sum(m, lab, range(1, n + 1)); keep = np.zeros(n + 1, bool); keep[1:] = s > 400
        a = a * ndimage.binary_dilation(keep[lab], iterations=3)
    aa = np.maximum(a, 0.05)[..., None]
    F = np.where(a[..., None] < 0.99, (rgb - (1 - aa) * bg) / aa, rgb)
    F = np.clip(F, 0, 255)
    sp = (np.minimum(F[..., 0], F[..., 2]) - F[..., 1] > 8) & (F[..., 2] > 0.6 * F[..., 0]) & (F[..., 0] > 0.6 * F[..., 2]) & (a > 0.05)
    F = np.where(sp[..., None], np.minimum(F, F[..., 1:2] + 8), F)          # magenta (rand, zwaardveeg, hoofddoekpunten) eruit: geen bandietkleur heeft rood en blauw allebei ruim boven groen
    F = np.where((a < 0.9)[..., None], F * 0.35, F)                          # rand wordt de zwarte omlijning
    return np.dstack([np.clip(F, 0, 255), a * 255]).astype(np.uint8)

# schaal: clip1-px naar originele px
idle = Image.open(IDLE); ib = idle.getbbox()
S1 = (1500 / 1136) * ((ib[3] - ib[1]) / 720)
# clip2-px naar clip1-px: p1 = (p2*1500/1168 - (95,-17)) * 1136/1500
S2 = S1 * (1136 / 1168)
OFF2 = np.array([-95, 17]) * 1136 / 1500 * S1          # extra verschuiving in uitvoer-px

def plaats(rgba, s, extra):
    im = Image.fromarray(rgba, 'RGBA')
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im, extra

f1, f2 = frames(C1), frames(C2)
# horizontale uitlijning: clip1 frame 0 op idle_in_00 (midden van de bbox)
k0, _ = plaats(key(f1[0]), S1, 0); b0 = k0.getbbox()
X1 = ((ib[0] + ib[2]) / 2) - (b0[0] + b0[2]) / 2
sets = {
    'afzet':   [(1, i) for i in range(0, 57, 2)],
    'zweef':   [(1, 57)],
    'landing': [(2, i) for i in range(0, 14)],
    'opkijk':  [(2, i) for i in range(14, 84, 4)],
}
geplaatst = {}
for naam, lijst in sets.items():
    for c, i in lijst:
        if c == 1: im, _ = plaats(key(f1[i]), S1, 0); x = X1
        else:      im, _ = plaats(key(f2[i]), S2, 0); x = X1 + OFF2[0]
        bb = im.getbbox()
        geplaatst[(naam, c, i)] = (im, x, bb)
# canvasbreedte uit de unie
xs0 = min(x + bb[0] for im, x, bb in geplaatst.values()); xs1 = max(x + bb[2] for im, x, bb in geplaatst.values())
marge = 8; L = int(np.floor(xs0)) - marge; W = int(np.ceil(xs1)) + marge - L
os.makedirs(OUT, exist_ok=True); meta = {'canvas': [W, H], 'grond': GROND, 'idle_x_in_canvas': -L, 'fps': 24, 'sets': {}}
for naam, lijst in sets.items():
    d = os.path.join(OUT, naam); os.makedirs(d, exist_ok=True); fr = []
    for j, (c, i) in enumerate(lijst):
        im, x, bb = geplaatst[(naam, c, i)]
        dy = GROND - bb[3]                      # sprongbaan eruit: elk frame op de grondlijn
        can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        can.alpha_composite(im, (int(round(x - L)), int(dy))) if dy >= 0 else can.paste(im, (int(round(x - L)), int(dy)), im)
        can.save(os.path.join(d, f'{naam}_{j:02d}.png'))
        fr.append({'f': j, 'ticks': 2 if naam in ('afzet', 'opkijk') else 1, 'bron': f'clip{c}:{i}'})
    meta['sets'][naam] = fr
# y_verwijderd: verschil tussen de echte onderkant (in de clip) en de grondlijn, t.o.v. het eerste/laatste grondframe
def onder(c, i):
    im, x, bb = geplaatst[next(k for k in geplaatst if k[1] == c and k[2] == i)]
    return bb[3] + (0 if c == 1 else OFF2[1])
g1 = onder(1, 0); g2 = onder(2, 13)
for naam, lijst in sets.items():
    for e, (c, i) in zip(meta['sets'][naam], lijst):
        e['y_verwijderd'] = round(float((g1 if c == 1 else g2) - onder(c, i)), 1)
json.dump(meta, open(os.path.join(OUT, 'sprites_galerij.json'), 'w'), indent=1)
print(W, H, -L, {k: len(v) for k, v in sets.items()})
