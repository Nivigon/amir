#!/bin/sh
# verwerk.sh werkmap sN postid idboven idonder : tegels plakken, terugzetten (print IoU), post-id bewaren in ids.json
W=$1; S=$2; P=$3
cd /home/claude/amir
tools/mkuki/tegel2.sh $W/${S}_grok.png $4 $5 && python3 tools/mkuki/paar.py terug $W/$S
python3 - "$W/ids.json" "$S" "$P" <<'X'
import json, sys, os
f, s, p = sys.argv[1:]
d = json.load(open(f)) if os.path.exists(f) else {}
d.setdefault(s, [])
if isinstance(d[s], str): d[s] = [d[s]]
if p not in d[s]: d[s].append(p)
json.dump(d, open(f, 'w'), indent=1)
X
