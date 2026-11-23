#!/usr/bin/env python3
"""Een andere stok in alle stokframes van Amir: de gebakken frames van de gewone stok, met de stok eruit en de nieuwe erin.

De gewone stokframes (karakters/amir/stokken/<set>/) hebben de stok erin gebakken (tools/stok_bak.py, en de ren met de
hand samengesteld). Dit script haalt per frame elke stok eruit en zet er een andere stok voor in de plaats, met de grip
in dezelfde vuist en in dezelfde hoek. Zo heeft een stok uit de winkel dezelfde animaties zonder dat er iets opnieuw
geplaatst hoeft te worden. Krijgt de gewone stokset er frames bij of komt er een set bij, dan moet stokhoeken.json mee
(zie notities/stokken.md, "De klauwstokken").

Bron (in karakters/amir/stokken/bron/):
  stokhoeken.json       per set, per frame, per stok: [hoek, gespiegeld, maat, knoop-x, knoop-y, kont], de plek van de gewone
                        stok in de speelframes. Gevonden door de gewone stok (stok_bak.py) op elke hoek langs de knoop uit
                        STOK.slip.punt te leggen en te kijken waar hij het best op het frame past; de ren (anders
                        samengesteld, een iets andere stok) op vorm, met een vrije maat en knoop, en kont: zoveel px
                        is die stok aan het uiteinde langer, zodat de nieuwe het oude uiteinde bedekt. Opnieuw zoeken: --zoek
  stokken_vet_grok.jpg  de plaat uit Grok met vier stokken op magenta, de grip links en de slagkant rechts

Uit:
  karakters/amir/<uit>/<set>/<set>_NN.png  dezelfde sets en frames als stokken/, op hetzelfde canvas
  karakters/amir/<uit>/slip.png            de slippen in de kleur van de grip, of de kwast die op de plaat onder de grip
                                           hangt (die gaat niet mee in de stok maar slingert als slip aan de knoop)

Gebruik:  python3 tools/stok_variant.py --rij 1 --uit stokken_klauw --grip 125,30,35
          python3 tools/stok_variant.py --rij 0 --uit stokken_ardhi --plaat design/ardhi/bron/stok_grok.jpg --grip 70,120,40
          python3 tools/stok_variant.py --rij 3 --uit stokken_goud --slip 24,30,12
          --rij: welke stok van de plaat (0 is de bovenste); --grip: de kleur van de slippen
Daarna:   de map ook naar klein/karakters/amir/ kopieren (de frames zijn lager dan de drempel van gen-klein.py, die
          kopieert ze ongewijzigd) en python3 tools/gen-offline-manifest.py
"""
import argparse, json, os, re, shutil
import numpy as np
from PIL import Image, ImageFilter
import stok_bak as sb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMIR = os.path.join(ROOT, 'karakters', 'amir')
BRON = os.path.join(AMIR, 'stokken', 'bron')


def oude_stok(k=1.0):
    """De gewone stok zoals stok_bak.py hem bakt (lengte 155, dikte 1,15), zoveel keer groter."""
    vol = sb.stok_maken([170, 108, 40]); va = np.array(vol)
    sa = va.copy(); sa[sb.STOK_BOX[3]:, :, 3] = 0
    stok = Image.fromarray(sa).crop(sb.STOK_BOX)
    s = 155 * k / stok.width
    stok = stok.resize((round(stok.width * s), round(stok.height * s * 1.15)), Image.LANCZOS)
    ncx, ncy = (sb.STOK_BOX[0] + sb.STOK_BOX[2]) / 2, (sb.STOK_BOX[1] + sb.STOK_BOX[3]) / 2
    return stok, ((sb.KNOOP_X - ncx) * s, (sb.STOK_BOX[3] - ncy) * s * 1.15)


def plaats(im, kn, knot, deg, flip, W, H):
    """im met zijn knoop (kn, vanaf zijn midden) op knot, gedraaid zoals stok_bak.item; een laag van W x H."""
    v = sb.draai(kn, deg, flip); nc = (knot[0] - v[0], knot[1] - v[1])
    i2 = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
    r = i2.rotate(-deg, expand=True, resample=Image.BICUBIC)
    lay = Image.new('RGBA', (W, H)); lay.alpha_composite(r, (round(nc[0] - r.width / 2), round(nc[1] - r.height / 2)))
    return lay


def sleutel(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.minimum(r, b) - g) / np.maximum(np.maximum(r, b), 1)
    al = np.clip((0.75 - m) / 0.30, 0, 1)
    ex = np.clip(np.minimum(r, b) - g, 0, None) * (1 - al)
    return np.dstack([r - ex, g, b - ex, al * 255])


PLAAT = os.path.join(BRON, 'stokken_vet_grok.jpg')   # --plaat zet een andere plaat (een stok per rij, grip links)


def nieuwe_stok(rij, k=1.0, kont=0.0):
    """De stok van rij `rij` uit de Grok-plaat, op de maat van de gewone stok: de grip waar die van de gewone zit, het
    uiteinde (bij de grip) even ver (plus kont: de stok in de ren is daar langer), de schacht zo dik als de gewone, en de kop (alles na de schacht) op zijn eigen
    verhouding erachter, voorbij de punt van de gewone stok. Geeft het beeld en de knoop vanaf zijn midden, zoals oude_stok."""
    a = np.array(Image.open(PLAAT).convert('RGB')).astype(float)
    rgba = sleutel(a)
    fg = rgba[..., 3] > 128
    ys = np.where(fg.any(1))[0]
    banden, s0, p = [], ys[0], ys[0]
    for y in ys[1:]:
        if y > p + 3: banden.append((s0, p)); s0 = y
        p = y
    banden.append((s0, p))
    y0, y1 = banden[rij]
    band = fg[y0:y1 + 1]
    xs = np.where(band.any(0))[0]; xa, xb = xs[0], xs[-1]          # het uiteinde (links) en de verste punt van de kop
    dik = np.array([band[:, x].sum() for x in range(xa, xb + 1)])
    schacht = int(np.median(dik[len(dik) // 4: len(dik) * 3 // 4]))   # de dikte van de schacht
    # de kop begint waar de band na de schacht (voorbij 60 procent van de lengte) dikker wordt dan de schacht
    i = len(dik) * 3 // 5
    while i < len(dik) - 1 and dik[i] <= schacht * 1.12: i += 1
    kop = xa + i
    rijen = np.where(band[:, (xa + kop) // 2])[0]; yc = y0 + (rijen[0] + rijen[-1]) / 2   # het midden van de schacht
    # wat onder de schacht hangt (een kwast van manen aan de grip): niet in de stok, maar los als slip (kwast_maken)
    onder = int(yc + schacht / 2 + 4)
    grens = xa + (xb - xa) * 2 // 5                                     # alleen bij de grip (de kop hangt ook onder de schacht)
    kwast = rgba.copy(); kwast[:onder] = 0; kwast[:, grens:] = 0; kwast[y1 + 1:] = 0
    rgba = rgba.copy(); rgba[onder:y1 + 1, :grens, 3] = 0
    # de grip: het stuk van links dat niet de kleur van de schacht heeft (de schacht meten op driekwart)
    xs4 = xa + (kop - xa) * 3 // 4
    sk = rgba[int(yc), xs4, :3]
    kol = [np.abs(rgba[int(yc) - 2:int(yc) + 3, x, :3] - sk).sum(-1).mean() for x in range(xa, kop)]
    j = len(kol) * 2 // 3
    while j > 0 and kol[j] < 90: j -= 1
    gripc = (xa + 10 + xa + j) / 2                                      # het midden van de grip
    # doelmaten, in de pixels van de gewone stok (lengte 155): uiteinde rechts op 155, grip op 121,9, de schacht 12 dik
    # rond rij 6,5, de kop begint op 28 en loopt naar links door
    oud, okn = oude_stok(1.0)
    ow = oud.width; ocy = 6.5
    ogrip = ow / 2 + 44.4
    sch_dik = 12.0
    kopx = 28.0
    sy = sch_dik / schacht
    kop_s = 0.15 * 1536 / 1508 * (ow / 155)                             # de kop: op zijn eigen verhouding
    kopIm = Image.fromarray(rgba[y0:y1 + 1, kop:xb + 1].astype(np.uint8))
    kw, kh = round(kopIm.width * kop_s), round(kopIm.height * kop_s)
    kopIm = kopIm.resize((kw, kh), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    # het lijf van de stok in twee stukken geschaald: uiteinde tot grip, en grip tot kop
    def stuk(x0, x1, w):
        im = Image.fromarray(rgba[y0:y1 + 1, x0:x1].astype(np.uint8))
        return im.resize((max(1, round(w)), max(1, round(im.height * sy))), Image.LANCZOS)
    a1 = stuk(xa, int(gripc), ow - ogrip + kont).transpose(Image.FLIP_LEFT_RIGHT)
    a2 = stuk(int(gripc), kop, ogrip - kopx).transpose(Image.FLIP_LEFT_RIGHT)
    links = kw + 4                                                      # ruimte links van x 0 voor de kop
    hoog = max(kh, a1.height) + 8
    W = int(ow + links + 2 + kont); H = int(hoog * 2)
    cy = H / 2                                                          # rij ocy van de gewone stok ligt op cy
    can = Image.new('RGBA', (W, H))
    ys_ = lambda im: round(cy - (yc - y0) * sy)                         # de schacht op cy
    can.alpha_composite(a2, (round(links + kopx), ys_(a2)))
    can.alpha_composite(a1, (round(links + ogrip), ys_(a1)))
    kys = round(cy - (yc - y0) * kop_s)
    can.alpha_composite(kopIm, (round(links + kopx - kw + 2), kys))
    # een donkere omlijning eromheen, net als de gewone stok (anders verdwijnt een lichte stok tegen een lichte lucht)
    al = can.getchannel('A').point(lambda v: 255 if v > 90 else 0).filter(ImageFilter.MaxFilter(3))
    rand = Image.new('RGBA', can.size, (34, 22, 18, 0)); rand.putalpha(al)
    rand.alpha_composite(can); can = rand
    # de knoop: waar hij in de gewone stok zit, gerekend vanaf het midden van dit canvas
    okx = ow / 2 + okn[0]; oky = oud.height / 2 + okn[1]
    kn = (links + okx - W / 2, cy + (oky - ocy) - H / 2)
    if k != 1.0:
        can = can.resize((round(W * k), round(H * k)), Image.LANCZOS); kn = (kn[0] * k, kn[1] * k)
    return can, kn, (kwast if (kwast[..., 3] > 128).sum() > 300 else None)


def stokkleur(fr):
    """Pixels die bij de gewone stok kunnen horen: donker hout zonder de warmte van de huid, of de okeren grip."""
    r, g, b, a = [fr[..., i] for i in range(4)]
    donker = (r + g + b < 170) & (r - b < 24) & (r - b > -8)    # niet het donkerpaars van de broek
    oker = (r > 95) & (g > 55) & (g < 120) & (b < 60) & (r - b > 60)
    ring = (r > 150) & (g > 120) & (b > 80) & (np.abs(r - g) < 50)    # de lichte ringen bij de punt
    return (a > 60) & (donker | oker | ring)


def wissel(fr_im, stokken, nieuw):
    """Haal de gewone stokken uit een frame en zet de nieuwe ervoor in de plaats."""
    W, H = fr_im.size
    fr = np.array(fr_im).astype(int)
    S = stokkleur(fr)
    weg = np.zeros((H, W), bool); kern = np.zeros((H, W), bool)
    lagen = []
    for deg, flip, k, kx, ky, *rest in stokken:
        kont = rest[0] if rest else 0
        oud, okn = oude_stok(k)
        ol = np.array(plaats(oud, okn, (kx, ky), deg, flip, W, H)).astype(int); m = ol[..., 3]
        kern |= m > 200
        # in de kern van de oude stok ook wat er gewoon op lijkt (de lichtere nerven die niet donker genoeg zijn)
        weg |= (m > 200) & (fr[..., 3] > 60) & (np.abs(ol[..., :3] - fr[..., :3]).sum(-1) < 90)
        ruim = np.array(Image.fromarray(((m > 40) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
        weg |= ruim & S
        ni, nkn = nieuw(k, kont)[:2]
        lagen.append(plaats(ni, nkn, (kx, ky), deg, flip, W, H))
    lijf = fr.copy(); lijf[weg, 3] = 0
    uit = Image.new('RGBA', (W, H))
    for l in lagen: uit.alpha_composite(l)
    uit.alpha_composite(Image.fromarray(lijf.astype(np.uint8)))
    # wat weg moest maar niet onder de nieuwe stok valt: de rand van het lijf terug (niet de kern van de oude stok)
    ua = np.array(uit)
    gat = weg & (ua[..., 3] < 128) & ~kern
    ua[gat] = fr[gat]
    return Image.fromarray(ua.astype(np.uint8))


def kwast_maken(kwast, w=17, h=26, piv=7.9, x2=2):
    """De kwast die onder de grip hing als slip: hangpunt bovenaan op piv, op de maat van STOK.slip (w x h, 2x zo scherp)."""
    a = kwast[..., 3] > 60
    ys, xs = np.where(a)
    sub = Image.fromarray(kwast[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8))
    bovenrij = a[ys.min():ys.min() + 6, xs.min():xs.max() + 1].any(0)   # waar hij vastzit: het midden van de bovenkant
    hx = np.where(bovenrij)[0].mean()
    s = min(h * x2 / sub.height, w * x2 / sub.width)
    sub = sub.resize((max(1, round(sub.width * s)), max(1, round(sub.height * s))), Image.LANCZOS)
    can = Image.new('RGBA', (w * x2, h * x2))
    can.alpha_composite(sub, (max(0, min(w * x2 - sub.width, round(piv * x2 - hx * s))), 0))
    return can


def slip_maken(kleur):
    vol = np.array(sb.stok_maken(kleur))
    pa = vol.copy(); pa[:sb.SLIP_BOX[1], :, 3] = 0
    slip = Image.fromarray(pa).crop(sb.SLIP_BOX)
    ss = 155 / (sb.STOK_BOX[2] - sb.STOK_BOX[0]) * 0.75
    return slip.resize((round(slip.width * ss), round(slip.height * ss)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rij', type=int, default=1)
    ap.add_argument('--uit', default='stokken_klauw')
    ap.add_argument('--grip', default='125,30,35')
    ap.add_argument('--slip', default='24,30,12', help='w,h,piv van een kwast als slip (zet die ook in STOK.skins)')
    ap.add_argument('--plaat', default=None, help='een andere Grok-plaat dan bron/stokken_vet_grok.jpg (pad vanaf de repo)')
    o = ap.parse_args()
    global PLAAT
    if o.plaat: PLAAT = os.path.join(ROOT, o.plaat)
    H = json.load(open(os.path.join(BRON, 'stokhoeken.json')))
    cache = {}
    def nieuw(k, kont=0):
        if (k, kont) not in cache: cache[(k, kont)] = nieuwe_stok(o.rij, k, kont)
        return cache[(k, kont)]
    uit = os.path.join(AMIR, o.uit)
    for zet, frames in H.items():
        os.makedirs(os.path.join(uit, zet), exist_ok=True)
        for i, st in enumerate(frames):
            fr = Image.open(os.path.join(AMIR, 'stokken', zet, f'{zet}_{i:02d}.png')).convert('RGBA')
            wissel(fr, st, nieuw).save(os.path.join(uit, zet, f'{zet}_{i:02d}.png'), optimize=True)
        print(zet, len(frames))
    kw = nieuw(1.0)[2]
    sw, sh, sp = [float(v) for v in o.slip.split(',')]
    (kwast_maken(kw, int(sw), int(sh), sp) if kw is not None else slip_maken([int(v) for v in o.grip.split(',')])).save(os.path.join(uit, 'slip.png'))


if __name__ == '__main__':
    main()
