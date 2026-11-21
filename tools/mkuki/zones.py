import numpy as np, sys, colorsys
from PIL import Image
from scipy import ndimage as nd
def zones(rgba):
    a=rgba[...,:3].astype(float)/255; al=rgba[...,3]>40
    r,g,b=a[...,0],a[...,1],a[...,2]
    mx=a.max(-1); mn=a.min(-1); L=(mx+mn)/2; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    Z={}
    Z['masker']=al&(g>r+0.12)&(b>r+0.08)
    Z['sjerp']=al&(r>0.30)&(r>g*1.7)&(r>b*1.5)&(s>0.45)
    tun=al&(L>0.55)&(s<0.30)&~Z['masker']
    lab,n=nd.label(tun); sz=nd.sum(tun,lab,range(1,n+1))
    for i,v in enumerate(sz):
        if v<80: tun[lab==i+1]=False          # oogwit en kleine glimmers niet
    Z['tuniek']=tun
    sj=Z['sjerp']; lab,n=nd.label(sj); sz=nd.sum(sj,lab,range(1,n+1))
    for i,v in enumerate(sz):
        if v<60: sj[lab==i+1]=False
    Z['sjerp']=sj
    Z['windsel']=al&(L>0.36)&(L<0.80)&(s>0.18)&(s<0.62)&(r>b+0.06)&(r>=g)&~tun&~Z['sjerp']&~Z['masker']
    Z['broek']=al&(L>0.15)&(L<0.55)&((s<0.20)|((s<0.45)&(b>=r-0.02)))&~tun&~Z['windsel']&~Z['masker']
    # alles opschonen: kleine spikkels weg, gaatjes dicht
    for k in Z:
        m=nd.binary_opening(Z[k],iterations=1) if k!='masker' else Z[k]
        Z[k]=nd.binary_closing(m,iterations=1)&al
    # randpixels (anti-aliasing) bij de zone trekken, zodat er geen lichte rand blijft
    bezet=np.zeros_like(al)
    for k in Z: bezet|=Z[k]
    for k in ('tuniek','masker','sjerp'):
        rand=nd.binary_dilation(Z[k],iterations=2)&al&~bezet&(L>0.30)
        Z[k]|=rand; bezet|=rand
    # losse lichte spikkels (hooglicht, rand) naast een zone: bij de dichtstbijzijnde zone; oogwit (groter) blijft
    licht=al&~bezet&(L>0.45)&(s<0.45)
    lab,n=nd.label(licht); sz=nd.sum(licht,lab,range(1,n+1))
    klein=np.isin(lab,[i+1 for i,v in enumerate(sz) if v<=12])
    keys=list(Z); stack=np.zeros(L.shape,int)-1
    for i,k in enumerate(keys): stack[Z[k]]=i
    dist,idx=nd.distance_transform_edt(stack<0,return_indices=True)
    pak=klein&(dist<=3)
    for i,k in enumerate(keys):
        Z[k]|=pak&(stack[idx[0],idx[1]]==i)
    # grotere lichte stukken die vooral aan een zone grenzen (de rand van de kap) horen daar ook bij
    bezet=np.zeros_like(al)
    for k in Z: bezet|=Z[k]
    licht=al&~bezet&(L>0.45)&(s<0.45)
    lab,n=nd.label(licht)
    for i in range(1,n+1):
        m=lab==i
        ring=nd.binary_dilation(m,iterations=2)&~m&al
        if ring.sum()==0: continue
        best=None;bf=0
        for k in Z:
            f=(ring&Z[k]).sum()/ring.sum()
            if f>bf: bf,best=f,k
        if best and bf>0.30: Z[best]|=m
    return Z,L
def kleur(rgba,Z,L,pal):
    out=rgba.copy().astype(float)
    for k,c in pal.items():
        m=Z[k]
        if not m.any(): continue
        ref=np.median(L[m]); t=np.array(c,float)
        f=np.clip(L[m]/max(ref,1e-3),0.35,1.6)[:,None]
        nc=np.clip(t*f,0,255)
        # zachte rand: alleen volle zone, randpixels half mengen
        out[...,:3][m]=nc
    return out.astype(np.uint8)
