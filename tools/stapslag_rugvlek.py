# De oog-vlekjes op de vacht weg op de frames waar we zijn rug zien (Tom, 16-11-2026)
import numpy as np, cv2, sys
from PIL import Image
def schoon(p, uit):
    a=np.array(Image.open(p).convert('RGBA')); rgb=a[...,:3].astype(int); al=a[...,3]
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    vacht=(r>140)&(g>100)&(r>b+35)&(g>b+15)&(al>200)
    vachtV=cv2.morphologyEx(vacht.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))>0
    binnen=cv2.erode(vachtV.astype(np.uint8),np.ones((5,5),np.uint8))>0
    vlek=binnen&~vacht&(al>200)
    n,lab,st,_=cv2.connectedComponentsWithStats(vlek.astype(np.uint8))
    m=np.zeros_like(vlek)
    for i in range(1,n):
        if 3<=st[i,cv2.CC_STAT_AREA]<=160: m|=lab==i
    m|=(r-g>45)&(b>g+15)&vachtV      # roze zweem op de vacht
    m=cv2.dilate(m.astype(np.uint8),np.ones((3,3),np.uint8))>0
    m&=vachtV
    out=cv2.inpaint(np.ascontiguousarray(a[...,:3]),(m*255).astype(np.uint8),3,cv2.INPAINT_TELEA)
    a[...,:3]=np.where(m[...,None],out,a[...,:3])
    Image.fromarray(a).save(uit); return int(m.sum())
if __name__=='__main__':
    for p in sys.argv[1:]: print(p, schoon(p,p))
