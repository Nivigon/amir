"""python3 klaar.py werkmap naam [skip,...] -> afwerken en de hulpkleur-lijven bewaren in /home/claude/werk/klaar/<pad>.npz"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster, afwerk
from speer_meet import meet
W, naam = sys.argv[1], sys.argv[2]
skip = set(sys.argv[3].split(',')) if len(sys.argv) > 3 else set()
meta = json.load(open(f'{W}/{naam}.json'))
ov = json.load(open(f'{W}/overrides.json')) if os.path.exists(f'{W}/overrides.json') else {}
for i, p in enumerate(meta['plekken']):
    if p['naam'] == 'anker' or os.path.basename(p['naam']) in skip:
        continue
    a = np.load(f'{W}/{naam}_{i}.npy'); o = raster.laad(p['naam'])
    b = os.path.basename(p['naam'])
    info = meet(o, ov.get(b)) if meta['speer'].get(b) else None
    r = afwerk.afwerk(a, o, info, **ov.get(b, {}).get('afwerk', {}))
    uit = '/home/claude/werk/klaar/' + p['naam'].replace('/', '__') + '.npz'
    np.savez_compressed(uit, lijf=r['lijf'], vuist=r['vuist'])
    print('klaar', b)
