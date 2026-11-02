#!/usr/bin/env python3
"""Nyundo (Brutus) donker: een tweede kleurstelling van dezelfde frames.

Leest enemies/brutus/frames/*.png (met brutus.json voor het anker) en schrijft naar
enemies/brutus/frames_donker/ (zelfde namen en maat, dus brutus.json geldt voor allebei):
- de huid donkerder bruin (de oranjebruine tinten, ook de steel en de sandalen een tikje);
- het haar zwart (de rode stukken bovenaan), het rood in het gezicht feller en het litteken
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


def maskers(a, dx, dy):
    """haar, rood in het gezicht, litteken, sjerp, broek en polswindsels, uit het origineel"""
    h, s, v = hsv(a); hd = h * 360; H, W = v.shape; zicht = a[..., 3] > 0.3
    hoog = (-dy - np.arange(H))[:, None] * np.ones(W)          # hoogte boven de grondlijn
    xs = np.arange(W)[None, :] + dx                            # afstand tot het anker
    rood = ((hd < 12) | (hd > 335)) & (s > 0.4) & zicht
    st = sorted([p for p in stukken(rood) if len(p) >= 6], key=lambda p: p[:, 0].min())
    haar = gz = lit = sjerp = np.zeros((H, W), bool)
    if st:
        top = ([p for p in st if len(p) >= 40] or st)[0][:, 0].min()
        haar = vul((H, W), [p for p in st if p[:, 0].min() < top + 34 and p[:, 0].mean() < top + 38])
        if haar.any():
            ys, xx = np.nonzero(haar)
            vak = np.zeros((H, W), bool)
            vak[max(0, ys.max() - 4):ys.max() + 45, max(0, xx.min() - 12):xx.max() + 12] = True
            gz = rood & vak & ~haar
            lit = vak & (hd > 8) & (hd < 40) & (s < 0.62) & (v > 0.71) & ~rood
            lit = vul((H, W), [p for p in stukken(lit) if len(p) >= 5])
        sjerp = vul((H, W), [p for p in st if 100 < -dy - p[:, 0].mean() < 260 and abs(p[:, 1].mean() + dx) < 100
                             and (np.ptp(p[:, 1]) + 1 > 1.8 * (np.ptp(p[:, 0]) + 1) or len(p) < 400)
                             and not haar[p[:, 0], p[:, 1]].any()])
    broek = (s < 0.3) & (v < 0.33) & (hoog > 40) & (hoog < 210) & zicht
    dicht = np.asarray(Image.fromarray((broek * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(5))).astype(np.float32) / 255
    broek &= (dicht > 0.55) & (np.abs(xs) < 150)               # het vlak, niet de dunne plooien of het ijzer
    broek = vul((H, W), [p for p in stukken(broek) if len(p) >= 300])
    grijs = (s < 0.22) & (v > 0.28) & (v < 0.85) & (a[..., 3] > 0.5) & (hoog > 140)
    pols = vul((H, W), [p for p in stukken(grijs) if 120 < len(p) < 1600 and np.ptp(p[:, 1]) < 70 and np.ptp(p[:, 0]) < 70
                        and abs(p[:, 1].mean() + dx) < 190 and v[p[:, 0], p[:, 1]].mean() > 0.33])
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
    h[gz] = h0[gz]; s[gz] = np.clip(s0[gz] * 1.1, 0, 1); v[gz] = np.clip(v0[gz] * 1.3 + 0.08, 0, 1)
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
