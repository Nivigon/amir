import sys
from PIL import Image
A,B,C,D,out=sys.argv[1:6]
A,B,C,D=[Image.open(p) for p in (A,B,C,D)]
S=Image.new('RGB',(1808,1104))
S.paste(A.crop((0,0,1530,646)),(0,0)); S.paste(B.crop((6,0,1536,646)),(278,0))
S.paste(C.crop((0,6,1530,646)),(0,464)); S.paste(D.crop((6,6,1536,646)),(278,464))
S.save(out)
