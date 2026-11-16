# Eenmalig gebruikt (16-11-2026): de doorstap-clip (3.mp4, omgerekend x1,02 naar normaalrechts-coordinaten in /tmp/c3/ns)
# naar lijf-frames voor de Animeer tool Amir stokken, met root motion per frame.
# Stapslag: clipframes 19-46 uit 1.mp4 naar de Animeer tool Amir stokken (594x301, grond 297, anker 297)
import numpy as np, cv2, json, sys
from PIL import Image
SRC='/tmp/c3/ns/%03d.png'   # clip 3 (doorstap), omgerekend naar normaalrechts-coordinaten (x1,02)
F0,F1=19,46
DX=0
S=0.95; CP=(356,377); TP=(297,297); W,H=594,301; L=115
def voeten(rgb):
  a=rgb.astype(int); m=((np.minimum(a[:,:,0],a[:,:,2])-a[:,:,1])<90)
  x=np.where(m[355:380].any(0))[0]; g=[];s=x[0];pv=x[0]
  for v in x[1:]:
    if v-pv>6: g.append((s,pv)); s=v
    pv=v
  g.append((s,pv)); return g
SLUIT={}   # stok over het hoofd: groter dichtmaken
OPEN={}         # dunne stokveeg weg
def verwerk(rgb,f=None):
  a=rgb.astype(np.float32); r,g,b=a[...,0],a[...,1],a[...,2]
  mx=np.maximum(np.maximum(r,b),1)
  k=np.clip((np.minimum(r,b)-g)/mx,0,1)            # magenta-score
  alpha=np.clip((0.92-k)/(0.92-0.62),0,1)
  groen=(((g-np.maximum(r,b))>35)&(g>90))|(((g-r)>45)&(b>r))|(((b-r)>45)&((g-r)>15))
  groenR=cv2.dilate(groen.astype(np.uint8),np.ones((5,5),np.uint8))>0
  # olijf/donkergroene rand van de stok
  rand=cv2.dilate(groenR.astype(np.uint8),np.ones((3,3),np.uint8))>0
  rand&=(g>r+8)
  # lichte koele vegen van de stok (wit, lichtblauw): grote vlekken weg, de oogjes blijven
  licht=(((np.minimum(np.minimum(r,g),b)>130)&(b>=g-5))|((g>r+15)&(b>r+30)))&(alpha>0.3)
  n2,lab2,st2,_=cv2.connectedComponentsWithStats(licht.astype(np.uint8))
  veeg=np.zeros_like(licht)
  for i in range(1,n2):
    if st2[i,cv2.CC_STAT_AREA]>25: veeg|=lab2==i
  veeg=cv2.dilate(veeg.astype(np.uint8),np.ones((3,3),np.uint8))>0
  weg=groenR|rand|veeg
  lijf=(alpha>0.5)&~weg
  # gaten van de stok in het lijf: sluiten en invullen
  dicht=cv2.morphologyEx(lijf.astype(np.uint8),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(SLUIT.get(f,7),)*2))>0
  gat=dicht&weg
  out=rgb.copy()
  # magenta-besmetting in vegen (roze armen, roze randjes): opvullen uit de buren
  besm=(r-g>35)&(b-g>35)&(r>105)&(alpha>0.5)&~weg
  besm=cv2.dilate(besm.astype(np.uint8),np.ones((3,3),np.uint8))>0
  # groene zweem op de vuisten: groen niet boven rood
  bij=cv2.dilate(groen.astype(np.uint8),np.ones((15,15),np.uint8))>0
  oi=out.astype(int); zweem=(((oi[...,1]>0.8*oi[...,0])&(oi[...,2]<0.45*oi[...,1]))|(bij&(oi[...,1]>0.72*oi[...,0])&(oi[...,1]>oi[...,2])))&(alpha>0.3)
  out[...,1]=np.where(zweem,(0.62*oi[...,0]).astype(int),oi[...,1]).astype(np.uint8)
  out[...,2]=np.where(zweem,np.maximum(oi[...,2],(0.5*oi[...,0]).astype(int)),oi[...,2]).astype(np.uint8)
  vul=(gat|besm)
  # de achtergrond eerst de kleur van het dichtstbijzijnde lijfpixel geven, anders trekt inpaint magenta naar binnen
  goed=((alpha>0.9)&~weg&~besm).astype(np.uint8)
  _,lbl=cv2.distanceTransformWithLabels(1-goed,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
  ys,xs=np.where(goed>0); idx=np.zeros(lbl.max()+1,int); idx[lbl[ys,xs]]=np.arange(len(ys))
  nb=out[ys[idx[lbl]],xs[idx[lbl]]]
  out=np.where(goed[...,None]>0,out,nb).astype(np.uint8)
  if vul.any(): out=cv2.inpaint(out,(vul*255).astype(np.uint8),5,cv2.INPAINT_TELEA)
  al=alpha.copy(); al[weg]=0; al[gat]=1
  # alleen het lijf en wat er tegenaan ligt
  n,lab,st,_=cv2.connectedComponentsWithStats((al>0.3).astype(np.uint8))
  if n>1:
    big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); hoofd=lab==big
    near=cv2.dilate(hoofd.astype(np.uint8),np.ones((7,7),np.uint8))>0
    al[(al>0)&~near]=0
  if f in OPEN:
    k_=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(OPEN[f],)*2)
    romp=cv2.morphologyEx((al>0.5).astype(np.uint8),cv2.MORPH_OPEN,k_)
    romp=cv2.dilate(romp,np.ones((3,3),np.uint8))>0
    al[~romp]=0
    n3,lab3,st3,_=cv2.connectedComponentsWithStats((al>0.3).astype(np.uint8))
    if n3>1: al[lab3!=1+np.argmax(st3[1:,cv2.CC_STAT_AREA])]=0
  # despill: magenta uit de randen
  o=out.astype(np.float32); spill=(al<1)&(al>0)
  lim=o[...,1]+20
  o[...,0]=np.where(spill,np.minimum(o[...,0],np.maximum(lim,o[...,0]*0.8)),o[...,0])
  o[...,2]=np.where(spill,np.minimum(o[...,2],lim),o[...,2])
  return np.dstack([np.clip(o,0,255),al*255]).astype(np.uint8), groen
def naarTool(rgba,sx=0.0):
  M=np.float32([[S,0,TP[0]-S*(CP[0]-DX)+sx],[0,S,TP[1]-S*CP[1]]])
  pm=rgba.astype(np.float32); pm[...,:3]*=pm[...,3:]/255
  w=cv2.warpAffine(pm,M,(W,H),flags=cv2.INTER_AREA if S<1 else cv2.INTER_LINEAR,borderValue=0)
  a=w[...,3:]; w[...,:3]=np.where(a>0,w[...,:3]*255/np.maximum(a,1e-3),0)
  return np.clip(w,0,255).astype(np.uint8)
SX=0.0
def pt(x,y): return ((x+DX-CP[0])*S+TP[0]+SX,(y-CP[1])*S+TP[1])
def lijnen(groen):
  global ROMP
  n,lab,st,_=cv2.connectedComponentsWithStats(groen.astype(np.uint8))
  comps=[]
  for i in range(1,n):
    if st[i,cv2.CC_STAT_AREA]<40: continue
    ys,xs=np.where(lab==i); P=np.c_[xs,ys].astype(float); c=P.mean(0)
    _,_,vt=np.linalg.svd(P-c); d=vt[0]; comps.append([P,c,d])
  # samenvoegen wat op een lijn ligt (de vuist onderbreekt de stok)
  groepen=[]
  for P,c,d in sorted(comps,key=lambda q:-len(q[0])):
    for gp in groepen:
      Q,cq,dq=gp; ang=abs(np.dot(d,dq))
      perp=abs(dq[0]*(c-cq)[1]-dq[1]*(c-cq)[0])
      if ang>0.96 and perp<10: gp[0]=np.r_[Q,P]; break
    else: groepen.append([P,c,d])
  res=[]
  for P,c,d in groepen[:2]:
    c=P.mean(0); _,_,vt=np.linalg.svd(P-c); d=vt[0]
    t=(P-c)@d; ts=np.sort(t)
    gaps=np.diff(ts); j=np.argmax(gaps) if len(gaps) else 0
    if len(gaps) and gaps[j]>8:
      gm=(ts[j]+ts[j+1])/2
      kort,lang=(ts[:j+1],ts[j+1:]) if j+1<len(ts)/2 else (ts[j+1:],ts[:j+1])
      vuist=c+d*gm
      u=d if np.mean(lang)>gm else -d
    else:
      # geen gat: de vuist zit aan het eind dat het dichtst bij het lijf ligt (laagste punt is de punt niet zeker); kies het korte eind niet
      e1,e2=c+d*ts[0],c+d*ts[-1]
      # de vuist zit aan het eind dat het dichtst bij de schouders ligt
      if np.hypot(*(e1-ROMP))<np.hypot(*(e2-ROMP)): vuist,u=e1,d
      else: vuist,u=e2,-d
      res.append(dict(vuist=vuist,u=u,c=c,len=len(P),gok=True)); continue
    res.append(dict(vuist=vuist,u=u,c=c,len=len(P),gok=False))
  return res
frames=[];vorige=None
LIJST=list(range(8,64,2))
for f in LIJST:
  rgb=np.array(Image.open(SRC%(f+1)).convert('RGB'))
  if vorige is not None and (np.abs(rgb.astype(int)-vorige.astype(int)).max(2)>40).mean()<0.012:
    frames[-1]['ms']+=84; frames[-1]['dub'].append(f); continue
  vorige=rgb
  frames.append(dict(f=f,rgb=rgb,ms=84,dub=[]))
print(len(frames),'unieke frames:',[x['f'] for x in frames])
# root motion: de geplante voet vastzetten vanaf frame 26 (achtervoet staat dan naast de voorvoet)
P={}
vals=[294,296,296,296,296,296,296,295,294,292,290,288]
for i,v in enumerate(vals): P[8+i]=v
for i,v in enumerate([285,282,279,276]): P[20+i]=v
for i,v in enumerate([274,270,268,266,262,260,259,258,256,256,254,252]): P[24+i]=v
ROOT={}; acc=0.0
for f in range(0,146):
  if f<=8: ROOT[f]=0.0; continue
  if f<=35: d=P.get(f,P[35] if f>35 else None)-P.get(f-1)
  else:
    nf=[422,422,420,418,416,414,412,408,406,406,404,402]
    a=nf[min(f-35,11)]; b=nf[min(f-36,11)]; d=a-b
  acc-=d; ROOT[f]=acc
SCHUIF=55.0                 # tool-px: het canvas schuift tijdens de stap zoveel naar links (anders valt het eind erbuiten)
def helling(f): return max(0.0,min(1.0,(f-8)/(35-8)))
for x in frames:
  x['schuif']=-SCHUIF*helling(x['f'])
  x['root']=float(ROOT[x['f']]*1.02*S - x['schuif'])
out={'anim':'stapslag','frames':[]}
vorigL=None
for i,x in enumerate(frames):
  rgba,groen=verwerk(x['rgb'],x['f'])
  globals()['SX']=x['schuif']
  Image.fromarray(naarTool(rgba,SX)).save(f'/home/claude/stapslag/f3/stapslag_{i:02d}.png')
  ys,xs=np.where(rgba[...,3]>128); top=ys<np.percentile(ys,45)
  ROMP=np.array([xs[top].mean(),ys[top].mean()])
  ls=lijnen(groen); items={}
  for l in ls:
    vx,vy=pt(*l['vuist']); u=l['u']
    cx,cy=vx+u[0]*0.3*L, vy+u[1]*0.3*L
    rot=float(np.degrees(np.arctan2(-u[1],-u[0])))
    l.update(cx=cx,cy=cy,rot=rot,vx=vx,vy=vy)
  # naam: eerst op hoogte (achter = hoog), daarna volgen op de vorige
  if vorigL is None:
    ls.sort(key=lambda l:l['vy']); namen=['stok_achter','stok_voor'][:len(ls)]
  else:
    namen=[]
    for l in ls:
      best=min(vorigL,key=lambda k:(vorigL[k]['vx']-l['vx'])**2+(vorigL[k]['vy']-l['vy'])**2)
      namen.append(best)
    if len(set(namen))<len(namen): namen=[min(vorigL,key=lambda k:(vorigL[k]['vx']-ls[0]['vx'])**2+(vorigL[k]['vy']-ls[0]['vy'])**2)]; namen.append('stok_voor' if namen[0]=='stok_achter' else 'stok_achter')
  cur={}
  for n,l in zip(namen,ls): cur[n]=l
  for n in ('stok_voor','stok_achter'):
    if n not in cur and vorigL and n in vorigL: cur[n]=vorigL[n]   # niet gevonden: houd de vorige
  vorigL=cur
  L_={n:dict(on=True,angle='zij',cx=round(l['cx']/W,4),cy=round(l['cy']/H,4),w=round(L/W,4),rot=int(round(l['rot'])),flip=False,behind=False,op=1,locked=False) for n,l in cur.items()}
  body={'basis':[{'t':'voor','s':0.037,'p':[[round(l['vx']/W,4),round(l['vy']/H,4)],[round((l['vx']+1)/W,4),round(l['vy']/H,4)]]} for l in cur.values()]}
  out['frames'].append(dict(src=f'f/stapslag_{i:02d}.png',orig=x['f'],ms=x['ms'],root=round(x['root'],1),L=L_,body=body,gok=[bool(l.get('gok')) for l in cur.values()]))
json.dump(out,open('/home/claude/stapslag/stapslag3.json','w'),indent=1)
for fr in out['frames']: print(fr['orig'],fr['ms'],fr['root'],{k:(v['rot'],round(v['cx']*W),round(v['cy']*H)) for k,v in fr['L'].items()},fr['gok'])
