# speerworp_04: hoofd en vuist uit frame 3 (zelfde houding), want in 4 ontbrak een groot stuk voorhoofd en hand
import numpy as np
from PIL import Image
def maak(M4, M3):
    D=np.roll(np.roll(M3,3,0),-9,1)          # hoofd van 3 op het hoofd van 4 (gemeten)
    yy,xx=np.mgrid[0:M4.shape[0],0:M4.shape[1]]
    F=M4.copy().astype(float)
    F[(xx<240)&(yy>140)&(yy<315)]=0          # puin voor het gezicht weg
    kop=(xx>=222)&(yy>140)&(yy<322)
    w=np.clip((322-yy)/8.0,0,1)[...,None]     # zachte naad in de nek, y 314-322
    F[kop]=(D[kop]*w[kop]+F[kop]*(1-w[kop]))
    hand=(M3[...,3]>0)&(xx<=239)&(yy>147)&(yy<318)
    # de vuist van 3, uitgelijnd op de armband van 4
    Hs=np.roll(np.roll(M3,-3,0),-2,1); hs=np.roll(np.roll(hand,-3,0),-2,1)
    a=Hs[...,3:4]/255.0
    F[hs,:3]=Hs[hs,:3]*a[hs]+F[hs,:3]*(1-a[hs]); F[hs,3]=np.maximum(F[hs,3],Hs[hs,3])
    return F.clip(0,255).astype(np.uint8)
