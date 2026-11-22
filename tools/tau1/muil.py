"""Proef: de leeuwenmuil beter leesbaar op spelgrootte. Kapopening donkerder, tanden groter en lichter, ogen feller,
krassen dikker en lichter. Werkt op het spelbeeld en de zonekaart van tau.maak.

muil(beeld, zones) -> nieuw beeld (RGBA). Zones: 1 vacht/kap, 4 tanden, 5 ogen.
"""
import numpy as np
from scipy import ndimage as nd

TAND = np.array([250, 244, 228], float)
OOG_KERN = np.array([255, 236, 150], float)
OOG = np.array([255, 170, 40], float)


def muil(b, z, oog_groei=1, gloed=5, donker=0.3):
    b = b.astype(float).copy()
    al = b[..., 3] > 40
    tand = z == 4
    oog = (z == 5) & nd.binary_dilation(tand, iterations=14)   # alleen ogen in de kap (niet de okeren grip)
    if not tand.any() and not oog.any():
        return b.astype(np.uint8)
    # de opening: alles binnen de tandenrij en de ogen, wat niet vacht of tand is (gezicht in de schaduw)
    kern = nd.binary_dilation(tand | oog, iterations=10)
    rgb = b[..., :3]; V = rgb.max(-1) / 255
    opening = kern & al & (z != 1) & (z != 4) & (z != 5) & (V < 0.55)
    # alleen het stuk aan de binnenkant van de kap (dichtbij de ogen of tussen de tanden)
    opening &= nd.binary_dilation(oog | tand, iterations=7)
    b[opening, :3] *= donker
    # tanden: iets groter, bijna wit, met een donkere rand eromheen
    # tanden: de vorm houden, alleen helder maken (de schaduw in de tand blijft licht zichtbaar)
    t2 = tand & al
    Vt = (b[..., :3].max(-1) / 255)[t2]
    b[t2, :3] = TAND[None] * np.clip(0.82 + 0.25 * Vt, 0, 1)[:, None]
    # ogen: groter, felle kern, oranje rand en een zachte gloed op wat er al staat
    o2 = nd.binary_dilation(oog, iterations=oog_groei) & al
    b[o2, :3] = OOG
    b[oog, :3] = OOG_KERN
    if gloed:
        d = nd.distance_transform_edt(~o2)
        g = np.clip(1 - d / gloed, 0, 1) * 0.55 * al * ~o2 * ~t2
        b[..., :3] = b[..., :3] * (1 - g[..., None]) + OOG[None, None] * g[..., None]
    return np.clip(b, 0, 255).astype(np.uint8)
