#!/usr/bin/env python3
"""Maakt de bodem en het sneeuwdek voor een grond die onderweg ondersneeuwt.

    python3 tools/sneeuwdek.py            # alles
    python3 tools/sneeuwdek.py rots       # of: dek

Nodig: pillow en numpy (pip install pillow numpy).

Het verschil met tools/winter_art.py: die bakt sneeuw en steen in één plaatje en
maakt de rots eronder grijs. Dat klopt hoog in de bergen, maar niet op de
savanne. Daar ligt de sneeuw op rode grond, en onder die sneeuw is de grond nog
altijd rood. Daarom staan hier twee dingen los van elkaar:

- de bodem: design/grondrand.png blijft zoals hij is (savanne), en
  design/grondrand_rots.png is diezelfde grond als grijze steen (rotsbodem).
- het dek: design/sneeuwlaag_25/50/75/100.png, vier doorzichtige lagen met
  alleen sneeuw erin. Die passen op allebei de bodems.

De vier lagen zijn genest: wat op 25 wit is, is dat op 50 ook. Daardoor kan het
spel onderweg van laag wisselen zonder dat er sneeuw verdwijnt; er komt alleen
wat bij. Alle ruis loopt in de breedte rond, dus de tegels blijven naadloos.
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sneeuw import blur, find_rim, load, shift_down, shift_up  # noqa: E402
from winter_art import noise_x_periodic  # noqa: E402

BRON = os.path.join(ROOT, 'design', 'grondrand.png')
STANDEN = (25, 50, 75, 100)
DEKKING = 0.93      # bij stand 100: zoveel van het loopvlak onder de sneeuw. De rest
                    # piept er doorheen, en juist dat laat zien dat er grond onder zit.
RIM_WIN = (140, 180)
SEED = 4


def bewaar(rgb, alpha, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    res = np.concatenate([np.clip(rgb, 0, 1), np.clip(alpha, 0, 1)[..., None]], -1)
    Image.fromarray((res * 255).round().astype(np.uint8), 'RGBA').save(dst, optimize=True)


def sneeuwmasker(t, rgb, alpha, lum, opaque, seed=SEED):
    """Waar ligt er sneeuw bij stand t (0 = niets, 1 = dicht)? Genest in t."""
    H, W = alpha.shape
    ys = np.arange(H)[:, None]
    rim = find_rim(lum, opaque, *RIM_WIN)
    rim = np.full(W, float(np.median(rim)))          # de rand ligt praktisch recht: houd hem recht, dan blijft hij naadloos
    top = np.where(opaque.any(0), opaque.argmax(0), H).astype(float)

    # drie maten ruis: velden, plekken en korrel. De korrel weegt mee zodat weinig
    # sneeuw eruitziet als losse plekken in de kuiltjes, niet als een half laken.
    field = (0.50 * noise_x_periodic((H, W), W // 8, seed)
             + 0.32 * noise_x_periodic((H, W), W // 26, seed + 1)
             + 0.18 * noise_x_periodic((H, W), W // 70, seed + 2))
    vlak = (ys >= top[None, :]) & (ys < rim[None, :]) & opaque
    deel = DEKKING * t ** 0.75
    if deel <= 0.001:
        return np.zeros((H, W), bool), rim
    drempel = np.percentile(field[vlak], 100 * (1 - deel))
    plane = vlak & (field > drempel)
    # vlak voor de breukrand altijd sneeuw, maar die band groeit pas laat mee
    band = 0.06 * H * max(0.0, (t - 0.45) / 0.55)
    if band > 0.5:
        plane |= (ys >= (rim - band)[None, :]) & (ys < rim[None, :]) & opaque
    # de sneeuwrand die over de breukrand hangt, alleen waar er ook sneeuw achter ligt
    n1 = noise_x_periodic((1, W), W // 25, seed + 3)[0]
    n2 = noise_x_periodic((1, W), W // 90, seed + 4)[0]
    fringe = 0.06 * min(1.0, t * 1.15)
    f = np.maximum(fringe * H * (0.6 + 0.8 * n1) + fringe * H * 0.5 * (n2 - 0.5), fringe * H * 0.35)
    rand = (ys >= rim[None, :]) & (ys < (rim + f)[None, :]) & opaque & (blur(plane.astype(float), 3.0) > 0.25)
    m = (blur((plane | rand).astype(float), 2.0) > 0.5) & opaque
    return m, rim


def sneeuwlaag(t, dst, seed=SEED):
    """Eén doorzichtige laag: alleen de sneeuw, plus de schaduwlijn eronder."""
    rgb, alpha, lum, opaque, dark = load(BRON)
    H, W = alpha.shape
    m, rim = sneeuwmasker(t, rgb, alpha, lum, opaque, seed)
    mf = m.astype(float)

    # de onderrand van elke sneeuwplek vangt schaduw: dat geeft de laag dikte
    s = max(4, int(H * 0.03))
    lower = np.zeros((H, W), bool)
    for k in range(1, s + 1):
        lower |= m & ~shift_up(m, k)
    shade = blur(lower.astype(float), s * 0.5) * mf
    relief = noise_x_periodic((H, W), W // 60, seed + 5)
    wit = np.array([0.97, 0.98, 1.0])
    schaduw = np.array([0.72, 0.80, 0.93])
    col = wit[None, None, :] * (0.92 + 0.08 * relief)[..., None]
    col = col * (1 - shade[..., None] * 0.6) + schaduw[None, None, :] * (shade[..., None] * 0.6)

    # een donkere lijn net onder de sneeuw. Half doorzichtig, want deze laag komt
    # op twee bodems te liggen: op rood hoort die lijn roodbruin te zakken, op
    # steen grijs, en dat regelt de doorzichtigheid vanzelf.
    lijn = np.zeros((H, W), bool)
    for k in range(1, 3):
        lijn |= shift_down(m, k) & ~m
    lijn &= opaque
    lijn_c = np.array([0.20, 0.22, 0.30])

    uit = np.where(lijn[..., None], lijn_c[None, None, :], col)
    a = np.where(m, alpha, np.where(lijn, 0.60 * alpha, 0.0))
    bewaar(uit, a, dst)


def rotsbodem(dst, donker=0.80):
    """Dezelfde grond als grijze steen: geen sneeuw, alleen een andere steensoort.

    Donkerder dan de wand in tools/winter_art.py, en met opzet. Daar zit de steen
    altijd onder een dicht sneeuwdek en is het een wand; hier loop je er zelf
    overheen, ook zonder sneeuw. Blijft het loopvlak lichtgrijs, dan valt witte
    sneeuw er niet tegen af en zie je de overgang niet.
    """
    rgb, alpha, lum, opaque, dark = load(BRON)
    grijs = 0.25 * rgb[..., 0] + 0.6 * rgb[..., 1] + 0.15 * rgb[..., 2]
    steen = np.stack([grijs * 0.98, grijs * 1.0, grijs * 1.06], -1) * 1.08 * donker
    bewaar(np.clip(steen, 0, 1), alpha, dst)


def doe_rots():
    dst = os.path.join(ROOT, 'design', 'grondrand_rots.png')
    rotsbodem(dst)
    print('bodem: design/grondrand_rots.png')


def doe_dek():
    for stand in STANDEN:
        dst = os.path.join(ROOT, 'design', 'sneeuwlaag_%d.png' % stand)
        sneeuwlaag(stand / 100, dst)
        print('dek:   design/sneeuwlaag_%d.png' % stand)


TAKEN = {'rots': doe_rots, 'dek': doe_dek}

if __name__ == '__main__':
    namen = sys.argv[1:] or list(TAKEN)
    for naam in namen:
        if naam not in TAKEN:
            sys.exit('onbekend: %s (kies uit: %s)' % (naam, ', '.join(TAKEN)))
        TAKEN[naam]()
