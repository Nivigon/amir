import sys,os,json; sys.path.insert(0,'/home/claude/lijn'); sys.path.insert(0,'/home/claude/gat')
import numpy as np; from PIL import Image; from scipy import ndimage
from skimage.morphology import convex_hull_image
from gem import L, orig
from vul import hoofdgat
from handkop import HAND, handkop
from rolcirkels import CIRK
MK='/home/claude/mkb/karakters/amir/mkuki'; OUD='/home/claude/oud/karakters/amir/mkuki'
def schijf(r):
    y,x=np.mgrid[-r:r+1,-r:r+1]; return y*y+x*x<=r*r
def kop(p,M,O):
    if p in HAND: return handkop(p,M)
    if p.startswith('beweging/rol/met/'):
        n=int(p.split('_')[-1][:-4])
        if n in CIRK:
            x,y,r=CIRK[n]; yy,xx=np.mgrid[0:M.shape[0],0:M.shape[1]]; return (yy-y)**2+(xx-x)**2<=r*r
    k,h=hoofdgat(O,M); return h
out=[]
for p in L:
    vp=MK+'/'+p[:-4]+'_vuist.png'
    if not os.path.exists(vp) or p=='speerworp/speerworp_04.png': continue
    V=np.array(Image.open(vp).convert('RGBA')); F=np.array(Image.open(MK+'/'+p).convert('RGBA'))
    M=np.array(Image.open(OUD+'/'+p).convert('RGBA')); O=np.array(Image.open(orig(p)).convert('RGBA'))
    h=kop(p,M,O)
    if h is None or not h.any(): continue
    zone=ndimage.binary_dilation(convex_hull_image(h),iterations=4)
    vk=(V[...,3]>0)&zone
    if vk.sum()<6 and not p.startswith('beweging/rol/met/'): continue
    # rafels: vuistpixels in de kopzone waar het nieuwe lijf leeg is
    weg=vk&(F[...,3]<30)
    # losse brokjes iets verder van het hoofd: kleine stukken vuist die niet op het lijf liggen
    ruim=ndimage.binary_dilation(zone,iterations=18)
    los=(V[...,3]>0)&ruim&(F[...,3]<30)
    lab,n=ndimage.label(V[...,3]>0)
    for i in range(1,n+1):
        c=lab==i
        if c.sum()<80 and (c&los).sum()>=0.5*c.sum(): weg|=c
    # kopdeel van de vuist: gesloten vorm, binnen het nieuwe lijf
    p_=8; g=np.pad(vk&~weg,p_)
    g=ndimage.binary_closing(g,structure=schijf(6)); g=ndimage.binary_fill_holes(g)[p_:-p_,p_:-p_]
    R=g&zone&(F[...,3]>0)
    if p.startswith('beweging/rol/met/'):
        weg|=(V[...,3]>0)&ruim&(F[...,3]<30)
    V2=V.copy(); V2[weg]=0; V2[R]=F[R]
    if not np.array_equal(V,V2):
        Image.fromarray(V2).save(vp,optimize=True)
        zp=vp[:-4]+'_zones.png'
        if os.path.exists(zp):
            Z=np.array(Image.open(zp).convert('RGBA')); Zl=np.array(Image.open(MK+'/'+p[:-4]+'_zones.png').convert('RGBA'))
            Z[weg]=0; Z[R]=Zl[R]; Image.fromarray(Z).save(zp,optimize=True)
        out.append((p,int(weg.sum()),int(R.sum())))
for o in out: print(o)
print(len(out))
