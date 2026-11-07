#!/usr/bin/env python3
"""De bloedstroom onder het gezicht van Nyundo als hij in zijn knots valt (BRU.bloed.dood).

Knipt de stroom bloed onder het gezicht van het lijk van de schildman (einde_val_15.png, de laatste val na de
executie) los, zodat Nyundo precies hetzelfde bloed krijgt: alleen de bloedrode en de lichtroze pixels in het stuk
onder zijn hoofd, en daarvan alleen het grootste aaneengesloten stuk (geen losse spikkels van de huidlijnen).
Schrijft design/bloed/nyundo_stroom.png. Draai daarna tools/gen-offline-manifest.py.
"""
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRON = ROOT / 'enemies/schildbandiet/executie/lagen/einde_val_15.png'
DOEL = ROOT / 'design/bloed/nyundo_stroom.png'
VAK = (0, 70, 104, 113)          # x0, y0, x1, y1: de stroom onder zijn gezicht (zonder het stuk dat naar zijn borst opklimt)

im = np.array(Image.open(BRON).convert('RGBA')).astype(int)
x0, y0, x1, y1 = VAK
im = im[y0:y1, x0:x1]
r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
bloed = (a > 30) & (((g < r * 0.3) & (r > 45)) | ((r > 150) & (g < 145) & (b > g * 0.9)))

# alleen het grootste aaneengesloten stuk (8 buren)
h, w = bloed.shape
label = np.zeros((h, w), int); beste, besteN, n = 0, 0, 0
for y in range(h):
    for x in range(w):
        if bloed[y, x] and not label[y, x]:
            n += 1; label[y, x] = n; q = deque([(y, x)]); tel = 0
            while q:
                cy, cx = q.popleft(); tel += 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and bloed[ny, nx] and not label[ny, nx]:
                            label[ny, nx] = n; q.append((ny, nx))
            if tel > besteN: beste, besteN = n, tel
uit = np.zeros_like(im)
m = label == beste
uit[m] = im[m]
ys, xs = np.nonzero(m)
uit = uit[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
Image.fromarray(uit.astype('uint8')).save(DOEL)
print(f'{DOEL.relative_to(ROOT)}: {uit.shape[1]} x {uit.shape[0]} px, {besteN} pixels bloed')
