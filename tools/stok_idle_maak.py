#!/usr/bin/env python3
"""De idle met de stokken op de schouders (STOK.idle) uit de Grok-lus.

Bron: karakters/amir/stokken/bron/idle/grok_9771961b.mp4 (Grok-post 9771961b, groene stokken op magenta). Eerst de frames
eruit:  ffmpeg -i karakters/amir/stokken/bron/idle/grok_9771961b.mp4 karakters/amir/stokken/bron/idle/ruw/f_%03d.png
Dan:    python3 tools/stok_idle_maak.py
Uit (in de bronmap): uit/idle_NN.png (18 frames, een ademhaling, clipframe 78 tot 129 om de 3, de knipper eruit) op het
STOK-canvas, en punt.json met de knopen voor STOK.slip.punt.idle. Kopieer uit/ naar karakters/amir/stokken/idle/ en
klein/karakters/amir/stokken/idle/, draai node tools/vacht_bak.js --alleen stokken/idle en tools/gen-offline-manifest.py.
Het groen wordt omgekleurd naar de stok (donker hout, okerkleurige grip aan het onderste kwart), niet weggeknipt.
"""
import numpy as np, json
from PIL import Image
from scipy import ndimage
import sys
R=sys.argv[1] if len(sys.argv)>1 else 'karakters/amir/stokken/bron/idle/'
IDX=list(range(78,130,3))           # een ademhaling, loopt rond (78 ~ 130)
BLINK={84:81,87:90}                 # knipperframes: ogen uit het buurframe
S=275/612                           # schaal naar de staan-frame van STOK
W,H,GR=511,384,378                  # STOK-canvas, voeten op 378
HOUT=np.array([40,31,27.]); GRIP=np.array([170,108,40.])
def lees(i): return np.array(Image.open(R+'ruw/f_%03d.png'%(i+1)).convert('RGB')).astype(float)
def key(a):
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(np.minimum(r,b)-g)/np.maximum(np.maximum(r,b),1)
    bgl=(m>0.5)&(r>140)&(b>100)
    lab,n=ndimage.label(bgl); sz=ndimage.sum(bgl,lab,range(1,n+1))
    bg=np.isin(lab,[k+1 for k,s in enumerate(sz) if s>60])
    rand=ndimage.binary_dilation(bg,iterations=2)&~bg
    al=np.ones(a.shape[:2]); al[bg]=0
    soft=np.clip((0.62-m)/0.3,0,1); al[rand]=np.minimum(al[rand],soft[rand])
    ex=np.clip(np.minimum(r,b)-g,0,None)*(1-al)          # despill aan de rand
    rgb=np.stack([r-ex,g,b-ex],-1)
    return rgb,al
def stokken(rgb,al):
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    gr=np.clip((g-np.maximum(r,b)-4)/45,0,1)*(al>0.3)
    m=gr>0.2
    ys,xs=np.nonzero(m); P=np.stack([xs,ys],1).astype(float); c=P.mean(0)
    _,_,vt=np.linalg.svd(P-c); d=vt[0]; nrm=np.array([-d[1],d[0]])
    if d[1]<0: d=-d                                     # d wijst omlaag (naar de handen)
    off=(P-c)@nrm; split=np.median(off)
    # twee groepen op de dwarsafstand
    for _ in range(10):
        a1=off[off<split].mean(); a2=off[off>=split].mean(); split=(a1+a2)/2
    lijnen=[]; grip=np.zeros(m.shape,bool)
    for sel in (off<split, off>=split):
        Q=P[sel]; cq=Q.mean(0); t=(Q-cq)@d; lo,hi=t.min(),t.max()
        g_sel=t>hi-0.27*(hi-lo)
        grip[Q[g_sel,1].astype(int),Q[g_sel,0].astype(int)]=True
        lijnen.append((cq+d*lo, cq+d*hi))              # boven, onder
    grip=ndimage.binary_dilation(grip,iterations=2)
    l=np.clip(g/255,0,1)[...,None]
    kl=np.where(grip[...,None],GRIP,HOUT)*(0.6+0.8*l)
    nieuw=rgb*(1-gr[...,None])+np.clip(kl,0,255)*gr[...,None]
    return nieuw,lijnen
def ogen(a,b):                        # oogvlak van b op a, na uitlijnen op het hoofd
    y0,y1,x0,x1=130,230,470,620
    best=None
    for dy in range(-4,5):
        for dx in range(-4,5):
            e=np.abs(a[y0:y1,x0:x1]-b[y0+dy:y1+dy,x0+dx:x1+dx]).mean()
            if best is None or e<best[0]: best=(e,dx,dy)
    _,dx,dy=best; a=a.copy()
    a[160:200,480:600]=b[160+dy:200+dy,480+dx:600+dx]
    return a
out={'frames':[],'punt':[]}
for k,i in enumerate(IDX):
    a=lees(i)
    if i in BLINK: a=ogen(a,lees(BLINK[i]))
    rgb,al=key(a)
    rgb,lijnen=stokken(rgb,al)
    im=Image.fromarray(np.dstack([np.clip(rgb,0,255),al*255]).astype(np.uint8))
    if k==0:
        ys,xs=np.nonzero(al>0.5); bot=ys.max()
        pa=(al>0.5)&(rgb[...,2]>rgb[...,0])&(rgb[...,2]>rgb[...,1]+15)&(np.arange(a.shape[0])[:,None]>450)
        cx=np.nonzero(pa)[1].mean()
        T=(300.6-cx*S, GR-bot*S)                     # broek boven de broek van staan, voeten op de grond
        print('voet',bot,'broek x',cx,'T',T)
    w,h=im.size; im=im.resize((round(w*S),round(h*S)),Image.LANCZOS)
    c=Image.new('RGBA',(W,H)); c.alpha_composite(im,(round(T[0]),round(T[1])))
    c.save(R+'uit/idle_%02d.png'%k)
    # knoop van de slip: net onder de hand, 8 procent van de stok boven het onderste eind
    pt=[]
    for j,(top,ond) in enumerate(lijnen):
        kn=ond+(top-ond)*0.08
        pt+= [round(kn[0]*S+T[0],1), round(kn[1]*S+T[1],1), 1 if j==1 else 0]
    out['punt'].append(pt)
json.dump(out,open(R+'punt.json','w'))
print(len(IDX), out['punt'][0])
