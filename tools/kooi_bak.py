#!/usr/bin/env python3
"""Bakt de dierenkooien, de doeken en het kistje voor de stad uit de Grok-segmenten.

Bron (design/stad/kooi/bron/, doorzichtige achtergrond, uit de segmenten van Grok):
  kooi_kaal.png    de kale kooi recht van voren (bovenblad in perspectief, dat gebruiken we niet)
  doek_half.png    het halve doek over de linkerkant (post 35883786)
  doek_over.png    het slordig overgegooide doek (post b5a45bb1)
  kist_kooi.png    de kooi onder het overgegooide doek (voor het kistje)

Uit (design/stad/kooi/), op A = 400 px per Amir:
  voor_<maat>.png   de voorkant: hoekpalen, balken, voortralies en het bovenblad uit galerij.png;
                    het donker binnen is doorzichtig, de engine legt de dekking zelf
  achter_<maat>.png de achtertralies, een halve tralie verschoven en donkerder
  doek_half.png, doek_over.png   de doeken, warmer gemaakt
  kistje.png        het kistje: een kleine kooi helemaal onder het overgegooide doek
  dier_hyena.png, dier_slang.png  het beest binnen (een stilstaand frame)
  kooi.json         maten per kooi en waar de doeken liggen (als deel van de kooi)

    python3 tools/kooi_bak.py

Daarna: python3 tools/gen-offline-manifest.py
"""
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad', 'kooi')
BRON = os.path.join(MAP, 'bron')
A = 400                      # px per Amir in de gebakken platen
DEK = 0.12                   # het bovenblad, in Amir

# breed en hoog (met blad) in Amir, per maat
MATEN = {
    'hoog':  (1.56, 0.95),   # hyenakooi: alleen via een kistje te halen
    'laag':  (1.56, 0.76),   # hyenakooi die je in een sprong haalt, de hyena zit gebukt
    'slang': (1.44, 0.74),
}


def im(n):
    return Image.open(os.path.join(BRON, n)).convert('RGBA')


def warm_hout(img):
    """Grok gaf bijna zwart hout: donker warm bruin, zoals de gekozen kooi."""
    a = np.asarray(img).astype(float)
    l = a[..., :3].mean(2, keepdims=True)
    a[..., :3] = np.clip(l * np.array([1.55, 1.25, 1.0]) + np.array([14, 8, 2]), 0, 255)
    return Image.fromarray(a.astype('uint8'), 'RGBA')


def warm_doek(img):
    a = np.asarray(img).astype(float)
    a[..., :3] = np.clip(a[..., :3] * np.array([1.05, 1.0, 0.9]), 0, 255)
    return Image.fromarray(a.astype('uint8'), 'RGBA')


# de voorkant van de kale kooi: onder het bovenblad (dat tekent Grok te diep)
kaal = im('kooi_kaal.png')
VOOR = warm_hout(kaal.crop((0, 184, kaal.width, kaal.height)))
VW, VH = VOOR.size
# tralies: de eerste staat op 0,1183 van de breedte, om de 0,0448
T0, PER = 0.1183, 0.0448
LINKS = T0 - PER / 2                          # hoekpaal met beslag
RECHTS = 1 - (0.8876 + PER / 2)

galerij = Image.open(os.path.join(ROOT, 'design', 'stad', 'galerij.png')).convert('RGBA')


def blad(breed, hoog):
    """Het bovenblad uit de galerij, met de korte schuine eindjes, donkerder."""
    gs = A / 450
    dek = galerij.crop((0, 96, galerij.width, 160))
    L, M0, M1, R = 262, 1205, 1348, 1492
    W = int(breed / gs)
    strook = Image.new('RGBA', (W + 1, dek.height), (0, 0, 0, 0))
    strook.alpha_composite(dek.crop((0, 0, L, dek.height)), (0, 0))
    x = L
    while x < W - (galerij.width - R):
        strook.alpha_composite(dek.crop((M0, 0, M1, dek.height)), (x, 0))
        x += M1 - M0
    strook.alpha_composite(dek.crop((R, 0, galerij.width, dek.height)), (W - (galerij.width - R), 0))
    strook = strook.resize((breed, hoog), Image.LANCZOS)
    a = np.asarray(strook).astype(float)
    a[..., :3] *= np.array([0.62, 0.5, 0.4])
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGBA')


def kooi(breed_a, hoog_a):
    W = round(breed_a * A)
    d = round(DEK * A)
    hf = round(hoog_a * A) - d + 4             # de voorkant schuift 4 px onder het blad
    f = hf / VH
    v = VOOR.resize((round(VW * f), hf), Image.LANCZOS)
    vw = v.width
    l, r, p = round(LINKS * vw), round(RECHTS * vw), PER * vw
    n = max(1, round((W - l - r) / p))
    mid = v.crop((l, 0, l + round(p), hf)).resize((max(1, round((W - l - r) / n)), hf), Image.LANCZOS)
    voor = Image.new('RGBA', (W, hf), (0, 0, 0, 0))
    voor.alpha_composite(v.crop((0, 0, l, hf)), (0, 0))
    for i in range(n):
        voor.alpha_composite(mid, (l + i * mid.width, 0))
    voor.alpha_composite(v.crop((vw - r, 0, vw, hf)), (W - r, 0))
    # binnen doorzichtig: het donker tussen de tralies (niet de palen en balken)
    o = np.asarray(voor).copy()
    lum = o[..., :3].astype(float).mean(2)
    y0, y1 = round(0.07 * hf), round(0.89 * hf)
    bin_ = np.zeros(lum.shape, bool)
    bin_[y0:y1, l:W - r] = True
    o[..., 3][(lum < 40) & bin_] = 0
    voor = Image.fromarray(o, 'RGBA')
    # achtertralies: dezelfde rij, een halve tralie verschoven en donkerder
    ach = np.zeros_like(o)
    s = round(mid.width / 2)
    ach[y0:y1, l + s:W - r] = o[y0:y1, l:W - r - s]
    ach[y0:y1, l:W - r, 3][(lum[y0:y1, l:W - r] < 40)] = 0
    ach[..., :3] = (ach[..., :3].astype(float) * 0.45).astype('uint8')
    achter = Image.fromarray(ach, 'RGBA')
    hoog = d - 4 + hf
    vol = Image.new('RGBA', (W, hoog), (0, 0, 0, 0))
    vol.alpha_composite(voor, (0, d - 4))
    vol.alpha_composite(blad(W, d), (0, 0))
    ach2 = Image.new('RGBA', (W, hoog), (0, 0, 0, 0))
    ach2.alpha_composite(achter, (0, d - 4))
    binnen = [l / W, (d - 4 + y0) / hoog, (W - r) / W, (d - 4 + y1) / hoog]
    return vol, ach2, binnen


def main():
    info = {'A': A, 'dek': DEK, 'maten': {}, 'doeken': {}}
    for naam, (b, h) in MATEN.items():
        vol, ach, binnen = kooi(b, h)
        vol.save(os.path.join(MAP, 'voor_%s.png' % naam), optimize=True)
        ach.save(os.path.join(MAP, 'achter_%s.png' % naam), optimize=True)
        info['maten'][naam] = {'breed': b, 'hoog': h, 'binnen': [round(v, 4) for v in binnen]}
    # de doeken: plek en maat als deel van de kooi (x, y vanaf linksboven, w, h), gemeten op de platen
    doeken = {
        'half': ('doek_half.png', [-0.006, 0.003, 0.595, 1.066]),
        'over': ('doek_over.png', [-0.152, -0.201, 1.20, 1.335]),
    }
    for naam, (bron, plek) in doeken.items():
        d = warm_doek(im(bron))
        d = d.crop(d.getbbox())
        w = round(plek[2] * 1.56 * A)
        d = d.resize((w, round(d.height * w / d.width)), Image.LANCZOS)
        d.save(os.path.join(MAP, 'doek_%s.png' % naam), optimize=True)
        info['doeken'][naam] = plek
    # het kistje: de kooi onder het overgegooide doek, als een plaat
    kk = warm_hout(im('kist_kooi.png'))
    dk = warm_doek(im('doek_over.png'))
    kx, ky, kw, kh = 134, 94, 316, 179          # op de plaat (schaal 0,31): kooi en doek
    dx, dy = 86, 58
    s = kk.width / kw
    can = Image.new('RGBA', (round(500 * s), round(320 * s)), (0, 0, 0, 0))
    can.alpha_composite(kk, (round((kx - 60) * s), round((ky - 40) * s)))
    dk2 = dk.resize((round(379 * s), round(239 * s)), Image.LANCZOS)
    can.alpha_composite(dk2, (round((dx - 60) * s), round((dy - 40) * s)))
    can = can.crop(can.getbbox())
    w = round(0.7 * A)
    can = can.resize((w, round(can.height * w / can.width)), Image.LANCZOS)
    can.save(os.path.join(MAP, 'kistje.png'), optimize=True)
    # het bovenvlak van het kistje: de bovenrand van het doek in het midden
    a = np.asarray(can)[..., 3]
    kol = [int(np.argmax(a[:, c] > 128)) for c in range(round(w * 0.25), round(w * 0.75))]
    info['kistje'] = {'breed': 0.7, 'hoog': round(can.height / A, 4), 'top': round(float(np.median(kol)) / can.height, 4)}
    # het beest binnen: een stilstaand frame
    for naam, pad, h in (('hyena', 'enemies/hyena/dreigen/dreigen_04.png', 0.6), ('slang', 'enemies/slang1/idle_1.png', 0.62)):
        b = Image.open(os.path.join(ROOT, pad)).convert('RGBA')
        b = b.crop(b.getbbox())
        info.setdefault('dieren', {})[naam] = {'breed': round(b.width / b.height * h, 4), 'hoog': h}
        hp = round(h * A)
        b.resize((round(b.width * hp / b.height), hp), Image.LANCZOS).save(os.path.join(MAP, 'dier_%s.png' % naam), optimize=True)
    with open(os.path.join(MAP, 'kooi.json'), 'w') as f:
        json.dump(info, f, indent=1)
    print(json.dumps(info, indent=1))


if __name__ == '__main__':
    main()
