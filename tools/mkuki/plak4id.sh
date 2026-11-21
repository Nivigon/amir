#!/bin/sh
# plak4id.sh uit.png id00 id10 id01 id11  : 2x2 tegels (864x576) tot 1728x1152
U=$1; shift
D=$(ls -dt /tmp/claude-tool-results/*/ | head -1)
python3 - "$U" "$D" "$@" <<'P'
import sys, glob
from PIL import Image
u, D, ks = sys.argv[1], sys.argv[2], sys.argv[3:]
S = Image.new('RGB', (1728, 1152))
for i, k in enumerate(ks):
    S.paste(Image.open(glob.glob(D + '*' + k + '*')[0]).convert('RGB').resize((864, 576)), ((i % 2) * 864, (i // 2) * 576))
S.save(u)
P
