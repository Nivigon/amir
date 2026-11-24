# Duka, de marktman (karakters/duka/): de Grok-clips van 24-11-2026 naar losse frames voor het spel.
# python3 tools/duka_knip.py <map met de mp4's van Tom>
# Elke clip (24 fps) gaat naar 12 fps, wordt van het magenta gehaald (key2 uit de marktman-tools), uitgesneden op een vast
# doek in de coordinaten van de 944-clips (de rugclips van 960 zijn een fractie groter en schuiven mee), wat gedimd voor het
# licht binnen (de hoge lichten van het hemd waren te fel in de winkel), verkleind en naar 256 kleuren gezet.
# Bij het schap (toonbank draai rug pakken) tekende Grok een plank achter hem: die gaat eruit (magenta-lijnen, dunne
# stukjes en alles wat niet aan hem vastzit). Het doek: 299x361, grondlijn op rij 349, figuur 340 hoog, lijf op x 130 (DUKA).
import numpy as np, os, sys, glob, subprocess, tempfile, matplotlib.colors as mc
from PIL import Image, ImageFilter
from scipy import ndimage
CLIPS = {'1': 'rugidle', 'broad laugh': 'lach', 'double clap': 'klap', 'kalebasachter toonbank': 'kalebas',
         'shoulder look': 'schouder', 'simpel draai rug': 'draai', 'tapping arm and reposition': 'idle',
         'toonbank draai rug pakken': 'schap', 'wcarmscrossed': 'loop', 'wcarmsloose': 'loop2', 'yawn': 'gaap',
         'yawn2mss of het is zelfde': 'gaap2'}
S = 400 / 819; CX0, CY0, CW, CH = 180, 30, 720, 870; F = 0.85
T = {'rugidle': (819 / 829, -2, -5), 'schouder': (819 / 829, -2, -5)}
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'karakters', 'duka')
def key2(im, thr=(45, 110)):
    a = np.asarray(im.convert('RGB')).astype(float)
    bg = np.median(np.concatenate([a[:4].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)]), 0)
    al = np.clip((np.sqrt(((a - bg) ** 2).sum(-1)) - thr[0]) / (thr[1] - thr[0]), 0, 1)
    al2 = np.asarray(Image.fromarray((al * 255).astype('uint8')).filter(ImageFilter.MinFilter(3))).astype(float) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = np.clip((np.minimum(r, b) - g - 20) / 120, 0, 1)
    near = np.asarray(Image.fromarray(((al2 < 0.99) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(7))) > 0
    w = np.where(near, mag, 0)[..., None]
    a2 = a * (1 - w) + np.array([35, 25, 28]) * w
    return np.dstack([a2, al2 * 255]).clip(0, 255).astype('uint8')
def licht(im):
    a = np.asarray(im).astype(float) / 255; h = mc.rgb_to_hsv(a[..., :3]); h[..., 1] *= 0.88; v = h[..., 2]
    h[..., 2] = np.where(v > 0.62, 0.62 + (v - 0.62) * 0.55, v) * 0.96
    rgb = mc.hsv_to_rgb(h) * np.array([1.0, 0.96, 0.88]); rgb = rgb * 0.93 + np.array([0.55, 0.45, 0.33]) * 0.07
    return Image.fromarray((np.dstack([np.clip(rgb, 0, 1), a[..., 3]]) * 255).astype('uint8'), 'RGBA')
def frame(clip, im):
    s, dx, dy = T.get(clip, (1, 0, 0))
    if s != 1:
        W = round(im.width * s); c = Image.new('RGB', (944, 944), tuple(np.asarray(im)[3, 3])); c.paste(im.resize((W, W), Image.LANCZOS), (dx, dy)); im = c
    a = key2(im)
    if clip == 'schap':
        rgb = np.asarray(im).astype(int); r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        a[..., 3][(g < 22) & (np.abs(r - b) < 30) & (r > 70)] = 0
    k = Image.fromarray(a, 'RGBA').crop((CX0, CY0, CX0 + CW, CY0 + CH)).resize((round(CW * S), round(CH * S)), Image.LANCZOS)
    if clip == 'schap':
        b = np.asarray(k).copy(); m = ndimage.binary_dilation(ndimage.binary_opening(b[..., 3] > 20, np.ones((4, 4))), iterations=1)
        b[..., 3] = np.where(m, b[..., 3], 0); lab, n = ndimage.label(b[..., 3] > 4)
        if n > 1: b[..., 3] = np.where(lab == np.argmax(ndimage.sum(np.ones(lab.shape), lab, range(1, n + 1))) + 1, b[..., 3], 0)
        k = Image.fromarray(b, 'RGBA')
    k = licht(k); k = k.resize((round(k.width * F), round(k.height * F)), Image.LANCZOS)
    return k.quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.NONE)
if __name__ == '__main__':
    bron = sys.argv[1]
    for naam, clip in CLIPS.items():
        os.makedirs(os.path.join(UIT, clip), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(bron, naam + '.mp4'), '-vf', "select='not(mod(n\\,2))'", '-vsync', '0', tmp + '/%03d.png'], check=True)
            for i, f in enumerate(sorted(glob.glob(tmp + '/*.png'))):
                frame(clip, Image.open(f).convert('RGB')).save(os.path.join(UIT, clip, f'{clip}_{i:02d}.png'), optimize=True)
        print(clip)
