#!/usr/bin/env python3
"""Tau 1 (de jonge leeuw) voor het spel: de frames uit de productie (branch claude/tau1, karakters/amir/tau1/) naar
karakters/amir/tau1_spel/ onder dezelfde naam als het gewone frame, voor de skin `tau1` (SKIN, Test 90).

Staan, rennen en springen krijgen de krassen erin (de voorbeeldbeelden uit tau1/.../krassen/); de rol heeft nog geen
krassen. Ook de kleine set (klein/) op dezelfde verhouding als het gewone kleine frame, en lijst.json.

Gebruik:  python3 tools/tau1_spel_bak.py PAD_NAAR_TAU1   (de map karakters/amir/tau1 van claude/tau1)
"""
import json, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'karakters/amir/')
UIT = os.path.join(A, 'tau1_spel/')
JUMP = ['amirjump0staand', 'amirjump1hurk', 'amirjump2afzet', 'amirjump3stijgen', 'amirjump4top', 'amirjump5vallen', 'amirjump6landing']


def main(T):
    rel = ['stokken/staan/staan_00.png'] + ['stokken/rennen/rennen_%02d.png' % i for i in range(12)] + \
          ['beweging/jump/jump/%s.png' % n for n in JUMP] + ['beweging/rol/zonder/rol_%d.png' % i for i in range(1, 29)]
    lijst = []
    for r in rel:
        d, f = os.path.split(r)
        kras = os.path.join(T, d, 'krassen', f[:-4] + '_voorbeeld.png')
        bron = kras if os.path.exists(kras) else os.path.join(T, r)
        im = Image.open(bron).convert('RGBA')
        assert im.size == Image.open(A + r).size, r
        os.makedirs(os.path.dirname(UIT + r), exist_ok=True)
        im.save(UIT + r, optimize=True)
        klein = os.path.join(ROOT, 'klein/karakters/amir/', r)
        if os.path.exists(klein):
            kw, kh = Image.open(klein).size
            p = os.path.join(ROOT, 'klein/karakters/amir/tau1_spel/', r)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            (im if (kw, kh) == im.size else im.resize((kw, kh), Image.LANCZOS)).save(p, optimize=True)
        lijst.append(r)
    json.dump(lijst, open(UIT + 'lijst.json', 'w'), indent=0)
    print(len(lijst), 'frames')


if __name__ == '__main__':
    main(sys.argv[1])
