"""python3 schedel.py <deelvan-klaar-naam> [straal]: een hap uit de schedelrand dichten in werk/klaar (sluiting op de
bovenste 18% van de figuur, gevuld met de dichtstbijzijnde kleur). Voor frames waar de speer door het hoofd liep."""
import sys, glob, numpy as np
from scipy import ndimage as nd
f = glob.glob('/home/claude/werk/klaar/*' + sys.argv[1] + '*')[0]
r = int(sys.argv[2]) if len(sys.argv) > 2 else 9
d = dict(np.load(f)); a = d['lijf'].copy()
al = a[..., 3] > 40
ys = np.where(al.any(1))[0]; y0, y1 = ys.min(), ys.min() + int(0.18 * (ys.max() - ys.min()))
sch = np.zeros_like(al); sch[y0:y1] = al[y0:y1]
yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; k = xx ** 2 + yy ** 2 <= r * r
dicht = nd.binary_closing(np.pad(sch, r), structure=k)[r:-r, r:-r] & ~al
dicht[y1:] = False
_, (iy, ix) = nd.distance_transform_edt(~al, return_indices=True)
a[dicht] = a[iy[dicht], ix[dicht]]; a[dicht, 3] = 255
d['lijf'] = a; np.savez_compressed(f, **d); print('gedicht', int(dicht.sum()), 'px')
