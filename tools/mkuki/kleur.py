"""Zones uit de hulpkleuren, de zonekaart en omkleuren.

Zones (index, hulpkleur van Grok, kleur in de zonekaart):
  1 broek      blauw  #2050FF   kaart #0000FF
  2 schort     geel   #FFE000   kaart #FFFF00
  3 riem       rood   #E01010   kaart #FF0000
  4 band       groen  #00B050   kaart #00FF00   (schuine band met ring)
  5 kralen     cyaan  #00E0E0   kaart #00FFFF
  6 armbanden  oranje #FF7A00   kaart #FF8000   (boven- en polsbanden)

omkleuren: nieuwe kleur = doelkleur * (V / Vref) per pixel, zodat licht en schaduw blijven. Vref is vast per zone
(gemeten in de proef op de hulpkleuren), dus geen geflikker tussen frames.
"""
import numpy as np
from scipy import ndimage as nd

ZONES = ['broek', 'schort', 'riem', 'band', 'kralen', 'armbanden']
KAART = {1: (0, 0, 255), 2: (255, 255, 0), 3: (255, 0, 0), 4: (0, 255, 0), 5: (0, 255, 255), 6: (255, 128, 0)}
# Vref per zone op de hulpkleuren (mediaan V in de proef)
VREF = {1: 0.65, 2: 0.95, 3: 0.63, 4: 0.37, 5: 0.66, 6: 0.86}
MKUKI = {1: (60, 56, 57), 2: (185, 140, 98), 3: (88, 52, 34), 4: (78, 48, 34), 5: (138, 36, 32), 6: (200, 132, 92)}
VARIANT_A = {1: (38, 52, 88), 2: (226, 214, 190), 3: (40, 36, 34), 4: (44, 40, 38), 5: (226, 186, 60), 6: (190, 190, 200)}  # indigo en wit, zilver
VARIANT_B = {1: (92, 40, 34), 2: (58, 92, 60), 3: (150, 110, 40), 4: (60, 40, 28), 5: (40, 120, 150), 6: (214, 170, 60)}   # oker-rood en groen, goud


def hsv(rgb):
    r, g, b = [rgb[..., i].astype(float) / 255 for i in range(3)]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    return h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx


def zones(rgba):
    """Index-kaart (0 = geen zone) uit een frame in hulpkleuren."""
    H, S, V = hsv(rgba[..., :3])
    al = rgba[..., 3] > 40
    z = np.zeros(H.shape, np.uint8)
    kern = al & (S > 0.5) & (V > 0.38)
    z[kern & (H >= 200) & (H < 250)] = 1
    z[kern & (H >= 37) & (H < 70) & (V > 0.5)] = 2
    z[kern & ((H >= 340) | (H < 12)) & (V > 0.45)] = 3
    z[al & (S > 0.45) & (V > 0.2) & (H >= 85) & (H < 160)] = 4
    z[kern & (H >= 165) & (H < 200)] = 5
    z[kern & (H >= 18) & (H < 37) & (V > 0.62) & (S > 0.62)] = 6
    # kleine spikkels weg
    for k in range(1, 7):
        m = z == k
        lab, n = nd.label(m)
        if n:
            sz = nd.sum(m, lab, range(1, n + 1))
            for i, v in enumerate(sz):
                if v < 6:
                    z[lab == i + 1] = 0
    # kralen die Grok blauwer tekent dan cyaan: blauw boven de riem is geen broek maar ketting
    if (z == 3).any() and (z == 1).any():
        riem_top = np.percentile(np.where(z == 3)[0], 10)
        lab, n = nd.label(z == 1)
        for i in range(1, n + 1):
            m = lab == i
            if np.where(m)[0].mean() < riem_top - 4:
                z[m] = 5
    # oranje vlekjes binnen de schort zijn schaduw van de schort
    lab, n = nd.label(z == 6)
    for i in range(1, n + 1):
        m = lab == i
        ring = nd.binary_dilation(m, iterations=2) & ~m
        if ring.any() and (z[ring] == 2).mean() > 0.5:
            z[m] = 2
    # donkere schaduw- en randpixels met dezelfde tint bij de zone trekken (binnen 2 px van de kern)
    zacht = al & (S > 0.25) & (V > 0.10) & (z == 0)
    for k, (lo, hi) in {1: (190, 265), 2: (34, 75), 3: (335, 372), 4: (80, 165), 5: (160, 205), 6: (16, 37)}.items():
        hh = np.where(H < 20, H + 360, H) if k == 3 else H
        bij = nd.binary_dilation(z == k, iterations=4 if k == 1 else 2)
        extra = zacht & bij & (hh >= lo) & (hh < hi)
        if k == 6:
            extra &= V > 0.45  # niet de huid
        z[extra] = k
    return z


def kaart_png(z, al):
    out = np.zeros(z.shape + (4,), np.uint8)
    for k, c in KAART.items():
        m = z == k
        out[m, :3] = c; out[m, 3] = 255
    return out


def kleur(rgba, z, pal, vref=None, bron_v=None):
    """Omkleuren. bron_v: de V waarmee gemeten wordt (standaard die van rgba); vref per zone."""
    vref = vref or VREF
    _, _, V = hsv(rgba[..., :3])
    if bron_v is not None:
        V = bron_v
    out = rgba.copy().astype(float)
    for k, c in pal.items():
        m = z == k
        if not m.any():
            continue
        f = np.clip(V[m] / vref[k], 0.15, 1.45)[:, None]
        out[..., :3][m] = np.clip(np.array(c, float) * f, 0, 255)
    return out.astype(np.uint8)


def vref_van(rgba, z):
    """Mediaan V per zone in een frame dat al in eigen kleuren staat (om een Mkuki-frame opnieuw te kleuren)."""
    _, _, V = hsv(rgba[..., :3])
    return {k: float(np.median(V[z == k])) if (z == k).any() else 1.0 for k in range(1, 7)}
