"""Tau 1: de stokken uit een gebakken stokframe halen (masker zoals tools/stok_variant.py, wissel).

stok_maskers(pad) -> (frame RGBA, [masker per stok], lijf RGBA zonder stokken)
Het masker per stok is wat in het origineel van die stok te zien is; dat leggen we na het aankleden terug.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import stok_variant as sv

HOEK = json.load(open(os.path.join(ROOT, 'karakters/amir/stokken/bron/stokhoeken.json')))


def stok_maskers(set_, i):
    pad = os.path.join(ROOT, 'karakters/amir/stokken/%s/%s_%02d.png' % (set_, set_, i))
    im = Image.open(pad).convert('RGBA'); W, H = im.size
    fr = np.array(im).astype(int)
    S = sv.stokkleur(fr)
    maskers = []
    for deg, flip, k, kx, ky, *rest in HOEK[set_][i]:
        oud, okn = sv.oude_stok(k)
        ol = np.array(sv.plaats(oud, okn, (kx, ky), deg, flip, W, H)).astype(int); m = ol[..., 3]
        w = (m > 200) & (fr[..., 3] > 60) & (np.abs(ol[..., :3] - fr[..., :3]).sum(-1) < 90)
        ruim = np.array(Image.fromarray(((m > 40) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
        w |= ruim & S
        maskers.append(w)
    lijf = fr.copy()
    for w in maskers: lijf[w, 3] = 0
    return fr.astype(np.uint8), maskers, lijf.astype(np.uint8)


if __name__ == '__main__':
    set_, i, uit = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    fr, ms, lijf = stok_maskers(set_, i)
    vis = fr.copy()
    for k, w in enumerate(ms): vis[w] = [0, 255, 0, 255] if k == 0 else [0, 160, 255, 255]
    Image.fromarray(np.hstack([fr, vis, lijf])).resize((fr.shape[1] * 3 * 2, fr.shape[0] * 2), Image.NEAREST).save(uit)
