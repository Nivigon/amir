#!/bin/sh
# tegel.sh uit.png breed hoog id00 id10 id01 id11 : vier zoom-tegels (elk breed/2 x hoog/2) tot een beeld
U=$1; W=$2; H=$3; shift 3
python3 - "$U" "$W" "$H" "$@" <<'P'
import sys, glob
from PIL import Image
u, W, H, ks = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
S = Image.new('RGB', (W, H))
for i, k in enumerate(ks):
    f = sorted(glob.glob('/tmp/claude-tool-results/*/*' + k + '*'))[-1]
    t = Image.open(f).convert('RGB').resize((W // 2, H // 2), Image.LANCZOS)
    S.paste(t, ((i % 2) * (W // 2), (i // 2) * (H // 2)))
S.save(u)
P
