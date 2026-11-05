#!/usr/bin/env python3
"""Nyundo (Brutus) donker: een tweede kleurstelling van dezelfde frames.

Leest enemies/brutus/frames/*.png (met brutus.json voor het anker) en schrijft naar
enemies/brutus/frames_donker/ (zelfde namen en maat, dus brutus.json geldt voor allebei):
- de huid donkerder bruin (de oranjebruine tinten, ook de steel en de sandalen een tikje);
- het haar en de wenkbrauwen zwart (de rode stukken bovenaan en in het gezicht), en het litteken
  over zijn oog licht, zodat het tegen de donkere huid te zien blijft;
- de broek bruin in plaats van zwart, de sjerp goud;
- de windsels om de polsen warm goud, met glans (een verloop van donker naar bijna wit).
In het spel: `brutus: { ..., huid: 'donker' }`, of de knop Huid in de sandbox.
Draai het opnieuw na tools/brutus_voeten.py, daarna gen-klein.py en gen-offline-manifest.py.
"""
import json, os
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

ROOT = 'enemies/brutus/'
DOEL = ROOT + 'frames_donker/'

HUID = dict(helder=0.58, verz=1.08, tint=-0.012)     # wat er van de huid overblijft, voller, iets naar rood
HAAR = dict(verz=0.2, helder=0.28)                   # zwart haar
SJERP = dict(tint=44, verz=1.0, helder=1.35)         # gouden sjerp
BROEK = dict(tint=30, verz=0.45, helder=1.9)         # bruine broek
POLS = [(70, 40, 8), (190, 130, 25), (250, 205, 80), (255, 245, 190)]   # warm goud, donker naar licht


def hsv(a):
    rgb = a[..., :3]; mx = rgb.max(-1); mn = rgb.min(-1); d = mx - mn + 1e-6
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    return h, np.where(mx > 0, d / (mx + 1e-6), 0), mx


def rgb(h, s, v):
    i = np.floor(h * 6); f = h * 6 - i
    p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s); i = i.astype(int) % 6
    return np.stack([np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]),
                     np.choose(i, [p, p, t, v, v, q])], -1)


def stukken(m):
    """de samenhangende stukken van een masker, elk als lijst (y, x)"""
    lab = np.zeros(m.shape, bool); H, W = m.shape; uit = []
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]: continue
        q = deque([(y0, x0)]); lab[y0, x0] = True; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for yy in (y - 1, y, y + 1):
                for xx in (x - 1, x, x + 1):
                    if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = True; q.append((yy, xx))
        uit.append(np.array(pts))
    return uit


def vul(vorm, lijst):
    m = np.zeros(vorm, bool)
    for p in lijst: m[p[:, 0], p[:, 1]] = True
    return m


def vorm_ok(p, max_rek=3.0):
    """compact genoeg: niet lang en smal zoals de steel van de knots"""
    hh, ww = np.ptp(p[:, 0]) + 1, np.ptp(p[:, 1]) + 1
    return max(hh, ww) / min(hh, ww) <= max_rek


def rand_van(m, r=2):
    """de ring pixels net buiten een masker"""
    g = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))
    return (np.asarray(g) > 0) & ~m


def maskers(a, dx, dy):
    """haar, wenkbrauwen, litteken, sjerp, broek en polswindsels, uit het origineel.
    Op kleur en vorm, niet op hoogte, zodat het ook klopt als hij zwaait, valt of ligt."""
    h, s, v = hsv(a); hd = h * 360; H, W = v.shape; zicht = a[..., 3] > 0.5
    leeg = np.zeros((H, W), bool)
    # de broek: het grote, dichte donkere vlak (niet de dunne lijnen of plooien)
    broek = (s < 0.3) & (v < 0.33) & zicht
    dicht = np.asarray(Image.fromarray((broek * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(5))).astype(np.float32) / 255
    broek &= dicht > 0.55
    st = [p for p in stukken(broek) if len(p) >= 300]
    groot = max((len(p) for p in st), default=0)
    broek = vul((H, W), [p for p in st if len(p) >= 0.25 * groot])   # de pijpen, niet de schaduw op de bal van de knots
    # de sjerp is in de bron al op een eigen tint gezet (rond 358 graden). Soms heeft een hand die tint ook, dus:
    # de stukken met die tint die tegen de broek aan liggen (dat doet de sjerp in elke houding, ook liggend)
    sj = (hd > 352) & (hd < 359.6) & (s > 0.7) & zicht
    bijbroek = np.asarray(Image.fromarray((broek * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
    huid = (hd > 8) & (hd < 46) & (s > 0.3) & zicht
    sjerp = []
    for p in stukken(sj):
        if len(p) < 25:
            continue
        ring = rand_van(vul((H, W), [p]), 6)
        rb, rh = bijbroek[ring].mean(), huid[ring].mean()
        if rb > 0.1 and rh > 0.08 and rb < 0.85:    # broek aan de ene kant, huid aan de andere
            sjerp.append(p)
    sjerp = vul((H, W), sjerp)
    # het haar: fel verzadigd rood (de steel, een roze hand en de rode gloed op zijn gezicht zijn minder fel),
    # het grootste compacte stuk, plus de plukken die ertegenaan liggen
    fel = ((hd < 12) | (hd > 359.6)) & (s > 0.82) & (v > 0.18) & zicht & ~sjerp
    st = [p for p in stukken(fel) if len(p) >= 6]
    kand = [p for p in st if len(p) >= 80 and vorm_ok(p, 2.6)]
    haar = gz = lit = leeg
    if kand:
        p0 = max(kand, key=len)
        y0, y1, x0, x1 = p0[:, 0].min(), p0[:, 0].max(), p0[:, 1].min(), p0[:, 1].max()
        haar = vul((H, W), [p for p in st if len(p) < 3000 and vorm_ok(p, 3.5)
                            and y0 - 6 <= p[:, 0].mean() <= y1 + 6 and x0 - 6 <= p[:, 1].mean() <= x1 + 6])
        # de randjes van de plukken: al het rood dat tegen het haar aan ligt hoort erbij
        bijhaar = np.asarray(Image.fromarray((haar * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 0
        haar = haar | (bijhaar & ((hd < 15) | (hd > 345)) & (s > 0.3) & zicht & ~sjerp)
        # rond het hoofd: de wenkbrauwen (kleine rode stukjes) en het litteken (een lichte streep)
        vak = np.zeros((H, W), bool)
        vak[max(0, y0 - 50):y1 + 50, max(0, x0 - 50):x1 + 50] = True
        rood = ((hd < 12) | (hd > 359.6)) & (s > 0.6) & zicht & ~sjerp & ~haar
        gz = vul((H, W), [p for p in stukken(rood & vak) if 4 <= len(p) <= 160 and vorm_ok(p, 4.5)])
        lit = vak & (hd > 8) & (hd < 40) & (s < 0.62) & (v > 0.71) & ~rood
        lit = vul((H, W), [p for p in stukken(lit) if len(p) >= 5])
    # de windsels: grijze stukken van middelmaat. Een polswindsel zit aan zijn arm, en die hangt aan zijn hele
    # bovenlijf: een groot stuk huid. Een enkelwindsel raakt alleen een voet, een stuk van de knots helemaal geen huid.
    # Zo klopt het in elke houding, ook als hij knielt en zijn handen naast zijn benen hangen.
    grijs = ((s < 0.22) | ((hd > 190) & (hd < 260) & (s < 0.7))) & (v > 0.28) & (v < 0.85) & zicht   # ook de blauwig getinte
    huidlab = np.zeros((H, W), np.int32); huidmaat = [0]
    for n, p in enumerate(stukken(huid), 1):
        huidlab[p[:, 0], p[:, 1]] = n; huidmaat.append(len(p))
    huidmaat = np.array(huidmaat); lijf = huidmaat.max()
    pols = []
    for p in stukken(grijs):
        # middelmaat (twee polsen tegen elkaar boven zijn hoofd tellen als een stuk), niet te donker
        if not (120 < len(p) < 2600 and np.ptp(p[:, 1]) < 100 and np.ptp(p[:, 0]) < 100 and v[p[:, 0], p[:, 1]].mean() > 0.33):
            continue
        ring = rand_van(vul((H, W), [p]), 3)
        raakt = np.unique(huidlab[ring]); raakt = raakt[raakt > 0]
        if len(raakt) and huidmaat[raakt].max() >= 0.25 * lijf and huid[ring].mean() >= 0.12:   # de bal kan zijn hand raken, maar is niet door huid omringd
            pols.append(p)
    pols = vul((H, W), pols)
    return haar, gz, lit, sjerp, broek, pols


def verloop(t, pal):
    pal = np.array(pal, np.float32) / 255; t = np.clip(t, 0, 1) * (len(pal) - 1)
    i = np.minimum(t.astype(int), len(pal) - 2); f = (t - i)[..., None]
    return pal[i] * (1 - f) + pal[i + 1] * f


def kleur(im, dx, dy):
    a0 = np.asarray(im.convert('RGBA')).astype(np.float32) / 255
    haar, gz, lit, sjerp, broek, pols = maskers(a0, dx, dy)
    h0, s0, v0 = hsv(a0); hd = h0 * 360
    # de huid: oranjebruin van 12 tot 45 graden en verzadigd genoeg, met zachte randen
    w = np.clip((hd - 8) / 8, 0, 1) * np.clip((48 - hd) / 8, 0, 1) * np.clip((s0 - 0.25) / 0.15, 0, 1)
    v = v0 * (1 - w * (1 - HUID['helder'])); s = np.clip(s0 * (1 + w * (HUID['verz'] - 1)), 0, 1)
    h = (h0 + w * HUID['tint']) % 1
    h[haar] = 0; s[haar] *= HAAR['verz']; v[haar] *= HAAR['helder']
    h[sjerp] = SJERP['tint'] / 360; s[sjerp] = np.clip(s[sjerp] * SJERP['verz'], 0, 1); v[sjerp] = np.clip(v[sjerp] * SJERP['helder'], 0, 1)
    wb = np.clip(v[broek] / 0.1 - 0.5, 0, 1)                   # de zwarte lijnen blijven zwart
    h[broek] = BROEK['tint'] / 360; s[broek] = BROEK['verz'] * wb; v[broek] = np.clip(v[broek] * (1 + wb * (BROEK['helder'] - 1)), 0, 1)
    h[gz] = 0; s[gz] *= HAAR['verz']; v[gz] = v0[gz] * HAAR['helder']     # de wenkbrauwen zwart, net als het haar
    h[lit] = 0.06; s[lit] = 0.32; v[lit] = 0.86
    a = a0.copy(); a[..., :3] = rgb(h % 1, np.clip(s, 0, 1), np.clip(v, 0, 1))
    a[pols, :3] = verloop(((v0[pols] - 0.2) / 0.55) ** 0.8, POLS)
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def main():
    m = json.load(open(ROOT + 'brutus.json'))
    frames = {f['src']: f for b in m['bewegingen'].values() for f in b['frames']}
    os.makedirs(DOEL, exist_ok=True)
    for src, f in sorted(frames.items()):
        kleur(Image.open(ROOT + src), f['dx'], f['dy']).save(DOEL + os.path.basename(src), optimize=True)
    print(f'{len(frames)} frames naar {DOEL}')


if __name__ == '__main__':
    main()
