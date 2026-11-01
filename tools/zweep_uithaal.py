#!/usr/bin/env python3
"""Bouwt de uithaal van de zweepman (fase 2, de nieuwe versie) uit de frames van de sprong.

De sprong-clip loopt: aanloop, een uitval naar voren met de arm gestrekt (frames 14 tot 19), terugtrekken met
de zweep in een lus over zijn hoofd (20 tot 26) en de arm achter hem (27 tot 44). In het spel knalde de zweep
op dat laatste stuk, dus achter hem, en kwam hij maar een stukje voor hem uit. De uithaal draait dat om:

  aanloop        sprong 0 tot 9 (gebukt, de rol in zijn handen)
  opzwaai        sprong 20 tot 36: de lus over zijn hoofd naar achteren, de arm achter hem
  klaar          36, even vast
  slag           35 terug tot 17: over zijn hoofd naar voren, de uitval, de arm gestrekt naar Amir; daar knalt hij
  terug          18 tot 44: weer naar de eindhouding, waarna sprongterug aansluit zoals na de sprong

Vanaf de opzwaai is het lijf VOOR (196 idle-px) naar achteren geschoven, zodat zijn voeten bij de overgang
van frame 9 naar 20 op hun plek blijven (in de clip bracht de eerste uitval hem daar). Aan het eind schuift
het spel zijn anker evenveel op (verschuif), zodat sprongterug op dezelfde plek begint. Van schuifVan tot
schuifTot schuift het spel hem naar Amir toe (ZWM_NIEUW.uithaal), zoals in de sprong.

In frames 17, 18 en 19 zit de zweep als rol in de tekening (voor zijn hand een rol, achter hem een lus). Daar
neemt het touw het over, dus dit script poetst de zweep daar weg (POETS: per frame waar hij ligt) en schrijft
lagen/f2_uit_*.png. De hand in die frames staat er niet in de json; HAND is hij, gemeten op de plaatjes.

Schrijft de beweging 'uithaal' in enemies/zweepman/zweepman.json. Daarna:
    python3 tools/gen-klein.py
    python3 tools/gen-offline-manifest.py
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies', 'zweepman')
JSON = os.path.join(ROOT, 'zweepman.json')

VOOR = 196                                   # idle-px: zo ver schuift het lijf vanaf de opzwaai naar achteren
MS = {'aanloop': None, 'opzwaai': 45, 'klaar': 160, 'slag': 24, 'vast': 45, 'vastN': 6, 'terug': 45}

# de hand in de uitval (idle-px van het anker, zonder VOOR), en de richting van de zweep uit de vuist
HAND = {17: [-414, -206, -1, 0.05], 18: [-320, -180, -1, 0.05], 19: [-270, -164, -1, 0.05]}

# waar de zweep ligt, in pixels van het plaatje. 'bruin': binnen dit vlak gaat alles wat zweepkleurig is weg
# (en zijn donkere rand); 'band': een strook (punten, breedte) die helemaal weg gaat, voor waar de zweep over
# zijn arm of vest loopt. Wat binnen zijn lijf valt wordt bijgeschilderd, wat erbuiten valt wordt doorzichtig.
POETS = {
    'f2_spr_071.png': {
        'bruin': [[(0, 85), (66, 85), (62, 140), (112, 145), (112, 300), (0, 300)],
                  [(355, 0), (612, 0), (612, 125), (382, 125), (370, 100), (352, 45)]],
        'band': [([(255, 140), (300, 128), (340, 120), (385, 112)], 16)]},
    'f2_spr_081.png': {
        'bruin': [[(0, 95), (188, 95), (186, 140), (212, 150), (245, 165), (245, 225), (0, 225)],
                  [(330, 0), (610, 0), (610, 112), (372, 112), (330, 40)]],
        'band': [([(285, 120), (320, 108), (350, 103), (368, 102)], 16)]},
    'f2_spr_084.png': {
        'bruin': [[(0, 165), (196, 165), (194, 200), (232, 207), (242, 265), (0, 265)],
                  [(240, 0), (555, 0), (555, 120), (330, 128), (300, 132), (270, 62), (240, 62)]],
        'band': [([(282, 132), (315, 127), (345, 122)], 16)]},
}


def masker(size, polys=(), banden=()):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    for p in polys: d.polygon(p, fill=255)
    for pts, w in banden:
        d.line(pts, fill=255, width=w, joint='curve')
        for x, y in pts: d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=255)
    return np.array(m) > 0


def morf(m, k, soort):                       # openen/sluiten/uitzetten met een vierkant van k
    im = Image.fromarray((m * 255).astype(np.uint8))
    if soort in ('open', 'dicht'):
        a, b = (ImageFilter.MinFilter(k), ImageFilter.MaxFilter(k)) if soort == 'open' else (ImageFilter.MaxFilter(k), ImageFilter.MinFilter(k))
        im = im.filter(a).filter(b)
    else:
        im = im.filter(ImageFilter.MaxFilter(k))
    return np.array(im) > 127


def bijschilder(rgb, gat, bekend):          # het gat van buiten naar binnen dichtschilderen met het gemiddelde van de buren
    rgb = rgb.astype(np.float64); bekend = bekend.copy(); gat = gat & ~bekend
    while gat.any():
        som = np.zeros_like(rgb); n = np.zeros(gat.shape)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            k = np.roll(np.roll(bekend, dy, 0), dx, 1)
            som += np.roll(np.roll(rgb, dy, 0), dx, 1) * k[..., None]; n += k
        rand = gat & (n > 0)
        if not rand.any(): break
        rgb[rand] = som[rand] / n[rand][:, None]
        bekend |= rand; gat &= ~rand
    return rgb


def poets(src, dst, P):
    im = np.array(Image.open(src).convert('RGBA')).astype(np.int32)
    r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
    vlak = masker((im.shape[1], im.shape[0]), P['bruin'])
    band = masker((im.shape[1], im.shape[0]), (), P['band'])
    bruin = (a > 40) & (r >= 60) & (r <= 190) & (g >= 30) & (g <= 125) & (b <= 85) & (r > g + 15) & (g >= b) & (r - b > 45)
    lum = (r * 3 + g * 6 + b) / 10
    donker = (a > 40) & (lum < 95) & (r >= b) & morf(bruin, 7, 'uit')          # de donkere rand langs de zweep
    zweep = (vlak & (bruin | donker)) | (band & (a > 0))
    zweep = morf(zweep, 3, 'uit') & (vlak | band)
    lijf = (a > 40) & ~zweep
    lijf = morf(lijf, 5, 'open')
    binnen = morf(lijf, 25, 'dicht')
    uit = im.copy()
    gat = zweep & binnen
    uit[..., :3] = np.clip(bijschilder(im[..., :3], gat, lijf & ~zweep), 0, 255).astype(np.int32)
    uit[..., 3][gat] = 255
    weg = (vlak | band) & ~binnen
    uit[..., 3][weg] = 0
    Image.fromarray(uit.astype(np.uint8), 'RGBA').save(dst)


def main():
    d = json.load(open(JSON))
    B = d['bewegingen']; spr = B['sprong']['frames']
    nieuw = {}
    for bron in POETS:
        doel = bron.replace('f2_spr_', 'f2_uit_')
        poets(os.path.join(ROOT, 'lagen', bron), os.path.join(ROOT, 'lagen', doel), POETS[bron])
        nieuw[bron] = doel

    def F(i, ms, schuif=True):
        f = json.loads(json.dumps(spr[i]))
        o = VOOR if schuif else 0
        f['lijf']['dx'] += o; f['cx'] = round(f['cx'] + o, 1)
        if f.get('stomp'): f['stomp'] = [f['stomp'][0] + o, f['stomp'][1]]
        h = f.get('hand') or HAND.get(i)
        if h: f['hand'] = [round(h[0] + o, 1), h[1], h[2], h[3]]
        src = os.path.basename(f['lijf']['src'])
        if src in nieuw: f['lijf']['src'] = 'lagen/' + nieuw[src]
        f['ms'] = ms
        return f

    fr = [F(i, spr[i]['ms'], False) for i in range(0, 10)]           # aanloop
    o0 = len(fr)
    fr += [F(i, MS['opzwaai']) for i in range(20, 37)]                 # opzwaai
    o1 = len(fr) - 1                                                   # arm achter (36)
    fr += [F(36, MS['klaar'])]
    fr += [F(i, MS['slag']) for i in range(35, 16, -1)]                # de slag, terug tot de uitval (17)
    s0 = o1 + 1 + 1 + (35 - 19)                                        # index van frame 19 in de slag: daar begint het touw
    knal = len(fr) - 1                                                 # frame 17: de arm gestrekt
    fr += [F(17, MS['vast']) for _ in range(MS['vastN'])]
    fr += [F(i, MS['terug']) for i in range(18, 45)]                   # terug naar de eindhouding
    t0 = len(fr) - (45 - 18)                                           # 18 in de terugweg
    r0 = t0 + (27 - 18)                                                # 27 in de terugweg: daar komt het touw weer
    a27 = o0 + (27 - 20)
    s27 = o1 + 2 + (35 - 27)                                           # 27 in de slag: het laatste slagframe met een hand
    touw = [
        {'van': a27, 'tot': s27, 'hang': 1, 'blijf': 1},                  # opzwaai en het begin van de slag: hij volgt de hand
        {'van': s0, 'knal': knal, 'tot': t0 + 1, 'boogVan': -100, 'boog': 85, 'kracht': 8, 'blijf': 1},
        {'van': r0, 'tot': len(fr) - 1, 'hang': 1, 'blijf': 1},          # terug: de zweep hangt uit de hand
    ]
    kw = t0 + (30 - 18)                                                # vanaf frame 30 van de terugweg is hij te raken
    B['uithaal'] = {'touw': touw, 'verschuif': VOOR, 'kwetsbaarVan': kw, 'schuifVan': o0, 'schuifTot': knal, 'frames': fr}
    with open(JSON, 'w') as f: json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    print('uithaal:', len(fr), 'frames, touw', touw, 'kwetsbaar vanaf', kw)


if __name__ == '__main__':
    main()
