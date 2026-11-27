# De gids van The First Hunt (design/tutorial/gids/): de Grok-clips van Tom (26/27-11-2026) naar spritebladen, en het
# spoor van de mentor (design/tutorial/mentor_spoor.json) gekoppeld aan zijn eigen animaties.
#   python3 tools/gids_bouw.py
# Leest de mp4's uit design/tutorial/gids/bron/ en schrijft per animatie een blad (<anim>.png) en gids.json.
#
# Keyen: magenta weg met een smalle ramp (0,92 en 0,62 van de achtergrond-key), randen terugrekenen zonder de achtergrond,
# en despill: waar rood en blauw samen boven groen uitkomen gaat dat eraf. Dat haalt de roze glans uit het donkere haar en
# de knot (Tom zag roze door zijn haar heen). Huid, rood, teal en koper raakt het niet (daar is blauw of rood lager dan groen).
# De speer is in de bron egaal groen (#00C800), zodat hij weg of te vervangen is; hier wordt hij voor het spel omgekleurd:
# het dikke deel (blad en lintje) staal, de schacht hout. Wil je een andere speer, pas SPEER aan of zet hem uit (None).
#
# Schaal: elke clip is anders ingezoomd. SCHAAL zegt per clip hoeveel pixels van de idle-clip een pixel is, geijkt op de
# grootte van het hoofd (27-11-2026, naast de idle gelegd). LENGTE is de gids staand in sprite-eenheden: 1,2 x Amir (de
# idle_ns van Amir is 275 hoog), ongeveer bandietmaat.
#
# Koppelen: het spoor bestaat uit beelden van Amir. Per beeld van het spoor kiest dit script een frame van de gids:
#  idle   -> 'idle' (het spel kiest zelf: de vertel-clip als hij net iets uitlegt, anders de idle-lus)
#  ren    -> rc, een lus van 24 frames, op afstand (24 frames per 330 px, dus sprinten gaat sneller door de lus)
#  sprong -> per fase van Amir (hurk, afzet, stijgen, top, vallen, landing) een stuk van jump_and_land, of van
#            grote_sprong als hij harder dan 380 px/s gaat (de sprintsprong en de race); opspringen is die clip achteruit.
#            Uit de ren (boven 200 px/s) slaat de gewone sprong het rechtop staan met de speer verticaal over.
#  bukken -> een stil gehurkt frame van slowcrouch; sluipen -> de lus van lowcrouch, op tijd
#  rol    -> roll1 (vanaf de duik), roll2 (tot hij zit) en roll3 (opveren naar de hurk), over de lengte van de rol
# Elke gids-frame krijgt een anker: midden en onderkant van het lijf (zonder speer). Het spel zet dat anker op het anker
# van het beeld van Amir (ook midden en onderkant van zijn figuur), gespiegeld als Amir gespiegeld is.
import json, os, subprocess, sys, tempfile, glob
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BRON = os.path.join(ROOT, 'design/tutorial/gids/bron')
UIT = os.path.join(ROOT, 'design/tutorial/gids')
SPOOR = os.path.join(ROOT, 'design/tutorial/mentor_spoor.json')

LENGTE = 1.2 * 275                     # de gids staand, in sprite-eenheden
IDLE_H = 641                           # de gids staand in de idle-clip, in pixels
SCHAAL = {'idle': 1, 'verteller': 1, 'rc': 0.8, 'jump_and_land': 1.72, 'grote_sprong': 0.85,
          'slowcrouch': 0.66, 'lowcrouch': 0.66, 'roll1': 0.68, 'roll2': 0.68, 'roll3': 0.69}
SPEER = {'staal': (178, 184, 190), 'staalDonker': (104, 110, 118), 'hout': (112, 72, 42), 'houtDonker': (70, 44, 26)}

# de animaties: welke frames uit welke clip
ANIMS = {
    'idle':      [('idle', range(0, 145, 2))],                       # 12 fps, heen en terug in het spel
    'verteller': [('verteller', range(0, 145, 2))],                  # 12 fps, een keer, dan de idle
    'ren':       [('rc', range(10, 34))],                            # lus van 24 (24 fps)
    'sprong':    [('jump_and_land', range(14, 112))],
    'groot':     [('grote_sprong', range(0, 40))],
    'buk':       [('slowcrouch', range(40, 64, 2))],
    'sluip':     [('lowcrouch', range(64, 122))],                    # lus van 58 (24 fps)
    'rol':       [('roll1', range(52, 145, 3)), ('roll2', range(0, 53, 3)), ('roll3', range(12, 25, 2))],   # over de kop, opzitten, opveren
}
# fasen van Amirs sprong (amirjump1..6) naar frames van de gids-animatie (indexen in het blad)
SPRONG = {1: (2, 10), 2: (14, 16), 3: (18, 24), 4: (26, 62), 5: (66, 74), 6: (82, 94)}   # jump_and_land vanaf 14, uit stilstand
SPRONG_REN = {1: (19, 19), 2: (20, 20), 3: (20, 22), 4: (26, 62), 5: (66, 74), 6: (82, 94)}   # uit de ren: niet eerst rechtop staan met de speer verticaal
STIL = 200                                                         # px/s: daaronder springt hij uit stilstand (de hoge korte sprong)
GROOT = {1: (36, 36), 2: (33, 22), 3: (20, 6), 4: (3, 0), 5: (2, 22), 6: (24, 39)}         # grote_sprong, 2 en 3 achteruit
SPRINT = 380                                                       # px/s: daarboven is het de grote sprong
REN = {'start': 0, 'n': 24, 'px': 330}
SLUIP_FPS = 24


def frames(clip, nodig):
    d = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(BRON, clip + '.mp4'), d + '/%03d.png'], check=True)
    return {i: np.asarray(Image.open(f'{d}/{i + 1:03d}.png').convert('RGB')) for i in nodig}


def key(a, HI=0.92, LO=0.62):
    a = a.astype(np.float32)
    rand = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    bg = np.median(rand, axis=0)
    kbg = min(bg[0], bg[2]) - bg[1]
    k = np.minimum(a[..., 0], a[..., 2]) - a[..., 1]
    al = np.clip((HI * kbg - k) / ((HI - LO) * kbg), 0, 1)
    am = np.maximum(al, 0.05)[..., None]
    c = np.clip(np.where(al[..., None] < 0.999, (a - (1 - am) * bg) / am, a), 0, 255)
    spill = np.maximum(0, np.minimum(c[..., 0], c[..., 2]) - c[..., 1])          # het roze in het haar
    c[..., 0] -= spill; c[..., 2] -= spill
    vast = al > 0.5
    lab, n = ndi.label(vast)
    if n:                                                                         # spikkels weg
        maat = ndi.sum(vast, lab, range(1, n + 1))
        houd = np.zeros(n + 1, bool); houd[1:] = maat >= max(400, maat.max() * 0.02)
        al[~ndi.binary_dilation(houd[lab], iterations=3)] = 0
    groen = ((c[..., 1] - np.maximum(c[..., 0], c[..., 2])) > 45) & (al > 0.3)
    return c, al, groen


def speer(c, al, groen):
    """de groene speer omkleuren: het dikke deel staal, de schacht hout, met een donkere rand"""
    if SPEER is None:
        al[groen] = 0
        return c
    if groen.sum() < 30:
        return c
    # de lengteas van de speer; de punt is het eind waar hij het breedst is (het blad), de laatste 17% daar is staal
    ys, xs = np.where(groen)
    P = np.stack([xs, ys], 1).astype(float); m = P.mean(0)
    _, _, vt = np.linalg.svd(P - m, full_matrices=False)
    t = (P - m) @ vt[0]; L = t.max() - t.min()
    dwars = np.abs((P - m) @ vt[1])
    eind = 0.2 * L
    lo, hi = t < t.min() + eind, t > t.max() - eind
    breed_lo = np.percentile(dwars[lo], 90) - np.median(dwars) if lo.any() else 0
    breed_hi = np.percentile(dwars[hi], 90) - np.median(dwars) if hi.any() else 0
    tip = t < t.min() + 0.17 * L if breed_lo >= breed_hi else t > t.max() - 0.17 * L
    blad = np.zeros_like(groen); blad[ys[tip], xs[tip]] = True
    dt = ndi.distance_transform_edt(groen)
    r = np.median(dt[groen]) + 0.5
    rand = groen & ~ndi.binary_erosion(groen, iterations=max(1, int(round(r * 0.5))))
    c = c.copy()
    for m, kl in [(groen & ~blad, SPEER['hout']), (blad, SPEER['staal']), (rand & ~blad, SPEER['houtDonker']), (rand & blad, SPEER['staalDonker'])]:
        c[m] = kl
    return c


def bouw():
    os.makedirs(UIT, exist_ok=True)
    f0 = LENGTE / IDLE_H
    info = {'lengte': LENGTE, 'anims': {}}
    cache = {}
    for naam, delen in ANIMS.items():
        cellen = []
        for clip, rng in delen:
            if clip not in cache:
                cache[clip] = frames(clip, range(145))
            s = f0 * SCHAAL[clip]
            for i in rng:
                c, al, groen = key(cache[clip][i])
                lijf = (al > 0.5) & ~groen
                ys, xs = np.where(lijf)
                c = speer(c, al, groen)
                rgba = np.dstack([c, al * 255]).clip(0, 255).astype(np.uint8)
                ys2, xs2 = np.where(al > 0.04)
                x0, x1, y0, y1 = xs2.min(), xs2.max() + 1, ys2.min(), ys2.max() + 1
                im = Image.fromarray(rgba[y0:y1, x0:x1])
                w, h = max(1, round(im.width * s)), max(1, round(im.height * s))
                im = im.resize((w, h), Image.LANCZOS)
                anker = ((xs.min() + xs.max()) / 2 - x0) * s, (ys.max() + 1 - y0) * s     # midden en onderkant van het lijf
                cellen.append((im, anker))
        cw = max(c[0].width for c in cellen) + 2; ch = max(c[0].height for c in cellen) + 2
        cols = max(1, min(len(cellen), 4096 // cw))
        rows = (len(cellen) + cols - 1) // cols
        blad = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0))
        ankers = []
        for k, (im, (ax, ay)) in enumerate(cellen):
            x, y = (k % cols) * cw, (k // cols) * ch
            blad.paste(im, (x + 1, y + 1))
            ankers.append([round(ax + 1, 1), round(ay + 1, 1)])
        blad.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(os.path.join(UIT, naam + '.png'), optimize=True)   # 256 kleuren, zoals Duka
        info['anims'][naam] = {'src': f'design/tutorial/gids/{naam}.png', 'n': len(cellen), 'cols': cols, 'cw': cw, 'ch': ch, 'anker': ankers}
        print(naam, len(cellen), 'cel', cw, ch, 'blad', blad.size)
    info['spoor'] = koppel(info)
    json.dump(info, open(os.path.join(UIT, 'gids.json'), 'w'), separators=(',', ':'))
    print('gids.json', os.path.getsize(os.path.join(UIT, 'gids.json')), 'bytes')


def soort(b):
    for k, n in [('idle', 'idle'), ('run/nieuw', 'ren'), ('jump/jump', 'spr'), ('bukken', 'buk'), ('sluipen', 'slp'), ('rol/', 'rol')]:
        if k in b:
            return n
    raise SystemExit('onbekend beeld in het spoor: ' + b)


def koppel(info):
    S = json.load(open(SPOOR))
    B = S['beelden']
    # het anker van elk beeld van Amir: midden en onderkant van zijn figuur, in beeldpixels, plus de maat van het beeld
    ankers = []
    for b in B:
        a = np.asarray(Image.open(os.path.join(ROOT, b)).convert('RGBA'))[..., 3] > 128
        ys, xs = np.where(a)
        ankers.append([round((xs.min() + xs.max()) / 2, 1), int(ys.max() + 1), a.shape[1], a.shape[0]])
    n = {k: v['n'] for k, v in info['anims'].items()}
    uit = {'amir': ankers, 'segs': []}
    for sg in [S['start']] + S['segs']:
        f = sg['f']; rij = [None] * len(f)
        i = 0
        while i < len(f):
            c = soort(B[f[i][2]]); j = i
            while j + 1 < len(f) and soort(B[f[j + 1][2]]) == c:
                j += 1
            run = range(i, j + 1)
            if c == 'idle':
                for k in run: rij[k] = ['idle', -1]
            elif c == 'ren':
                afst = 0
                for k in run:
                    if k > i: afst += abs(f[k][0] - f[k - 1][0])
                    rij[k] = ['ren', REN['start'] + int(afst / REN['px'] * 24) % REN['n']]
            elif c == 'buk':
                for k in run: rij[k] = ['buk', min(n['buk'] - 1, (k - i) // 2)]
            elif c == 'slp':
                for k in run: rij[k] = ['sluip', int((k - i) / 30 * SLUIP_FPS) % n['sluip']]
            elif c == 'rol':
                L = len(run)
                for k in run: rij[k] = ['rol', min(n['rol'] - 1, round((k - i) / max(1, L - 1) * (n['rol'] - 1)))]
            elif c == 'spr':
                v = abs(f[j][0] - f[i][0]) / max(1, j - i) * 30
                groot = v > SPRINT
                tab, anim = (GROOT, 'groot') if groot else ((SPRONG, 'sprong') if v < STIL else (SPRONG_REN, 'sprong'))
                k = i
                while k <= j:                                     # per fase van Amir een stuk van de clip
                    p = int(B[f[k][2]].split('amirjump')[1][0]); e = k
                    while e + 1 <= j and int(B[f[e + 1][2]].split('amirjump')[1][0]) == p:
                        e += 1
                    a, b = tab[p]
                    for q in range(k, e + 1):
                        t = (q - k) / max(1, e - k)
                        rij[q] = [anim, round(a + (b - a) * t)]
                    k = e + 1
            i = j + 1
        uit['segs'].append(rij)
    return uit


if __name__ == '__main__':
    bouw()
