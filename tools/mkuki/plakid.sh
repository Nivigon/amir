#!/bin/sh
# plakid.sh uit.png id1 id2 id3 id4 id5 id6  (de willekeurige stukjes uit de bestandsnamen van de zoom-tegels)
U=$1; shift
D=$(ls -dt /tmp/claude-tool-results/*/ | head -1)
P=""
for k in "$@"; do P="$P $(ls $D*$k*.png)"; done
python3 "$(dirname "$0")/plak.py" "$U" $P
