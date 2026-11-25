# De slang van Sack o' Fangs (Kivuli): de zwart-rode slang uit enemies/slang2, de rode banden goud.
# Het masker pakt alleen de banden (g < 0,3 r, b < 0,25 r, verzadigd), zodat de roze bek blijft.
# Draaien: python3 tools/slang_kivuli.py, daarna gen-klein.py en gen-offline-manifest.py.
import glob, os, numpy as np
from PIL import Image
SRC, DST = 'enemies/slang2', 'enemies/slang_kivuli'
os.makedirs(DST, exist_ok=True)
for f in sorted(glob.glob(SRC + '/*_[0-9].png')):
    a = np.asarray(Image.open(f).convert('RGBA')).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    band = (g < r * 0.3) & (b < r * 0.25) & (sat > 0.6) & (mx > 0.25)
    lum = mx[band]
    o = a.copy()
    o[..., 0][band] = np.clip(0.95 * lum + 0.12, 0, 1)
    o[..., 1][band] = np.clip(0.72 * lum + 0.06, 0, 1)
    o[..., 2][band] = np.clip(0.18 * lum, 0, 1)
    Image.fromarray((o * 255).astype(np.uint8)).save(DST + '/' + os.path.basename(f), optimize=True)
print('klaar:', DST)
