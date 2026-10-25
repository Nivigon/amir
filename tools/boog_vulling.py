#!/usr/bin/env python3
"""Maakt de stenen bogen in design/boog/ uit de aangeleverde platen in design/boog/bron/.

De platen staan op wit met een magenta opening. Dit script haalt het wit weg en vult het
magenta zoals de opening van de deur (design/deur/deur_open.png): van boven naar onder
donkerbruin dat iets oploopt, links iets lichter dan rechts (het licht valt van links),
een lichtere vloerstrook onderin, en een zachte schaduw net onder de boog. De roze zweem
langs de stenen wordt eruit gerekend, zodat er geen roze rand blijft.

bron/boog_laag.jpg bevat vier bogen onder elkaar; die worden apart uitgeknipt.
De maat van de opening per boog komt in metadata.json (in pixels van het eindbeeld).

    python3 tools/boog_vulling.py

Vereist Pillow en numpy.
"""
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'design', 'boog')

# de kleuren uit de opening van deur_open.png
WAND_BOVEN = np.array([28, 21, 20.])
WAND_ONDER = np.array([54, 40, 30.])
VLOER_LINKS = np.array([78, 58, 41.])
VLOER_RECHTS = np.array([61, 46, 34.])
VLOER_VANAF = 0.875   # dit deel van de openingshoogte is wand, de rest vloer
ZIJLICHT = 8          # links zoveel lichter, rechts zoveel donkerder
BOVENSCHADUW = 0.12   # over dit deel van de hoogte loopt de schaduw onder de boog weg

def schoon(im):
    a = np.asarray(im.convert('RGB')).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r + b) / 2 - g                          # hoe roze een pixel is
    mref = np.percentile(m, 99)                  # het magenta van deze plaat
    mag = np.clip((m - 40) / (mref * 0.92 - 40), 0, 1)
    wit = np.clip((np.minimum(np.minimum(r, g), b) - 212) / 24, 0, 1)
    ys, xs = np.where(mag > 0.9)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    H, W = r.shape
    Y, X = np.mgrid[0:H, 0:W]
    ty = np.clip((Y - y0) / max(1, y1 - y0), 0, 1)
    tx = np.clip((X - x0) / max(1, x1 - x0), 0, 1)
    wand = WAND_BOVEN + (WAND_ONDER - WAND_BOVEN) * np.clip(ty / VLOER_VANAF, 0, 1)[..., None]
    wand += (ZIJLICHT - 2 * ZIJLICHT * tx)[..., None]
    vloer = VLOER_LINKS + (VLOER_RECHTS - VLOER_LINKS) * tx[..., None]
    vul = np.where((ty > VLOER_VANAF)[..., None], vloer, wand)
    vul *= (0.75 + 0.25 * np.clip(ty / BOVENSCHADUW, 0, 1))[..., None]
    MAG = np.median(a[mag >= 1], axis=0)
    k = np.clip(1 - mag, 1e-3, 1)[..., None]
    rots = np.clip((a - (1 - k) * MAG) / k, 0, 255)
    uit = rots * k + vul * (1 - k)
    alfa = np.maximum(1 - wit, mag)
    img = Image.fromarray(np.dstack([uit, alfa * 255]).astype(np.uint8), 'RGBA')
    bb = img.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    return img.crop(bb), [int(x0 - bb[0]), int(y0 - bb[1]), int(x1 - bb[0]), int(y1 - bb[1])]

def main():
    meta = {}
    def bewaar(im, naam):
        c, o = schoon(im)
        c.save(os.path.join(DIR, naam + '.png'), optimize=True)
        meta[naam] = {'maat': list(c.size), 'opening': o}
        print(naam, c.size, 'opening', o)
    bewaar(Image.open(os.path.join(DIR, 'bron', 'boog_steen.jpg')), 'boog_steen')
    bewaar(Image.open(os.path.join(DIR, 'bron', 'boog_rots.jpg')), 'boog_rots')
    plaat = Image.open(os.path.join(DIR, 'bron', 'boog_laag.jpg'))
    grijs = np.asarray(plaat.convert('L'))
    leeg = (grijs < 200).sum(1) < 3
    rijen, binnen = [], False
    for y, e in enumerate(leeg):
        if not e and not binnen:
            s, binnen = y, True
        if e and binnen:
            if y - s > 100:
                rijen.append((s, y))
            binnen = False
    for i, (s, e) in enumerate(rijen):
        bewaar(plaat.crop((0, max(0, s - 4), plaat.width, min(plaat.height, e + 4))), f'boog_laag_{i + 1}')
    with open(os.path.join(DIR, 'metadata.json'), 'w') as f:
        json.dump({'opening': '[x0, y0, x1, y1] van de donkere opening, onderkant = grondlijn',
                   'bogen': meta}, f, indent=2)
        f.write('\n')

if __name__ == '__main__':
    main()
