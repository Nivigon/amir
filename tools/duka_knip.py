# Duka, de marktman (karakters/duka/): de Grok-clips van 24-11-2026 naar losse frames voor het spel.
# python3 tools/duka_knip.py <map met de mp4's van Tom>
# python3 tools/duka_knip.py --herstel   alleen de tulband in de bestaande schap-frames dichtmaken (zie tulband_herstel)
# Elke clip (24 fps) gaat naar 12 fps, wordt van het magenta gehaald (key2 uit de marktman-tools), uitgesneden op een vast
# doek in de coordinaten van de 944-clips (de rugclips van 960 zijn een fractie groter en schuiven mee), verkleind en naar
# 256 kleuren gezet. In de originele kleuren uit Grok (Tom koos dat op 24-11-2026); --dim dimt hem voor het binnenlicht
# (licht), zoals de eerste versie.
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
def schijf(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]; return x * x + y * y <= r * r
def tulband_herstel(k):
    # De plank-regel van het schap (g<22, r~b) pakt ook de schaduwplooien van de paarse tulband: daar vielen gaten in
    # waar de muur doorheen scheen (25-11-2026). Binnen de omtrek van de tulband gaat alles weer dicht, in de kleur van
    # de dichtstbijzijnde dichte tulbandpixel, wat donkerder waar het gat helemaal open was (het was een plooi).
    b = np.asarray(k.convert('RGBA')).copy(); al = b[..., 3]
    r, g, bl = [b[..., i].astype(int) for i in range(3)]
    paars = (al > 200) & (np.minimum(r, bl) - g > 25) & (bl > 60)
    lab, n = ndimage.label(ndimage.binary_closing(paars, schijf(3)))
    if n == 0: return k
    maat = ndimage.sum(np.ones(lab.shape), lab, range(1, n + 1))
    hoog = ndimage.mean(np.indices(lab.shape)[0], lab, range(1, n + 1))
    kand = [i for i in range(n) if maat[i] > 300]
    if not kand: return k
    paars &= lab == min(kand, key=lambda i: hoog[i]) + 1   # het bovenste grote paarse stuk: de tulband
    romp = ndimage.binary_fill_holes(ndimage.binary_closing(paars, schijf(6)))
    gat = ndimage.binary_erosion(romp, schijf(1)) & (al < 240)
    if not gat.any(): return k
    _, (iy, ix) = ndimage.distance_transform_edt(~((al >= 240) & romp), return_indices=True)
    kl = b[iy, ix, :3].astype(float) * np.where(al[..., None] == 0, 0.82, 1.0); w = al[..., None] / 255.0
    b[gat, :3] = (b[..., :3] * w + kl * (1 - w))[gat].clip(0, 255).astype('uint8'); b[gat, 3] = 255
    return Image.fromarray(b, 'RGBA')
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
        k = tulband_herstel(Image.fromarray(b, 'RGBA'))
    if DIM: k = licht(k)
    k = k.resize((round(k.width * F), round(k.height * F)), Image.LANCZOS)
    return k.quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.NONE)
DIM = '--dim' in sys.argv
if __name__ == '__main__' and '--herstel' in sys.argv:
    # zonder de mp4's: alleen de tulband in de bestaande schap-frames repareren
    for f in sorted(glob.glob(os.path.join(UIT, 'schap', '*.png'))):
        tulband_herstel(Image.open(f)).quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.NONE).save(f, optimize=True)
    print('schap hersteld')
elif __name__ == '__main__':
    bron = [a for a in sys.argv[1:] if not a.startswith('--')][0]
    for naam, clip in CLIPS.items():
        os.makedirs(os.path.join(UIT, clip), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(bron, naam + '.mp4'), '-vf', "select='not(mod(n\\,2))'", '-vsync', '0', tmp + '/%03d.png'], check=True)
            for i, f in enumerate(sorted(glob.glob(tmp + '/*.png'))):
                frame(clip, Image.open(f).convert('RGB')).save(os.path.join(UIT, clip, f'{clip}_{i:02d}.png'), optimize=True)
        print(clip)
