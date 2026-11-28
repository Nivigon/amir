# De gids van The First Hunt (design/tutorial/gids/): de Grok-clips van Tom (26/27-11-2026) naar spritebladen, en het
# spoor van de mentor (design/tutorial/mentor_spoor.json) gekoppeld aan zijn eigen animaties.
#   python3 tools/gids_bouw.py            alles
#   python3 tools/gids_bouw.py idle       alleen die animatie(s), de rest van gids.json en het spoor blijven staan
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
# Resolutie (27-11-2026): de vellen staan op de resolutie van Amirs eigen sprites. Amir staand is in
# karakters/amir/mkuki_spel/idle/idle_ns.png 276 px (AMIR_H), de gids staat in zijn vellen GIDS_KEER (1,15) keer zo hoog.
# LENGTE blijft de maat in de wereld; PX in gids.json zegt hoeveel wereld-eenheden een pixel van het vel is, zodat hij
# in beeld even groot blijft. Verkleinen met Lanczos op voorvermenigvuldigde alfa (geen donkere of roze rand), en de
# frames staan strak ingepakt: elk frame zijn eigen rechthoek (f: x, y, b, h, ankerX, ankerY) in plaats van een raster
# met de maat van het grootste frame. Daarnaast een halve set in klein/ voor Beeld: Licht (zelfde gids.json, het spel
# deelt de rechthoeken door de factor van het plaatje, zie gidsTeken). gen-klein.py laat die set staan (EIGEN).
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gids_kleur import kleur   # de kleuren van de gids (Indigo Sage), per frame voor de speer erop komt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BRON = os.path.join(ROOT, 'design/tutorial/gids/bron')
UIT = os.path.join(ROOT, 'design/tutorial/gids')
SPOOR = os.path.join(ROOT, 'design/tutorial/mentor_spoor.json')

LENGTE = 1.2 * 275                     # de gids staand, in sprite-eenheden
IDLE_H = 641                           # de gids staand in de idle-clip, in pixels
AMIR_H = 276                           # Amir staand in zijn idle-sprite (alleen de figuur), in pixels
GIDS_KEER = 1.15                       # de gids staand in zijn vellen: zoveel keer Amir
PIX = GIDS_KEER * AMIR_H / LENGTE      # pixels van het vel per wereld-eenheid (de wereldmaat blijft LENGTE)
RAND = 2                               # lege pixels om elk frame in het vel, ook na halveren nog een
BLAD_B = 4096                          # breedte van een vel (hooguit 4096 hoog en breed: de grens van zwakke videokaarten)
KLEIN = os.path.join(ROOT, 'klein/design/tutorial/gids')
STAP = {}                              # reserve: alleen elk zoveelste frame houden, bv. {'idle': 2} (nu niet nodig)
SCHAAL = {'idle': 1, 'verteller': 1, 'rc': 0.8, 'jump_and_land': 1.72, 'grote_sprong': 0.85,
          'slowcrouch': 0.66, 'lowcrouch': 0.66, 'roll1': 0.68, 'roll2': 0.68, 'roll3': 0.69}
# Clips waarin Grok langzaam inzoomt (27-11-2026): in de idle werd de gids over de clip 5 tot 6% groter (frame 0 641 px,
# het eind 672 px; de hele figuur, niet rechter op staan). Omdat de idle heen en weer speelt zwol hij in het spel op en
# kromp hij weer, en bij de wissel naar de verteller (die wel even groot blijft) sprong hij ineens 13 px kleiner. Hier
# meet het script per frame de lijfhoogte, legt er een gladde kromme door (graad 2, zodat het ademen niet meetelt) en
# schaalt elk frame terug naar de maat van het eerste.
ZOOM_VAST = ('idle',)
# Hoe groot elke animatie in het spel getekend wordt, bovenop de schaal van de vellen (gids.json: k per animatie; gidsTeken
# vermenigvuldigt ermee). 27-11-2026: eerst 1,135 voor alles in beweging (hij leek te krimpen als hij ging rennen), maar
# daarmee leek hij rennend juist groter. Gemeten (hoofd van de idle als sjabloon, op schaal gezocht in elk frame): op 1 is
# zijn hoofd in ren, buk, sluip en sprong even groot als in de idle, net als bij Amir (diens hoofd is in zijn ren ook even
# groot als in zijn idle). Dat hij rennend lager is komt door de houding. Het krimpen dat Tom eerst zag kwam vooral van de
# idle-clip die 6% inzoomde (rechtgezet met ZOOM_VAST). Alleen de sprintsprong had een iets kleiner hoofd: 1,05.
GROOTTE = {'idle': 1, 'verteller': 1, 'ren': 1.1, 'sprong': 1, 'groot': 1.05, 'buk': 1.15, 'sluip': 1.15, 'rol': 1}   # sluip en buk 1,15 (28-11-2026, Tom: sluipend leek hij veel kleiner dan staand)
SPEER = {'staal': (178, 184, 190), 'staalDonker': (104, 110, 118), 'hout': (112, 72, 42), 'houtDonker': (70, 44, 26)}
# 28-11-2026 (Tom): de gids draagt de Mkuki-basisspeer van Amir (met het rode doek) in plaats van de omgekleurde Grok-speer.
# Per frame: de lengteas en de punt van de groene speer (zoals hieronder in speer()), dan Amirs speer erlangs, de punt op de
# punt, even lang als de Grok-speer in de idle (SPEER_LEN, in pixels van de idle-clip; per clip gedeeld door SCHAAL). Het
# lijf komt er weer overheen (de vuist om de schacht); wat van de Grok-speer niet onder Amirs speer valt wordt leeg, of
# lijf als het midden in het lijf ligt. Wijst de speer naar links, dan wordt hij gespiegeld (het doek blijft boven).
# None = de oude omgekleurde Grok-speer (SPEER).
SPEER_AMIR = {'pad': os.path.join(ROOT, 'karakters/amir/mkuki_spel/bron/amirspeer_proj.png'),
              'punt': (623, 33), 'kont': (0, 42.5)}
SPEER_LEN = 595

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
SPRINT = 10**9                                                     # px/s: daarboven de grote sprong; uit (27-11-2026, Tom): ook bij het ravijn en in de race jump_and_land, dat lijkt op Amirs sprong (was 380)
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


def speer_amir(c, al, groen, lengte):
    """de groene speer vervangen door Amirs Mkuki-speer (SPEER_AMIR), zie boven"""
    gr = groen | (ndi.binary_dilation(groen, iterations=2) & ((c[..., 1] - np.maximum(c[..., 0], c[..., 2])) > 8))
    if groen.sum() < 30:
        al[gr] = 0
        return c
    ys, xs = np.where(groen)
    P = np.stack([xs, ys], 1).astype(float); m = P.mean(0)
    _, _, vt = np.linalg.svd(P - m, full_matrices=False)
    t = (P - m) @ vt[0]; L = t.max() - t.min()
    dwars = np.abs((P - m) @ vt[1])
    # de punt: het eind waar hij het breedst is (het blad), gemeten zonder wat tegen het lijf aan ligt (een groene vlek bij
    # de vuist leek anders een blad); twijfel (minder dan 1,3 keer zo breed) dan het eind dat het verst van het lijf af ligt
    lijf0 = (al > 0.5) & ~groen
    vrij = ~ndi.binary_dilation(lijf0, iterations=6)[ys, xs]
    lo, hi = (t < t.min() + 0.2 * L) & vrij, (t > t.max() - 0.2 * L) & vrij
    med = np.median(dwars)
    breed_lo = np.percentile(dwars[lo], 90) - med if lo.sum() > 10 else 0
    breed_hi = np.percentile(dwars[hi], 90) - med if hi.sum() > 10 else 0
    if max(breed_lo, breed_hi) > 1.3 * max(min(breed_lo, breed_hi), 0.5):
        naar_lo = breed_lo > breed_hi
    else:
        ly, lx = np.where(lijf0); zw = np.array([lx.mean(), ly.mean()]) if len(lx) else m
        naar_lo = np.linalg.norm(m + vt[0] * t.min() - zw) > np.linalg.norm(m + vt[0] * t.max() - zw)
    d = vt[0] * (-1 if naar_lo else 1)                                     # naar de punt
    T = m + d * ((P - m) @ d).max()                                        # de punt
    n = np.array([-d[1], d[0]]) if d[0] >= 0 else np.array([d[1], -d[0]])  # naar links gespiegeld: het doek blijft boven
    sp = SPEER_AMIR.setdefault('_im', np.asarray(Image.open(SPEER_AMIR['pad']).convert('RGBA')).astype(np.float32) / 255)
    Ti, Bi = np.array(SPEER_AMIR['punt'], float), np.array(SPEER_AMIR['kont'], float)
    e = (Ti - Bi) / np.linalg.norm(Ti - Bi); f = np.array([-e[1], e[0]])
    k = np.linalg.norm(Ti - Bi) / lengte                                   # beeldpixels van de speer per framepixel
    H, W = al.shape
    hb = sp.shape[0] / k                                                   # halve breedte ruim genomen
    hoeken = np.array([T + d * u + n * v for u in (-lengte - 4, 4) for v in (-hb, hb)])
    x0, y0 = np.floor(hoeken.min(0)).astype(int); x1, y1 = np.ceil(hoeken.max(0)).astype(int) + 1
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    laag = np.zeros((H, W, 4), np.float32)
    if x1 > x0 and y1 > y0:
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(float)
        u = (xx - T[0]) * d[0] + (yy - T[1]) * d[1]; v = (xx - T[0]) * n[0] + (yy - T[1]) * n[1]
        bx = Ti[0] + k * (u * e[0] + v * f[0]); by = Ti[1] + k * (u * e[1] + v * f[1])
        pm = np.dstack([sp[..., :3] * sp[..., 3:], sp[..., 3]])
        for ch in range(4):
            laag[y0:y1, x0:x1, ch] = ndi.map_coordinates(pm[..., ch], [by, bx], order=1, mode='constant', cval=0)
    sa = laag[..., 3]
    # wat van de Grok-speer overblijft: midden in het lijf (lijf aan beide kanten dwars op de speer) vullen met lijf, anders leeg
    lijf = (al > 0.5) & ~gr
    rest = gr & (sa < 0.5)
    alb = al.copy(); alb[gr] = 0
    if rest.any():
        ry, rx = np.where(rest); w = 10
        def op(dx, dy):
            qx = np.clip(np.round(rx + dx).astype(int), 0, W - 1); qy = np.clip(np.round(ry + dy).astype(int), 0, H - 1)
            return lijf[qy, qx]
        binnen = op(n[0] * w, n[1] * w) & op(-n[0] * w, -n[1] * w)
        if binnen.any():
            _, (iy, ix) = ndi.distance_transform_edt(~lijf, return_indices=True)
            by_, bx_ = ry[binnen], rx[binnen]
            c[by_, bx_] = c[iy[by_, bx_], ix[by_, bx_]]; alb[by_, bx_] = 1
    a2 = alb[..., None]
    uit = c / 255 * a2 + laag[..., :3] * (1 - a2)
    nal = alb + sa * (1 - alb)
    c[...] = np.clip(uit / np.maximum(nal, 1e-4)[..., None] * 255, 0, 255)
    al[...] = nal
    return c


def verklein(im, w, h):
    """Lanczos op voorvermenigvuldigde alfa: de kleur van de lege pixels lekt niet in de rand"""
    a = np.asarray(im.convert('RGBA')).astype(np.float32) / 255
    pm = np.dstack([a[..., :3] * a[..., 3:], a[..., 3]])
    kan = [np.asarray(Image.fromarray(pm[..., i]).resize((w, h), Image.LANCZOS)) for i in range(4)]
    al = np.clip(kan[3], 0, 1)
    rgb = np.clip(np.dstack(kan[:3]) / np.maximum(al, 1e-4)[..., None], 0, 1)
    al[al < 3 / 255] = 0                                   # het waas van de Lanczos-overslag weg
    rgb[al == 0] = 0
    return Image.fromarray((np.dstack([rgb, al[..., None]]) * 255 + 0.5).astype(np.uint8))


def inpak(cellen):
    """strak inpakken in rijen (planken), de hoogste frames eerst; geeft de maat van het vel en de plek per frame"""
    volg = sorted(range(len(cellen)), key=lambda k: -cellen[k][0].height)
    plek = [None] * len(cellen)
    x = y = rij_h = 0
    for k in volg:
        w, h = cellen[k][0].width + 2 * RAND, cellen[k][0].height + 2 * RAND
        if x + w > BLAD_B:
            x, y, rij_h = 0, y + rij_h, 0
        plek[k] = (x + RAND, y + RAND)
        x += w; rij_h = max(rij_h, h)
    return (BLAD_B if y else x), y + rij_h, plek


def opslaan(blad, pad):
    blad.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(pad, optimize=True)   # 256 kleuren, zoals Duka


def bouw(alleen=None):
    """alleen: een lijst animaties om opnieuw te bouwen; de rest van gids.json (en het spoor) blijft dan staan. Kan alleen
    als het aantal frames van die animaties gelijk blijft (het spoor wijst naar framenummers); draai daarna gids_glad.py."""
    os.makedirs(UIT, exist_ok=True); os.makedirs(KLEIN, exist_ok=True)
    f0 = LENGTE / IDLE_H
    info = {'lengte': LENGTE, 'px': round(1 / PIX, 6), 'anims': {}}
    oud = json.load(open(os.path.join(UIT, 'gids.json'))) if alleen else None
    cache = {}; nvol = {}
    for naam, delen in ANIMS.items():
        if alleen and naam not in alleen:
            info['anims'][naam] = dict(oud['anims'][naam], k=GROOTTE.get(naam, 1))
            continue
        cellen = []
        for clip, rng in delen:
            if clip not in cache:
                cache[clip] = frames(clip, range(145))
            s = f0 * SCHAAL[clip] * PIX
            zoom = {i: 1.0 for i in rng}
            if clip in ZOOM_VAST:
                hs = []
                for i in rng:
                    c, al, groen = key(cache[clip][i])
                    ys = np.where((al > 0.5) & ~groen)[0]
                    hs.append(ys.max() + 1 - ys.min())
                kr = np.polyval(np.polyfit(np.arange(len(hs)), hs, 2), np.arange(len(hs)))
                zoom = {i: kr[0] / kr[k] for k, i in enumerate(rng)}
                print(f'{clip}: zoom van de clip rechtgezet, {min(zoom.values()):.3f} .. {max(zoom.values()):.3f}')
            for i in rng:
                s = f0 * SCHAAL[clip] * PIX * zoom[i]
                c, al, groen = key(cache[clip][i])
                lijf = (al > 0.5) & ~groen
                ys, xs = np.where(lijf)
                # eerst de kleuren (Indigo Sage, met de groene speer er nog in), dan de speer: zo blijft het rode doek rood
                kl = np.asarray(kleur(Image.fromarray(np.dstack([c, al * 255]).clip(0, 255).astype(np.uint8)), 1 / s)).astype(np.float32)
                c = kl[..., :3].copy()
                wz = al * ~groen                                   # het lijf zonder speer: daarop zet gids_glad.py het anker
                c = speer_amir(c, al, groen, SPEER_LEN / SCHAAL[clip]) if SPEER_AMIR else speer(c, al, groen)
                rgba = np.dstack([c, al * 255]).clip(0, 255).astype(np.uint8)
                ys2, xs2 = np.where(al > 0.04)
                x0, x1, y0, y1 = xs2.min(), xs2.max() + 1, ys2.min(), ys2.max() + 1
                im = Image.fromarray(rgba[y0:y1, x0:x1])
                im = verklein(im, max(1, round(im.width * s)), max(1, round(im.height * s)))
                anker = ((xs.min() + xs.max()) / 2 - x0) * s, (ys.max() + 1 - y0) * s     # midden en onderkant van het lijf
                zx = ((wz.sum(0) * np.arange(wz.shape[1])).sum() / max(wz.sum(), 1e-6) - x0) * im.width / (x1 - x0)
                cellen.append((im, anker, round(float(zx), 1)))
        stap = STAP.get(naam, 1); nvol[naam] = len(cellen)
        cellen = cellen[::stap]
        bw, bh, plek = inpak(cellen)
        blad = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        fr = []
        zw = []
        for (im, (ax, ay), zx), (x, y) in zip(cellen, plek):
            blad.paste(im, (x, y))
            fr.append([x, y, im.width, im.height, round(ax, 1), round(ay, 1)])
            zw.append(zx)
        opslaan(blad, os.path.join(UIT, naam + '.png'))
        opslaan(verklein(blad, (bw + 1) // 2, (bh + 1) // 2), os.path.join(KLEIN, naam + '.png'))
        info['anims'][naam] = {'src': f'design/tutorial/gids/{naam}.png', 'n': len(cellen), 'stap': stap, 'k': GROOTTE.get(naam, 1), 'f': fr, 'zw': zw}
        print(naam, len(cellen), 'blad', blad.size, round(bw * bh * 4 / 1048576, 1), 'MiB')
    if alleen:
        for naam in alleen:
            if info['anims'][naam]['n'] != oud['anims'][naam]['n']:
                raise SystemExit(f'{naam}: aantal frames veranderd, bouw alles opnieuw (zonder argumenten)')
        info['spoor'] = oud['spoor']
    else:
        info['spoor'] = koppel(nvol)                               # in frames van de volle reeks
    if not alleen and any(v['stap'] > 1 for v in info['anims'].values()):   # het spoor wijst naar frames van de volle reeks
        for rij in info['spoor']['segs']:
            for k, e in enumerate(rij):
                if e and e[1] >= 0: rij[k] = [e[0], e[1] // info['anims'][e[0]]['stap']]
    # de controle: hoe hoog staat de gids in zijn vel, naast Amir
    im, (x, y) = None, info['anims']['idle']['f'][0][:2]
    w, h = info['anims']['idle']['f'][0][2:4]
    a = np.asarray(Image.open(os.path.join(UIT, 'idle.png')).convert('RGBA'))[y:y + h, x:x + w, 3] > 128
    ys, xs = np.where(a[:, int(w * 0.27):])                          # zonder de speer links
    print(f'gids staand {ys.max() + 1 - ys.min()} px, Amir {AMIR_H} px: {(ys.max() + 1 - ys.min()) / AMIR_H:.3f} keer')
    json.dump(info, open(os.path.join(UIT, 'gids.json'), 'w'), separators=(',', ':'))
    print('gids.json', os.path.getsize(os.path.join(UIT, 'gids.json')), 'bytes')


def soort(b):
    for k, n in [('idle', 'idle'), ('run/nieuw', 'ren'), ('jump/jump', 'spr'), ('bukken', 'buk'), ('sluipen', 'slp'), ('rol/', 'rol')]:
        if k in b:
            return n
    raise SystemExit('onbekend beeld in het spoor: ' + b)


def koppel(nvol):
    S = json.load(open(SPOOR))
    B = S['beelden']
    # het anker van elk beeld van Amir: midden en onderkant van zijn figuur, in beeldpixels, plus de maat van het beeld
    ankers = []
    for b in B:
        a = np.asarray(Image.open(os.path.join(ROOT, b)).convert('RGBA'))[..., 3] > 128
        ys, xs = np.where(a)
        ankers.append([round((xs.min() + xs.max()) / 2, 1), int(ys.max() + 1), a.shape[1], a.shape[0]])
    n = dict(nvol)
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
    bouw(sys.argv[1:] or None)                                     # bv. python3 tools/gids_bouw.py idle
