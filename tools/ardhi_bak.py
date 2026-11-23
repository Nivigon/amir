#!/usr/bin/env python3
"""De Ardhi-wapens en hun effecten: uit de Grok-platen in design/ardhi/bron/ (screenshots van de originelen, 1:1).

  stok_grok.jpg   de wortelknoest-stok met botklauw (grip links), op magenta en een roze vlak
  speer_grok.jpg  Ardhi's Reach, liggend, punt naar rechts
  heel_grok.jpg   vier heal-effecten op zwart: de vine-ring (links) en de sapdruppel (rechts) gebruiken we

Uit:
  design/ardhi/bron/stok_schoon.png      de stokplaat op zuiver magenta, voor tools/stok_variant.py (--plaat)
  design/speer/ardhi/jav.png             de speer zoals javImg: punt rechts op (w-1, midden van de schacht)
  design/ardhi/druppel.png               de sapdruppel met zijn gloed (alfa uit het zwart)
  design/ardhi/druppel_los.png           de kale druppel (zonder blaadjes en plasje), die in het spel valt
  design/ardhi/ring.png                  de vine-ring met aarde, het plantje bij de voeten van een geroote vijand
  karakters/amir/mkuki_spel/bron/ar_<hoek>.png en 'ar' in los.json: de speer in Amirs hand, zoals de Pathfinder
  items/winkel/ardhi.png (Ardhi's Grip), ardhireach.png, ardhiroots.png: de plaatjes in de winkel

Gebruik:  python3 tools/ardhi_bak.py      (zet de regel die het print in ARDHI.speer)
          python3 tools/ardhi_bak.py --speer   alleen de speer, bijvoorbeeld na een andere kleur in KLEUR
Daarna:   python3 tools/stok_variant.py --rij 0 --uit stokken_ardhi --plaat design/ardhi/bron/stok_schoon.png --grip 70,120,40
          de map stokken_ardhi ook naar klein/karakters/amir/, en python3 tools/gen-offline-manifest.py
"""
import json, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'design', 'ardhi', 'bron')


# ---- Ardhi's Reach: de kleuren per zone, de ranken, de dikte en de rand ----
# De speer wordt in zones verdeeld (hout, ranken, greep, bot), zodat elke kleur hier een regel is. None houdt de kleur
# uit de Grok-plaat; een (r, g, b) kleurt die zone om met zijn eigen licht en schaduw (de helderheid ten opzichte van
# het midden van de zone). Daarna krijgen de ranken een donkere contour (zodat ze in de hand niet wegvallen), wordt de
# schacht dikker en komt de rand van de gewone speer erom, net als bij de Pathfinder (tools/pathfinder_speer.py).
KLEUR = {
    'hout':  None,              # de schacht
    'rank':  (96, 168, 52),     # de ranken, feller dan de bron
    'greep': (222, 205, 170),   # het leren bandje halverwege: bot-wit, zoals de klauw en de punt
    'bot':   None,              # de klauw en de punt
}
RANK_CONTOUR = (38, 70, 22)     # de donkergroene lijn om de ranken
RANK_DIK = 2                    # hoe dik die lijn is (px op de 624 lange speer)
GREEP = (247, 309)              # waar het bandje zit, in x op de 624 lange speer
DIKKER = 1.3                    # de schacht dikker (alleen in de hoogte)
RAND_DIK = 2                    # de donkere omlijning (px)
RAND_LIJN = (34, 26, 22); RAND_GLIM = (186, 183, 183, 78); RAND_SCHADUW = (0, 0, 0, 140)


def zones(a):
    """Per pixel de zone: rank (groen), bot (licht en ongekleurd), greep (het bandje) en de rest is hout."""
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    vol = al > 60
    rank = vol & (g > r * 1.08) & (g > b * 1.15)
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    bot = vol & ~rank & (lum > 150) & (r - b < 70)
    x = np.arange(a.shape[1])[None, :]
    greep = vol & ~rank & ~bot & (x >= GREEP[0]) & (x < GREEP[1])
    hout = vol & ~rank & ~bot & ~greep
    return {'hout': hout, 'rank': rank, 'greep': greep, 'bot': bot}, lum


def speer_kleur(im):
    a = np.array(im).astype(float)
    Z, lum = zones(a)
    for naam, kl in KLEUR.items():
        m = Z[naam]
        if kl is None or not m.any(): continue
        sch = np.clip(lum[m] / max(np.median(lum[m]), 1), 0.35, 1.6)
        for i in range(3): a[..., i][m] = np.clip(kl[i] * sch, 0, 255)
    # de contour om de ranken, ook een stukje erbuiten, dekkend
    om = ndimage.binary_dilation(Z['rank'], iterations=RANK_DIK) & ~Z['rank'] & ~Z['bot']
    a[om, :3] = RANK_CONTOUR; a[om, 3] = 255
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def speer_rand(im):
    a = np.array(im).astype(np.int32); m = a[..., 3] > 128
    lijn = m & ~ndimage.binary_erosion(m, iterations=RAND_DIK)
    uit = np.zeros_like(a); uit[m] = a[m]; uit[m, 3] = 255; uit[lijn, :3] = RAND_LIJN
    for x in range(a.shape[1]):
        ys = np.where(m[:, x])[0]
        if not len(ys): continue
        if ys[0] > 0: uit[ys[0] - 1, x] = RAND_GLIM
        if ys[-1] + 1 < a.shape[0]: uit[ys[-1] + 1, x] = RAND_SCHADUW
    return Image.fromarray(uit.astype(np.uint8), 'RGBA')


def magenta_alfa(a):
    """Alfa uit magenta en het roze vlak: hoe magenta (min(r,b) boven g) een pixel is."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    al = np.clip((0.62 - m) / 0.30, 0, 1)
    ex = np.clip(np.minimum(r, b) - g, 0, None) * (1 - al)          # despill: het roze uit de randen
    rgb = np.dstack([r - ex, g, b - ex])
    return np.clip(rgb, 0, 255), al


def zwart_alfa(a, drempel=34):
    """Alfa uit zwart: wat vanaf de rand met zwart verbonden is wordt doorzichtig naar zijn helderheid (de gloed),
    de rest (de vaste vormen met hun donkere omlijning) blijft heel."""
    mx = a.max(-1)
    donker = mx < drempel
    lab, _ = ndimage.label(donker)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    # ook een groot ingesloten zwart vlak is achtergrond (het midden van de ring)
    n = lab.max()
    if n:
        maat = ndimage.sum(np.ones_like(mx), lab, range(1, n + 1))
        rand |= {i + 1 for i in range(n) if maat[i] > 1500}
    buiten = np.isin(lab, list(rand))
    # de gloed rond de vormen: ook licht dat niet donker is maar wel buiten de vormen (zacht) via helderheid
    al = np.ones(mx.shape)
    gl = np.clip((mx - 6) / 120.0, 0, 1)
    al[buiten] = gl[buiten]
    # kleine lichtjes (stuifmeel) zijn gloed, geen vorm: ook die naar hun helderheid
    lv, nv = ndimage.label(~buiten)
    if nv:
        mv = ndimage.sum(np.ones_like(mx), lv, range(1, nv + 1))
        klein = np.isin(lv, [i + 1 for i in range(nv) if mv[i] < 400])
        al[klein] = gl[klein]; buiten = buiten | klein
    # een zachte overgang aan de rand van de vormen
    vast = ~buiten
    afst = ndimage.distance_transform_edt(vast)
    rand_z = (afst > 0) & (afst < 2.5)
    al[rand_z] = np.maximum(al[rand_z], np.clip(afst[rand_z] / 2.5, 0, 1))
    rgb = a / np.maximum(al[..., None], 1e-3)                           # zwart eruit (unpremultiply)
    return np.clip(rgb, 0, 255), al


def schoon(al, deel=0.02):
    """Alleen de grote vormen en wat er vlak bij ligt (geen muiscursor of ruis in een hoek van de screenshot)."""
    lab, n = ndimage.label(ndimage.binary_dilation(al > 0.3, iterations=12))
    if n > 1:
        maat = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
        hou = np.isin(lab, [i + 1 for i in range(n) if maat[i] >= maat.max() * deel])
        al = al * hou
    return al


def licht_alfa(a):
    """Alfa uit de helderheid (voor licht op zwart, zoals de druppel): helder dekt, donker laat door. Over een scene
    getekend geeft dat bijna wat 'screen' geeft: de gloed licht op, de donkere omlijning valt weg."""
    mx = a.max(-1)
    al = np.clip(mx / 200.0, 0, 1) ** 0.85
    rgb = a / np.maximum(al[..., None], 1e-3)
    return np.clip(rgb, 0, 255), al


def bijsnijden(rgb, al, marge=4):
    al = schoon(al)
    ys, xs = np.where(al > 0.04)
    y0, y1, x0, x1 = max(0, ys.min() - marge), ys.max() + marge + 1, max(0, xs.min() - marge), xs.max() + marge + 1
    return Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8)[y0:y1, x0:x1])


def stokplaat():
    a = np.array(Image.open(os.path.join(BRON, 'stok_grok.jpg')).convert('RGB')).astype(float)
    rgb, al = magenta_alfa(a)
    al[al < 0.08] = 0
    uit = rgb * al[..., None] + np.array([255, 0, 255]) * (1 - al[..., None])
    Image.fromarray(uit.astype(np.uint8)).save(os.path.join(BRON, 'stok_schoon.png'))
    # het winkelplaatje: de stok schuin, zoals de andere stokken
    im = bijsnijden(rgb, al)
    return im


def speer():
    a = np.array(Image.open(os.path.join(BRON, 'speer_grok.jpg')).convert('RGB')).astype(float)
    rgb, al = magenta_alfa(a)
    al[al < 0.08] = 0
    al = schoon(al); al[al < 0.2] = 0
    im = bijsnijden(rgb, al, 0)
    # de punt: de meest rechtse pixel; de schacht: zijn midden, gemeten aan de kont-kant
    A = np.array(im)[..., 3] > 100
    xs = np.where(A.any(0))[0]; tipx = xs[-1]
    rij = np.where(A[:, tipx - 2])[0]; tipy = rij.mean()
    kolom = np.where(A[:, 120])[0]                                      # schacht, achter de knop, voor de eerste rank
    dik = kolom[-1] - kolom[0] + 1
    # schaal: even lang als javImg (624); de gewone speer is daar 19 dik, deze mag iets dikker
    s = 624 / im.width
    im = im.resize((624, max(1, round(im.height * s))), Image.LANCZOS)
    # kleuren per zone, dan dikker, met een marge voor de rand, en de rand erom
    im = speer_kleur(im)
    im = im.resize((624, round(im.height * DIKKER)), Image.LANCZOS)
    m = Image.new('RGBA', (624, im.height + 4)); m.alpha_composite(im, (0, 2)); im = speer_rand(m)
    A = np.array(im)[..., 3] > 100; tipx = np.where(A.any(0))[0][-1]; tipy = np.where(A[:, tipx - 2])[0].mean(); s = 1
    d = os.path.join(ROOT, 'design', 'speer', 'ardhi'); os.makedirs(d, exist_ok=True)
    im.save(os.path.join(d, 'jav.png'), optimize=True)
    return im, (623, round(tipy, 1)), dik * DIKKER


def hand(jav, tip):
    """De speer in de hoeken van de gewone speer in Amirs hand, zoals pathfinder() in tools/mkuki_spel_los.py."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import mkuki_spel_los as L
    PF = jav
    uit = {}
    for hid, f in [('proj', 1.0)] + [('k%02d' % round(k * 100), k) for k in L.KS] + [('l%03d' % round(f * 100), f) for f in L.LS]:
        if f > 1:   # langer: de schacht tussen de knop en de grip en tussen de grip en de kop rekt, de uiteinden niet
            extra = round(PF.width * (f - 1)); e1 = extra // 2; e2 = extra - e1
            n = Image.new('RGBA', (PF.width + extra, PF.height))
            # de knop (0-40), schacht (40-245), het leren bandje (245-312), schacht (312-350), de kop (350-)
            n.paste(PF.crop((0, 0, 40, PF.height)), (0, 0))
            n.paste(PF.crop((40, 0, 245, PF.height)).resize((205 + e1, PF.height), Image.LANCZOS), (40, 0))
            n.paste(PF.crop((245, 0, 312, PF.height)), (245 + e1, 0))
            n.paste(PF.crop((312, 0, 350, PF.height)).resize((38 + e2, PF.height), Image.LANCZOS), (312 + e1, 0))
            n.paste(PF.crop((350, 0, PF.width, PF.height)), (350 + extra, 0))
            im = n
        elif f < 1: im = PF.resize((round(PF.width * f), PF.height), Image.LANCZOS)
        else: im = PF
        im.save(os.path.join(L.B.BRON, 'ar_%s.png' % hid), optimize=True)
        uit[hid] = {'asp': round(PF.height / im.width, 4), 'ty': round(tip[1] / PF.height, 4)}
    p = os.path.join(ROOT, 'karakters', 'amir', 'mkuki_spel', 'los.json')
    D = json.load(open(p)); D['ar'] = uit
    json.dump(D, open(p, 'w'), separators=(',', ':'))
    return uit


def effecten():
    a = np.array(Image.open(os.path.join(BRON, 'heel_grok.jpg')).convert('RGB')).astype(float)
    d = os.path.join(ROOT, 'design', 'ardhi')
    # de ring links, de druppel rechts (in pixels van de screenshot)
    for naam, (x0, x1) in {'ring': (20, 430), 'druppel': (1190, 1490)}.items():
        rgb, al = (licht_alfa if naam == 'druppel' else zwart_alfa)(a[:, x0:x1])
        im = bijsnijden(rgb, al)
        im.save(os.path.join(d, naam + '.png'), optimize=True)
        print(naam, im.size)


def druppel_los():
    """De kale druppel (design/ardhi/druppel_los.png): alleen het goud van de druppel, zonder de blaadjes en zonder het
    plasje eronder (geknipt op de smalste rij onder de buik). Die valt in het spel in Amirs hoofd."""
    a = np.array(Image.open(os.path.join(ROOT, 'design', 'ardhi', 'druppel.png')).convert('RGBA')).astype(float)
    r, g, al = a[..., 0], a[..., 1], a[..., 3]
    goud = (r >= 0.85 * g) & (al > 110)
    lab, n = ndimage.label(goud)
    k = np.argmax(ndimage.sum(goud, lab, range(1, n + 1))) + 1
    m = ndimage.binary_dilation(ndimage.binary_fill_holes(lab == k), iterations=3)
    a[..., 3] = al * np.clip(ndimage.gaussian_filter(m.astype(float), 2.0) * 1.3, 0, 1)
    ys, xs = np.where(a[..., 3] > 10)
    a = a[ys.min() - 3:ys.max() + 4, xs.min() - 3:xs.max() + 4]
    w = (a[..., 3] > 120).sum(1); buik = int(np.argmax(w)); nek = buik + int(np.argmin(w[buik:buik + 120]))
    a = a[:nek + 4]; a[-10:, :, 3] *= np.linspace(1, 0, 10)[:, None]
    Image.fromarray(a.astype(np.uint8)).save(os.path.join(ROOT, 'design', 'ardhi', 'druppel_los.png'), optimize=True)


def icoon(im, naam, hoek=35):
    im = im.rotate(hoek, expand=True, resample=Image.BICUBIC)
    bb = im.getbbox(); im = im.crop(bb)
    s = 150 / max(im.size); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new('RGBA', (160, 160)); c.alpha_composite(im, ((160 - im.width) // 2, (160 - im.height) // 2))
    c.save(os.path.join(ROOT, 'items', 'winkel', naam + '.png'), optimize=True)


def main():
    import sys
    if '--speer' in sys.argv:      # alleen de speer (na een andere KLEUR): jav.png, de hand en het winkelplaatje
        jav, tip, dik = speer(); icoon(jav, 'ardhireach', 35); hand(jav, tip)
        print("ARDHI.speer = { w: %d, h: %d, tipX: %d, tipY: %s }" % (jav.width, jav.height, tip[0], tip[1])); return
    st = stokplaat()
    icoon(st, 'ardhi', 40)
    jav, tip, dik = speer()
    icoon(jav, 'ardhireach', 35)
    print("jav", jav.size, "tip", tip, "schachtdikte", round(dik, 1))
    print("ARDHI.speer = { w: %d, h: %d, tipX: %d, tipY: %s }" % (jav.width, jav.height, tip[0], tip[1]))
    hand(jav, tip)
    effecten()
    druppel_los()
    ring = Image.open(os.path.join(ROOT, 'design', 'ardhi', 'ring.png'))
    icoon(ring, 'ardhiroots', 0)


if __name__ == '__main__':
    main()
