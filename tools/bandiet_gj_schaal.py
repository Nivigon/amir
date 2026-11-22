# De galerijsprong van de chaser (enemies/bandiet_as/: afzet, zweef, landing, opkijk) op de maat van zijn ren brengen.
#
# De Grok-clips zoomen tijdens het spelen in: de afzet loopt van 1,02 naar 1,05 keer de idle-maat, en de landingsclip
# zoomt tijdens de klap (frame 1 tot 7) van 1,05 naar 1,16. Vanaf de klap (landing 7) en het hele opkijken was de
# chaser zo 14% groter dan in zijn ren. Gemeten met de kop (template-match op idle_in_00) en de dolk in zijn sjerp
# (knop tot punt: idle_in_00 76 px, opkijk_17 88 px). De ren staat op 1,02.
#
# Dit script schaalt elk frame rond het voetpunt (anker 229, grondlijn 555) met 1,02 gedeeld door de gemeten maat,
# en de kleine set rond de helft daarvan. De factor per frame gaat als "schaal" in sprites_galerij.json; staat die er
# al, dan stopt het script (anders krimpt hij twee keer). Draai daarna gen-offline-manifest.py.
# Na deze correctie moet BAN_GJ.landY in de HTML mee: die hoogtes zijn canvas-px van de oude landingsframes.
import os, sys, json
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MAP = os.path.join(ROOT, 'enemies', 'bandiet_as')
KLEIN = os.path.join(ROOT, 'klein', 'enemies', 'bandiet_as')
ANKER, GROND = 229, 555
DOEL = 1.02                       # de maat van de ren (idle_in_00 = 1)

def ramp(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]

MAAT = {
    'afzet':   ramp(1.02, 1.05, 8) + [1.05] * 21,              # 29 frames: de inzoom tot frame 7, daarna vlak
    'zweef':   [1.05],
    'landing': [1.05, 1.05] + ramp(1.05, 1.16, 7)[1:] + [1.16] * 6,   # 14 frames: de inzoom tijdens de klap, tot frame 7
    'opkijk':  [1.16] * 18,
}

def schaal(pad, f, ax, gy):
    im = Image.open(pad).convert('RGBA')
    W, H = im.size
    k = im.resize((max(1, round(W * f)), max(1, round(H * f))), Image.LANCZOS)
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    can.alpha_composite(k, (round(ax - ax * f), round(gy - gy * f)))   # het voetpunt blijft staan
    can.save(pad, optimize=True)

meta_pad = os.path.join(MAP, 'sprites_galerij.json')
meta = json.load(open(meta_pad))
if any('schaal' in fr for set_ in meta['sets'].values() for fr in set_):
    sys.exit('sprites_galerij.json heeft al een schaal per frame: de frames zijn al gecorrigeerd')
for naam, maten in MAAT.items():
    frames = meta['sets'][naam]
    assert len(frames) == len(maten), (naam, len(frames), len(maten))
    for fr, m in zip(frames, maten):
        f = DOEL / m
        bestand = f'{naam}_{fr["f"]:02d}.png'
        schaal(os.path.join(MAP, naam, bestand), f, ANKER, GROND)
        kl = os.path.join(KLEIN, naam, bestand)
        if os.path.exists(kl):
            schaal(kl, f, ANKER / 2, GROND / 2)
        fr['schaal'] = round(f, 4)
json.dump(meta, open(meta_pad, 'w'), indent=1)
print('klaar; landing-factoren voor BAN_GJ.landY:', [fr['schaal'] for fr in meta['sets']['landing'][:7]])
