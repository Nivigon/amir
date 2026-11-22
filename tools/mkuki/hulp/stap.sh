#!/bin/sh
# stap.sh SET N postid fileid origpad
cd /home/claude/amir
/home/claude/doe2.sh $1 $2 $3 $4 | grep png; python3 tools/mkuki/klaar1.py /home/claude/werk/$1/s$2.npy $5 --eiland --geenhoofd | tail -1
grep "^s$2\|png" /dev/null
b=$(echo $5 | sed "s|^karakters/amir/||; s|/|__|g; s|png$||")
python3 /home/claude/spel.py $b $5
python3 -c "
from PIL import Image; im=Image.open('/tmp/spel.png'); im.resize((im.width*2//5,im.height*2//5)).save('/tmp/spel.png')"
tail -1 /home/claude/werk/$1/ids.json >/dev/null
