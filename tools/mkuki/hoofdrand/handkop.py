import numpy as np; from scipy import ndimage
# met de hand: x van het midden van de schedel, en de straal (ongeveer de helft van de hoofdmaat van de set)
HAND={'beweging/rol/worp/worp_14.png':(210,34),'beweging/rol/worp/worp_27.png':(167,34),'beweging/rol/worp/worp_28.png':(192,34),'speerworp/speerworp_10.png':(499,58),'aanval/lowsweep/sweep_13.png':(652,56),'beweging/rol/worp/worp_23.png':(195,34),'beweging/rol/worp/worp_24.png':(187,34)}
def handkop(p,M):
    cx,r=HAND[p]; a=M[...,3]>128
    kol=np.where(a[:,cx-3:cx+4].any(1))[0]; top=kol.min()
    cy=top+r
    yy,xx=np.mgrid[0:M.shape[0],0:M.shape[1]]
    cirkel=(yy-cy)**2+(xx-cx)**2<=(r*1.08)**2
    m=M.astype(int); rood=(m[...,0]>140)&(m[...,1]<90)&(m[...,2]<90)
    h=a&cirkel&~ndimage.binary_dilation(rood,iterations=3)
    lab,n=ndimage.label(h); 
    if n>1:
        sz=ndimage.sum(h,lab,range(1,n+1)); h=lab==(np.argmax(sz)+1)
    return ndimage.binary_erosion(h,iterations=3)
