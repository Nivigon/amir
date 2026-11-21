#!/bin/sh
# tegelxy.sh uit.png x:y:id ... : zoom-tegels van 1209x576 op beeldpositie (x,y) in een 1728x1152-beeld (rest magenta)
U=$1; shift
python3 - "$U" "$@" <<'P'
import sys, glob
from PIL import Image
u, ks = sys.argv[1], sys.argv[2:]
S = Image.new('RGB', (1728, 1152), (255, 0, 255))
for k in ks:
    x, y, i = k.split(':')
    f = sorted(glob.glob('/tmp/claude-tool-results/*/*' + i + '*'))[-1]
    S.paste(Image.open(f).convert('RGB').resize((1209, 576)), (int(x), int(y)))
S.save(u)
P
