#!/usr/bin/env python3
"""Maakt de stenen bogen in design/boog/ uit de aangeleverde platen in design/boog/bron/.

De platen staan op wit met een magenta opening. Dit script haalt het wit weg en vult het
magenta zoals de opening van de deur (design/deur/deur_open.png): van boven naar onder
donkerbruin dat iets oploopt, links iets lichter dan rechts (het licht valt van links),
een lichtere vloerstrook onderin, en een zachte schaduw net onder de boog. De roze zweem
langs de stenen wordt eruit gerekend, zodat er geen roze rand blijft.

bron/boog_laag.jpg bevat vier bogen onder elkaar; die worden apart uitgeknipt.
De maat van de opening per boog komt in metadata.json (in pixels van het eindbeeld).

Per boog komen er twee kleurversies bij, voor de look van een poort in het spel:
- _sneeuw: een sneeuwkap op de bovenkant (rock_snow uit tools/sneeuw.py, zoals de rotsen) en
  de koude tint op de steen;
- _savanne: de steen in de warme kleur van de savannegrond (SAVANNE, dezelfde tint als de
  richel met look savanne, LEDGE_SAVANNE in de HTML), licht en donker blijven.
De opening zelf blijft in beide het donker van de gewone boog (het magenta van de bron is het
masker), zodat er geen sneeuw of oranje in het gat komt.

    python3 tools/boog_vulling.py          alles opnieuw
    python3 tools/boog_vulling.py --gat    alleen de maskers van de opening (_gat.png)

Per boog komt er ook een masker van de opening bij, <naam>_gat.png: wit, met als alfa de
opening (het magenta van de bron). Het hek van een poort (design/boog/hek.png) wordt daarop
afgeknipt, zodat het achter de stenen van de boog verdwijnt als het omhoog gaat.

Vereist Pillow en numpy.
"""
import json, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sneeuw import rock_snow  # noqa: E402

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
SAVANNE = np.array([0xc4, 0x8a, 0x4a]) / 255.   # LEDGE_SAVANNE in de HTML
SAVANNE_MENG = 0.85   # zoveel van de savannekleur, de rest blijft de grijze steen
SNEEUW = dict(cap_min=0.035, cap_max=0.09, slope_k=4.0)   # de kap: dun, maar ook op de ronding (een hoge slope_k laat hem op de schuine stenen liggen)

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
    gat = Image.fromarray((mag * 255).astype(np.uint8), 'L').crop(bb)
    return img.crop(bb), [int(x0 - bb[0]), int(y0 - bb[1]), int(x1 - bb[0]), int(y1 - bb[1])], gat

def met_gat(pad, basis, gat):
    """zet de opening van de gewone boog terug in de kleurversie op pad"""
    a = np.asarray(Image.open(pad).convert('RGBA')).astype(float)
    b = np.asarray(basis).astype(float)
    g = (np.asarray(gat).astype(float) / 255)[..., None]
    a[..., :3] = a[..., :3] * (1 - g) + b[..., :3] * g
    Image.fromarray(a.round().astype(np.uint8), 'RGBA').save(pad, optimize=True)

def savanne(basis, pad):
    """de steen naar de savannekleur, met het licht en donker van de steen zelf"""
    a = np.asarray(basis).astype(float) / 255
    rgb = a[..., :3]
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2])[..., None]
    lt = 0.299 * SAVANNE[0] + 0.587 * SAVANNE[1] + 0.114 * SAVANNE[2]
    getint = np.clip(SAVANNE[None, None, :] * lum / lt, 0, 1)
    a[..., :3] = rgb * (1 - SAVANNE_MENG) + getint * SAVANNE_MENG
    Image.fromarray((a * 255).round().astype(np.uint8), 'RGBA').save(pad, optimize=True)

def gat_bewaar(gat, naam):
    """het masker van de opening: wit met de opening als alfa"""
    g = np.asarray(gat)
    wit = np.full(g.shape + (3,), 255, np.uint8)
    Image.fromarray(np.dstack([wit, g]), 'RGBA').save(os.path.join(DIR, naam + '_gat.png'), optimize=True)

def main():
    alleen_gat = '--gat' in sys.argv
    meta = {}
    def bewaar(im, naam):
        c, o, gat = schoon(im)
        gat_bewaar(gat, naam)
        if alleen_gat:
            print(naam, 'gat'); return
        c.save(os.path.join(DIR, naam + '.png'), optimize=True)
        rock_snow(os.path.join(DIR, naam + '.png'), os.path.join(DIR, naam + '_sneeuw.png'), **SNEEUW)
        met_gat(os.path.join(DIR, naam + '_sneeuw.png'), c, gat)
        savanne(c, os.path.join(DIR, naam + '_savanne.png'))
        met_gat(os.path.join(DIR, naam + '_savanne.png'), c, gat)
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
    if alleen_gat:
        return
    with open(os.path.join(DIR, 'metadata.json'), 'w') as f:
        json.dump({'opening': '[x0, y0, x1, y1] van de donkere opening, onderkant = grondlijn',
                   'bogen': meta}, f, indent=2)
        f.write('\n')

if __name__ == '__main__':
    main()
