#!/bin/sh
# plakmaat.sh uit.png breed hoog id00 id10 id01 id11 : 2x2 tegels van een beeld met andere maat (tegel = 864x576 beeldpixels, stap breed/2)
U=$1; W=$2; H=$3; shift 3
D=$(ls -dt /tmp/claude-tool-results/*/ | head -1)
python3 - "$U" "$D" "$W" "$H" "$@" <<'P'
import sys, glob
from PIL import Image
u, D, W, H, ks = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:]
S = Image.new('RGB', (W, H))
for i, k in enumerate(ks):
    S.paste(Image.open(glob.glob(D + '*' + k + '*')[0]).convert('RGB').resize((864, 576)), ((i % 2) * W // 2, (i // 2) * H // 2))
S.crop((0, 0, W, H)).save(u)
P
