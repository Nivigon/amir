"""Per stokframe het vak rond kop en schouders voor Grok (bouw_kop), en de werkvolgorde."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tau
SETS = ['bukken', 'sluipen', 'slag', 'blok', 'draaislag', 'draaiterug', 'stapslag', 'slag2', 'laag', 'grondklap']
N = {'bukken': 12, 'sluipen': 28, 'slag': 18, 'blok': 13, 'draaislag': 15, 'draaiterug': 6, 'stapslag': 28, 'slag2': 27, 'laag': 23, 'grondklap': 26}


def box(set_, i, w=210):
    _, _, l = tau.bron(set_, i)
    al = l[..., 3] > 100
    ys, xs = np.where(al)
    H, W = al.shape
    # de kop: het hoogste stuk lijf; neem de kolommen van de bovenste 30 px
    top = ys.min()
    band = al[top:top + 30]
    cx = int(np.where(band.any(0))[0].mean())
    x0 = int(np.clip(cx - w // 2, 0, W - w)); y0 = int(np.clip(top - 20, 0, H - w))
    return (x0, y0, x0 + w, y0 + w)


if __name__ == '__main__':
    lijst = []
    for s in SETS:
        for i in range(N[s]):
            b = box(s, i)
            tau.bouw_kop('k_%s_%d' % (s, i), s, i, b)
            lijst.append(['k_%s_%d' % (s, i), s, i])
    json.dump(lijst, open('/home/claude/werk/todo.json', 'w'))
    print(len(lijst))
