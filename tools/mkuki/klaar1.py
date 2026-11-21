"""python3 klaar1.py frame.npy pad [--benen] [--draai] [--geenhoofd] [--voeten] [--schoon]: een los uitgelijnd frame afwerken
en bewaren in werk/klaar.

--draai: ondersteboven-frame (rol). Afwerken gebeurt op het 180 graden gedraaide frame, zodat "boven de kralen" weer het
hoofd is en "onder de broek" weer de voeten; daarna terug gedraaid.
--geenhoofd: gezicht niet uit het origineel terugzetten (liggende poses, waar boven niet klopt).
--voeten: voeten uit het origineel terugzetten (standaard blijven de voeten van Grok)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster, afwerk
from speer_meet import meet_pad
npy, pad = sys.argv[1], sys.argv[2]
a = np.load(npy); o = raster.laad(pad)
b = os.path.basename(pad)
spr = not ('_ns' in b or '/zonder/' in pad or '/jump/jump/' in pad or '/bukken/bukken/' in pad or (b.startswith('sluipen_') and 'speer' not in b))
info = meet_pad(pad, o) if spr else None
draai = '--draai' in sys.argv
if draai:
    H, W = o.shape[:2]
    a = a[::-1, ::-1].copy(); o = o[::-1, ::-1].copy()
    if info is not None:
        info = dict(info)
        info['masker'] = info['masker'][::-1, ::-1].copy()
        info['handen'] = [[W - 1 - x, H - 1 - y] for x, y in info.get('handen', [])]
r = afwerk.afwerk(a, o, info, hoofd='--geenhoofd' not in sys.argv, benen='--benen' in sys.argv,
                  voeten='--voeten' in sys.argv)
lijf, vuist = r['lijf'], r['vuist']
if '--schoon' in sys.argv:
    # dunne losse sliertjes (randjes van het speergat, lintresten) weg: wat na een opening verder dan 4 px van het lijf ligt
    from scipy import ndimage as nd
    al = lijf[..., 3] > 40
    kern = nd.binary_opening(al, iterations=2)
    ver = al & ~nd.binary_dilation(kern, iterations=4)
    lijf = lijf.copy(); lijf[ver] = 0
if draai:
    lijf = lijf[::-1, ::-1].copy(); vuist = vuist[::-1, ::-1].copy()
os.makedirs('/home/claude/werk/klaar', exist_ok=True)
np.savez_compressed('/home/claude/werk/klaar/' + pad.replace('/', '__') + '.npz', lijf=lijf, vuist=vuist)
print('klaar', b, ('vuist niet geplakt: %s' % afwerk.MIS) if afwerk.MIS else '')
