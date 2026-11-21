"""Plak de zes zoom-tegels (484x444 CSS = 605x555 px, 3 kolommen x 2 rijen) tot het Grok-beeld van 1808x1104.

python3 plak.py uit.png t00 t10 t20 t01 t11 t21   (tegels in volgorde kolom, rij; rij 0 eerst)
"""
import sys
from PIL import Image
uit = sys.argv[1]; ts = sys.argv[2:]
S = Image.new('RGB', (1808, 1104))
for k, p in enumerate(ts):
    c, r = k % 3, k // 3
    S.paste(Image.open(p).convert('RGB'), (c * 605, r * 555))
S.save(uit)
