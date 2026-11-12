# Maakt de sets voor de opening van Murghtaan 3 uit twee Grok-clips (enemies/hyena_baas/bron/):
#   vreet_omkijk.mp4: hij vreet (twee rukjes) en kijkt over zijn schouder om
#   vreet_whoop.mp4:  hij vreet en heft zijn kop voor een roep
# De clips zijn gemaakt vanaf een beeld met dezelfde houding als brul_00 (de kop omlaag). Per clip zoekt het script
# de schaal en verschuiving waarop het achterlijf het best op brul_00 valt, zodat de sets op het charge-canvas
# (800x400, grondlijn 380) passen. Kleur: de oranje zone wordt kale grauwe huid, net als in murg_kleur.py (fase 1).
# Gebruik: python3 tools/murc_intro_sets.py
import numpy as np, json, os, subprocess, tempfile, glob, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(__file__), '..')
BRON = os.path.join(ROOT, 'enemies/hyena_baas/bron')
UIT = os.path.join(ROOT, 'enemies/hyena_baas/charge')
W, H, GY = 800, 400, 380
SETS = [
  # naam, clip, clipframes (1-based, 24 fps), fps in het spel
  ('vreet',      'vreet_omkijk', list(range(24, 48)), 24),
  ('omkijk',     'vreet_omkijk', list(range(69, 86)), 24),
  ('omkijk_lus', 'vreet_omkijk', list(range(85, 146, 4)), 8),
  ('whoop',      'vreet_whoop',  list(range(52, 70)), 18),
]
import importlib.util
spec = importlib.util.spec_from_file_location('ms', os.path.join(os.path.dirname(__file__), 'murg_sets.py'))
src = open(os.path.join(os.path.dirname(__file__), 'murg_sets.py')).read()
ns = {}
exec(src.split('def zoomfix')[0].replace('OUT = sys.argv[1]', 'OUT = None'), ns)   # alleen de key van murg_sets
key = ns['key']

def frames(clip):
    d = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(BRON, clip + '.mp4'), os.path.join(d, 'f_%03d.png')], check=True)
    return d

def kleur(a):
    # de oranje zone wordt kale grauwe huid (zoals murg_kleur.py, fase 1)
    from scipy import ndimage
    rgb = a[..., :3].astype(np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    oranje = (r > 140) & (r > g * 1.65) & (g > b * 1.4) & (sat > 0.68)
    oz = ndimage.binary_dilation(oranje, iterations=1) & (r > g * 1.4)
    Yo = np.median(Y[oranje]) if oranje.any() else 150
    huid = np.array([132, 114, 104], np.float32)
    rgb[oz] = np.clip(huid * (Y[oz] / Yo)[:, None], 0, 255)
    return np.dstack([rgb, a[..., 3:].astype(np.float32)]).astype(np.uint8)

def plaats(k, s, dx, dy):
    im = Image.fromarray(k).resize((round(k.shape[1] * s), round(k.shape[0] * s)), Image.LANCZOS)
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # alpha_composite kent geen negatieve plek: knip zelf
    x0, y0 = max(0, -dx), max(0, -dy)
    can.alpha_composite(im.crop((x0, y0, im.width, im.height)), (max(0, dx), max(0, dy)))
    return can

def pas(k):
    # schaal en verschuiving waarop het achterlijf (rechts van x 360) het best op brul_00 valt, poten op de grondlijn
    ref = np.array(Image.open(os.path.join(UIT, 'brul/brul_00.png')))[..., 3] > 128
    best = None
    for s in np.arange(0.50, 0.70, 0.005):
        m = np.array(Image.fromarray(k[..., 3]).resize((round(k.shape[1] * s), round(k.shape[0] * s)))) > 128
        ys, xs = np.nonzero(m); dy = GY - ys.max()
        for dx in range(-200, 300, 2):
            can = np.zeros((H, W), bool)
            h, w = m.shape
            yy0, xx0 = max(0, dy), max(0, dx); yy1, xx1 = min(H, dy + h), min(W, dx + w)
            can[yy0:yy1, xx0:xx1] = m[yy0 - dy:yy1 - dy, xx0 - dx:xx1 - dx]
            a, b = can[:, 360:], ref[:, 360:]
            iou = (a & b).sum() / max(1, (a | b).sum())
            if best is None or iou > best[0]: best = (iou, s, dx, int(dy))
    return best

meta = json.load(open(os.path.join(UIT, 'metadata.json')))
cache = {}
for naam, clip, cf, fps in SETS:
    if clip not in cache:
        d = frames(clip)
        # de pasvorm op het eerste frame van de clip (de kop omlaag, de houding van het startbeeld)
        k0 = key(np.array(Image.open(os.path.join(d, 'f_001.png')).convert('RGB')))
        cache[clip] = (d, pas(k0))
        print(clip, 'pas', cache[clip][1])
    d, (iou, s, dx, dy) = cache[clip]
    os.makedirs(os.path.join(UIT, naam), exist_ok=True)
    for f in glob.glob(os.path.join(UIT, naam, '*.png')): os.remove(f)
    bbox = []
    for i, c in enumerate(cf):
        k = kleur(key(np.array(Image.open(os.path.join(d, f'f_{c:03d}.png')).convert('RGB'))))
        can = plaats(k, s, dx, dy)
        al = np.array(can)[..., 3]; ys, xs = np.nonzero(al > 128)
        bbox.append([int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
        can.save(os.path.join(UIT, naam, f'{naam}_{i:02d}.png'), optimize=True)
    meta['sets'][naam] = {'frames': len(cf), 'bron': clip, 'clipframes': cf, 'bbox': bbox, 'fps': fps, 'reis': 0.0}
    print(naam, len(cf))
json.dump(meta, open(os.path.join(UIT, 'metadata.json'), 'w'))
print('klaar')
