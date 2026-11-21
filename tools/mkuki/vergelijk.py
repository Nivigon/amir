"""python3 vergelijk.py werkmap naam  ->  terugzetten, uitlijnen, npy per frame en een vergelijkplaat (2x)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import raster, uitlijn
import numpy as np
from PIL import Image
from scipy import ndimage as nd
W, naam = sys.argv[1], sys.argv[2]
res = raster.terug(f'{W}/{naam}_grok.png', f'{W}/{naam}.json')
meta = json.load(open(f'{W}/{naam}.json'))
x0, y0, x1, y1 = meta['crop']
cw, ch = x1 - x0, y1 - y0
S = Image.new('RGBA', (len(res) * cw, ch), (255, 0, 255, 255))
uit = {}
for i, (pad, a) in enumerate(res):
    if pad == 'anker':
        continue
    o = raster.laad(pad)
    if meta['speer'].get(os.path.basename(pad)):
        o, _ = raster.zonder_speer(o)
    b, dx, dy, v = uitlijn.lijn_uit(a, o)
    uit[pad] = {'dx': dx, 'dy': dy, 'iou': round(float(v), 3)}
    print(os.path.basename(pad), dx, dy, round(v, 3))
    np.save(f'{W}/{naam}_{i}.npy', b)
    m = o[..., 3] > 128; rand = m ^ nd.binary_erosion(m)
    c = b.copy(); c[rand] = [255, 255, 255, 255]
    S.alpha_composite(Image.fromarray(c[y0:y1, x0:x1]), (i * cw, 0))
S = S.resize((S.width * 2, S.height * 2), Image.NEAREST)
S.save(f'{W}/{naam}_vergelijk.png')
json.dump(uit, open(f'{W}/{naam}_iou.json', 'w'), indent=1)
