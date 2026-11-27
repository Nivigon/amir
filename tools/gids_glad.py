#!/usr/bin/env python3
"""De gids van The First Hunt glad laten bewegen: draai dit na tools/gids_bouw.py (en na een nieuwe opname van het spoor).

Wat het in design/tutorial/gids/gids.json rechtzet (meting 27-11-2026, zie notities/tutorial.md, "De gids beweegt glad"):

1. Het anker (gx) van elk frame. gids_bouw.py zette het op het midden van het hele plaatje, met de speer en de wapperende
   sjaal erbij. Daardoor stond zijn hoofd in de idle 27 eenheden van het anker, in de ren 0 en in het sluipen -45: bij elke
   wissel van animatie sprong hij opzij, en binnen de renlus schoof zijn hoofd 23 eenheden heen en weer. Nu is gx het
   zwaartepunt van zijn silhouet (alfa-gewogen, zonder de speer als gids_bouw.py dat meegeeft: 'zw'), dat glad meebeweegt; gy blijft de onderkant (zijn voeten).
2. De sprong in de lucht. Het spoor koppelde de clip aan Amirs sprong: tien beelden dezelfde stijgende houding, dan in vier
   beelden frame 26 tot 62 (negen keer te snel), dan de landing. Nu loopt elk luchtstuk (sprong en groot) gelijkmatig
   van zijn eerste naar zijn laatste frame; afzet en landing op de grond blijven zoals ze waren.

De renlus (12 echte houdingen, elk twee keer in het vel) loopt in het spel op afgelegde afstand (gidsRenFrame), niet hier.
"""
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIDS = os.path.join(ROOT, 'design/tutorial/gids/gids.json')
SPOOR = os.path.join(ROOT, 'design/tutorial/mentor_spoor.json')
LUCHT = ('sprong', 'groot')


def ankers(g):
    for naam, a in g['anims'].items():
        vel = np.array(Image.open(os.path.join(ROOT, a['src'])).convert('RGBA'))[:, :, 3].astype(float)
        voor = []
        zw = a.pop('zw', None)   # het zwaartepunt zonder speer uit gids_bouw.py (28-11-2026: de dikkere Mkuki-speer trok het anker mee)
        for k, f in enumerate(a['f']):
            fx, fy, fw, fh, gx, gy = f
            al = vel[fy:fy + fh, fx:fx + fw]
            som = al.sum()
            mx = (al.sum(axis=0) * np.arange(al.shape[1])).sum() / som if som else gx
            if zw:
                mx = zw[k]
            voor.append(round(gx - mx, 1))
            f[4] = round(float(mx), 1)
        print(f'{naam:9s} anker verschoven {min(voor):6.1f} .. {max(voor):6.1f} px')


def lucht(g, sp):
    n = 0
    for s, rij in enumerate(g['spoor']['segs']):
        if s == 0 or not rij:
            continue
        beelden = sp['segs'][s - 1]['f']
        i = 0
        while i < len(rij):
            an = rij[i][0]
            if an in LUCHT and i < len(beelden) and not beelden[i][8]:
                j = i
                while j + 1 < len(rij) and j + 1 < len(beelden) and rij[j + 1][0] == an and not beelden[j + 1][8]:
                    j += 1
                a0, a1 = rij[i][1], rij[j][1]
                if j > i and a1 > a0:
                    for k in range(i, j + 1):
                        rij[k] = [an, int(round(a0 + (a1 - a0) * (k - i) / (j - i)))]
                    n += 1
                i = j + 1
            else:
                i += 1
    print(f'luchtstukken gelijkmatig gemaakt: {n}')


def main():
    g = json.load(open(GIDS))
    sp = json.load(open(SPOOR))
    ankers(g)
    lucht(g, sp)
    json.dump(g, open(GIDS, 'w'), separators=(',', ':'))
    print('geschreven:', os.path.relpath(GIDS, ROOT))


if __name__ == '__main__':
    sys.exit(main())
