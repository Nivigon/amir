#!/usr/bin/env python3
"""De Pathfinder Spear: de speer uit de winkel van Co-op, met het rode vaantje dat meewaait.

Uit de Grok-platen in design/speer/pathfinder/bron/ (al uitgeknipt, op doorzichtig):
  speer.png            de speer, punt rechts, het vaantje er al af (alleen het rode bandje om de binding)
  vaantje_1..4.png     het vaantje los, in vier standen: stil, licht wiegen, wind, harde wind
  knopen.json          per vaantje waar het knoopje zit (in px van dat plaatje)
schrijft het
  design/speer/pathfinder/jav.png        even lang en bijna even slank als de gewone speer (speer_projectiel.png, 624 px),
                                         punt rechts; het hout rekt mee, dop, greep en kop houden hun vorm
  design/speer/pathfinder/vaantje_n.png  het vaantje, maal VAAN_K (scherper)

en print de getallen voor PATHFINDER in de HTML: de maat, waar de punt zit en waar het knoopje van het vaantje
aan de speer hangt (in px van jav.png), en per vaantje zijn knoopje.

  python3 tools/pathfinder_speer.py
daarna tools/gen-offline-manifest.py.
"""
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'design/speer/pathfinder')
BRON = os.path.join(MAP, 'bron')
JAV_W = 624            # de lengte van de gewone speer (JAV.w): dezelfde schaal
SCHACHT = 17           # de dikte van de schacht in jav.png; de gewone speer is 15 (een upgrade mag iets steviger)
VAAN_S = 0.30 * JAV_W / 1313   # het vaantje ten opzichte van bron/speer.png: dezelfde maat als in de eerste versie
VAAN_K = 2             # de vaantjes twee keer zo groot opslaan als ze getekend worden, voor de scherpte
KNOOP = (985, 119)     # waar het vaantje aan de speer hangt, in px van bron/speer.png (onder het rode bandje)
# de stukken langs de speer, in px van bron/speer.png: de dop, het hout, de greep met kralen, het hout, de kop
# (binding, dwarsstuk en blad). De dop, de greep en de kop krijgen een vaste schaal, het hout rekt mee tot de
# speer even lang is als de gewone; zo is hij even lang en even slank, zonder dat de kralen of de kop vervormen.
DOP, GREEP, KOP = (0, 75), (385, 722), 968

# De rand van de gewone speer (speer_projectiel.png), zodat hij verkleind in het spel even goed loskomt van de grond:
# een harde donkere lijn om het hele silhouet, boven langs een lichte glimlijn en onder een zachte schaduw.
RAND_LIJN = (34, 26, 22)            # de omlijning, dekkend (de gewone: 37,33,33 boven en 30,20,14 onder)
RAND_GLIM = (186, 183, 183, 78)     # de glimlijn erboven, half doorzichtig (zo staat hij in de gewone)
RAND_SCHADUW = (0, 0, 0, 140)       # de schaduw eronder

def rand(im):
    a = np.array(im).astype(np.int32)
    m = a[..., 3] > 128
    p = np.pad(m, 1)
    binnen = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    lijn = m & ~binnen
    uit = np.zeros_like(a)
    uit[m] = a[m]; uit[m, 3] = 255
    uit[lijn, :3] = RAND_LIJN
    for x in range(a.shape[1]):
        ys = np.where(m[:, x])[0]
        if not len(ys): continue
        if ys[0] > 0: uit[ys[0] - 1, x] = RAND_GLIM
        if ys[-1] + 1 < a.shape[0]: uit[ys[-1] + 1, x] = RAND_SCHADUW
    return Image.fromarray(uit.astype(np.uint8), 'RGBA')

sp = Image.open(os.path.join(BRON, 'speer.png')).convert('RGBA')
sp = sp.crop(sp.getbbox())

# De kleuren (22-11-2026, op verzoek): een schacht van ivoor, een creme punt en een helemaal rode greep in plaats van
# de rood-witte kralen. Per stuk wordt de bron omgekleurd met zijn eigen licht en schaduw, de donkere omlijning blijft.
IVOOR = (214, 188, 146)      # de schacht: licht essenhout (A1)
CREME = (246, 234, 204)      # het blad van de punt
ROOD = (168, 32, 30)         # de greep
BLAD = 1058                  # waar het blad begint, in px van bron/speer.png (na het dwarsstuk en de huls)

def kleur(a, x0, x1, doel, glad=False):
    d = a[:, x0:x1].astype(float)
    m = d[..., 3] > 128
    lum = d[..., :3].mean(-1)
    ref = np.median(lum[m])
    r = np.clip(lum / ref, 0.45, 1.25)
    if glad:                 # een gladde ronde greep: licht van boven, donker naar onder, de kralen vallen weg
        ys = np.where(m.any(1))[0]; t = (np.arange(len(lum)) - ys[0]) / max(1, ys[-1] - ys[0])
        r = np.repeat((0.6 + 0.55 * np.exp(-((t - 0.32) / 0.3) ** 2))[:, None], lum.shape[1], 1)
    rand = m & (d[..., :3].mean(-1) < ref * 0.35)        # de omlijning houdt zijn donker
    if glad: rand[:] = False                             # de greep: ook de lijntjes tussen de kralen weg (rand() legt de buitenlijn)
    for c in range(3):
        k = d[..., c]; k[m & ~rand] = np.clip(doel[c] * r, 0, 255)[m & ~rand]
    a[:, x0:x1] = d.astype(np.uint8)

_a = np.array(sp)
kleur(_a, 75, 385, IVOOR)
kleur(_a, 722, 968, IVOOR)
kleur(_a, 385, 722, ROOD, glad=True)
kleur(_a, BLAD, _a.shape[1], CREME)
sp = Image.fromarray(_a)
a0 = np.array(sp)[..., 3] > 128
dik = int(a0[:, (GREEP[1] + KOP) // 2].sum())        # de dikte van de schacht in de bron
s = SCHACHT / dik
H = round(sp.height * s)
def stuk(x0, x1, w=None):
    im = sp.crop((x0, 0, x1, sp.height))
    return im.resize((w or max(1, round((x1 - x0) * s)), H), Image.LANCZOS)
def bouw(totaal):
    """De speer op een lengte: dop, greep en kop vast, het hout rekt mee. Is hij te kort voor de greep (de korte
    lengtes van de hand-set, een speer in verkorting), dan krimpt de greep mee en blijft er wat hout over."""
    vast = [stuk(*DOP), stuk(*GREEP), stuk(KOP, sp.width)]
    rest = totaal - vast[0].width - vast[2].width
    if rest < vast[1].width + 2 * HOUT_MIN:
        g = max(0, round((rest - 2 * HOUT_MIN) * 0.5))
        vast[1] = stuk(*GREEP, w=g) if g > 0 else None
    hout = rest - (vast[1].width if vast[1] else 0)
    h1 = GREEP[0] - DOP[1]; h2 = KOP - GREEP[1]
    w1 = round(hout * h1 / (h1 + h2)); w2 = hout - w1
    delen = [vast[0], stuk(DOP[1], GREEP[0], max(1, w1)), vast[1], stuk(GREEP[1], KOP, max(1, w2)), vast[2]]
    im = Image.new('RGBA', (totaal, H)); x = 0
    for d in delen:
        if d is None: continue
        im.alpha_composite(d, (x, 0)); x += d.width
    return im, totaal - vast[2].width

HOUT_MIN = 12          # zoveel hout houdt elke kant van de greep minstens, in px van jav.png
jav, kop_x = bouw(JAV_W)
a = np.array(jav)[..., 3] > 128                 # de punt meten zonder de schaduwrand eronder
jav = rand(jav)
jav.save(os.path.join(MAP, 'jav.png'))
tip_y = float(np.where(a[:, JAV_W - 3])[0].mean())
knoop = (kop_x + (KNOOP[0] - KOP) * s, KNOOP[1] * s)
s0 = s
k = VAAN_S

knopen = json.load(open(os.path.join(BRON, 'knopen.json')))
vaan = []
for i, kn in enumerate(knopen):
    f = Image.open(os.path.join(BRON, kn['file'])).convert('RGBA')
    s = VAAN_S * VAAN_K
    f = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
    f.save(os.path.join(MAP, 'vaantje_%d.png' % (i + 1)))
    vaan.append([round(kn['knoop'][0] * s, 1), round(kn['knoop'][1] * s, 1)])

# De hand-set: dezelfde lengtes als de speer van de Mkuki-skin (karakters/amir/mkuki_spel/bron/amirspeer_*.png), met
# dezelfde maat en de punt op dezelfde plek, zodat tools/mkuki_spel_bak.py --pathfinder de frames ermee kan bakken met
# precies de plaatsing uit de Mkuki animeer tool. Het vaantje zit er vast aan, in de stand van de wind (4), langs de
# schacht naar achteren: in Amirs handen draait het mee met de speer, net als het lint van de gewone.
HAND_BRON = os.path.join(ROOT, 'karakters/amir/mkuki_spel/bron')
HAND = os.path.join(MAP, 'hand')
os.makedirs(HAND, exist_ok=True)
v4 = Image.open(os.path.join(MAP, 'vaantje_4.png')).convert('RGBA')
fk = 1 / VAAN_K
v4 = v4.resize((max(1, round(v4.width * fk)), max(1, round(v4.height * fk))), Image.LANCZOS)
for naam in sorted(os.listdir(HAND_BRON)):
    if not (naam.startswith('amirspeer_') and naam.endswith('.png')): continue
    orig = Image.open(os.path.join(HAND_BRON, naam))
    W0, H0 = orig.size
    im, kx = bouw(W0)
    oa = np.array(orig)[..., 3] > 128
    ty = float(np.where(oa[:, W0 - 3])[0].mean())     # de punt van de gewone, daar moet de onze ook zitten
    dy = round(ty - tip_y)
    vol = Image.new('RGBA', (W0, H)); vol.alpha_composite(rand(im))
    kn = (kx + (KNOOP[0] - KOP) * s0, KNOOP[1] * s0)
    vol.alpha_composite(v4, (round(kn[0] - vaan[3][0] * fk), round(kn[1] - vaan[3][1] * fk)))
    uit = Image.new('RGBA', (W0, H0)); uit.alpha_composite(vol, (0, dy))
    uit.save(os.path.join(HAND, naam), optimize=True)

print('PATHFINDER = { w: %d, h: %d, tipX: %d, tipY: %.1f, knoop: [%.1f, %.1f], vaanK: %d, vaan: %s }'
      % (jav.width, jav.height, JAV_W - 1, tip_y, knoop[0], knoop[1], VAAN_K, json.dumps(vaan)))
