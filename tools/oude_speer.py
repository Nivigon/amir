#!/usr/bin/env python3
"""De oude speer: Amirs eigen speer, verweerd en gespalkt, in drie standen.

Uit de gewone speer, zonder nieuwe art:
  amir runc/amir_sprites/design/amir/speer_projectiel.png  (liggend, punt rechts: de worp, de rug, los)
  design/speer.png                                         (staand, punt boven: in de grond)
schrijft het
  design/speer/oud/jav_3.png, jav_2.png, jav_1.png
  design/speer/oud/grond_3.png, grond_2.png, grond_1.png

Het cijfer is hoe vaak je hem nog kunt gebruiken. 3: verweerd, een touw om een barst. 2: een
tweede touw, meer roest en scheuren. 1: de schacht is gebroken onder het touw, de punt is
geschilferd. Het rode lint wordt een vale bruine lap (in de hand doet speerVerf hetzelfde).

  python3 tools/oude_speer.py
daarna tools/gen-offline-manifest.py.
"""
import colorsys, os, random
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAV = os.path.join(ROOT, 'amir runc/amir_sprites/design/amir/speer_projectiel.png')
GROND = os.path.join(ROOT, 'design/speer.png')
UIT = os.path.join(ROOT, 'design/speer/oud')

ROEST = [(120, 62, 28), (88, 48, 26)]
LAP = (128, 100, 74)          # de vale lap, waar het rode lint was
TOUW = ((168, 138, 92), (96, 72, 44))
BARST = (32, 20, 12)


def mix(c, d, t):
    return tuple(int(c[i] * (1 - t) + d[i] * t) for i in range(3))


def soort(p, x, punt):
    """punt: vanaf deze x (langs de as) begint het blad."""
    r, g, b, a = p
    if a < 20:
        return None
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if x >= punt * 0.75 and r > g * 1.5 and r > 60 and s > 0.45:
        return 'lap'
    if x >= punt and s < 0.25:
        return 'metaal'
    return 'hout'


def kolom(px, x, H):
    ys = [y for y in range(H) if px[x, y][3] > 120]
    return (ys[0], ys[-1]) if ys else None


def touw(im, x0, x1, schacht):
    """een touw om de schacht, van x0 tot x1 (langs de as), schuin gewikkeld"""
    px = im.load()
    W, H = im.size
    dik = max(1, round((x1 - x0) / 6))
    for x in range(max(0, x0), min(W, x1)):
        k = schacht.get(x)
        if not k:
            continue
        y0, y1 = k[0] - 1, k[1] + 1
        for y in range(max(0, y0), min(H, y1 + 1)):
            s = int((x - x0) + (y - y0) * 0.7) // dik
            c = TOUW[0] if s % 2 == 0 else TOUW[1]
            if y in (y0, y1):
                c = mix(c, (40, 28, 18), 0.5)
            px[x, y] = c + (255,)


def barst(im, rng, x0, x1, schacht, n):
    px = im.load()
    for _ in range(n):
        x = rng.randint(x0, x1)
        k = schacht.get(x)
        if not k:
            continue
        y = rng.randint(k[0] + 1, max(k[0] + 1, k[1] - 1))
        for i in range(rng.randint(6, 22) * max(1, (x1 - x0) // 300)):
            x += 1
            y += rng.choice([0, 0, 0, 1, -1])
            k = schacht.get(x)
            if not k or not (k[0] < y < k[1]):
                break
            px[x, y] = BARST + (255,)


def maak(bron, n, seed):
    """bron liggend, punt rechts. n = hoe vaak hij nog kan."""
    rng = random.Random(seed)
    im = bron.copy()
    W, H = im.size
    px = im.load()
    punt = int(W * 0.83)
    lap = [x for x in range(W) for y in range(H) if soort(px[x, y], x, punt) == 'lap']
    lapVan = min(lap) if lap else punt
    # de schacht per kolom, voor de lap uit
    schacht = {x: kolom(px, x, H) for x in range(W) if x < lapVan}
    oud = 3 - n                                           # 0, 1, 2
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            s = soort(p, x, punt)
            if not s:
                continue
            c = p[:3]
            z = rng.random()
            if s == 'metaal':
                t = (0.35 + 0.2 * oud) * (0.5 + 0.8 * z) if z > 0.25 else 0.15
                c = mix(c, ROEST[0] if z > 0.5 else ROEST[1], min(1, t))
            elif s == 'hout':
                g = sum(c) / 3
                c = mix(c, (g, g, g * 0.95), 0.35 + 0.05 * oud)
                c = tuple(int(v * (0.95 - 0.07 * oud)) for v in c)
                if z < 0.06 + 0.04 * oud:
                    c = tuple(int(v * 0.72) for v in c)
            elif s == 'lap':
                c = mix(c, LAP, 0.72)
            px[x, y] = c + (p[3],)
    # gaten in de lap
    for _ in range(0):
        if not lap:
            break
        cx = rng.choice(lap)
        ys = [y for y in range(H) if soort(px[cx, y], cx, punt) == 'lap']
        if not ys:
            continue
        cy = rng.choice(ys)
        r = max(1, H // 30)
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if 0 <= xx < W and 0 <= yy < H and soort(px[xx, yy], xx, punt) == 'lap':
                    px[xx, yy] = (0, 0, 0, 0)
    # de barst in het midden, en bij stand 1 de breuk: het achterste stuk zakt iets
    dikte = max((k[1] - k[0]) for k in schacht.values() if k)
    mid = int(lapVan * 0.48)
    lang = max(4, round(dikte * 1.7))
    if n == 1:
        zak = max(1, round(dikte * 0.22))
        achter = im.crop((0, 0, mid, H))
        im.paste((0, 0, 0, 0), (0, 0, mid, H))
        im.alpha_composite(achter, (0, zak))
        px = im.load()
        schacht = {x: kolom(px, x, H) for x in range(W) if x < lapVan}
        # gekartelde naad vlak naast het touw
        for x in range(mid - lang // 2 - 2, mid + lang // 2 + 3):
            k = schacht.get(x)
            if k and abs(x - mid) > lang // 2 - 2:
                for y in range(k[0], k[1] + 1):
                    if rng.random() < 0.85:
                        px[x, y] = BARST + (255,)
    barst(im, rng, 10, lapVan - 10, schacht, 2 + 4 * oud)
    touw(im, mid - lang // 2, mid + lang // 2, schacht)
    if n <= 2:
        m2 = int(lapVan * 0.22)
        touw(im, m2 - lang // 2, m2 + lang // 2, schacht)
    if n == 1:
        # een schilfer uit de punt
        d = ImageDraw.Draw(im)
        tip = max(x for x in range(W) for y in range(H) if px[x, y][3] > 120)
        ys = [y for y in range(H) if px[tip - 2, y][3] > 120]
        ym = ys[len(ys) // 2] if ys else H // 2
        st = max(2, (W - punt) // 7)
        d.polygon([(tip - st * 2, 0), (W, 0), (W, ym - 1), (tip - st, ym - 1)], fill=(0, 0, 0, 0))
    return im


def main():
    os.makedirs(UIT, exist_ok=True)
    jav = Image.open(JAV).convert('RGBA')
    grond = Image.open(GROND).convert('RGBA').rotate(-90, expand=True)   # punt naar rechts
    for n in (3, 2, 1):
        maak(jav, n, 10 + n).save(os.path.join(UIT, f'jav_{n}.png'))
        maak(grond, n, 20 + n).rotate(90, expand=True).save(os.path.join(UIT, f'grond_{n}.png'))
    print('geschreven:', UIT)


if __name__ == '__main__':
    main()
