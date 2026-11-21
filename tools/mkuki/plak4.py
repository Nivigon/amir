"""Plak de laatste vier 2x2-tegels (864x576) tot het hele Grok-beeld: plak4.py uit.png"""
import sys, glob, os
from PIL import Image
D = sorted(glob.glob('/tmp/claude-tool-results/*/'), key=os.path.getmtime)[-1]
fs = sorted(glob.glob(D + '*.png'), key=os.path.getmtime)[-4:]
ims = [Image.open(f).convert('RGB') for f in fs]
w, h = ims[0].size
S = Image.new('RGB', (2 * w, 2 * h))
for k, im in enumerate(ims):
    S.paste(im, ((k % 2) * w, (k // 2) * h))
S.save(sys.argv[1])
