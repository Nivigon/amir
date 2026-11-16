#!/usr/bin/env python3
"""Maakt het leeuwenhoofd van Tau (de zonnestraal) uit de Grok-clip in karakters/amir/tau/bron/.

Bron: tau_brul.mp4, een leeuwenkop in tribal lijnwerk, zwarte inkt op wit, recht van voren: eerst rustig, dan de brul.
Uit:  karakters/amir/tau/tau_00.png (de rustige kop, voor het opkomen tijdens de trance) en tau_01.png en verder (de brul).

Het zwart wordt de vorm: hoe donkerder de inkt, hoe minder doorzichtig. De lijnen krijgen KLEUR, een licht grijswit als
van een geest; het wit tussen de lijnen is helemaal doorzichtig. Elk frame staat op hetzelfde canvas, met het midden van
de kop op dezelfde plek, zodat het spel ze zonder verschuiving na elkaar kan tekenen. Andere kleur nodig (goud, rood)?
Pas KLEUR aan en draai opnieuw, of kleur in het spel met een doekje.

    python3 tools/tau_leeuw.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist ffmpeg, Pillow en numpy.
"""
import os
import glob
import shutil
import subprocess
import tempfile
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'karakters', 'amir', 'tau', 'bron', 'tau_brul.mp4')
UIT = os.path.join(ROOT, 'karakters', 'amir', 'tau')
KLEUR = (236, 241, 246)            # de lijnen: licht grijswit, als een geest
RUST = 1                           # het clipframe met de rustige kop (1-geteld)
BRUL = list(range(50, 93, 2))      # de brul: van de mond die opengaat tot de volle brul (elk tweede frame, Grok dubbelt)
LAAG, HOOG = 0.10, 0.85            # inkt (0 wit, 1 zwart) onder LAAG is leeg, boven HOOG vol; ertussen een zachte rand
MARGE = 6                          # px lege rand om de kop

tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', BRON, os.path.join(tmp, '%03d.png')], check=True)
nummers = [RUST] + BRUL
inkt = []
for n in nummers:
    g = np.array(Image.open(os.path.join(tmp, '%03d.png' % n)).convert('L')).astype(float) / 255
    inkt.append(np.clip(((1 - g) - LAAG) / (HOOG - LAAG), 0, 1))
shutil.rmtree(tmp)

# een kader om alle frames samen, zodat ze op een canvas en op een plek staan
som = np.max(np.stack(inkt), axis=0)
ys, xs = np.where(som > 0.02)
x0, x1 = max(0, xs.min() - MARGE), min(som.shape[1], xs.max() + 1 + MARGE)
y0, y1 = max(0, ys.min() - MARGE), min(som.shape[0], ys.max() + 1 + MARGE)

for f in glob.glob(os.path.join(UIT, 'tau_*.png')):
    os.remove(f)
for i, a in enumerate(inkt):
    a = a[y0:y1, x0:x1]
    rgba = np.zeros(a.shape + (4,), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = KLEUR
    rgba[..., 3] = np.round(a * 255).astype(np.uint8)
    Image.fromarray(rgba, 'RGBA').save(os.path.join(UIT, 'tau_%02d.png' % i), optimize=True)

print('%d frames, canvas %dx%d (tau_00 rustig, tau_01 tot tau_%02d de brul)' % (len(inkt), x1 - x0, y1 - y0, len(inkt) - 1))
print("TAU.frames = %d, TAU.w = %d, TAU.h = %d" % (len(inkt), x1 - x0, y1 - y0))
