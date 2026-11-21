#!/usr/bin/env python3
"""De Pathfinder Spear: de speer uit de winkel van Co-op, met het rode vaantje dat meewaait.

Uit de Grok-platen in design/speer/pathfinder/bron/ (al uitgeknipt, op doorzichtig):
  speer.png            de speer, punt rechts, het vaantje er al af (alleen het rode bandje om de binding)
  vaantje_1..4.png     het vaantje los, in vier standen: stil, licht wiegen, wind, harde wind
  knopen.json          per vaantje waar het knoopje zit (in px van dat plaatje)
schrijft het
  design/speer/pathfinder/jav.png        even lang als de gewone speer (speer_projectiel.png, 624 px), punt rechts
  design/speer/pathfinder/vaantje_n.png  op dezelfde schaal als jav.png, maal VAAN_K (scherper)

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
VAAN_S = 0.30          # het vaantje ten opzichte van de bron van de speer (zo zag het er op de plaat goed uit)
VAAN_K = 2             # de vaantjes twee keer zo groot opslaan als ze getekend worden, voor de scherpte
KNOOP = (985, 119)     # waar het vaantje aan de speer hangt, in px van bron/speer.png (onder het rode bandje)

sp = Image.open(os.path.join(BRON, 'speer.png')).convert('RGBA')
sp = sp.crop(sp.getbbox())
k = JAV_W / sp.width
jav = sp.resize((JAV_W, round(sp.height * k)), Image.LANCZOS)
jav.save(os.path.join(MAP, 'jav.png'))
a = np.array(jav)[..., 3] > 128
tip_y = float(np.where(a[:, JAV_W - 3])[0].mean())

knopen = json.load(open(os.path.join(BRON, 'knopen.json')))
vaan = []
for i, kn in enumerate(knopen):
    f = Image.open(os.path.join(BRON, kn['file'])).convert('RGBA')
    s = k * VAAN_S * VAAN_K
    f = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
    f.save(os.path.join(MAP, 'vaantje_%d.png' % (i + 1)))
    vaan.append([round(kn['knoop'][0] * s, 1), round(kn['knoop'][1] * s, 1)])

print('PATHFINDER = { w: %d, h: %d, tipX: %d, tipY: %.1f, knoop: [%.1f, %.1f], vaanK: %d, vaan: %s }'
      % (jav.width, jav.height, JAV_W - 1, tip_y, KNOOP[0] * k, KNOOP[1] * k, VAAN_K, json.dumps(vaan)))
