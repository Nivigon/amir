"""python3 vergelijk.py werkmap naam  ->  terugzetten, uitlijnen, npy per frame en een vergelijkplaat (2x)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import raster, uitlijn, afwerk
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
# Grok verwisselt soms twee figuren van plek: elk figuur bij het origineel dat er het best op past
orig = {}
for pad, a in res:
    if pad == 'anker':
        continue
    o = raster.laad(pad)
    if meta['speer'].get(os.path.basename(pad)):
        o, _ = raster.zonder_speer(o, raster.override(pad))
    # uitlijnen zonder de vacht: die is in het aangeklede frame weg en trok de figuur opzij
    vacht = nd.binary_dilation(afwerk._vacht(o) & (o[..., 3] > 40), iterations=3)
    o = o.copy(); o[vacht, 3] = 0
    orig[pad] = o
paren = []
for i, (pad, a) in enumerate(res):
    for q, o in orig.items():
        b, dx, dy, v = uitlijn.lijn_uit(a, o, bereik=24)
        paren.append((v, i, q, b, dx, dy))
# eigen plek eerst: alleen ruilen als een ander origineel duidelijk beter past (Grok ruilt zelden, en idle-poses lijken op elkaar)
eigen = {}
for v, i, q, b, dx, dy in paren:
    if res[i][0] == q:
        eigen[i] = v
paren = [(v + (0.08 if res[i][0] == q else 0), i, q, b, dx, dy) for v, i, q, b, dx, dy in paren]
paren.sort(key=lambda t: -t[0])
gebruikt_i, gebruikt_q, keus = set(), set(), {}
for v, i, q, b, dx, dy in paren:
    if i in gebruikt_i or q in gebruikt_q:
        continue
    gebruikt_i.add(i); gebruikt_q.add(q); keus[i] = (q, b, dx, dy, v)
for i, (pad0, a) in enumerate(res):
    if i not in keus:
        meta['plekken'][i]['naam'] = 'anker'
        continue
    pad, b, dx, dy, v = keus[i]
    v = v - (0.08 if pad == pad0 else 0)
    o = orig[pad]
    if pad != pad0:
        print('verwisseld: tegel', i, 'is', os.path.basename(pad))
    meta['plekken'][i]['naam'] = pad
    uit[pad] = {'dx': dx, 'dy': dy, 'iou': round(float(v), 3)}
    print(os.path.basename(pad), dx, dy, round(v, 3))
    np.save(f'{W}/{naam}_{i}.npy', b)
    m = o[..., 3] > 128; rand = m ^ nd.binary_erosion(m)
    c = b.copy(); c[rand] = [255, 255, 255, 255]
    S.alpha_composite(Image.fromarray(c[y0:y1, x0:x1]), (i * cw, 0))
S = S.resize((S.width * 2, S.height * 2), Image.NEAREST)
S.save(f'{W}/{naam}_vergelijk.png')
json.dump(uit, open(f'{W}/{naam}_iou.json', 'w'), indent=1)
json.dump(meta, open(f'{W}/{naam}.json', 'w'), indent=1)
