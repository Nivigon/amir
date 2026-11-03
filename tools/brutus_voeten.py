#!/usr/bin/env python3
"""De voeten van Brutus (Nyundo) in de zwaai, de kap en de terugslag op de grond zetten.

    python3 tools/brutus_voeten.py                  de zwaai
    python3 tools/brutus_voeten.py kap terug        de kap en de terugslag (of elke beweging uit BEWEGING)

In de Grok-clip van de zwaai zweeft hij zo'n 30 tot 60 grote-set-pixels boven de grondlijn, en staat
de ene voet hoger dan de andere (eerst de voorste, aan het eind de achterste). In een zijaanzicht moeten
allebei zijn voeten op de grondlijn staan. Per zwaaiframe:

1. meet de onderkant van elke voet: de laagste huid- of sandaalpixel links en rechts van het anker
   (verzadigd en warm, dus niet de grijze knotsbal);
2. schuif het hele frame omlaag tot de laagste voet op DOEL staat (net als de achterste voet in de idle);
3. buig het been van de hogere voet omlaag tot die ook op DOEL staat: een zachte verschuiving die
   onder de heup begint (0) en bij de voet vol is, en die van het kruis naar buiten oploopt, zodat
   het lijf, de heup en het andere been blijven waar ze zijn.

In de kap (tophit1) stond hij net zo: de achterste voet 15 px boven de lijn, de voorste tot 42 px. In de
terugslag schuift zijn lijf een pas op (verplaatsing), dus daar meet het script rond het meeschuivende
midden; een voet die verder dan BUIG_MAX boven de lijn staat is een pas (het been is opgetild) en wordt
niet omlaag gebogen.

De originelen gaan eerst naar enemies/brutus/bron/ (eenmalig, ook hun regels uit brutus.json); het script werkt altijd vanaf die
originelen, dus je kunt het opnieuw draaien. Daarna: python3 tools/gen-klein.py en
python3 tools/gen-offline-manifest.py.
"""
import json, os, shutil, sys
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

ROOT = os.path.join(os.path.dirname(__file__), '..', 'enemies', 'brutus')
BRON = os.path.join(ROOT, 'bron')
DOEL = -3            # waar de voeten moeten staan (anker-coordinaten, 0 is de grondlijn, negatief is erboven)
HEUP = -175          # vanaf deze hoogte begint de buiging (anker-coordinaten)
KRUIS = (8, 70)      # de buiging loopt op van zoveel px naast het anker tot zoveel px (naar buiten)
SPRONG = 6           # een voet die meer dan zoveel px uit de pas loopt met zijn buren: de knots, niet de voet
VENSTER = 175        # alleen zo ver naast het midden zoeken (niet de steel van de knots voor hem)
BUIG_MAX = 30        # een voet die hoger staat dan dit boven de lijn is opgetild (een pas): niet buigen

# per beweging: het venster rond het midden (None: overal) en hoe het midden meeschuift (frame -> px)
def terugMidden(m):
    T = m['bewegingen']['terug']; v = T['verplaatsing']
    return lambda i: v * min(1.0, max(0.0, (i - 5) / 20))      # zoals bruLijfDX: zwiep van frame 5 tot 25
BEWEGING = {
    'zwaai': { 'venster': None, 'buigMax': None, 'midden': None },
    'kap':   { 'venster': VENSTER, 'buigMax': BUIG_MAX, 'midden': None },
    'terug': { 'venster': VENSTER, 'buigMax': BUIG_MAX, 'midden': terugMidden },
}

def zacht(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

def voeten(a, dx, dy, venster=None):
    R, G, B, A = [a[..., i].astype(int) for i in range(4)]
    mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
    sat = (mx - mn) / np.maximum(mx, 1)
    ok = (A > 120) & (sat > 0.3) & (R > G) & (G >= B) & (R - B > 40)
    xs = np.arange(A.shape[1]) + dx
    if venster: ok &= (np.abs(xs) <= venster)[None, :]
    uit = []
    for kant in (xs < 0, xs >= 0):
        rijen = np.where(ok[:, kant].any(1))[0]
        uit.append(int(rijen.max() + dy) if len(rijen) else None)
    return uit

def buig(a, dx, dy, d, kant, voet):
    """buig het been aan kant (-1 voor, 1 achter) d px omlaag; voet: de onderkant van die voet (anker-y)"""
    h, w = a.shape[:2]
    H2 = h + int(np.ceil(d)) + 2
    yy, xx = np.mgrid[0:H2, 0:w].astype(float)
    ax = xx + dx; ay = yy + dy                                   # anker-coordinaten van de uitvoer
    s = zacht((ay - HEUP) / max(1.0, (voet + d) - HEUP))        # 0 bij de heup, 1 bij de (nieuwe) voet
    u = zacht((ax * kant - KRUIS[0]) / (KRUIS[1] - KRUIS[0]))   # 0 bij het kruis, 1 naar buiten
    bron_y = yy - d * s * u
    pm = a.astype(float); pm[..., :3] *= pm[..., 3:4] / 255.0  # voorvermenigvuldigd: geen randjes
    uit = np.zeros((H2, w, 4))
    for c in range(4):
        uit[..., c] = map_coordinates(pm[..., c], [bron_y, xx], order=1, mode='constant', cval=0)
    al = np.maximum(uit[..., 3:4], 1e-6)
    uit[..., :3] = np.where(uit[..., 3:4] > 0, uit[..., :3] * 255.0 / al, 0)
    return np.clip(uit, 0, 255).astype(np.uint8)

def zet(m, orig, naam):
    cfg = BEWEGING[naam]
    midden = cfg['midden'](orig) if cfg['midden'] else (lambda i: 0)
    fr_o = orig['bewegingen'][naam]['frames']
    metingen = []
    for i, f in enumerate(fr_o):
        src = os.path.join(ROOT, f['src']); b = os.path.join(BRON, os.path.basename(f['src']))
        if not os.path.exists(b): shutil.copy(src, b)
        metingen.append(voeten(np.array(Image.open(b).convert('RGBA')), f['dx'] - midden(i), f['dy'], cfg['venster']))
    # een uitschieter (de knotsbal vlak bij de grond) vervangen door het gemiddelde van zijn buren
    for k in (0, 1):
        for i in range(1, len(metingen) - 1):
            a, b, c = metingen[i - 1][k], metingen[i][k], metingen[i + 1][k]
            if None in (a, b, c): continue
            if abs(b - a) > SPRONG and abs(b - c) > SPRONG: metingen[i][k] = round((a + c) / 2)
    nieuw = []
    for i, f in enumerate(fr_o):
        a = np.array(Image.open(os.path.join(BRON, os.path.basename(f['src']))).convert('RGBA'))
        voor, achter = metingen[i]
        if voor is None: voor = achter - 999                     # geen voet aan die kant: die is opgetild
        if achter is None: achter = voor - 999
        laag = max(voor, achter)
        schuif = DOEL - laag                                     # het hele frame omlaag (of omhoog)
        dy = f['dy'] + schuif
        hoog_kant = -1 if voor < achter else 1
        hoog = min(voor, achter) + schuif
        d = DOEL - hoog
        mag = cfg['buigMax'] is None or d <= cfg['buigMax']      # anders zet hij een pas: het been blijft opgetild
        if d > 1 and mag: a = buig(a, f['dx'] - midden(i), dy, d, hoog_kant, hoog)
        Image.fromarray(a).save(os.path.join(ROOT, f['src']))
        g = dict(f); g['dy'] = dy; g['h'] = a.shape[0]
        nieuw.append(g)
        print('%s %2d  voeten %4d %4d  schuif %3d  buig %s %3d%s' % (naam, i, voor, achter, schuif, 'voor' if hoog_kant < 0 else 'achter', d, '' if mag else ' (pas)'))
    m['bewegingen'][naam]['frames'] = nieuw

def main():
    namen = sys.argv[1:] or ['zwaai']
    pad = os.path.join(ROOT, 'brutus.json')
    m = json.load(open(pad))
    os.makedirs(BRON, exist_ok=True)
    bpad = os.path.join(BRON, 'brutus.json')
    if not os.path.exists(bpad): shutil.copy(pad, bpad)
    orig = json.load(open(bpad))
    for naam in namen:                                           # eenmalig: de onbewerkte regels van deze beweging bewaren
        if naam not in orig['bewegingen']: orig['bewegingen'][naam] = m['bewegingen'][naam]
    json.dump(orig, open(bpad, 'w'), ensure_ascii=False, indent=1)
    for naam in namen: zet(m, orig, naam)
    m['zwaaiVoeten'] = 'zwaai, kap en terug: voeten op de grondlijn gezet en het hogere been omlaag gebogen (tools/brutus_voeten.py)'
    json.dump(m, open(pad, 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
