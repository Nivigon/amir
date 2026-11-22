#!/bin/sh
# doe2.sh SET N postid fileid
cd /home/claude/amir
W=/home/claude/werk/$1
sh tools/mkuki/verwerk1.sh $W s$2 $3 $4
python3 - $W $2 <<'X'
import sys, json
from PIL import Image
W,n=sys.argv[1:]
o=Image.open(json.load(open(f'{W}/s{n}.json'))['pad']).convert('RGBA')
o=o.crop(o.getbbox())
v=Image.open(f'{W}/s{n}_vergelijk.png').convert('RGBA')
h=150
o=o.resize((int(o.width*h/o.height),h)); v=v.resize((int(v.width*h/v.height),h))
C=Image.new('RGBA',(o.width+v.width+10,h),(255,255,255,255))
C.alpha_composite(o,(0,0)); C.alpha_composite(v,(o.width+10,0))
C.save('/tmp/vgl.png')
X
