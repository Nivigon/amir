"""Cyclusplaat: per frame het origineel boven en Mkuki eronder, op dezelfde schaal, voor het nakijken van een loopcyclus
(ren, lopen, sluipen). Controleer per frame welk been voor staat en welke arm voor zit: bij een stap met het linkerbeen
voor hoort de rechterarm voor, en wisselt het been, dan wisselen de armen mee. Een arm die de hele cyclus aan dezelfde
kant blijft is fout, ook als elk frame op zich lijkt.

python3 tools/mkuki/cyclus.py uit.png schaal pad1 pad2 ...   (paden onder karakters/amir/; Mkuki uit karakters/amir/mkuki/)
"""
import sys, os
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
B = os.path.join(REPO, 'karakters/amir/')
uit, s, ps = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
rij = [[Image.open(B + p).convert('RGBA') for p in ps], [Image.open(B + 'mkuki/' + p).convert('RGBA') for p in ps]]
bb = None
for r in rij:
    for im in r:
        b = im.getbbox()
        if b: bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
w, h = bb[2] - bb[0], bb[3] - bb[1]
C = Image.new('RGBA', (len(ps) * w, 2 * h), (214, 196, 160, 255))
for j, r in enumerate(rij):
    for i, im in enumerate(r): C.alpha_composite(im.crop(bb), (i * w, j * h))
C.resize((int(C.width * s), int(C.height * s))).convert('RGB').save(uit)
