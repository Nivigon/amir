#!/usr/bin/env python3
"""Maakt de nieuwe huistypes voor de stad (D1, gevelvarianten) uit de Grok-platen in design/stad/bron/.

Bron (1296x1536, witte achtergrond):
  gevel_relief_grok.jpg    het reliefhuis: lichte kalk met rode en blauwe versiering (Hausa)
  gevel_koopman_grok.jpg   het koopmanshuis: rozerode leem met een houten erker
  gevel_pilaren_grok.jpg   het pilarenhuis: staande pilaren met punten erop (Djenne)
  gevel_vervallen_grok.jpg het vervallen huis: kale baksteen, dichtgemetselde ramen, een hangend luik
  gevel_toren_grok.jpg     het torenhuis: een ronde toren rechts, een halve verdieping boven het dak
  gevel_ruine_grok.jpg     de ruine met gaten: de bovenste verdieping ingestort, de lucht door de gaten
  gevel_ruine2_grok.jpg    de ruine met de V: het midden ingestort, een balk over het gat
  gevel_winkel_grok.jpg    het winkelhuis: een brede opening met een luik op een stok, een leembank (geen deur)
  gevel_winkel_dicht_grok.jpg  hetzelfde met het luik dicht

Uit: design/stad/gevel_<soort>.png, op de maat van gevel.png, zodat alles wat aan een gevel hangt
(het dak, de verdiepingen, de deur, de kartels, de galerijen) gewoon doorwerkt:
  - 970 breed, de muur van x 44 tot 922, het midden van het deurgat op x 473;
  - van boven naar onder vier banden: het dak (zo hoog als de plaat het geeft), dan de bovenste
    verdieping (alt, 417), de gewone verdieping (ver, 417) en de begane grond (bod, 508);
  - de looplijn van het dak (dakAchter) ligt 52 bronpx boven de onderkant van het dak, net als bij gevel.png.
De plaat is breder dan de oude gevel: een strook kale muur gaat eruit (een smalle links van de deur,
zodat het deurgat op zijn plek valt, en een brede rechts), met een zachte overgang over de naad.

Het script print de maten voor STAD.gevelSoort en zet ze in design/stad/metadata.json.

    python3 tools/gevel_soorten.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
Vereist Pillow, numpy en scipy.
"""
import json, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAD = os.path.join(ROOT, 'design', 'stad')
BRON = os.path.join(STAD, 'bron')

W_UIT, MUUR, MIDDEN = 970, (44, 922), 473
VER_H, BOD_H, DAK_ONDER = 417, 508, 52   # de maten van gevel.png: ver 580-997, bod 997-1505, dak 177 - dakAchter 125
NAAD = 28                                 # zo breed loopt de overgang over een geknipte naad

# per soort, in bronpx van de Grok-plaat (nagemeten op een raster):
#   muur   de linker- en rechterrand van de muur (zonder de balkkoppen die uitsteken)
#   deur   het donkere deurgat: x0, x1 (het midden komt op MIDDEN)
#   dak    de onderkant van het dak: net onder de bovenste balkenrij (of de stompjes ervan)
#   alt    de bovenste verdieping, ver de gewone, bod de begane grond (elk tot net onder een balkenrij)
#   knipL  waar links de smalle strook uit gaat (in kale muur), knipR waar de brede rechts begint
SOORTEN = {
    'relief':  dict(muur=(50, 1247), deur=(398, 605), dak=235, alt=(235, 615), ver=(615, 1012), bod=(1012, 1512),
                    knipL=128, knipR=700, zand=(10, -1, -5)),
    'koopman': dict(muur=(53, 1247), deur=(413, 598), dak=190, alt=(190, 595), ver=(595, 1005), bod=(1005, 1503),
                    knipL=140, knipR=700, zand=(-4, 3, 1)),
    'pilaren': dict(muur=(45, 1255), deur=(400, 612), dak=210, alt=(210, 655), ver=(655, 1058), bod=(1058, 1534),
                    knipL=222, knipR=690, zand=(-9, 2, -2)),
    # de tweede ronde (gemaakt uit gevel_breed_start.png): de deur staat hier links van het midden, dus links komt er
    # kale muur bij in plaats van eraf (een negatieve knip plakt de strook knipL - n .. knipL er nog een keer achter)
    'vervallen': dict(muur=(46, 1251), deur=(306, 496), dak=205, alt=(205, 600), ver=(600, 1010), bod=(1010, 1515),
                      knipL=290, knipR=620, zand=(-4, 2, 1)),
    # het torenhuis: de verdiepingen zijn lager dan bij de rest, dus eerst de hele plaat 1,2 keer groter (schaal);
    # de maten hier zijn die van de Grok-plaat zelf. Rechts gaat de raamkolom eruit, de toren blijft.
    'toren':   dict(muur=(108, 1188), deur=(317, 456), dak=440, alt=(440, 762), ver=(762, 1092), bod=(1092, 1500),
                    knipL=280, knipR=492, schaal=1.2, zand=(3, 1, 2)),
    # de ruines: de ingestorte verdieping is het dak (dak tot net onder de middelste balkenrij), de verdieping met de
    # gaten de eerste (ver), en de verdiepingen daartussen (alt) komen uit het vervallen huis: beschadigd maar dicht,
    # zodat er nooit twee keer dezelfde gaten boven elkaar staan. gaten: elk wit vlak in de muur wordt doorzichtig.
    'ruine':   dict(muur=(41, 1256), deur=(342, 538), dak=600, ver=(600, 1010), bod=(1010, 1535),
                    knipL=300, knipR=560, zand=(-6, 1, 0), ruine=True),
    'ruine2':  dict(muur=(85, 1229), deur=(366, 548), dak=600, ver=(600, 1010), bod=(1010, 1519),
                    knipL=300, knipR=700, zand=(-6, 1, 0), ruine=True),
    # het winkelhuis zonder deur (de winkel staat op de plek van de deur): midden is het midden van de winkel, de
    # deur en de raamkolom erboven gaan er links uit, rechts komt kale muur bij. Open en dicht liggen precies over elkaar.
    'winkel':  dict(muur=(46, 1250), midden=878, dak=205, alt=(205, 600), ver=(600, 1010), bod=(1010, 1508),
                    knipL=140, knipR=1235, zand=(5, 2, 3)),
    'winkel_dicht': dict(muur=(46, 1250), midden=878, dak=205, alt=(205, 600), ver=(600, 1010), bod=(1010, 1508),
                         knipL=140, knipR=1235, zand=(5, 2, 3)),
}
#   zand   de tint ten opzichte van gevel.png, in Lab (licht, rood, geel): de huizen blijven zandkleurig, elk met een
#          eigen tint (relief licht zand, koopman warm rossig zand, pilaren donkere leem). De kleur in de straat komt van
#          doeken, was en vaandels, niet van de muren.
ZAND_T = (1.0, 0.9)    # hoe ver het pleisterwerk naar die tint gaat: licht, kleur
ZAND_DONKER = 22       # onder deze helderheid (L) blijft alles zoals het was: het deurgat, het hout, de schaduw


def lab(c):
    c = c / 255
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    x = c @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T
    x = x / np.array([0.9505, 1, 1.089])
    f = np.where(x > 0.008856, np.cbrt(x), 7.787 * x + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def rgb(L):
    fy = (L[..., 0] + 16) / 116
    f = np.stack([fy + L[..., 1] / 500, fy, fy - L[..., 2] / 200], -1)
    x = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * np.array([0.9505, 1, 1.089])
    c = x @ np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]).T
    c = np.where(c > 0.0031308, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055, 12.92 * c)
    return np.clip(c * 255, 0, 255)


def lab_stats(a):
    m = a[..., 3] > 200
    L = lab(a[..., :3][m])
    return L.mean(0), L.std(0)


def zand(a, tint):
    """Het pleisterwerk naar de zandkleur van gevel.png, met een eigen tint; het donker blijft."""
    ref = np.asarray(Image.open(os.path.join(STAD, 'gevel.png')).convert('RGBA')).astype(float)
    rm, rs = lab_stats(ref)
    mm, ss = lab_stats(a)
    doel = rm + np.array(tint, float)
    t = np.array([ZAND_T[0], ZAND_T[1], ZAND_T[1]])
    L = lab(a[..., :3])
    nieuw = (L - mm) / ss * (ss * (1 - t) + rs * t) + (mm * (1 - t) + doel * t)
    d = ZAND_DONKER if mm[0] >= 40 else ZAND_DONKER * 0.55    # het pilarenhuis is zelf donker: dan lager beschermen
    w = np.clip((L[..., :1] - d) / d, 0, 1)
    w = w * w * (3 - 2 * w)
    uit = a.copy()
    uit[..., :3] = rgb(L * (1 - w) + nieuw * w)
    return uit


def wit_weg(rgb, gaten=False):
    """Het witte vlak rond de gevel doorzichtig: flood-fill vanaf de rand op bijna zuiver wit.
    gaten: ook elk groot wit vlak binnen in de muur (de gaten van een ruine, waar je de lucht door ziet)."""
    a = rgb.astype(int)
    wit = (a.min(2) > 238) & ((a.max(2) - a.min(2)) < 18)
    lab, _ = nd.label(wit)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    if gaten:
        maat = np.bincount(lab.ravel())
        rand |= set(np.nonzero(maat > 300)[0]) - {0}
    weg = np.isin(lab, list(rand))
    weg = nd.binary_dilation(weg, iterations=1)          # de lichte jpg-rand mee
    alpha = np.where(weg, 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8)))
    return np.dstack([rgb, alpha])


def knip(a, x0, x1):
    """Haal kolommen x0..x1 weg, met een zachte overgang van NAAD breed over de naad."""
    h = NAAD // 2
    links, rechts = a[:, :x0 + h].astype(float), a[:, x1 - h:].astype(float)
    t = np.linspace(0, 1, NAAD)[None, :, None]
    mid = links[:, -NAAD:] * (1 - t) + rechts[:, :NAAD] * t
    return np.concatenate([links[:, :-NAAD], mid, rechts[:, NAAD:]], axis=1)


def band(a, y0, y1, h):
    stuk = Image.fromarray(a[y0:y1].round().clip(0, 255).astype(np.uint8), 'RGBA')
    return np.asarray(stuk.resize((stuk.width, h), Image.LANCZOS)).astype(float)


def maak(naam, S):
    S = dict(S)
    im = Image.open(os.path.join(BRON, f'gevel_{naam}_grok.jpg')).convert('RGB')
    k = S.pop('schaal', 1)
    if k != 1:                                            # de hele plaat groter, en alle maten mee
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        for n, v in list(S.items()):
            if n in ('zand', 'ruine'): continue
            S[n] = tuple(round(x * k) for x in v) if isinstance(v, tuple) else round(v * k)
    bron = np.asarray(im)
    a = zand(wit_weg(bron, S.get('ruine')).astype(float), S['zand'])
    m0, m1 = S['muur']
    mid = S['midden'] if 'midden' in S else (S['deur'][0] + S['deur'][1]) / 2
    remL = round((mid - m0) - (MIDDEN - MUUR[0]))       # zo komt het midden van de deur op MIDDEN (negatief: er komt muur bij)
    remR = round((m1 - m0 - remL) - (MUUR[1] - MUUR[0]))  # en de muur op zijn breedte
    a = knip(a, S['knipR'], S['knipR'] + remR)
    a = knip(a, S['knipL'], S['knipL'] + remL)
    # links bijsnijden of aanvullen zodat de muur op x 44 begint, dan op 970 breed
    dx = m0 - MUUR[0]
    a = a[:, dx:] if dx >= 0 else np.concatenate([np.zeros((a.shape[0], -dx, 4)), a], axis=1)
    if a.shape[1] < W_UIT: a = np.concatenate([a, np.zeros((a.shape[0], W_UIT - a.shape[1], 4))], axis=1)
    a = a[:, :W_UIT]
    # de banden op hun maat
    dak = a[:S['dak']]
    D = S['dak']
    if S.get('ruine'):
        # de ruine: dak, de verdieping met de gaten, de begane grond, en onderaan de dichte verdieping van het vervallen huis
        alt = np.asarray(Image.open(os.path.join(STAD, 'gevel_vervallen.png')).convert('RGBA')).astype(float)
        V = META_VERVALLEN['alt']
        delen = [dak, band(a, *S['ver'], VER_H), band(a, *S['bod'], BOD_H), alt[V[0]:V[1]]]
        maat = {'dak': [0, D], 'ver': [D, D + VER_H], 'bod': [D + VER_H, D + VER_H + BOD_H],
                'alt': [D + VER_H + BOD_H, D + 2 * VER_H + BOD_H], 'ruine': True}
    else:
        delen = [dak, band(a, *S['alt'], VER_H), band(a, *S['ver'], VER_H), band(a, *S['bod'], BOD_H)]
        maat = {'dak': [0, D], 'alt': [D, D + VER_H], 'ver': [D + VER_H, D + 2 * VER_H], 'bod': [D + 2 * VER_H, D + 2 * VER_H + BOD_H]}
    uit = np.concatenate(delen, axis=0).round().clip(0, 255).astype(np.uint8)
    Image.fromarray(uit, 'RGBA').save(os.path.join(STAD, f'gevel_{naam}.png'), optimize=True)
    deurW = (S['deur'][1] - S['deur'][0]) / 214 if 'deur' in S else 0   # het deurgat t.o.v. dat van gevel.png; 0: geen deur
    return {'src': f'gevel_{naam}.png', 'h': uit.shape[0], **maat, 'dakAchter': D - DAK_ONDER, 'deur': round(deurW, 3)}


META_VERVALLEN = None


def main():
    global META_VERVALLEN
    maten = {}
    for naam, S in SOORTEN.items():                     # in volgorde: het vervallen huis voor de ruines
        maten[naam] = maak(naam, S)
        if naam == 'vervallen': META_VERVALLEN = maten[naam]
    pad = os.path.join(STAD, 'metadata.json')
    meta = json.load(open(pad))
    meta['gevel_soorten'] = maten
    json.dump(meta, open(pad, 'w'), indent=1, ensure_ascii=False)
    for naam, m in maten.items():
        print(f"  {naam}: {{ src: '{m['src']}', dak: {m['dak']}, alt: {m['alt']}, ver: {m['ver']}, bod: {m['bod']}, "
              f"dakAchter: {m['dakAchter']}, deur: {m['deur']}{', ruine: true' if m.get('ruine') else ''} }},")


if __name__ == '__main__':
    main()
