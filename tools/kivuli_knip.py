# Kivuli, de reizende handelaar (karakters/kivuli/): de Grok-clips van Tom (25-11-2026) naar losse frames voor het spel.
# python3 tools/kivuli_knip.py <map met de mp4's van Tom>   (nieuwe frames komen al getemperd uit frame(), DIM)
# python3 tools/kivuli_knip.py --temper                      (eenmalig: de frames die er al staan temperen, zonder de mp4's)
# Zoals duka_knip.py: 24 fps naar 12 fps, van het magenta af (key2 van Duka), op een vast doek, 256 kleuren.
# Het doek: 333x394, grondlijn op rij 386, lijf op x 187 (KIV in het spel). Bron 1168x768: figuur 609 hoog, voeten op
# rij 731, midden x 614. De korte wegdraai (1280x720) heeft een andere maat: die schalen en schuiven we op de voeten
# van zijn eerste frame, en de eerste 1,2 s (Grok staat daar stil) gaan eraf.
import numpy as np, os, sys, glob, subprocess, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duka_knip import key2
import matplotlib.colors as mc
DIM = 0.5        # Kivuli iets getemperd (Tom, 25-11-2026): de helft van de dimstap van Duka's versie 1 (zie licht)
def licht(im, k):
    # dezelfde stap als Duka's versies: iets minder verzadiging, de hoge lichten ingedrukt en een zweem warm; k 0 is het origineel
    a = np.asarray(im).astype(float) / 255; h = mc.rgb_to_hsv(a[..., :3]); h[..., 1] *= 1 - 0.12 * k; v = h[..., 2]
    h[..., 2] = np.where(v > 0.62, 0.62 + (v - 0.62) * (1 - 0.45 * k), v) * (1 - 0.04 * k)
    rgb = mc.hsv_to_rgb(h) * (1 - k * np.array([0, 0.04, 0.12])); rgb = rgb * (1 - 0.07 * k) + np.array([0.55, 0.45, 0.33]) * 0.07 * k
    return Image.fromarray((np.dstack([np.clip(rgb, 0, 1), a[..., 3]]) * 255).astype('uint8'), 'RGBA')
CLIPS = {'idle': 'idle', 'Jas open': 'jas', 'kap af': 'kapaf', 'kap op': 'kapop', 'kortewegdraai': 'draai',
         'lachgrijns': 'grijns', 'leunen': 'leun', 'muntgooien': 'munt', 'munttesten mond': 'bijt', 'psst wenk': 'psst',
         'schouderkijken': 'schouder', 'small walk opduiken lach': 'opduik', 'verdwijnen': 'verdwijn', 'wc': 'loop',
         'weglopenrug': 'weg', 'weigeren': 'weiger', 'zakje aanreiken': 'aanreik'}
S = 350 / 609; CX0, CY0, CW, CH = 290, 60, 580, 685
VAN = {'draai': 14}          # vanaf welk 12 fps-frame (de stilstand eraf)
UIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'karakters', 'kivuli')
def frame(clip, im):
    if im.size != (1168, 768):
        # de draai: zelfde lengte als idle, voeten op dezelfde plek
        k = 609 / 589; c = Image.new('RGB', (1168, 768), tuple(np.asarray(im)[3, 3]))
        g = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        c.paste(g, (round(614.5 - 640.5 * k), round(731 - 669 * k))); im = c
    a = key2(im)
    k = licht(Image.fromarray(a, 'RGBA'), DIM) if DIM else Image.fromarray(a, 'RGBA')
    k = k.crop((CX0, CY0, CX0 + CW, CY0 + CH)).resize((round(CW * S), round(CH * S)), Image.LANCZOS)
    return k.quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.NONE)
def tempering():
    # de bestaande frames in de repo (de mp4's staan er niet in) een keer temperen; het stempel voorkomt dubbel temperen
    stempel = os.path.join(UIT, '.getemperd')
    if os.path.exists(stempel): print('al getemperd:', open(stempel).read().strip()); return
    n = 0
    for f in sorted(glob.glob(UIT + '/*/*.png')):
        im = Image.open(f).convert('RGBA'); k = licht(im, DIM)
        k.quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.NONE).save(f, optimize=True); n += 1
    open(stempel, 'w').write('licht k=%s, %d frames\n' % (DIM, n)); print(n, 'frames getemperd')
if __name__ == '__main__' and sys.argv[1:] == ['--temper']:
    tempering(); sys.exit()
if __name__ == '__main__':
    bron = sys.argv[1]
    for naam, clip in CLIPS.items():
        d = os.path.join(UIT, clip); os.makedirs(d, exist_ok=True)
        for f in glob.glob(d + '/*.png'): os.remove(f)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(bron, naam + '.mp4'), '-vf', "select='not(mod(n\\,2))'", '-vsync', '0', tmp + '/%03d.png'], check=True)
            for i, f in enumerate(sorted(glob.glob(tmp + '/*.png'))[VAN.get(clip, 0):]):
                frame(clip, Image.open(f).convert('RGB')).save(os.path.join(d, f'{clip}_{i:02d}.png'), optimize=True)
        print(clip, len(glob.glob(d + '/*.png')))
