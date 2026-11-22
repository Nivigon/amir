import sys; sys.path.insert(0,'/home/claude/lijn')
import numpy as np; from scipy import ndimage
from rolcirkels import CIRK
from rand import lum, zoom_kleur
def vul_kop(M, n):
    x,y,r=CIRK[n]; H,W=M.shape[:2]
    yy,xx=np.mgrid[0:H,0:W]; D=(yy-y)**2+(xx-x)**2<=(r+0.5)**2
    A=M.copy(); a=A[...,3]>40
    lab,nn=ndimage.label(a); sz=ndimage.sum(a,lab,range(1,nn+1)); hl=np.argmax(sz)+1
    buurt=ndimage.binary_dilation(D,iterations=int(r*0.6))
    for i in range(1,nn+1):
        c=lab==i
        if i!=hl and sz[i-1]<600 and (c&buurt).any(): A[c]=0
    # oude snijresten onder de kin, buiten de hoofdcirkel en links van de vuisten
    onder=(~((yy-y)**2+(xx-x)**2<=(r+1.5)**2))&(yy>y+r*0.5)&(yy<y+r+14)&(xx>x-r-6)&(xx<x+8)
    A[onder&(A[...,3]>0)]=0
    a=A[...,3]>128
    rood=(A[...,0]>140)&(A[...,1]<90)&(A[...,2]<90)&a
    roodz=ndimage.binary_dilation(rood,iterations=2)
    # ingesloten gaten vlak bij het hoofd (bv. rol_17) horen er ook bij
    D2=(yy-y)**2+(xx-x)**2<=(r+12)**2
    ingesl=ndimage.binary_fill_holes(a|D)&~a&D2
    if n!=17: ingesl[:]=False
    nieuw=((D&~a)|ingesl)&~roodz
    # spleten tussen hoofd en arm/hand niet vullen: een stuk dat aan lijf buiten de cirkel grenst, en smal is
    buiten_c=a&~ndimage.binary_dilation(D,iterations=2)
    lab2,n2=ndimage.label(nieuw)
    for i in range(1,n2+1):
        c=lab2==i
        smal=ndimage.binary_erosion(c,iterations=2).sum()==0
        if smal and (ndimage.binary_dilation(c,iterations=2)&buiten_c).sum()>3: nieuw[c]=False
    huidkl=np.median(A[D&a&~roodz][:,:3],0)
    kd=np.abs(A[...,:3].astype(float)-huidkl).max(-1)
    bij=ndimage.binary_dilation(nieuw,iterations=6)&(D|ingesl)
    oud=bij&((kd>16)|zoom_kleur(A)|(A[...,3]<235))
    L=lum(A); huidL=np.median(L[D&a&~roodz])
    med=ndimage.median_filter(L,5)
    bleek=D&a&~roodz&((L>huidL*1.12)|(L-med>10))&~(L>huidL*2.2)   # lichte streepjes, niet het oogwit
    onb=nieuw|oud|bleek
    betr=(D|ingesl)&a&~onb&~roodz&(kd<30)
    f=np.zeros(A.shape[:2]+(3,)); w=betr.astype(float)
    for s in (3.0,7.0,14.0):
        num=np.dstack([ndimage.gaussian_filter(A[...,c]*w,s) for c in range(3)]); den=ndimage.gaussian_filter(w,s)[...,None]
        g=num/np.maximum(den,1e-6); vul=(f.sum(-1)==0)&(den[...,0]>0.15)
        f[vul]=g[vul]
    rest=(f.sum(-1)==0)
    if rest.any():
        num=np.dstack([ndimage.gaussian_filter(A[...,c]*w,30) for c in range(3)]); den=ndimage.gaussian_filter(w,30)[...,None]
        f[rest]=(num/np.maximum(den,1e-9))[rest]
    A[onb,:3]=f[onb].round().clip(0,255).astype(np.uint8); A[onb,3]=255
    head=ndimage.binary_erosion((D|ingesl)&(A[...,3]>128)&~ndimage.binary_dilation(rood,iterations=3),iterations=3)
    return A, head, onb
