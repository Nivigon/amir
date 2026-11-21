# Asloper (chaser): asgrijs gewaad + hoofddoek, felle oranje sjerp. Huid, khaki broek en staal blijven origineel
# (een houtskool broek gaf geflikker: huid en broek zijn per pixel en per frame niet betrouwbaar te scheiden).
import sys, os, colorsys, shutil
import numpy as np
from PIL import Image
def R(d,m,l,h): return np.array([d,m,l,h],float)
STOPS=np.array([0,0.40,0.70,1.0])
GEW=R((34,34,36),(82,82,86),(130,128,128),(178,174,170))
SJE=R((70,24,6),(160,62,14),(214,110,30),(246,170,80))
BR =R((22,20,20),(46,42,40),(70,64,60),(104,96,90))
def ramp(L,c): return np.stack([np.interp(L,STOPS,c[:,k]) for k in range(3)],-1)
def recolor(im):
    a=np.asarray(im.convert('RGBA')).astype(float); rgb=a[...,:3]; al=a[...,3]
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    mx=rgb.max(-1); mn=rgb.min(-1); v=mx/255; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    hsvh=np.zeros_like(r)
    d=np.maximum(mx-mn,1e-6)
    hsvh=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
    L=((0.299*r+0.587*g+0.114*b)/255)**0.82
    vis=al>0
    blauw=(hsvh>=190)&(hsvh<=280)&(s>=0.08)
    rood=((hsvh>=330)|(hsvh<=4))&(s>=0.50)&(v>=0.18)&(b>g+2)
    huid=(hsvh<=33)&((r-g)>=8)&(s>=0.18)&~rood
    staal=(v>0.48)&(s<0.30)
    # rood onderin de figuur is huid (voeten in de ren), geen sjerp: vlakken met hun midden in het onderste kwart vallen af
    from scipy import ndimage
    ys=np.nonzero(vis)[0]
    if len(ys):
        y0,y1=ys.min(),ys.max(); lab,n=ndimage.label(ndimage.binary_dilation(vis&rood,iterations=1))
        if n:
            cy=np.array(ndimage.center_of_mass(np.ones_like(r),lab,range(1,n+1)))[:,0]
            ok=np.r_[False, cy < y0+0.75*(y1-y0)]
            rood=rood&ok[lab]
    lijn=(v<0.12)&~blauw
    out=rgb.copy()
    out=np.where((vis&blauw)[...,None],ramp(np.clip(L*1.5,0,1),GEW),out)
    out=np.where((vis&rood&~blauw)[...,None],ramp(L,SJE),out)
    # magenta zoom uit de bron (rood en blauw allebei ruim boven groen, ongeveer gelijk): wordt omlijning
    mag=vis&(np.minimum(r,b)-g>18)&(b>0.6*r)&(r>0.6*b)&~blauw
    out=np.where(mag[...,None],np.array([24,22,24.]),out)
    # diepe blauwe schaduw van het gewaad
    out=np.where((vis&blauw&(v<0.12))[...,None],GEW[0],out)
    return Image.fromarray(np.dstack([np.clip(out,0,255),al]).astype(np.uint8),'RGBA')
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]; n=0
    for sub,_,files in os.walk(src):
        dd=os.path.join(dst,os.path.relpath(sub,src)); os.makedirs(dd,exist_ok=True)
        for f in files:
            if f.lower().endswith('.png'): recolor(Image.open(os.path.join(sub,f))).save(os.path.join(dd,f)); n+=1
            else: shutil.copyfile(os.path.join(sub,f),os.path.join(dd,f))
    print(n,'frames ->',dst)
