#!/usr/bin/env python3
"""Maakt het wapenrek voor de stad uit de Grok-plaat in design/stad/wapenrek/bron/.

Bron: wapenrek_grok.webp, vier lege rekken op wit. We nemen het rek linksboven.
Uit:
  design/stad/wapenrek/wapenrek.png    het lege rek, uitgeknipt, zonder witte rand
  design/stad/wapenrek/wapenrek.json   de maten: w, h, de x van de vier touwlussen, de hoogte
                                       van de bovenste en onderste balk, en de x van de palen

De plaat heeft al een doorzichtige achtergrond, maar de randpixels zijn wit gekleurd: in het spel
gaf dat een wit randje. Die pixels krijgen de kleur van het hout ernaast (hun alpha blijft).

    python3 tools/wapenrek_knip.py

Daarna: python3 tools/gen-offline-manifest.py (niet gen-klein.py: hij is al klein).
Vereist Pillow, numpy en scipy.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad', 'wapenrek')
BRON = os.path.join(MAP, 'bron', 'wapenrek_grok.webp')
VAK = (80, 50, 760, 610)          # het rek linksboven in de plaat
RAND = 2                          # zo breed (px) is de strook dekkend hout langs de rand die de kleur van binnen krijgt
LUS_ZOOM = (159, 257, 361, 459)   # de touwlussen op de bovenste balk, x in wapenrek.png (nagemeten)

bron = np.array(Image.open(BRON).convert('RGBA').crop(VAK)).astype(float)
rgb, alpha = bron[..., :3], bron[..., 3]
# de rand: halfdoorzichtig, of de buitenste RAND px dekkend hout (die zijn lichter dan het hout erbinnen: het randje van Grok)
leeg = alpha < 8
buurt = nd.binary_dilation(leeg, iterations=RAND)
rand = (~leeg) & ((alpha < 255) | buurt)
kern = (~leeg) & ~rand
# elke randpixel krijgt de kleur van de dichtstbijzijnde kernpixel (het hout ernaast); de alpha blijft,
# en de buitenste dekkende ring wordt wat doorzichtiger zodat de rand zacht blijft
_, (iy, ix) = nd.distance_transform_edt(~kern, return_indices=True)
rgb = np.where(rand[..., None], rgb[iy, ix], rgb)
alpha = np.where(rand & (alpha >= 255), 200, alpha)
alpha[leeg] = 0
out = np.dstack([rgb, alpha]).astype(np.uint8)
img = Image.fromarray(out, 'RGBA')
box = img.getbbox()
img = img.crop(box)
w, h = img.size
A = np.array(img)[..., 3] > 128
# de balken: rijen tussen de palen die bijna helemaal hout zijn; de palen: kolommen die bijna helemaal hout zijn
kol = A.mean(axis=0)
palen = [x for x in range(w) if kol[x] > 0.8]
links = [x for x in palen if x < w / 2]; rechts = [x for x in palen if x > w / 2]
binnen = A[:, max(links) + 5:min(rechts) - 5].mean(axis=1)
rijen = [y for y in range(h) if binnen[y] > 0.9]
groepen = []
for y in rijen:
    if groepen and y - groepen[-1][-1] <= 1: groepen[-1].append(y)
    else: groepen.append([y])
balken = [round(sum(g) / len(g)) for g in groepen if len(g) > 4]
maat = {'w': w, 'h': h,
        'lussen': list(LUS_ZOOM),
        'boven': balken[0], 'onder': balken[-1],
        'paal': [round(sum(links) / len(links)), round(sum(rechts) / len(rechts))]}
img.save(os.path.join(MAP, 'wapenrek.png'), optimize=True)
json.dump(maat, open(os.path.join(MAP, 'wapenrek.json'), 'w'))
print('wapenrek.png', w, 'x', h, maat)
