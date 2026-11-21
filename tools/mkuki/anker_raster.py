"""python3 anker_raster.py werkmap naam ankerpad [--draai] [--geen-speer] frame1 frame2 ...
Bouwt een raster met het aangeklede anker (uit /home/claude/werk/klaar) in tegel 1 en de nieuwe frames erna."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster
args = sys.argv[1:]
draai = '--draai' in args; geen = '--geen-speer' in args
args = [a for a in args if not a.startswith('--')]
W, naam, anker = args[0], args[1], args[2]
fr = args[3:]
a = np.load('/home/claude/werk/klaar/' + anker.replace('/', '__') + '.npz')['lijf']
items = [{'pad': f, 'speer': not geen and '_ns' not in os.path.basename(f), 'draai': draai} for f in fr]
m = raster.bouw(items, f'{W}/{naam}.png', f'{W}/{naam}.json', anker=a)
print(m['crop'], round(m['schaal'], 3))
