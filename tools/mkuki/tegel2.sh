#!/bin/sh
# tegel2.sh uit.png idboven idonder : twee zoom-tegels van 1209x576 (rechts vanaf x=519) tot een 1728x1152-beeld.
# Links blijft magenta: daar staat alleen de kleine referentie, die terug niet nodig heeft.
U=$1; shift
python3 - "$U" "$@" <<'P'
import sys, glob
from PIL import Image
u, ks = sys.argv[1], sys.argv[2:]
S = Image.new('RGB', (1728, 1152), (255, 0, 255))
for i, k in enumerate(ks):
    f = sorted(glob.glob('/tmp/claude-tool-results/*/*' + k + '*'))[-1]
    S.paste(Image.open(f).convert('RGB').resize((1209, 576)), (519, 576 * i))
S.save(u)
P
