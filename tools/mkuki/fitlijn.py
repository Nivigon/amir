"""python3 fitlijn.py pad... : verfijnt tip en kont in overrides.json door een lijn te fitten op de schachtpixels
(bruin, binnen 12 px van de gemeten lijn). Voor frames waar de band naast de schacht valt (rol 23)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, raster
from speer_meet import meet, override, rel, OVF, _kleuren
ov = json.load(open(OVF))
for p in sys.argv[1:]:
    a = raster.laad(p); r = meet(a, override(p))
    al, grijs, rood, bruin, donker = _kleuren(a)
    t0, k0 = np.array(r['tip']), np.array(r['kont'])
    for it in range(3):
        d = (k0 - t0) / np.linalg.norm(k0 - t0); L = np.linalg.norm(k0 - t0)
        ys, xs = np.where(bruin)
        t = (xs - t0[0]) * d[0] + (ys - t0[1]) * d[1]
        s = (xs - t0[0]) * (-d[1]) + (ys - t0[1]) * d[0]
        m = (t > 0.25 * L) & (t < L + 10) & (np.abs(s) < (12 if it == 0 else 6))
        if m.sum() < 30: break
        P = np.stack([xs[m], ys[m]], 1).astype(float); c = P.mean(0)
        u = np.linalg.svd(P - c)[2][0]
        if u @ d < 0: u = -u
        # tip blijft op de lijn door het centrum, lengte gelijk
        tt = (t0 - c) @ u; t0 = c + u * tt; k0 = t0 + u * L
    o = ov.setdefault(rel(p), {})
    o['tip'] = [round(float(t0[0]), 1), round(float(t0[1]), 1)]; o['kont'] = [round(float(k0[0]), 1), round(float(k0[1]), 1)]
    print(rel(p), r['tip'], r['kont'], '->', o['tip'], o['kont'])
json.dump(ov, open(OVF, 'w'), indent=1)
