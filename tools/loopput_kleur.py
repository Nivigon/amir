#!/usr/bin/env python3
"""De loopput van de savanne in de kleur van het dorp: de steen en het zand van de Grok-plaat
(bron/put_loop_savanne_bron.png) voller en iets donkerder, richting het oker van de hutten en de savannegrond.
De kruik (al terracotta, voller) blijft zoals hij is. Schrijft design/savanne/putten/put_loop_savanne.png."""
import colorsys
import numpy as np
from PIL import Image

BRON = 'design/savanne/putten/bron/put_loop_savanne_bron.png'
UIT = 'design/savanne/putten/put_loop_savanne.png'
TINT = 25 / 360      # de tint van het oker van de hutten
VOL = 2.1            # verzadiging erbij
LICHT = 0.80         # iets donkerder
GRENS = 0.36         # alleen wat grijzer is dan dit (steen, zand, hout); de kruik niet

im = Image.open(BRON).convert('RGBA')
a = np.array(im).astype(np.float64) / 255
rgb = a[..., :3].reshape(-1, 3)
uit = rgb.copy()
for i, (r, g, b) in enumerate(rgb):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s > GRENS:
        continue
    w = 1 - s / GRENS * 0.35                         # hoe grijzer, hoe meer
    h2 = h + (TINT - h) * 0.9 * w
    s2 = min(1, s * (1 + (VOL - 1) * w))
    l2 = l * (1 - (1 - LICHT) * w)
    uit[i] = colorsys.hls_to_rgb(h2, l2, s2)
a[..., :3] = uit.reshape(a[..., :3].shape)
Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(UIT)
print('geschreven', UIT)
