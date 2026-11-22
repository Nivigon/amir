import sys, numpy as np, glob
from PIL import Image
n=sys.argv[1]; pad=sys.argv[2]
d=np.load(glob.glob(f'/home/claude/werk/klaar/*{n}*')[0])
o=Image.open(pad).convert('RGBA')
im=Image.fromarray(d['lijf']); C=Image.new('RGBA',im.size,(200,200,200,255)); C.alpha_composite(im)
O=Image.new('RGBA',o.size,(200,200,200,255)); O.alpha_composite(o)
W=Image.new('RGBA',(im.width*2,im.height)); W.paste(O,(0,0)); W.paste(C,(im.width,0)); W.save('/tmp/spel.png')
