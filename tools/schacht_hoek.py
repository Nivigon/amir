"""Knipt het geschilderde hoekstuk voor de schacht (rond.jpg, magenta achtergrond) tot een game-sprite.

Het hoekstuk verzacht de rechte snede tussen de savanne-kap en de rotswand bovenin de schacht (Test 27),
en loopt over de tanden heen. Stappen: magenta ontmengen (sleutel min(r,b)-g, zoals baviaan_knip), de
grootste samenhangende vlek houden (losse key-pixels blazen de bbox op), bbox snijden, de kleur op de
grondrand-tinten afstemmen (rij-afhankelijk: de soil nauwelijks, de wand meer), de linkerrand in de band
laten overlopen en de onderrand in de rots laten vervagen.

Twee looplijnen worden gemeten en geprint, om in de HTML te bakken (SCHACHT_HOEK): crest (het
grondoppervlak, waar het stuk op de wandtop aansluit) en lip (waar de soil in de klif overgaat).
Verandert de bron, draai dit opnieuw en neem de geprinte crest/lip over.
"""
import sys
from collections import deque
from PIL import Image, ImageFilter

ROOT = '/home/user/amir'
BRON = ROOT + '/design/klimmen/bron/schacht_hoek.jpg'
UIT = ROOT + '/design/klimmen/schacht_hoek.png'
VOL, WEG = 30, 235
LIPFRAC = 0.44   # soil -> klif overgang, als fractie van de hoogte (gemeten uit de bron)

def knip(im):
    w, h = im.size; px = im.load()
    out = Image.new('RGBA', (w, h)); op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            m = min(r, b) - g
            if m <= VOL: op[x, y] = (r, g, b, 255)
            elif m >= WEG: op[x, y] = (0, 0, 0, 0)
            else:
                a = 1 - (m - VOL) / (WEG - VOL)
                f = lambda c, mg: max(0, min(255, round((c - (1 - a) * mg) / a)))
                op[x, y] = (f(r, 255), f(g, 0), f(b, 255), round(a * 255))
    return out

def grootste(spr):
    w, h = spr.size; px = spr.load()
    op = [[px[x, y][3] > 128 for x in range(w)] for y in range(h)]
    seen = [[False] * w for _ in range(h)]; best, bl = None, 0
    for y0 in range(h):
        for x0 in range(w):
            if op[y0][x0] and not seen[y0][x0]:
                q = deque([(x0, y0)]); seen[y0][x0] = True; comp = []
                while q:
                    x, y = q.popleft(); comp.append((x, y))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and op[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True; q.append((nx, ny))
                if len(comp) > bl: best, bl = comp, len(comp)
    mask = Image.new('L', (w, h), 0); mp = mask.load()
    for (x, y) in (best or []): mp[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(7)); mp = mask.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] == 0:
                r, g, b, a = px[x, y]
                if a: px[x, y] = (r, g, b, 0)
    return spr

def crestrij(spr):
    # de kruin (het grondoppervlak) aan de LINKERkant, waar het stuk op de band aansluit: de bovenste rij
    # met brede ondoorzichtige grond (graspol-smal overslaan). Daar verankert de HTML de hoogte op.
    w, h = spr.size; px = spr.load()
    lw = int(w * 0.30)
    def breed(y): return sum(1 for x in range(lw) if px[x, y][3] > 180)
    maxb = max((breed(y) for y in range(h)), default=1)
    return next((y for y in range(h) if breed(y) > 0.5 * maxb), 0)

def randweg(spr):
    # de magenta zoom langs de buitenrand weg-eroderen: de alfa 1 px intrekken (MinFilter), zonder de
    # zachte anti-aliasrand te verliezen. Zonder dit staat er een paars/magenta lijntje langs de bovenrand.
    r, g, b, a = spr.split()
    a = a.filter(ImageFilter.MinFilter(3))
    return Image.merge('RGBA', (r, g, b, a))

def main():
    im = Image.open(BRON).convert('RGB')
    spr = randweg(grootste(knip(im)))
    bb = spr.getbbox(); spr = spr.crop(bb)
    w, h = spr.size
    lip = int(h * LIPFRAC)
    crest = crestrij(spr)
    # kleur op de ECHTE band-tinten afstemmen (in-game gemeten, dicht bij de hoek): rij-afhankelijk,
    # zodat de soil nauwelijks donkerder wordt maar de wand duidelijk meer (anders is de sprite te oranje)
    RTOP = [0.925, 0.929, 0.972]      # soil-top
    RCL = [0.860, 0.894, 0.924]       # wand
    px = spr.load()
    for y in range(h):
        t = max(0.0, min(1.0, (y - 0.1 * h) / (0.5 * h)))
        rr = [RTOP[i] * (1 - t) + RCL[i] * t for i in range(3)]
        for x in range(w):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (round(r * rr[0]), round(g * rr[1]), round(b * rr[2]), a)
    # linkerrand ruim laten overlopen in de band (brede, zachte cross-fade met een smoothstep-curve)
    fw = int(w * 0.40)
    for x in range(fw):
        tt = x / fw; k = tt * tt * (3 - 2 * tt)
        for y in range(h):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (r, g, b, int(a * k))
    # onderrand laten vervagen in de rots (laatste 22%)
    fb = int(h * 0.22); h0 = h - fb
    for y in range(h0, h):
        k = 1 - (y - h0) / fb
        for x in range(w):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (r, g, b, int(a * k))
    spr.save(UIT)
    print('geschreven:', UIT)
    print('SCHACHT_HOEK: w=%d h=%d crest=%d lip=%d' % (w, h, crest, lip))

if __name__ == '__main__':
    main()
