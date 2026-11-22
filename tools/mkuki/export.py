"""Exporteer afgewerkte frames naar de repo, met zonekaart, vuistlaag, speerplaatsing en een rapport per set.

python3 export.py setnaam fps pad1 pad2 ...   (paden van de originele frames, relatief aan de repo)

Schrijft per frame in karakters/amir/mkuki/<pad onder karakters/amir/>:
  naam.png            Mkuki in eigen kleuren, het lijf zonder speer (spelbeeld)
  naam_zones.png      zonekaart (vaste indexkleuren, zie kleur.py)
  naam_vuist.png      de vuist als bovenste laag (alleen bij frames met speer en een hand)
  naam_vuist_zones.png
en werkt karakters/amir/mkuki/plaatsing.json bij. Rapport: rapport/<set>_plaat.png en rapport/<set>.gif.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, kleur, raster
from speer_meet import override, meet, meet_pad
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MK = os.path.join(REPO, 'karakters/amir/mkuki')
KLAAR = '/home/claude/werk/klaar/'


def laad_klaar(pad):
    f = KLAAR + pad.replace('/', '__') + '.npz'
    if not os.path.exists(f):
        return None
    d = np.load(f)
    return d['lijf'], d['vuist']


def speerlaag(o, info):
    import afwerk
    sp = o.copy()
    weg = ~info['masker'] | afwerk._broek_oud(o) | afwerk._vacht(o)
    sp[weg, 3] = 0
    return sp


def main():
    setnaam, fps = sys.argv[1], float(sys.argv[2])
    paden = sys.argv[3:]
    ov = {}
    pf = os.path.join(MK, 'plaatsing.json')
    pl = json.load(open(pf)) if os.path.exists(pf) else {'uitleg': 'Speer per frame, gemeten in het originele frame (canvas-px). tip = punt, kont = achterkant, hoek in graden (punt naar kont, 0 = naar rechts, tegen de klok in), handen = midden van elke vuist om de schacht, achter = speer achter het lijf. Tekenvolgorde: lijf, speer, vuist.', 'frames': {}}
    origs, mks = [], []
    for p in paden:
        k = laad_klaar(p)
        rel0 = p.split('karakters/amir/', 1)[1]
        al = os.path.join(MK, rel0)
        if k is None and os.path.exists(al) and ('_ns' in os.path.basename(p) or setnaam.find('_ns') >= 0):
            # Werkdata uit een eerdere chat is weg, het frame zelf staat al in de repo: dat beeld gebruiken
            # (alleen voor het rapport; zonder speer is er geen vuist of plaatsing om bij te werken).
            print('BESTAAND', p)
            origs.append(Image.fromarray(raster.laad(os.path.join(REPO, p)))); mks.append(Image.open(al).convert('RGBA'))
            continue
        if k is None and os.path.exists(al):
            # Frame staat al in de repo en is in deze chat niet opnieuw gemaakt: bestaand beeld (met speer en
            # vuistlaag) alleen voor het rapport gebruiken; plaatsing.json blijft voor dit frame ongemoeid.
            print('BESTAAND', p)
            o = raster.laad(os.path.join(REPO, p))
            comp = Image.open(al).convert('RGBA')
            hs = '_ns' not in os.path.basename(p) and setnaam.find('_ns') < 0
            if hs and not (override(os.path.join(REPO, p)) or {}).get('geen'):
                info = meet_pad(os.path.join(REPO, p), o)
                comp.alpha_composite(Image.fromarray(speerlaag(o, info)))
                vf = al[:-4] + '_vuist.png'
                if os.path.exists(vf):
                    comp.alpha_composite(Image.open(vf).convert('RGBA'))
            origs.append(Image.fromarray(o)); mks.append(comp)
            continue
        if k is None:
            print('ONTBREEKT', p); continue
        lijf, vuist = k
        o = raster.laad(os.path.join(REPO, p))
        z = kleur.zones(lijf); vz = kleur.zones(vuist) if vuist[..., 3].any() else None
        mk = kleur.kleur(lijf, z, kleur.MKUKI)
        rel = p.split('karakters/amir/', 1)[1]
        uit = os.path.join(MK, rel)
        os.makedirs(os.path.dirname(uit), exist_ok=True)
        b = uit[:-4]
        Image.fromarray(mk).save(uit)
        Image.fromarray(kleur.kaart_png(z, lijf[..., 3] > 40)).save(b + '_zones.png')
        heeft_speer = '_ns' not in os.path.basename(p) and setnaam.find('_ns') < 0
        if heeft_speer and (override(os.path.join(REPO, p)) or {}).get('geen'):
            heeft_speer = False  # frame zonder speer in een speerset (na de worp)
        info = meet_pad(os.path.join(REPO, p), o) if heeft_speer else None
        comp = Image.fromarray(mk)
        if info is not None:
            vk = kleur.kleur(vuist, vz, kleur.MKUKI) if vz is not None else vuist
            if vuist[..., 3].any():
                Image.fromarray(vk).save(b + '_vuist.png')
                Image.fromarray(kleur.kaart_png(vz, vuist[..., 3] > 40)).save(b + '_vuist_zones.png')
            pl['frames'][rel] = {k2: info[k2] for k2 in ('tip', 'kont', 'hoek', 'lengte', 'handen')}
            pl['frames'][rel]['achter'] = False
            comp.alpha_composite(Image.fromarray(speerlaag(o, info)))
            comp.alpha_composite(Image.fromarray(vk))
        origs.append(Image.fromarray(o)); mks.append(comp)
    json.dump(pl, open(pf, 'w'), indent=1)
    rapport(setnaam, fps, origs, mks)


def rapport(setnaam, fps, origs, mks):
    rd = os.path.join(MK, 'rapport'); os.makedirs(rd, exist_ok=True)
    m = np.zeros(np.asarray(origs[0]).shape[:2], bool)
    for im in origs + mks:
        m |= np.asarray(im)[..., 3] > 20
    ys, xs = np.where(m)
    x0, y0, x1, y1 = max(0, xs.min() - 6), max(0, ys.min() - 6), xs.max() + 7, ys.max() + 7
    w, h = x1 - x0, y1 - y0
    bg = (214, 196, 160, 255)
    # GIF: origineel links, Mkuki rechts
    beelden = []
    for o, k in zip(origs, mks):
        f = Image.new('RGBA', (2 * w + 10, h), bg)
        f.alpha_composite(o.crop((x0, y0, x1, y1)), (0, 0)); f.alpha_composite(k.crop((x0, y0, x1, y1)), (w + 10, 0))
        beelden.append(f.convert('RGB'))
    beelden[0].save(os.path.join(rd, setnaam + '.gif'), save_all=True, append_images=beelden[1:],
                    duration=int(1000 / fps), loop=0)
    # overzichtsplaat: per frame boven origineel, onder Mkuki
    n = len(mks); kol = min(n, 12); rij = (n + kol - 1) // kol
    P = Image.new('RGBA', (kol * w, rij * (2 * h + 8)), bg)
    for i, (o, k) in enumerate(zip(origs, mks)):
        cx, cy = (i % kol) * w, (i // kol) * (2 * h + 8)
        P.alpha_composite(o.crop((x0, y0, x1, y1)), (cx, cy)); P.alpha_composite(k.crop((x0, y0, x1, y1)), (cx, cy + h))
    P.convert('RGB').save(os.path.join(rd, setnaam + '_plaat.png'))
    print('rapport', setnaam, n, 'frames')


if __name__ == '__main__':
    main()
