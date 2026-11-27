"""Kleuren van de gids van The First Hunt (28-11-2026): Tom koos 'Indigo Sage' uit vijf voorstellen.
Teal jas -> indigo, roestrode sjaal en sjerp -> saffraan, broek -> donker indigo; zandrand, huid, koper en
speer blijven.
  python3 tools/gids_kleur.py      kleurt de vellen in design/tutorial/gids/ en klein/design/tutorial/gids/ om
gids_bouw.py roept kleur() ook aan bij het opslaan, zodat een nieuwe bouw de kleur houdt. Draai dit script dus alleen
op vellen die nog teal zijn (op een al omgekleurd vel doet het niets meer: geen teal of roestrood over).

Hoe: per pixel in HSV. Teal = tint 180-215 graden, verzadiging > 0,35. Roestrood = tint < 14 of > 345 met verzadiging > 0,72, of tint < 17 met verzadiging > 0,8
(lichte rafels); huidschaduw (tot 0,65) en koper (0,67) blijven eronder.
De rode streep op het gezicht en de kraaltjes hebben dezelfde kleur als de sjaal; die blijven rood doordat kleine losse
vlekjes (kleiner dan KLEIN_VLEK pixels, geschaald met het vel) niet meedoen, behalve snippers die tegen de sjaal
aan liggen (franjes). Helderheid volgt het origineel, zodat
schaduw en licht blijven staan."""
import os, sys, colorsys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

KLEUREN = {   # (doel, referentie in het origineel: tint, verzadiging, helderheid)
    'jas':   ('#1f2a5c', (198, 0.74, 0.30)),
    'sjaal': ('#d99a1e', (9, 0.80, 0.58)),
}
KLEIN_VLEK = 120   # pixels op het grote vel; gezichtsstreep en kralen zijn kleiner


def _hsv(hexkl):
    r, g, b = (int(hexkl[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s, v


def kleur(im, schaal=1.0):
    """im: PIL-beeld (RGBA); schaal: 1 voor het grote vel, 0,5 voor klein/. Geeft een nieuw RGBA-beeld."""
    a = np.asarray(im.convert('RGBA')).astype(np.float64) / 255
    hsv = rgb_to_hsv(a[..., :3]); H = hsv[..., 0] * 360; S = hsv[..., 1]; V = hsv[..., 2]
    zicht = a[..., 3] > 0
    # jas en broek samen: in een paar clips (groot, ren) is de broek net zo teal als de jas, dus kleur kan ze niet scheiden.
    # Ze schuiven als één familie naar indigo; de tint-afstand wordt kleiner (x0,3), de broek blijft donkerder.
    jas = zicht & (H > 180) & (H < 265) & (S > 0.2) & (V > 0.06)
    kern = zicht & (((H < 14) | (H > 345)) & (S > 0.72) | (H < 17) & (S > 0.8)) & (V > 0.15)   # huidschaduw tot ca. 0,65, koper 0,67
    # in sommige clips (sprong) is de sjaal in de schaduw oranjebruin (tint tot 24); die doet mee als hij vastzit aan een
    # flink stuk echte sjaal, losse oranje plekjes (koper) niet
    ruim = kern | (zicht & ((H < 25) | (H > 345)) & (S > 0.68) & (V > 0.12))
    lab, n = ndi.label(ruim, structure=np.ones((3, 3)))
    roest = np.zeros_like(kern)
    if n:
        idx = range(1, n + 1)
        maat = np.asarray(ndi.sum(ruim, lab, idx)); kernmaat = np.asarray(ndi.sum(kern, lab, idx))
        groot = np.zeros(n + 1, bool); groot[1:] = kernmaat >= KLEIN_VLEK * schaal * schaal
        sjaal = groot[lab]
        # losse snippers van de sjaal (franjes, rafels, door een lijntje afgesneden) liggen er vlak tegenaan en gaan mee;
        # de gezichtsstreep (ca. 60 px) en verdwaalde pixels op huid en koper liggen verder weg of zijn groter
        afst = ndi.distance_transform_edt(~sjaal)
        dichtst = np.asarray(ndi.minimum(afst, lab, idx))
        licht = np.asarray(ndi.mean(V, lab, idx))                   # schaduw op de huid is donkerder dan de stof
        mee = groot.copy(); mee[1:] |= (kernmaat > 0) & (maat < 40 * schaal * schaal) & (dichtst <= 6 * schaal + 0.5) & (licht > 0.35)
        roest = mee[lab]
    uit = hsv.copy()
    for m, (doel, (rh, rs, rv)) in [(jas, KLEUREN['jas']), (roest, KLEUREN['sjaal'])]:
        th, ts, tv = _hsv(doel)
        rel = np.clip(V[m] / rv, 0, 3)
        dh = (H[m] - rh + 180) % 360 - 180
        uit[..., 0][m] = ((th + dh * 0.3) % 360) / 360
        uit[..., 1][m] = np.clip(S[m] * ts / rs, 0, 1)
        uit[..., 2][m] = np.clip(np.where(rel <= 1, tv * rel, tv + (1 - tv) * (1 - np.exp(-(rel - 1) * 1.2))), 0, 1)
    rgb = hsv_to_rgb(uit)
    return Image.fromarray((np.dstack([rgb, a[..., 3:]]) * 255 + 0.5).astype(np.uint8))


if __name__ == '__main__':
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for map_, schaal in [('design/tutorial/gids', 1.0), ('klein/design/tutorial/gids', 0.5)]:
        for f in sorted(os.listdir(os.path.join(ROOT, map_))):
            if f.endswith('.png'):
                p = os.path.join(ROOT, map_, f)
                kleur(Image.open(p), schaal).quantize(256, method=Image.Quantize.FASTOCTREE,
                                                     dither=Image.Dither.NONE).save(p, optimize=True)
                print(p)
