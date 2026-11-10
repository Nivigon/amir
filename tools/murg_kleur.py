# Kleurt de sets van Murghtaan: fase 1 (de oranje zone wordt kale grauwe huid) en bezeten
# (bijna zwarte vacht, verkoolde poot met paarse gloed in de barsten; botten, tanden en bek blijven).
import numpy as np, glob, os, sys
from PIL import Image
SRC, F1, BZ = sys.argv[1], sys.argv[2], sys.argv[3]
MAGIE = np.array([190, 80, 255], np.float32)
def zones(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    oranje = (r > 140) & (r > g * 1.65) & (g > b * 1.4) & (sat > 0.68)
    bot = (Y > 165) & (sat < 0.32)
    bek = (r > 80) & (r > g * 1.7) & (r > b * 1.3) & ~oranje
    return Y, oranje, bot, bek
for f in sorted(glob.glob(f'{SRC}/*/*.png')):
    rel = f[len(SRC) + 1:]
    a = np.array(Image.open(f)).astype(np.float32)
    rgb = a[..., :3]; al = a[..., 3:]
    Y, oranje, bot, bek = zones(rgb)
    # oranje zone iets verbreden voor de randpixels
    from scipy import ndimage
    oz = ndimage.binary_dilation(oranje, iterations=1) & (rgb[..., 0] > rgb[..., 1] * 1.4)
    Yo = np.median(Y[oranje]) if oranje.any() else 150
    # fase 1
    f1 = rgb.copy()
    huid = np.array([132, 114, 104], np.float32)
    f1[oz] = np.clip(huid * (Y[oz] / Yo)[:, None], 0, 255)
    # bezeten
    bz = rgb.copy()
    t = (Y / 255.0) ** 1.25
    vacht = np.stack([t * 78 + 8, t * 66 + 6, t * 82 + 10], -1)
    bz = vacht
    bz[bot] = rgb[bot] * 0.80
    bz[bek] = rgb[bek] * 0.75
    # verkoolde poot: donkere barsten gloeien
    rel_l = Y[oz] / Yo
    kool = np.stack([rel_l * 40 + 10, rel_l * 34 + 8, rel_l * 38 + 10], -1)
    gloed = np.clip((0.86 - rel_l) / 0.22, 0, 1)[:, None]
    bz[oz] = kool * (1 - gloed) + MAGIE * gloed
    for dst, img in ((F1, f1), (BZ, bz)):
        os.makedirs(os.path.dirname(f'{dst}/{rel}'), exist_ok=True)
        Image.fromarray(np.concatenate([np.clip(img, 0, 255), al], -1).astype(np.uint8), 'RGBA').save(f'{dst}/{rel}', optimize=True)
print('klaar')
