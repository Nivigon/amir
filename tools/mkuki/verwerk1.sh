#!/bin/sh
# verwerk1.sh werkmap sN postid id : een zoom-tegel van het hele beeld (op 0,6 getoond, 1037x691) opschalen naar
# 1728x1152, terugzetten (print IoU) en de post-id bewaren in ids.json. Scheelt een tegel per frame; de figuur is op
# 0,6 nog steeds groter dan het eindframe.
W=$1; S=$2; P=$3; K=$4
cd /home/claude/amir
python3 - "$W/${S}_grok.png" "$K" <<'P'
import sys, glob
from PIL import Image
u, k = sys.argv[1:]
f = sorted(glob.glob('/tmp/claude-tool-results/*/*' + k + '*'))[-1]
Image.open(f).convert('RGB').resize((1728, 1152), Image.LANCZOS).save(u)
P
python3 tools/mkuki/paar.py terug $W/$S
python3 - "$W/ids.json" "$S" "$P" <<'X'
import json, sys, os
f, s, p = sys.argv[1:]
d = json.load(open(f)) if os.path.exists(f) else {}
d.setdefault(s, [])
if p not in d[s]: d[s].append(p)
json.dump(d, open(f, 'w'), indent=1)
X
