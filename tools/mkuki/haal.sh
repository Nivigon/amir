#!/bin/sh
# Plak de laatste zes zoom-tegels uit de tool-map tot een Grok-beeld: haal.sh uit.png
D=$(ls -dt /tmp/claude-tool-results/*/ | head -1)
python3 "$(dirname "$0")/plak.py" "$1" $(ls -tr "$D"*.png | tail -6)
