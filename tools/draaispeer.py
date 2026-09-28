#!/usr/bin/env python3
"""Twee draaiende speren uit de video van Grok (draaispeer.mp4).

De video (design/speer/bron/draaispeer.mp4) laat een speer met twee koppen om zijn lengteas
draaien: links de gekartelde kop van de valspeer, rechts Amirs gewone kop met het rode lint. Alleen
het begin is bruikbaar (frame 0 tot 17: van plat naar op zijn kant); daarna spiegelt de speer en
worden de bladen een boor. Elk beeld staat er twee keer in.

Een hele omwenteling maken we uit dat ene stuk: plat -> kant (A), dan verticaal gespiegeld terug
van kant naar plat (de andere kant van het blad), weer gespiegeld naar de kant, en normaal terug.
Het blad is symmetrisch, dus zo is het een echte rol om de as, en de lus sluit naadloos.

De valspeer krijgt daarna zijn eigen uiterlijk (`zwart_staal`): een blad van zwart staal met
een geslepen, lichte snede langs de kartels en een middenrib, de ring onder het blad in goud, een
smalle gouden ring op de schacht en een gouden kap achteraan. Dat gebeurt op de frames van plat
naar kant, voor het spiegelen, met de maten en het licht van frame 0 voor alle frames, zodat niets
flikkert als hij rolt.

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
from PIL import Image, ImageFilter

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


GOUD = [(0, (70, 48, 14)), (0.4, (176, 132, 50)), (0.75, (230, 196, 106)), (1, (255, 244, 196))]
HOUT = [(0, (18, 12, 10)), (0.6, (52, 36, 28)), (1, (92, 66, 50))]
STAAL = ((8, 8, 10), (150, 152, 160), 3.2)       # donker, licht, en hoe steil: alleen de bolle plekken glimmen
SNEDE = ((196, 198, 204), 0.85)                  # de geslepen rand langs de kartels
RIB = ((120, 122, 130), 0.5)                     # de middenrib


def helder(a):
    return (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255


def verloop(a, m, stops, lo, hi):
    l = np.clip((helder(a) - lo) / max(1e-3, hi - lo), 0, 1)
    ps = [s[0] for s in stops]; cs = np.array([s[1] for s in stops], float)
    for c in range(3):
        a[..., c] = np.where(m, np.interp(l, ps, cs[:, c]), a[..., c])


def krimp(m, n):
    im = Image.fromarray((m * 255).astype(np.uint8))
    for _ in range(n):
        im = im.filter(ImageFilter.MinFilter(3))
    return np.array(im) > 128


def zwart_staal(frames, cy):
    """de valspeer: zwart staal, geslepen snede, goud op de ring, de schacht en de kap"""
    a0 = np.array(frames[0]).astype(float)
    H, W = a0.shape[:2]
    xx = np.tile(np.arange(W), (H, 1)); yy = np.tile(np.arange(H)[:, None], (1, W))
    hoog = (a0[..., 3] > 128).sum(0)
    schacht = int(np.median(hoog[W // 4:W // 2]))
    kx = next(x for x in range(W // 2, W) if hoog[x] >= schacht + 5)      # de ring onder het blad
    bx = next(x for x in range(kx, W) if hoog[x] > 35)                  # de voet van het blad
    # de maten van het licht, een keer uit frame 0
    def bereik(m):
        l = helder(a0)[m]
        return np.percentile(l, 3), np.percentile(l, 97)
    vol0 = a0[..., 3] > 20
    blad0, ring0 = vol0 & (xx >= bx), vol0 & (xx >= kx - 4) & (xx < bx)
    hout0 = vol0 & (xx < kx - 4)
    lr, lh = bereik(ring0), bereik(hout0)
    lo_b, hi_b = np.percentile(helder(a0)[blad0], 3), np.percentile(helder(a0)[blad0], 99)
    # een smalle gouden ring: een plakje van de ring onder het blad
    plak = a0[:, kx + 8:kx + 17].copy()
    verloop(plak, plak[..., 3] > 0, GOUD, *lr)
    plak = Image.fromarray(plak.clip(0, 255).astype(np.uint8)); plak = plak.crop(plak.getbbox())
    plak = plak.resize((max(3, round(plak.width * 0.8)), plak.height), Image.LANCZOS)
    uit = []
    for f in frames:
        a = np.array(f).astype(float)
        vol = a[..., 3] > 20
        blad = vol & (xx >= bx)
        l = np.clip((helder(a) - lo_b) / max(1e-3, hi_b - lo_b), 0, 1) ** STAAL[2]
        for c in range(3):
            a[..., c] = np.where(blad, STAAL[0][c] + (STAAL[1][c] - STAAL[0][c]) * l, a[..., c])
        ijzer = (a[..., 3] > 128) & (xx >= kx - 4)
        rand = krimp(ijzer, 2) & ~krimp(ijzer, 5) & (xx >= bx + 15)
        f_r = np.where(rand, SNEDE[1] * np.clip((xx - bx - 15) / 90, 0.25, 1), 0)[..., None]
        a[..., :3] = a[..., :3] * (1 - f_r) + np.array(SNEDE[0]) * f_r
        rib = blad & (np.abs(yy - cy) <= 1) & (xx < W - 18)
        a[..., :3] = np.where(rib[..., None], a[..., :3] * (1 - RIB[1]) + np.array(RIB[0]) * RIB[1], a[..., :3])
        verloop(a, vol & (xx >= kx - 4) & (xx < bx), GOUD, *lr)              # de ring onder het blad
        verloop(a, vol & (xx < kx - 4) & (xx >= 16), HOUT, *lh)              # de schacht, donker hout
        verloop(a, vol & (xx < 16), GOUD, *lh)                               # de kap achteraan
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        im.alpha_composite(plak, (round(kx - 25 - plak.width / 2), round(cy - plak.height / 2)))
        uit.append(im)
    return uit


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
        if naam == 'val':
            A = zwart_staal(A, cy)
        V = [im.transpose(Image.FLIP_TOP_BOTTOM) for im in A]
        rol = A + V[::-1][1:] + V[1:] + A[::-1][1:-1]
        for i, im in enumerate(rol):
            im.save(os.path.join(uit, f'{naam}_{i:02d}.png'), optimize=True)
        print(f'{naam}: {len(rol)} frames van {tot} bij {H}, punt op ({tot - 1}, {cy:.1f})')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else VIDEO, sys.argv[2] if len(sys.argv) > 2 else UIT)
