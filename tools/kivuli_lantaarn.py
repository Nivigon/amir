# Kivuli's lantaarn (design/kivuli/): uit de Grok-plaat (design/kivuli/bron/lantaarn_bron.png) twee zachte, dofe versies,
# uit en aan (Tom koos variant 2, 25-11-2026): minder verzadiging en helderheid, minder contrast, licht wazig en wat
# doorzichtig, zodat hij nauwelijks opvalt. Draai: python3 tools/kivuli_lantaarn.py
import numpy as np, os
from PIL import Image, ImageFilter
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'design', 'kivuli')
def maak(sat, hel, naam):
    im = Image.open(os.path.join(D, 'bron', 'lantaarn_bron.png')).convert('RGBA'); a = np.asarray(im).astype(float) / 255
    al = a[..., 3:]; rgb = a[..., :3]
    g = rgb.mean(axis=2, keepdims=True); rgb = g + (rgb - g) * sat                         # minder verzadigd
    rgb = rgb * hel; rgb = (rgb - 0.5) * 0.8 + 0.5                                         # minder contrast
    rgb = rgb * np.array([1.0, 0.96, 0.88]) * 0.5 + rgb * 0.5                              # zweem warm (sepia licht)
    pm = Image.fromarray((np.dstack([np.clip(rgb, 0, 1) * al, al]) * 255).astype('uint8'), 'RGBA').filter(ImageFilter.GaussianBlur(1.5))
    p = np.asarray(pm).astype(float) / 255; A = p[..., 3:]; C = np.where(A > 0.003, p[..., :3] / np.maximum(A, 1e-3), 0)
    out = np.dstack([np.clip(C, 0, 1), A * 0.8])                                           # 80% dekking
    Image.fromarray((out * 255).astype('uint8'), 'RGBA').save(os.path.join(D, naam), optimize=True)
maak(0.5, 0.5, 'lantaarn_uit.png'); maak(0.7, 0.76, 'lantaarn_aan.png')
