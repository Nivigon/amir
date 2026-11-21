"""python3 speercheck.py uit.png [--ov overrides.json] pad... : plaat met per frame het origineel en de speer eruit (groen = weg, rood = hand)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster
from speer_meet import meet, override, set_lengte
from PIL import Image, ImageDraw
args = sys.argv[1:]; ov = {}
if '--ov' in args:
    i = args.index('--ov'); ov = json.load(open(args[i + 1])); del args[i:i + 2]
uit, paden = args[0], args[1:]
set_lengte(paden)
ims = []
for p in paden:
    a = raster.laad(p); b = os.path.basename(p)
    r = meet(a, override(p))
    c = a.copy(); c[r['masker']] = [0, 255, 0, 255]
    im = Image.new('RGBA', (a.shape[1], a.shape[0]), (255, 0, 255, 255)); im.alpha_composite(Image.fromarray(c))
    d = ImageDraw.Draw(im)
    for hx, hy in r['handen']:
        d.ellipse((hx - 4, hy - 4, hx + 4, hy + 4), outline=(255, 0, 0, 255), width=2)
    d.text((4, 4), b, fill=(0, 0, 0, 255))
    print(b, r['tip'], r['kont'], r['lengte'], r['handen'])
    ims.append(im)
m = np.zeros(np.asarray(ims[0]).shape[:2], bool)
for p in paden:
    m |= raster.laad(p)[..., 3] > 20
ys, xs = np.where(m); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
w, h = x1 - x0, y1 - y0
kol = min(6, len(ims)); rij = (len(ims) + kol - 1) // kol
S = Image.new('RGB', (kol * w, rij * h))
for i, im in enumerate(ims):
    S.paste(im.crop((x0, y0, x1, y1)).convert('RGB'), ((i % kol) * w, (i // kol) * h))
f = min(1.0, 1800 / S.width)
S.resize((int(S.width * f), int(S.height * f))).save(uit)
