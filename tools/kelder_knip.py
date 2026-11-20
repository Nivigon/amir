#!/usr/bin/env python3
"""Maakt het kelderluik (de wig en het luik) uit de Grok-platen in design/stad/kelder/bron/.

Bron: wig_grok.jpg  de wig van leem in zijaanzicht, zonder luik, op wit (een schermafdruk van de Grok-plaat)
      luik_grok.jpg het houten luik alleen, in dezelfde stand en op dezelfde plek, op wit
      design/stad/gevel.png  de textuur: Grok tekende de wig te glad, dus de muur van de wig krijgt de leem,
                             regenstrepen en bakstenen van de gevel, op de maat van de stenen in het spel
Uit:  design/stad/kelder/wig.png en luik.png, allebei op hetzelfde canvas (de omhullende van de wig), zodat het luik
      zonder verschuiving op de wig past. Het scharnier van het luik en de rest van de maten staan in KELDER.

    python3 tools/kelder_knip.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist Pillow, numpy en scipy.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad', 'kelder')
WIT = 222                       # zo licht (in elk kanaal) is de witte achtergrond van Grok
BREED = 1221                    # rechts van deze kolom staat in de schermafdruk alleen nog leeg canvas
GEVEL_K = 1.15                  # de gevel op deze schaal: dan zijn de stenen even groot als in het spel
RAND = (52, 34, 22)             # de donkere omtrek, zoals om de rest van de stad
LUIK_LICHT = (1.45, (18, 8, 0)) # het luik iets lichter en warmer, naar de houten deuren in de straten


def knip(pad):
    """Wit dat aan de rand vastzit gaat weg, met een zachte rand van een paar pixels naar binnen."""
    im = np.array(Image.open(pad).convert('RGB')).astype(int)[:, :BREED]
    wit = im.min(axis=2) > WIT
    lab, _ = nd.label(wit)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    vol = nd.binary_erosion(nd.binary_opening(~np.isin(lab, list(rand)), iterations=1), iterations=2)
    a = np.array(Image.fromarray((vol * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8)))
    return np.dstack([im, a]).astype('uint8')


wig = knip(os.path.join(MAP, 'bron', 'wig_grok.jpg'))
luik = knip(os.path.join(MAP, 'bron', 'luik_grok.jpg'))

# de muur van de wig: alles behalve de houten sleuf en de voetlijn (de grote donkere stukken) krijgt de gevel
alfa = wig[..., 3] > 128
d0 = alfa & (wig[..., :3].mean(axis=2) < 70)
lab, n = nd.label(d0)
groot = nd.sum(d0, lab, range(1, n + 1))
hout = np.isin(lab, [i + 1 for i, v in enumerate(groot) if v > 1500])
muur = nd.binary_opening(alfa & ~hout, iterations=2)

g0 = Image.open(os.path.join(ROOT, 'design', 'stad', 'gevel.png')).convert('RGBA')
L, R = g0.crop((40, 1000, 350, 1505)), g0.crop((600, 1000, 930, 1505))   # de voet links en rechts van de deur
g = Image.new('RGBA', (L.width + R.width, L.height)); g.paste(L, (0, 0)); g.paste(R, (L.width, 0))
G = np.array(g.resize((int(g.width * GEVEL_K), int(g.height * GEVEL_K)), Image.LANCZOS))
ys, xs = np.where(alfa)
x0, y1 = xs.min(), ys.max()
yy, xx = np.where(muur)
ty = np.clip(yy + G.shape[0] - 1 - y1, 0, G.shape[0] - 1)   # de voet van de wig op de voet van de gevel
tx = np.clip(xx - x0 + 10, 0, G.shape[1] - 1)
tex = G[ty, tx]; ok = tex[:, 3] > 200
wig[yy[ok], xx[ok], :3] = tex[ok, :3]
achter = muur & (np.arange(wig.shape[1])[None, :] < x0 + 95)          # de hoge achterkant iets in de schaduw
wig[achter, :3] = (wig[achter, :3] * 0.82).astype('uint8')
omtrek = alfa & ~nd.binary_erosion(alfa, iterations=7)
wig[omtrek, :3] = (np.array(RAND) * 0.85 + wig[omtrek, :3] * 0.15).astype('uint8')

lf = luik.astype(float)
lf[..., :3] = np.clip(lf[..., :3] * LUIK_LICHT[0] + np.array(LUIK_LICHT[1]), 0, 255)
luik = lf.astype('uint8')

bb = Image.fromarray(wig, 'RGBA').getbbox()
Image.fromarray(wig, 'RGBA').crop(bb).save(os.path.join(MAP, 'wig.png'), optimize=True)
Image.fromarray(luik, 'RGBA').crop(bb).save(os.path.join(MAP, 'luik.png'), optimize=True)
lb = Image.fromarray(luik, 'RGBA').getbbox()
print('canvas', bb[2] - bb[0], 'x', bb[3] - bb[1], '(KELDER.canvas)')
print('luik in het canvas', lb[0] - bb[0], lb[1] - bb[1], lb[2] - bb[0], lb[3] - bb[1])
