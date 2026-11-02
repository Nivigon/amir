#!/usr/bin/env python3
"""De voeten van Brutus (Nyundo) in de zwaai op de grond zetten.

In de Grok-clip van de zwaai zweeft hij zo'n 30 tot 60 grote-set-pixels boven de grondlijn, en staat
de ene voet hoger dan de andere (eerst de voorste, aan het eind de achterste). In een zijaanzicht moeten
allebei zijn voeten op de grondlijn staan. Per zwaaiframe:

1. meet de onderkant van elke voet: de laagste huid- of sandaalpixel links en rechts van het anker
   (verzadigd en warm, dus niet de grijze knotsbal);
2. schuif het hele frame omlaag tot de laagste voet op DOEL staat (net als de achterste voet in de idle);
3. buig het been van de hogere voet omlaag tot die ook op DOEL staat: een zachte verschuiving die
   onder de heup begint (0) en bij de voet vol is, en die van het kruis naar buiten oploopt, zodat
   het lijf, de heup en het andere been blijven waar ze zijn.

De originelen gaan eerst naar enemies/brutus/bron/ (eenmalig); het script werkt altijd vanaf die
originelen, dus je kunt het opnieuw draaien. Daarna: python3 tools/gen-klein.py en
python3 tools/gen-offline-manifest.py.
"""
import json, os, shutil
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

ROOT = os.path.join(os.path.dirname(__file__), '..', 'enemies', 'brutus')
BRON = os.path.join(ROOT, 'bron')
DOEL = -3            # waar de voeten moeten staan (anker-coordinaten, 0 is de grondlijn, negatief is erboven)
HEUP = -175          # vanaf deze hoogte begint de buiging (anker-coordinaten)
KRUIS = (8, 70)      # de buiging loopt op van zoveel px naast het anker tot zoveel px (naar buiten)
SPRONG = 6           # een voet die meer dan zoveel px uit de pas loopt met zijn buren: de knots, niet de voet

def zacht(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

def voeten(a, dx, dy):
    R, G, B, A = [a[..., i].astype(int) for i in range(4)]
    mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
    sat = (mx - mn) / np.maximum(mx, 1)
    ok = (A > 120) & (sat > 0.3) & (R > G) & (G >= B) & (R - B > 40)
    xs = np.arange(A.shape[1]) + dx
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

def main():
    pad = os.path.join(ROOT, 'brutus.json')
    m = json.load(open(pad))
    os.makedirs(BRON, exist_ok=True)
    if not os.path.exists(os.path.join(BRON, 'brutus.json')): shutil.copy(pad, os.path.join(BRON, 'brutus.json'))
    orig = json.load(open(os.path.join(BRON, 'brutus.json')))
    fr_o = orig['bewegingen']['zwaai']['frames']
    metingen = []
    for f in fr_o:
        src = os.path.join(ROOT, f['src']); b = os.path.join(BRON, os.path.basename(f['src']))
        if not os.path.exists(b): shutil.copy(src, b)
        metingen.append(voeten(np.array(Image.open(b).convert('RGBA')), f['dx'], f['dy']))
    # een uitschieter (de knotsbal vlak bij de grond) vervangen door het gemiddelde van zijn buren
    for k in (0, 1):
        for i in range(1, len(metingen) - 1):
            a, b, c = metingen[i - 1][k], metingen[i][k], metingen[i + 1][k]
            if abs(b - a) > SPRONG and abs(b - c) > SPRONG: metingen[i][k] = round((a + c) / 2)
    nieuw = []
    for i, f in enumerate(fr_o):
        a = np.array(Image.open(os.path.join(BRON, os.path.basename(f['src']))).convert('RGBA'))
        voor, achter = metingen[i]
        laag = max(voor, achter)
        schuif = DOEL - laag                                     # het hele frame omlaag
        dy = f['dy'] + schuif
        hoog_kant = -1 if voor < achter else 1
        hoog = min(voor, achter) + schuif
        d = DOEL - hoog
        if d > 1: a = buig(a, f['dx'], dy, d, hoog_kant, hoog)
        Image.fromarray(a).save(os.path.join(ROOT, f['src']))
        g = dict(f); g['dy'] = dy; g['h'] = a.shape[0]
        nieuw.append(g)
        print('zwaai %2d  voeten %4d %4d  omlaag %3d  buig %s %3d' % (i, voor, achter, schuif, 'voor' if hoog_kant < 0 else 'achter', d))
    m['bewegingen']['zwaai']['frames'] = nieuw
    m['zwaaiVoeten'] = 'zwaai: voeten op de grondlijn gezet en het hogere been omlaag gebogen (tools/brutus_voeten.py)'
    json.dump(m, open(pad, 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
