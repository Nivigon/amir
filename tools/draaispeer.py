#!/usr/bin/env python3
"""Twee draaiende speren uit de video van Grok (draaispeer.mp4).

De video (design/speer/bron/draaispeer.mp4) laat een speer met twee koppen om zijn lengteas
draaien: links de gekartelde kop van de valspeer, rechts Amirs gewone kop met het rode lint. Alleen
het begin is bruikbaar (frame 0 tot 17: van plat naar op zijn kant); daarna spiegelt de speer en
worden de bladen een boor. Elk beeld staat er twee keer in.

Een hele omwenteling maken we uit dat ene stuk: plat -> kant (A), dan verticaal gespiegeld terug
van kant naar plat (de andere kant van het blad), weer gespiegeld naar de kant, en normaal terug.
Het blad is symmetrisch, dus zo is het een echte rol om de as, en de lus sluit naadloos.

Per frame: magenta eruit (met de roze rand), de lichte scheefstand recht, in het midden doorknippen,
en elke helft aanvullen met een langere schacht en het achtereind van Amirs werpspeer. Beide sets
krijgen de schacht even dik als die werpspeer (18 bronpixels), de punt rechts.

De frames komen in design/speer/draai/ (val_00 tot val_35 en gewoon_00 tot gewoon_35); het spel
tekent ze met DRAAI in de HTML. Frame 0 is plat, zoals de gewone werpspeer.

    python3 tools/draaispeer.py
    python3 tools/gen-offline-manifest.py

Vereist Pillow, numpy en imageio: pip install pillow numpy imageio imageio-ffmpeg
"""
import os, sys
import numpy as np
from PIL import Image

try:
    import imageio
except ImportError:
    sys.exit('imageio ontbreekt: pip install imageio imageio-ffmpeg')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, 'design/speer/bron/draaispeer.mp4')
UIT = os.path.join(ROOT, 'design/speer/draai')
PROJ = os.path.join(ROOT, 'amir runc/amir_sprites/design/amir/speer_projectiel.png')
UNIEK = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]     # plat tot op zijn kant, zonder de dubbele beelden
MIDDEN = 688                                    # hier knippen we de twee speren uit elkaar
DIK = 18                                        # schachtdikte van Amirs werpspeer, in bronpixels
LENGTE = {'gewoon': 624, 'val': None}           # gewoon: net zo lang als de werpspeer; val: de kop maal 3,2


def uitknippen(f):
    a = f.astype(float)
    bg = np.median(np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3)]), axis=0)
    d = np.abs(a - bg).sum(-1)
    al = np.clip((d - 40) / 120, 0, 1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.clip(np.minimum(r, b) - g, 0, None)
    paars = (b > 0.6 * r) & (m > 0)
    a[..., 0] = np.where(paars, r - m, r)
    a[..., 2] = np.where(paars, b - m, b)
    al = np.where(al < 0.43, 0, al)
    return Image.fromarray(np.dstack([a, al * 255]).clip(0, 255).astype(np.uint8))


def schacht_midden(im, x):
    c = np.nonzero(np.array(im)[:, x, 3] > 128)[0]
    return (c.min() + c.max()) / 2, c.max() - c.min() + 1


def main(video, uit):
    os.makedirs(uit, exist_ok=True)
    frames = [f for f in imageio.get_reader(video)]
    ruw = [uitknippen(frames[i]) for i in UNIEK]
    # de scheefstand, gemeten op de schacht in frame 0
    (y1, _), (y2, _) = schacht_midden(ruw[0], 420), schacht_midden(ruw[0], 880)
    hoek = np.degrees(np.arctan2(y2 - y1, 880 - 420))
    ruw = [im.rotate(hoek, resample=Image.BICUBIC, center=(MIDDEN, (y1 + y2) / 2)) for im in ruw]
    as_y, dik = schacht_midden(ruw[0], MIDDEN)
    k = DIK / dik

    proj = Image.open(PROJ).convert('RGBA')
    pa = np.array(proj)[..., 3]
    pc = np.nonzero(pa[:, 20] > 128)[0]
    p_as, p_dik = (pc.min() + pc.max()) / 2, pc.max() - pc.min() + 1
    kp = DIK / p_dik
    eind = proj.crop((0, 0, 60, proj.height)).resize((round(60 * kp), round(proj.height * kp)), Image.LANCZOS)
    eind_as = p_as * kp

    # de kopgrens per helft: waar het ijzer (of het lint) begint, gemeten over alle frames
    def kopbegin(helft):
        xs = []
        for im in ruw:
            a = np.array(helft(im))[..., 3] > 128
            breed = [x for x in range(a.shape[1]) if a[:, x].sum() > dik + 4]
            xs.append(min(breed))
        return min(xs)

    helften = {
        'val': lambda im: im.crop((0, 0, MIDDEN, im.height)).transpose(Image.FLIP_LEFT_RIGHT),
        'gewoon': lambda im: im.crop((MIDDEN, 0, im.width, im.height)),
    }
    for naam, helft in helften.items():
        x0 = kopbegin(helft) - 12                 # een stukje schacht voor de kop blijft aan de kop
        stukken = []
        for im in ruw:
            h = helft(im)
            kop = h.crop((x0, 0, h.width, h.height))
            kop = kop.resize((round(kop.width * k), round(kop.height * k)), Image.LANCZOS)
            stukken.append(kop)
        kopw = stukken[0].width
        tot = LENGTE[naam] or round(kopw * 3.2)
        # het schachtstuk: uit frame 0, tussen het midden en de kop, op dezelfde schaal
        h0 = helft(ruw[0])
        sch = h0.crop((20, 0, x0, h0.height))
        sch = sch.resize((round(sch.width * k), round(sch.height * k)), Image.LANCZOS)
        a_s = as_y * k
        hoog = max(s.height for s in stukken)
        # het canvas: de as in het midden, zodat verticaal spiegelen om de as gaat
        boven = max(a_s, hoog - a_s, eind_as, eind.height - eind_as)
        H = int(np.ceil(boven * 2)) + 2
        cy = H / 2

        def bouw(kop):
            c = Image.new('RGBA', (tot, H))
            lang = tot - kopw - eind.width + 8
            x = eind.width - 8
            while x < eind.width - 8 + lang:
                w = min(sch.width, eind.width - 8 + lang - x)
                c.alpha_composite(sch.crop((0, 0, w, sch.height)), (x, round(cy - a_s)))
                x += w
            c.alpha_composite(eind, (0, round(cy - eind_as)))
            c.alpha_composite(kop, (tot - kopw, round(cy - a_s)))
            return c

        A = [bouw(s) for s in stukken]
        V = [im.transpose(Image.FLIP_TOP_BOTTOM) for im in A]
        rol = A + V[::-1][1:] + V[1:] + A[::-1][1:-1]
        for i, im in enumerate(rol):
            im.save(os.path.join(uit, f'{naam}_{i:02d}.png'), optimize=True)
        print(f'{naam}: {len(rol)} frames van {tot} bij {H}, punt op ({tot - 1}, {cy:.1f})')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else VIDEO, sys.argv[2] if len(sys.argv) > 2 else UIT)
