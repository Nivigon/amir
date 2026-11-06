#!/usr/bin/env python3
"""Maakt de houten ton voor de stad uit de Grok-platen in design/stad/ton/bron/.

Bron (allemaal met een doorzichtige achtergrond):
  ton_heel.png     de hele ton (1024 breed, dezelfde compositie als de andere twee, kleiner)
  ton_gat.png      na de eerste treffer: een gat in een duig
  ton_breuk.png    na de tweede: de bovenkant eruit; de losse hoepel ernaast valt weg
  ton_stukken.png  een plaat losse stukken: duigen, hoepels, de bodem, splinters

Uit:
  design/stad/ton/ton_0.png, ton_1.png, ton_2.png   de drie standen, op een maat en een voetlijn
  design/stad/ton/stuk_01.png ... stuk_NN.png        de losse stukken, op dezelfde schaal als de ton
  design/stad/ton/ton.json                           maten: breed, hoog, en per stuk w en h

Kleur: Grok gaf koel grijsbruin hout met veel contrast; op het zonnige plein stond hij daardoor
in de schaduw. Iets minder contrast, lichter en warmer, zodat hij bij het hout van de put past.

    python3 tools/ton_kleur.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
Vereist Pillow, numpy en scipy.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad', 'ton')
BRON = os.path.join(MAP, 'bron')

DOEL_H = 300        # hoogte van de hele ton in de uitvoer (px)
MARGE = 4
MIN_OPP = 900       # kleinere vlekjes op de stukkenplaat zijn ruis
GROEPEER = 6        # stukjes binnen deze afstand horen bij elkaar


def laad(naam):
    return Image.open(os.path.join(BRON, naam)).convert('RGBA')


def kleur(a):
    """Warmer, lichter en zachter; alleen de kleur, de alfa blijft."""
    rgb = a[..., :3].astype(np.float32) / 255
    l = rgb.mean(2, keepdims=True)
    rgb = l + (rgb - l) * 0.85
    rgb = 0.5 + (rgb - 0.5) * 0.8 + 0.10
    rgb = rgb * np.array([1.10, 1.00, 0.84], dtype=np.float32)
    uit = a.copy()
    uit[..., :3] = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return uit


def grootste(a):
    """Alleen het grootste stuk: wat los ligt (de hoepel naast de breuk, ruis langs de rand) valt weg."""
    m = a[..., 3] > 128
    lab, n = nd.label(m)
    opp = nd.sum(m, lab, range(1, n + 1))
    houd = lab == (int(np.argmax(opp)) + 1)
    houd = nd.binary_dilation(houd, iterations=2)
    uit = a.copy()
    uit[..., 3] = np.where(houd, uit[..., 3], 0)
    return uit


def main():
    # de drie standen in de maat van ton_gat (1408): ton_heel is dezelfde compositie op 1024
    gat = laad('ton_gat.png')
    W = gat.size[0]
    heel = laad('ton_heel.png').resize((W, W), Image.LANCZOS)
    breuk = laad('ton_breuk.png')
    standen = [grootste(np.asarray(s)) for s in (heel, gat, breuk)]   # ook een vage rand van de plaat valt weg

    # een gezamenlijk kader: de voetlijn en het midden van de hele ton tellen
    m = standen[0][..., 3] > 40
    ys, xs = np.where(m)
    y1 = ys.max() + 1
    alle = np.zeros_like(m)
    for s in standen:
        alle |= s[..., 3] > 40
    ys2, xs2 = np.where(alle)
    x0, x1, y0 = xs2.min() - MARGE, xs2.max() + 1 + MARGE, ys2.min() - MARGE
    y1 = max(y1, ys2.max() + 1)
    hoog = y1 - y0
    f = DOEL_H / (ys.max() + 1 - ys.min())        # schaal: de hele ton wordt DOEL_H hoog
    maat = {}
    for i, s in enumerate(standen):
        im = Image.fromarray(kleur(s[y0:y1, x0:x1]))
        im = im.resize((round((x1 - x0) * f), round(hoog * f)), Image.LANCZOS)
        im.save(os.path.join(MAP, 'ton_%d.png' % i))
        maat = {'w': im.size[0], 'h': im.size[1]}
    # het midden van de ton (van de hele, niet van de breuk) in de uitvoer
    maat['mid'] = round(((xs.min() + xs.max()) / 2 - x0) * f)
    maat['romp'] = round((xs.max() - xs.min()) * f)

    # de losse stukken: dezelfde schaal (de plaat is ook 1408 en de hoepels zijn zo breed als de ton)
    st = np.asarray(laad('ton_stukken.png'))
    m = st[..., 3] > 40
    lab, n = nd.label(nd.binary_dilation(m, iterations=GROEPEER))
    stukken = []
    for i, sl in enumerate(nd.find_objects(lab)):
        deel = (lab[sl] == i + 1) & m[sl]
        if deel.sum() < MIN_OPP:
            continue
        stukken.append((sl, deel))
    stukken.sort(key=lambda t: (t[0][0].start // 200, t[0][1].start))
    for oud in os.listdir(MAP):
        if oud.startswith('stuk_') and oud.endswith('.png'):
            os.remove(os.path.join(MAP, oud))
    lijst = []
    for k, (sl, deel) in enumerate(stukken, 1):
        a = st[sl].copy()
        a[..., 3] = np.where(deel, a[..., 3], 0)
        a = np.pad(a, ((MARGE, MARGE), (MARGE, MARGE), (0, 0)))
        im = Image.fromarray(kleur(a))
        im = im.resize((max(1, round(im.size[0] * f)), max(1, round(im.size[1] * f))), Image.LANCZOS)
        im.save(os.path.join(MAP, 'stuk_%02d.png' % k))
        lijst.append({'w': im.size[0], 'h': im.size[1]})
    maat['stukken'] = lijst
    with open(os.path.join(MAP, 'ton.json'), 'w') as fh:
        json.dump(maat, fh)
    print('ton: %dx%d, midden %d, romp %d; %d stukken' % (maat['w'], maat['h'], maat['mid'], maat['romp'], len(lijst)))
    for k, s in enumerate(lijst, 1):
        print('  stuk_%02d %dx%d' % (k, s['w'], s['h']))


if __name__ == '__main__':
    main()
