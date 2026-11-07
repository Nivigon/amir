#!/usr/bin/env python3
"""Maakt de nieuwe huistypes voor de stad (D1, gevelvarianten) uit de Grok-platen in design/stad/bron/.

Bron (1296x1536, witte achtergrond):
  gevel_relief_grok.jpg    het reliefhuis: lichte kalk met rode en blauwe versiering (Hausa)
  gevel_koopman_grok.jpg   het koopmanshuis: rozerode leem met een houten erker
  gevel_pilaren_grok.jpg   het pilarenhuis: staande pilaren met punten erop (Djenne)

Uit: design/stad/gevel_<soort>.png, op de maat van gevel.png, zodat alles wat aan een gevel hangt
(het dak, de verdiepingen, de deur, de kartels, de galerijen) gewoon doorwerkt:
  - 970 breed, de muur van x 44 tot 922, het midden van het deurgat op x 473;
  - van boven naar onder vier banden: het dak (zo hoog als de plaat het geeft), dan de bovenste
    verdieping (alt, 417), de gewone verdieping (ver, 417) en de begane grond (bod, 508);
  - de looplijn van het dak (dakAchter) ligt 52 bronpx boven de onderkant van het dak, net als bij gevel.png.
De plaat is breder dan de oude gevel: een strook kale muur gaat eruit (een smalle links van de deur,
zodat het deurgat op zijn plek valt, en een brede rechts), met een zachte overgang over de naad.

Het script print de maten voor STAD.gevelSoort en zet ze in design/stad/metadata.json.

    python3 tools/gevel_soorten.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
Vereist Pillow, numpy en scipy.
"""
import json, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAD = os.path.join(ROOT, 'design', 'stad')
BRON = os.path.join(STAD, 'bron')

W_UIT, MUUR, MIDDEN = 970, (44, 922), 473
VER_H, BOD_H, DAK_ONDER = 417, 508, 52   # de maten van gevel.png: ver 580-997, bod 997-1505, dak 177 - dakAchter 125
NAAD = 28                                 # zo breed loopt de overgang over een geknipte naad

# per soort, in bronpx van de Grok-plaat (nagemeten op een raster):
#   muur   de linker- en rechterrand van de muur (zonder de balkkoppen die uitsteken)
#   deur   het donkere deurgat: x0, x1 (het midden komt op MIDDEN)
#   dak    de onderkant van het dak: net onder de bovenste balkenrij (of de stompjes ervan)
#   alt    de bovenste verdieping, ver de gewone, bod de begane grond (elk tot net onder een balkenrij)
#   knipL  waar links de smalle strook uit gaat (in kale muur), knipR waar de brede rechts begint
SOORTEN = {
    'relief':  dict(muur=(50, 1247), deur=(398, 605), dak=235, alt=(235, 615), ver=(615, 1012), bod=(1012, 1512),
                    knipL=128, knipR=700),
    'koopman': dict(muur=(53, 1247), deur=(413, 598), dak=190, alt=(190, 595), ver=(595, 1005), bod=(1005, 1503),
                    knipL=140, knipR=700),
    'pilaren': dict(muur=(45, 1255), deur=(400, 612), dak=210, alt=(210, 655), ver=(655, 1058), bod=(1058, 1534),
                    knipL=222, knipR=690),
}


def wit_weg(rgb):
    """Het witte vlak rond de gevel doorzichtig: flood-fill vanaf de rand op bijna zuiver wit."""
    a = rgb.astype(int)
    wit = (a.min(2) > 238) & ((a.max(2) - a.min(2)) < 18)
    lab, _ = nd.label(wit)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    weg = np.isin(lab, list(rand))
    weg = nd.binary_dilation(weg, iterations=1)          # de lichte jpg-rand mee
    alpha = np.where(weg, 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8)))
    return np.dstack([rgb, alpha])


def knip(a, x0, x1):
    """Haal kolommen x0..x1 weg, met een zachte overgang van NAAD breed over de naad."""
    h = NAAD // 2
    links, rechts = a[:, :x0 + h].astype(float), a[:, x1 - h:].astype(float)
    t = np.linspace(0, 1, NAAD)[None, :, None]
    mid = links[:, -NAAD:] * (1 - t) + rechts[:, :NAAD] * t
    return np.concatenate([links[:, :-NAAD], mid, rechts[:, NAAD:]], axis=1)


def band(a, y0, y1, h):
    stuk = Image.fromarray(a[y0:y1].round().clip(0, 255).astype(np.uint8), 'RGBA')
    return np.asarray(stuk.resize((stuk.width, h), Image.LANCZOS)).astype(float)


def maak(naam, S):
    rgb = np.asarray(Image.open(os.path.join(BRON, f'gevel_{naam}_grok.jpg')).convert('RGB'))
    a = wit_weg(rgb).astype(float)
    m0, m1 = S['muur']
    mid = (S['deur'][0] + S['deur'][1]) / 2
    remL = round((mid - m0) - (MIDDEN - MUUR[0]))       # zo komt het midden van de deur op MIDDEN
    remR = round((m1 - m0 - remL) - (MUUR[1] - MUUR[0]))  # en de muur op zijn breedte
    assert remL >= 0 and remR >= 0, (naam, remL, remR)
    a = knip(a, S['knipR'], S['knipR'] + remR)
    a = knip(a, S['knipL'], S['knipL'] + remL)
    # links bijsnijden of aanvullen zodat de muur op x 44 begint, dan op 970 breed
    dx = m0 - MUUR[0]
    a = a[:, dx:] if dx >= 0 else np.concatenate([np.zeros((a.shape[0], -dx, 4)), a], axis=1)
    if a.shape[1] < W_UIT: a = np.concatenate([a, np.zeros((a.shape[0], W_UIT - a.shape[1], 4))], axis=1)
    a = a[:, :W_UIT]
    # de banden op hun maat
    dak = a[:S['dak']]
    delen = [dak, band(a, *S['alt'], VER_H), band(a, *S['ver'], VER_H), band(a, *S['bod'], BOD_H)]
    uit = np.concatenate(delen, axis=0).round().clip(0, 255).astype(np.uint8)
    Image.fromarray(uit, 'RGBA').save(os.path.join(STAD, f'gevel_{naam}.png'), optimize=True)
    D = S['dak']
    deurW = (S['deur'][1] - S['deur'][0]) / 214         # het deurgat ten opzichte van dat van gevel.png
    return {'src': f'gevel_{naam}.png', 'h': uit.shape[0], 'dak': [0, D], 'alt': [D, D + VER_H],
            'ver': [D + VER_H, D + 2 * VER_H], 'bod': [D + 2 * VER_H, D + 2 * VER_H + BOD_H],
            'dakAchter': D - DAK_ONDER, 'deur': round(deurW, 3)}


def main():
    maten = {naam: maak(naam, S) for naam, S in SOORTEN.items()}
    pad = os.path.join(STAD, 'metadata.json')
    meta = json.load(open(pad))
    meta['gevel_soorten'] = maten
    json.dump(meta, open(pad, 'w'), indent=1, ensure_ascii=False)
    for naam, m in maten.items():
        print(f"  {naam}: {{ src: '{m['src']}', dak: {m['dak']}, alt: {m['alt']}, ver: {m['ver']}, bod: {m['bod']}, "
              f"dakAchter: {m['dakAchter']}, deur: {m['deur']} }},")


if __name__ == '__main__':
    main()
