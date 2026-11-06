#!/usr/bin/env python3
"""De schade in de pleinvloer van Nyundo (Brutus), uit de Grok-platen in design/stad/bron/.

Twee bronnen:
  plein_schade_grok.jpg    vier platen gebarsten plaveisel (licht, zwaar, breed, op een plek), op wit
  plein_brokken_grok.png   een rij losse brokken plaveisel, op wit

Wat eruit komt, in design/stad/:
  plein_schade_1.png .. _4.png   alleen het beschadigde stuk van elke plaat, omgerekend naar de maat van
                                 plein.png (rij 0 van het plaatje valt op rij PLEIN_TOP van de vloertegel),
                                 in de kleur van het plein, met een grillige zachte rand die overloopt in de
                                 echte vloer. Het puin op de aarde onder de tegelrand vervaagt naar onder.
  plein_brokken.png              de losse brokken naast elkaar op een strook; het script print de rechthoeken
                                 voor BRU.schade.brokken.

    python3 tools/plein_schade.py
    python3 tools/plein_schade.py --proef map    ook een proefbeeld van elke plaat op plein.png

Daarna: python3 tools/gen-offline-manifest.py

Vereist Pillow, numpy en scipy.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design', 'stad')
BRON = os.path.join(MAP, 'bron')

# plein.png: de bovenkant van de tegels begint op rij 48, de onderrand van de voorste tegels ligt rond 128
PLEIN_TOP, PLEIN_RAND = 48, 128
# in een Grok-plaat ligt de onderrand van de voorste tegels zoveel rijen onder de bovenkant
GROK_RAND = 160
BROK_KLEUR = np.array([0.93, 0.86, 0.78])   # de brokken: iets warmer en donkerder dan de Grok-plaat
SX = 0.95          # horizontaal: de tegels van Grok een fractie kleiner, de verticale maat volgt uit de randen
# per plaat het midden van de schade en de halve breedte, in pixels van de plaat (840 breed)
PLATEN = [
    {'box': (27, 150, 869, 425), 'mid': 375, 'half': 150},   # licht: een plek
    {'box': (921, 150, 1761, 425), 'mid': 390, 'half': 300}, # zwaar
    {'box': (27, 554, 869, 835), 'mid': 370, 'half': 320},   # breed
    {'box': (921, 554, 1761, 835), 'mid': 420, 'half': 210}, # op een plek
]


def kleur_naar_plein(a, ref):
    """Schuif de kleur per kanaal zo dat het gave plaveisel van Grok de gemiddelde kleur van het plein krijgt."""
    return np.clip(a * ref, 0, 255)


def plein_ref(grok_gaaf):
    p = np.asarray(Image.open(os.path.join(MAP, 'plein.png')).convert('RGB')).astype(np.float32)
    plein = p[PLEIN_TOP + 4:PLEIN_RAND - 20].reshape(-1, 3).mean(axis=0)
    return plein / grok_gaaf


def schade():
    im = np.asarray(Image.open(os.path.join(BRON, 'plein_schade_grok.jpg')).convert('RGB')).astype(np.float32)
    # de kleur van het gave plaveisel bij Grok: de uiterste stroken van de eerste plaat
    x0, y0, x1, y1 = PLATEN[0]['box']
    gaaf = np.concatenate([im[y0 + 10:y0 + 120, x0 + 10:x0 + 150], im[y0 + 10:y0 + 120, x1 - 150:x1 - 10]], axis=1)
    ref = plein_ref(gaaf.reshape(-1, 3).mean(axis=0))
    sy = (PLEIN_RAND - PLEIN_TOP) / GROK_RAND
    rng = np.random.default_rng(7)
    uit = []
    for n, P in enumerate(PLATEN, 1):
        x0, y0, x1, y1 = P['box']
        plaat = im[y0:y1, x0:x1]
        # de bovenste rijen zijn de overgang naar wit: weg
        top = 0
        while plaat[top].min(axis=1).mean() > 200: top += 1
        top += 3
        plaat = kleur_naar_plein(plaat[top:], ref)
        h, w = plaat.shape[:2]
        # alfa: horizontaal een grillige zachte rand rond de schade, verticaal vervaagt de aarde onder de tegelrand
        ys = np.arange(h)[:, None]; xs = np.arange(w)[None, :]
        ruis = np.zeros(h)
        for f, amp in ((0.021, 26), (0.057, 12), (0.13, 5)):
            ruis += amp * np.sin(ys[:, 0] * f + rng.uniform(0, 6.28))
        d = np.abs(xs - P['mid']) - ruis[:, None]
        hor = np.clip((P['half'] * 1.12 - d) / (P['half'] * 0.4), 0, 1)
        ver = np.clip((GROK_RAND + 60 - ys) / 45.0, 0, 1)
        alfa = (hor * ver)
        alfa = alfa * alfa * (3 - 2 * alfa)
        # bijsnijden tot waar er iets staat
        kol = np.where(alfa.max(axis=0) > 0.01)[0]; rij = np.where(alfa.max(axis=1) > 0.01)[0]
        c0, c1, r1 = kol[0], kol[-1] + 1, rij[-1] + 1
        rgba = np.dstack([plaat, alfa[..., None] * 255])[:r1, c0:c1]
        beeld = Image.fromarray(rgba.astype(np.uint8), 'RGBA')
        nw, nh = round(beeld.width * SX), round(beeld.height * sy)
        beeld = beeld.resize((nw, nh), Image.LANCZOS)
        pad = os.path.join(MAP, 'plein_schade_%d.png' % n)
        beeld.save(pad, optimize=True)
        # het midden van de schade in het plaatje (waar de inslag valt)
        mid = round((P['mid'] - c0) * SX)
        print('%s  %dx%d  midden %d' % (os.path.relpath(pad, ROOT), nw, nh, mid))
        uit.append((beeld, mid))
    return uit


def brokken():
    bron = np.asarray(Image.open(os.path.join(BRON, 'plein_brokken_grok.png')).convert('RGBA')).astype(np.float32)
    im = bron[..., :3]
    if (bron[..., 3] < 10).mean() > 0.2:
        # de plaat is al uitgeknipt (doorzichtig in plaats van wit)
        alfa = bron[..., 3] / 255.0
        rgb = im
    else:
        mn = im.min(axis=2)
        lab, _ = nd.label(mn > 225)
        rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        weg = np.isin(lab, list(rand))
        zacht = np.clip((mn - 150) / 90.0, 0, 1)
        alfa = np.where(weg, 0.0, 1.0)
        rr = nd.binary_dilation(weg, iterations=2) & ~weg
        alfa[rr] = 1.0 - zacht[rr]
        a = alfa[..., None]
        los = np.clip((im - 255.0 * (1 - a)) / np.maximum(a, 0.05), 0, 255)
        rgb = np.where(((alfa > 0) & (alfa < 1))[..., None], los, im)
    # dezelfde kleur als de platen (het gave plaveisel van het plein), en iets donkerder: los op de vloer lezen ze
    # anders als witte stipjes
    rgb = np.clip(rgb * BROK_KLEUR, 0, 255)
    voor = alfa > 0.05
    lab, n = nd.label(voor)
    stukken = []
    for sl in nd.find_objects(lab):
        if (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start) < 300: continue
        stukken.append(sl)
    stukken.sort(key=lambda sl: sl[1].start)
    schaal = 0.6
    delen, rects, x = [], [], 0
    for sl in stukken:
        y0, y1 = max(0, sl[0].start - 2), sl[0].stop + 2
        x0, x1 = max(0, sl[1].start - 2), sl[1].stop + 2
        st = Image.fromarray(np.dstack([rgb[y0:y1, x0:x1], alfa[y0:y1, x0:x1, None] * 255]).astype(np.uint8), 'RGBA')
        st = st.resize((max(1, round(st.width * schaal)), max(1, round(st.height * schaal))), Image.LANCZOS)
        delen.append((st, x)); rects.append([x, 0, st.width, st.height]); x += st.width + 4
    hoog = max(st.height for st, _ in delen)
    vel = Image.new('RGBA', (x, hoog), (0, 0, 0, 0))
    for st, px in delen: vel.paste(st, (px, 0))
    pad = os.path.join(MAP, 'plein_brokken.png')
    vel.save(pad, optimize=True)
    print('%s  %dx%d, %d brokken' % (os.path.relpath(pad, ROOT), vel.width, vel.height, len(rects)))
    print('brokken: ' + str(rects).replace(' ', ''))


def proef(map_, platen):
    os.makedirs(map_, exist_ok=True)
    vloer = Image.open(os.path.join(MAP, 'plein.png')).convert('RGBA')
    for n, (beeld, mid) in enumerate(platen, 1):
        p = vloer.copy()
        p.alpha_composite(beeld, (p.width // 2 - mid, PLEIN_TOP))
        p.save(os.path.join(map_, 'proef_%d.png' % n))


if __name__ == '__main__':
    platen = schade()
    brokken()
    if '--proef' in sys.argv:
        proef(sys.argv[sys.argv.index('--proef') + 1], platen)
