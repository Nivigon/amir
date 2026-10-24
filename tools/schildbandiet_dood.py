"""De dood van de schildbandiet: de speer eruit, en het lijf op de grond.

In de bron-frames (enemies/schildbandiet/dood/dood_00..38, zoals ze in commit BRON staan) zit de speer
in de tekening: hij glipt op frame 7 uit zijn hand en ligt vanaf frame 13 plat voor zijn voeten. Het
spel laat die speer nu zelf vallen (een losse speer, enemies/schildbandiet/speer/speer_overlay.png, met
echte zwaartekracht, zodat hij ook in een ravijn of op een kei kan vallen). Dit script:

1. laat bron-frame 7 en 8 weg (WEG): daar valt de speer voor zijn tuniek en broek langs, en wat erachter
   zat is niet netjes terug te halen. Op frame 6 houdt hij hem nog vast, op het volgende frame (bron 9)
   hangt zijn hand leeg en valt de losse speer van het spel vanaf zijn heup (de pose op frame 6);
2. haalt uit de rest de speer weg: de losse speer-sprite op de plek van de getekende speer gelegd (punt
   en eind per frame, POSE), wat ruimer gemaakt, en alles daarbinnen weg; van bron 9 tot en met STAAN
   komen de voeten uit bron 8 terug (daar staan ze stil, en daar zit de speer er nog niet voor);
3. gooit losse vlekjes weg (de vegen en schaduwen van de vallende speer);
4. zet elk frame waarin hij ligt zo ver omlaag dat zijn lijf op de grondlijn ligt in plaats van erboven
   te zweven (LIG: de onderkant van het brede deel van het lijf).

Schrijft dood_00..36 (37 frames). Leest altijd uit commit BRON, dus het mag opnieuw draaien. Draai daarna
tools/gen-klein.py en tools/gen-offline-manifest.py. Schrijft in dood.json waar de speer loslaat (zijn
pose op frame 6, voor SCHB.dood.speer in het spel) en hoeveel elk frame omlaag is gezet.
"""
import io, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

HIER = Path(__file__).resolve().parent.parent
MAP = HIER / 'enemies' / 'schildbandiet' / 'dood'
SPEER = HIER / 'enemies' / 'schildbandiet' / 'speer' / 'speer_overlay.png'
BRON = '54bca24'
N, LOS, STAAN, VALT = 39, 9, 24, 30   # bron-frames; VALT: vanaf hier ligt hij met zijn lijf op de grond
WEG = (7, 8)                          # die gaan eruit: daar valt de speer voor zijn lijf langs
LIG = 484                             # daar komt de onderkant van het brede deel van zijn lijf
DIEPST = 496                          # lager dan dit komt niets van hem (een voet of hand ligt iets voor hem)
# punt en eind van de getekende speer per frame (canvas-px), opgemeten; vanaf 13 ligt hij bijna stil
POSE = {6: ((122, 277), (427, 291)), 7: ((124, 325), (427, 357)), 8: ((130, 392), (427, 442)),
        9: ((132, 481), (432, 475)), 10: ((135, 489), (427, 425)), 11: ((135, 476), (429, 426)),
        12: ((135, 475), (433, 460))}
VOET_VAK = (130, 440, 303, 488)       # x0, y0, x1, y1: de enkels en schoenen
# punt en eind in de sprite: de punt links, het eind van de schacht rechtsboven
S0, S1 = complex(1, 196), complex(1562, 21)
RUIM = 3            # zoveel px rond de speer gaat mee weg
KLEIN = 400         # losse vlekjes kleiner dan dit (in px) gaan weg


def bron(i):
    b = subprocess.run(['git', 'show', f'{BRON}:enemies/schildbandiet/dood/dood_{i:02d}.png'],
                       cwd=HIER, capture_output=True, check=True).stdout
    return np.array(Image.open(io.BytesIO(b)).convert('RGBA'))


def pose(i, a):
    if i in POSE:
        return POSE[i]
    al = a[:, :, 3] > 60                                  # hij ligt: het meest linkse en rechtse stuk speer
    ys, xs = np.where(al[488:]); k = np.argmin(xs); t = (int(xs[k]), int(ys[k]) + 488)
    ys, xs = np.where(al[479:]); k = np.argmax(xs); b = (int(xs[k]), int(ys[k]) + 479)
    return t, b


SP = Image.open(SPEER).convert('RGBA')


def dilate(m, r):
    o = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


def speerMasker(T, B, shape):
    c0, c1 = complex(*T), complex(*B)
    a = (S1 - S0) / (c1 - c0); b = S0 - a * c0
    data = (a.real, -a.imag, b.real, a.imag, a.real, b.imag)
    m = np.array(SP.transform((shape[1], shape[0]), Image.AFFINE, data, resample=Image.BILINEAR))[:, :, 3] > 10
    # en een strook langs de as, voor een schacht die in de tekening net anders loopt; onder de speer
    # wat ruimer, voor zijn schaduw en de veeg van de val
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    d = np.array([B[0] - T[0], B[1] - T[1]], float); L = np.hypot(*d); d /= L
    u = (xx - T[0]) * d[0] + (yy - T[1]) * d[1]
    v = -(xx - T[0]) * d[1] + (yy - T[1]) * d[0]
    breed = np.where(u < 0.3 * L, 10, 5)
    m |= (u > -3) & (u < L + 3) & (v > -breed) & (v < breed + 4)
    return dilate(m, RUIM)


def vlekken(al):
    """labels van samenhangende stukken (4-buren), met hun maat en hun bovenste rij"""
    h, w = al.shape
    lab = np.zeros((h, w), int); n = 0; info = {}
    for y0, x0 in zip(*np.where(al)):
        if lab[y0, x0]:
            continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n; c = 0; top = y0
        while st:
            y, x = st.pop(); c += 1; top = min(top, y)
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and al[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; st.append((yy, xx))
        info[n] = (c, top)
    return lab, info


def onderkant(a, minst):
    """de laagste rij met minstens zoveel dekkende px"""
    rijen = np.where((a[:, :, 3] > 128).sum(1) >= minst)[0]
    return int(rijen.max())


def main():
    frames = [bron(i) for i in range(N)]
    h, w = frames[0].shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    x0, y0, x1, y1 = VOET_VAK
    voetvak = (yy >= y0) & (yy < y1) & (xx >= x0) & (xx < x1)
    zolen = (yy <= 483) & (xx >= 150) & (xx <= 305)
    poses = {i: pose(i, frames[i]) for i in range(LOS, N)}
    schoon = [f.copy() for f in frames]
    for i in range(LOS, N):
        a = schoon[i]
        m = speerMasker(*poses[i], (h, w))
        if i > 12:
            m &= ~zolen                                    # de speer ligt: de zolen erboven blijven heel
        a[m] = 0
        if i <= STAAN:
            a[voetvak] = frames[8][voetvak]                # de voeten: het schone stuk uit bron 8
        lab, info = vlekken(a[:, :, 3] > 0)
        groot = max(info, key=lambda k: info[k][0])
        weg = [k for k, (c, top) in info.items() if k != groot and (c < KLEIN or top > 485)]
        a[np.isin(lab, weg)] = 0
    # het lijf op de grond: zodra hij ligt de onderkant van het brede deel van zijn lijf op LIG
    zak = [max(0, LIG - onderkant(schoon[i], 60)) if i >= VALT else 0 for i in range(N)]
    for k, f in ((1, 0.35), (2, 0.12)):                   # de landing loopt over de twee frames ervoor
        zak[VALT - k] = round(zak[VALT] * f)
    # en wat het laagst hangt (een voet, een hand) komt niet meer dan een paar px onder de grondlijn
    zak = [min(z, max(0, DIEPST - onderkant(schoon[i], 12))) if z else 0 for i, z in enumerate(zak)]
    for i in range(N):
        dy = zak[i]
        if dy:
            schoon[i] = np.roll(schoon[i], dy, 0); schoon[i][:dy] = 0
    volg = [i for i in range(N) if i not in WEG]
    for k, i in enumerate(volg):
        doel = MAP / f'dood_{k:02d}.png'
        if k == i and doel.exists() and np.array_equal(np.array(Image.open(doel).convert('RGBA')), schoon[i]):
            continue                                       # ongewijzigd: niet opnieuw wegschrijven
        Image.fromarray(schoon[i]).save(doel, optimize=True)
    for k in range(len(volg), N):                          # de oude laatste frames bestaan niet meer
        (MAP / f'dood_{k:02d}.png').unlink(missing_ok=True)
    js = json.loads(subprocess.run(['git', 'show', f'{BRON}:enemies/schildbandiet/dood/dood.json'],
                                   cwd=HIER, capture_output=True, check=True).stdout)
    fr = []
    for k, i in enumerate(volg):
        f = dict(js['frames'][i]); f['bestand'] = f'dood_{k:02d}.png'; f['omlaag'] = zak[i]; fr.append(f)
    js['frames'] = fr
    js['speer_los'] = {'frame': volg.index(LOS), 'pose_punt_eind': POSE[6],
                       'sprite': 'enemies/schildbandiet/speer/speer_overlay.png',
                       'sprite_punt_eind': [[1, 196], [1562, 21]]}
    (MAP / 'dood.json').write_text(json.dumps(js, indent=1, ensure_ascii=False) + '\n')
    print(len(volg), 'frames; speer los op', volg.index(LOS), '; omlaag', [zak[i] for i in volg])


if __name__ == '__main__':
    main()
