#!/usr/bin/env python3
# De hangende stam van het regenwoud (HSTAM): knipt de Grok-plaat in design/regenwoud/hangstam/bron/ in twee stukken.
#   stam.png   de boomstam met de knopen van de lianen erom (zonder de lianen erboven)
#   liaan.png  een rechtgetrokken stuk liaan dat naadloos onder elkaar past (het spel stapelt het tot boven beeld)
# Het wit gaat weg met een flood-fill vanaf de rand (en de witte gaatjes tussen de strengen), de rand krijgt een
# ontmenging tegen wit zodat er geen lichte zoom overblijft. Draai daarna tools/gen-offline-manifest.py.
import numpy as np
from PIL import Image
from scipy import ndimage

BRON = 'design/regenwoud/hangstam/bron/hangstam_grok.png'
UIT = 'design/regenwoud/hangstam/'

im = np.array(Image.open(BRON).convert('RGB')).astype(float)
mn, mx = im.min(2), im.max(2)
wit = (mn > 205) & ((mx - mn) < 30)
lab, _ = ndimage.label(wit)
rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(rand))
# witte gaatjes binnen de vorm (tussen de strengen van een liaan)
gat = (mn > 226) & ((mx - mn) < 25) & ~bg
lab2, k = ndimage.label(gat)
for i, s in enumerate(ndimage.sum(gat, lab2, range(1, k + 1))):
    if s >= 6: bg |= lab2 == i + 1
alpha = np.where(bg, 0.0, 1.0)
# de rand: twee px zacht, alpha uit hoe donker de pixel is, en de kleur ontmengd tegen wit
rnd = ndimage.binary_dilation(bg, iterations=2) & ~bg
a2 = np.clip((235 - mn) / 115, 0, 1)
alpha[rnd] = a2[rnd]
rgb = im.copy()
m = rnd & (alpha > 0.04)
rgb[m] = np.clip((im[m] - 255 * (1 - alpha[m, None])) / alpha[m, None], 0, 255)
# en de buitenste rij nog iets donkerder (de outline van de stijl), zodat er geen licht randje blijft
rgb[rnd] *= 0.82
# losse spikkels weg
vast = alpha > 0.1
lab3, k = ndimage.label(vast)
for i, s in enumerate(ndimage.sum(vast, lab3, range(1, k + 1))):
    if s < 400: alpha[lab3 == i + 1] = 0
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)

ys, xs = np.where(alpha > 0.5)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
breed = x1 - x0
rij = (alpha[:, x0:x1] > 0.5).sum(1)
stamTop = int(np.argmax(rij > 0.6 * breed))          # de eerste rij waar de stam over de volle breedte loopt
print('stam: bovenrand', stamTop, 'onderrand', y1, 'breed', breed)

# ---- de stam: vanaf een stukje boven de bovenrand, zodat de knopen heel blijven ----
knip = stamTop - 26
stam = Image.fromarray(rgba[knip:y1, x0:x1], 'RGBA')
stam.save(UIT + 'stam.png')

# waar de twee lianen de stam raken (als deel van de breedte), voor HSTAM.haak
boven = alpha[stamTop - 120:stamTop - 30, x0:x1] > 0.5
kol = boven.sum(0)
glad = ndimage.gaussian_filter1d(kol.astype(float), 12)
mid = [int(np.argmax(glad[:breed // 2])), breed // 2 + int(np.argmax(glad[breed // 2:]))]
print('lianen op', [round(c / breed, 3) for c in mid], 'stamhoogte', y1 - knip, 'bovenrand in stam.png', stamTop - knip)

# ---- de liaan: de linker, rechtgetrokken, een stuk dat naadloos onder elkaar past ----
cx = int(x0 + mid[0]); half = 46
stuk = rgba[y0 + 10:stamTop - 40, cx - half:cx + half].copy()
a = stuk[..., 3].astype(float)
# rechttrekken: elke rij schuift zo dat het midden van de stengel in het midden staat (gladgestreken)
kern = a > 200
mids = np.array([np.mean(np.where(r)[0]) if r.any() else np.nan for r in kern])
ok = ~np.isnan(mids)
mids = np.interp(np.arange(len(mids)), np.where(ok)[0], mids[ok])
mids = ndimage.uniform_filter1d(mids, 31)
recht = np.zeros_like(stuk)
for i in range(stuk.shape[0]):
    s = int(round(half - mids[i]))
    recht[i] = np.roll(stuk[i], s, axis=0)
    if s > 0: recht[i, :s] = 0
    elif s < 0: recht[i, s:] = 0
# naadloos: de onderste rijen lopen over in de bovenste
over = 40
h = recht.shape[0] - over
tegel = recht[:h].astype(float)
for i in range(over):
    t = i / over
    tegel[i] = recht[i] * t + recht[h + i] * (1 - t)
Image.fromarray(tegel.astype(np.uint8), 'RGBA').save(UIT + 'liaan.png')
print('liaan', tegel.shape[1], 'x', tegel.shape[0])
