#!/usr/bin/env python3
"""Knipt de raamvarianten voor het oude huis (een accent, zie "accenten" in notities/stad.md) uit
design/stad/bron/ramen_grok.png.

De Grok-plaat (1792x1008, doorzichtige achtergrond) heeft zes ramen, elk in een vierkant stuk leemmuur, drie naast elkaar
en twee rijen: spitsboog, doek over de vensterbank, dichtgemetseld, luiken half open, traliewerk, pot op de vensterbank.
Per raam zoeken we het kozijn (het hout en het donker, niet de leem), nemen er een randje muur omheen met een zachte rand,
en kleuren die muur naar de leem van gevel.png rond zijn raam. Het spel legt het stuk zo neer dat het kozijn precies over
het raam van het oude huis valt (STAD_NACHT.ramen.gevel).

Uit: design/stad/raam_<naam>.png, en de maten (het kozijn in het stuk) voor STAD_RAMEN.

    python3 tools/ramen_knip.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAD = os.path.join(ROOT, 'design', 'stad')
BRON = os.path.join(STAD, 'bron', 'ramen_grok.png')
KOL = [(92, 548), (665, 1126), (1248, 1703)]
RIJ = [(34, 468), (520, 958)]
NAMEN = ['spitsboog', 'doek', 'dicht', 'luiken', 'tralie', 'pot']
RAAM = (411, 668, 536, 848)      # het raam van gevel.png (links, boven, rechts, onder), zoals STAD_NACHT.ramen.gevel
RAND = 0.22                      # zoveel muur (deel van de kozijnbreedte) blijft er rondom
ZACHT = 0.55                     # zo ver (deel van de rand) loopt de rand zacht uit


def leem_om(a, r, dik=40):
    """De gemiddelde kleur van de muur in een ring om rechthoek r."""
    x0, y0, x1, y1 = r
    ring = np.concatenate([a[y0 - dik:y0, x0:x1].reshape(-1, 4), a[y1:y1 + dik, x0:x1].reshape(-1, 4),
                           a[y0:y1, x0 - dik:x0].reshape(-1, 4), a[y0:y1, x1:x1 + dik].reshape(-1, 4)])
    ring = ring[ring[:, 3] > 200][:, :3].astype(float)
    return ring.mean(0)


def main():
    vel = np.asarray(Image.open(BRON).convert('RGBA')).astype(float)
    gevel = np.asarray(Image.open(os.path.join(STAD, 'gevel.png')).convert('RGBA')).astype(float)
    doel = leem_om(gevel, RAAM)
    i = 0
    for (ry0, ry1) in RIJ:
        for (kx0, kx1) in KOL:
            naam = NAMEN[i]; i += 1
            p = vel[ry0:ry1, kx0:kx1]
            # het kozijn: wat duidelijk donkerder is dan de leem (hout, donker, doek), in het midden van het stuk
            lum = p[..., :3].mean(2)
            leem = np.median(lum[p[..., 3] > 200])
            k = (lum < leem * 0.72) & (p[..., 3] > 200)
            h, w = k.shape
            k[:int(h * 0.08)] = False; k[-int(h * 0.08):] = False; k[:, :int(w * 0.08)] = False; k[:, -int(w * 0.08):] = False
            ys, xs = np.nonzero(k)
            # de buitenste 1 procent weg: een losse donkere spikkel in de muur telt niet mee
            fx0, fx1 = np.percentile(xs, [1, 99]); fy0, fy1 = np.percentile(ys, [1, 99])
            fw = fx1 - fx0; m = RAND * fw
            cx0, cy0 = int(max(0, fx0 - m)), int(max(0, fy0 - m)); cx1, cy1 = int(min(w, fx1 + m)), int(min(h, fy1 + m))
            stuk = p[cy0:cy1, cx0:cx1].copy()
            # de muur in het stuk naar de leem van het oude huis
            zelf = stuk[..., :3][(stuk[..., 3] > 200) & (stuk[..., :3].mean(2) > leem * 0.85)].mean(0)
            stuk[..., :3] = np.clip(stuk[..., :3] + (doel - zelf) * 0.9, 0, 255)
            # een zachte rand: de alfa loopt naar buiten toe af
            sh, sw = stuk.shape[:2]
            yy, xx = np.mgrid[0:sh, 0:sw]
            afst = np.minimum.reduce([xx, sw - 1 - xx, yy, sh - 1 - yy]).astype(float)
            stuk[..., 3] *= np.clip(afst / (m * ZACHT), 0, 1) ** 1.5
            Image.fromarray(stuk.round().astype(np.uint8)).save(os.path.join(STAD, f'raam_{naam}.png'), optimize=True)
            # het kozijn in het stuk (links, boven, rechts, onder)
            print(f"    {naam}: {{ w: {sw}, h: {sh}, k: [{round(fx0 - cx0)}, {round(fy0 - cy0)}, {round(fx1 - cx0)}, {round(fy1 - cy0)}] }},")


if __name__ == '__main__':
    main()
