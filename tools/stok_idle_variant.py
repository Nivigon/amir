"""De idle met de stokken op de schouders voor de winkelstokken (klauw, goud, ardhi).

De stokken in de idle komen uit Grok (groen, omgekleurd naar hout), niet uit stok_bak.py, dus stok_variant.py kan ze niet
op zijn bekende hoek weghalen. Dit script doet het met wat tools/stok_idle_maak.py meet: het masker van de stokken
(uit/idle_NN_stok.png) en de lijn van elke stok (punt.json, 'lijnen'). Het lijf zonder de oude stok gaat over de nieuwe
stok heen (zo sluiten de vuisten om de stok), en waar de oude stok over het lijf lag en de nieuwe hem niet afdekt komt
de oude terug.

  python3 tools/stok_idle_variant.py <map van stok_idle_maak.py> --rij 1 --uit stokken_klauw
  python3 tools/stok_idle_variant.py <map> --rij 3 --uit stokken_goud
  python3 tools/stok_idle_variant.py <map> --rij 0 --uit stokken_ardhi --plaat design/ardhi/bron/stok_schoon.png

Daarna de map naar klein/karakters/amir/<uit>/idle/ kopieren, vacht_bak.js en gen-offline-manifest.py.
"""
import argparse, json, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import stok_variant as sv, stok_bak as sb

K = 0.96          # de stok in de idle is iets korter dan de gewone (lengte 155)
LENGTE = 148.3    # van de punt tot het uiteinde bij de grip, ook waar dat achter de hand zit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('map'); ap.add_argument('--rij', type=int, default=1); ap.add_argument('--uit', default='stokken_klauw')
    ap.add_argument('--plaat', default=None)
    o = ap.parse_args()
    if o.plaat: sv.PLAAT = os.path.join(sv.ROOT, o.plaat)
    d = json.load(open(os.path.join(o.map, 'punt.json')))
    ni, nkn = sv.nieuwe_stok(o.rij, K)[:2]
    uit = os.path.join(sv.AMIR, o.uit, 'idle'); os.makedirs(uit, exist_ok=True)
    for i, ln in enumerate(d['lijnen']):
        fr = Image.open(os.path.join(o.map, 'uit', f'idle_{i:02d}.png')).convert('RGBA'); W, H = fr.size
        gr = np.array(Image.open(os.path.join(o.map, 'uit', f'idle_{i:02d}_stok.png'))).astype(float) / 255
        fa = np.array(fr).astype(float)
        lijf = fa.copy(); lijf[..., 3] *= np.clip(1 - gr * 1.6, 0, 1)
        can = Image.new('RGBA', (W, H))
        for j in (1, 0):                                    # de achterste stok (j 1) eerst
            x0, y0, x1, y1 = ln[j]
            deg = math.degrees(math.atan2(y1 - y0, x1 - x0)); u = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
            E = (x0 + u[0] * LENGTE, y0 + u[1] * LENGTE)
            # knoop zo dat het uiteinde (de rechterkant van het stokbeeld) op E valt, net als bij de gewone stok
            oud, okn = sv.oude_stok(K)
            h = sb.draai((oud.width / 2, 0), deg, False); C = (E[0] - h[0], E[1] - h[1]); kk = sb.draai(okn, deg, False)
            can.alpha_composite(sv.plaats(ni, nkn, (C[0] + kk[0], C[1] + kk[1]), deg, False, W, H))
        can.alpha_composite(Image.fromarray(lijf.astype(np.uint8)))
        ua = np.array(can).astype(float)
        gat = (gr > 0.2) & (ua[..., 3] < 128) & (fa[..., 3] > 128)   # stok over het lijf, niet afgedekt: de oude terug
        ua[gat] = fa[gat]
        Image.fromarray(ua.astype(np.uint8)).save(os.path.join(uit, f'idle_{i:02d}.png'), optimize=True)
    print(o.uit, len(d['lijnen']))


if __name__ == '__main__':
    main()
