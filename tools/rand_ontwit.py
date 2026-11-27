#!/usr/bin/env python3
"""Haalt de witte rand weg om decor dat van een witte achtergrond is geknipt.

Bij het wegknippen van het wit blijven de randpixels half doorzichtig maar licht: in hun kleur zit nog
wit van de achtergrond. Op het spel (een donkere savanne, een lucht) geeft dat een lelijke lichte franje
om de hut. Dit script kleurt elke pixel in de buitenste RAND px van de figuur opnieuw met de kleur van
de dichtstbijzijnde pixel verder naar binnen, maar alleen als die randpixel lichter is (een donkere
contour blijft staan). Ingesloten wit (de vork van een paal) gaat helemaal weg. De alfa blijft zoals hij is, alleen de bijna doorzichtige stofjes eromheen gaan weg.

    python3 tools/rand_ontwit.py                       de hutten en putten van het savannedorp
    python3 tools/rand_ontwit.py pad/naar/plaat.png    alleen deze
    python3 tools/rand_ontwit.py --meet ...            alleen tellen, niets schrijven
"""
import sys, glob
import numpy as np
from PIL import Image

RAND = 4        # zoveel px vanaf de buitenkant telt als rand
LICHTER = 6     # zoveel lichter dan binnen en hij krijgt de kleur van binnen
STOF = 24       # pixels met minder alfa dan dit zijn witte stofjes: weg

STANDAARD = sorted(glob.glob('design/savanne/hutten/*.png') + glob.glob('design/savanne/putten/*.png'))


def schuif(a, dy, dx):
    """a verschoven, de nieuwe randen leeg."""
    b = np.zeros_like(a)
    h, w = a.shape[:2]
    b[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = a[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return b


def ontwit(pad, meet=False):
    im = np.array(Image.open(pad).convert('RGBA')).astype(np.int32)
    rgb, al = im[..., :3], im[..., 3]
    al = np.where(al < STOF, 0, al)
    # ingesloten wit (de vork van een paal, een gat tussen takken): het knippen kwam er niet bij, het gaat alsnog weg
    wit = (rgb.min(-1) > 228) & (rgb.max(-1) - rgb.min(-1) < 14) & (al > 0)
    for _ in range(1):
        wit = wit | ((schuif(wit, 1, 0) | schuif(wit, -1, 0) | schuif(wit, 0, 1) | schuif(wit, 0, -1)) & (rgb.min(-1) > 190))
    al = np.where(wit, 0, al)
    # binnen: dicht, en RAND keer ingekrompen
    binnen = al >= 250
    for _ in range(RAND):
        b = binnen.copy()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            b &= schuif(binnen, dy, dx)
        binnen = b
    # de kleur van binnen naar buiten laten uitlopen
    kleur = np.where(binnen[..., None], rgb, 0)
    heb = binnen.copy()
    for _ in range(RAND + 3):
        som = np.zeros_like(kleur); n = np.zeros(al.shape, np.int32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            hb = schuif(heb, dy, dx)
            som += np.where(hb[..., None], schuif(kleur, dy, dx), 0); n += hb
        nieuw = (~heb) & (n > 0)
        kleur = np.where(nieuw[..., None], som // np.maximum(n, 1)[..., None], kleur)
        heb = heb | nieuw
    rand = (al > 0) & ~binnen & heb
    lum = rgb.sum(-1) / 3
    lumB = kleur.sum(-1) / 3
    fout = rand & (lum > lumB + LICHTER)
    print(f'{pad}: {int(fout.sum())} lichte randpixels van {int(rand.sum())}')
    if meet:
        return
    rgb = np.where(fout[..., None], kleur, rgb)
    uit = np.dstack([rgb, al]).clip(0, 255).astype(np.uint8)
    Image.fromarray(uit, 'RGBA').save(pad, optimize=True)


if __name__ == '__main__':
    arg = [a for a in sys.argv[1:] if not a.startswith('--')]
    for p in (arg or STANDAARD):
        ontwit(p, meet='--meet' in sys.argv)
