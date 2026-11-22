"""Zes kop-crops in een raster van 3x2 (1800x1100) naar Grok, zodat een generatie zes frames doet.

bouw(naam, items) items = [(set, i, box)] -> werk/naam.png + .json
terug(naam) -> per item werk/<itemnaam>.npy (zoals tau.terug_kop), print IoU
"""
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tau, raster, uitlijn
W, H, TW, TH = 1800, 1100, 600, 550


def bouw(naam, items):
    C = Image.new('RGB', (W, H), (255, 0, 255))
    meta = []
    for k, (set_, i, box) in enumerate(items):
        o = raster.laad(tau.pad(set_, i))
        x0, y0, x1, y1 = box
        c = o[y0:y1, x0:x1]
        s = min((TW - 40) / c.shape[1], (TH - 30) / c.shape[0])
        im = Image.fromarray(c).resize((round(c.shape[1] * s), round(c.shape[0] * s)), Image.LANCZOS)
        tx, ty = (k % 3) * TW, (k // 3) * TH
        px, py = tx + (TW - im.width) // 2, ty + (TH - im.height) // 2
        C.paste(Image.fromarray(raster.op_magenta(np.asarray(im))), (px, py))
        meta.append({'naam': 'k_%s_%d' % (set_, i), 'set': set_, 'i': i, 'box': list(box), 's': s, 'px': px, 'py': py,
                     'w': im.width, 'h': im.height})
    C.save(tau.WERK + naam + '.png')
    json.dump(meta, open(tau.WERK + naam + '.json', 'w'))


def terug(naam, bereik=24):
    meta = json.load(open(tau.WERK + naam + '.json'))
    g = np.asarray(Image.open(tau.WERK + naam + '_grok.png').convert('RGB'))
    rij = np.where(g.max(axis=(1, 2)) > 40)[0]
    g = Image.fromarray(g[:rij[-1] + 1]).resize((W, H), Image.LANCZOS)
    k = raster.key(np.asarray(g))
    uit = []
    for m in meta:
        o = raster.laad(tau.pad(m['set'], m['i']))
        x0, y0, x1, y1 = m['box']; oc = o[y0:y1, x0:x1]
        best = None
        for f in np.linspace(0.95, 1.05, 5):
            s = m['s'] * f
            gx0, gy0 = max(0, m['px'] - 30), max(0, m['py'] - 25)
            gx1, gy1 = min(W, m['px'] + m['w'] + 30), min(H, m['py'] + m['h'] + 25)
            tx0, ty0 = (m['px'] // TW) * TW, (m['py'] // TH) * TH
            gx0, gy0 = max(gx0, tx0), max(gy0, ty0); gx1, gy1 = min(gx1, tx0 + TW), min(gy1, ty0 + TH)
            st = k[gy0:gy1, gx0:gx1]
            kl = np.asarray(Image.fromarray(st).resize((max(1, round(st.shape[1] / s)), max(1, round(st.shape[0] / s))), Image.LANCZOS))
            ox, oy = round((gx0 - m['px']) / s), round((gy0 - m['py']) / s)
            doek = np.zeros_like(oc); Hh, Ww = oc.shape[:2]
            ya, xa = max(0, oy), max(0, ox); yb, xb = min(Hh, oy + kl.shape[0]), min(Ww, ox + kl.shape[1])
            if yb > ya and xb > xa:
                doek[ya:yb, xa:xb] = kl[ya - oy:yb - oy, xa - ox:xb - ox]
            b, dx, dy, v = uitlijn.lijn_uit(doek, oc, bereik)
            if best is None or v > best[3]:
                best = (b, dx, dy, v)
        vol = np.zeros_like(o); vol[y0:y1, x0:x1] = best[0]
        np.save(tau.WERK + m['naam'] + '.npy', vol)
        json.dump({'set': m['set'], 'i': m['i'], 'box': m['box'], 'kop': True}, open(tau.WERK + m['naam'] + '.json', 'w'))
        uit.append((m['naam'], round(float(best[3]), 3)))
    print(uit)
    return uit


if __name__ == '__main__':
    if sys.argv[1] == 'bouw':
        L = json.load(open('/home/claude/werk/todo.json'))
        namen = sys.argv[3].split(',')
        import kopbox
        items = [(s, i, kopbox.box(s, i)) for n, s, i in L if n in namen]
        bouw(sys.argv[2], items)
    else:
        tau.haal(sys.argv[2], sys.argv[3], 1800)
        r = terug(sys.argv[2])
        f = '/home/claude/werk/ids.json'; d = json.load(open(f))
        for n, v in r: d.setdefault(n, []).append(sys.argv[4])
        json.dump(d, open(f, 'w'), indent=1)
