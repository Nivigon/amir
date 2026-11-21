"""python3 klaar1.py frame.npy pad [--benen]: een los uitgelijnd frame afwerken en bewaren in werk/klaar."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster, afwerk
from speer_meet import meet_pad
npy, pad = sys.argv[1], sys.argv[2]
a = np.load(npy); o = raster.laad(pad)
b = os.path.basename(pad)
spr = not ('_ns' in b or '/zonder/' in pad or '/jump/jump/' in pad or '/bukken/bukken/' in pad or (b.startswith('sluipen_') and 'speer' not in b))
info = meet_pad(pad, o) if spr else None
r = afwerk.afwerk(a, o, info, benen='--benen' in sys.argv)
np.savez_compressed('/home/claude/werk/klaar/' + pad.replace('/', '__') + '.npz', lijf=r['lijf'], vuist=r['vuist'])
print('klaar', b)
