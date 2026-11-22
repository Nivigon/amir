# Past de hoofdrand (methode synth) toe op alle Mkuki-lijven, vanaf de versie van voor de eerste fix.
import sys, os, json, shutil; sys.path.insert(0,'/home/claude/lijn'); sys.path.insert(0,'/home/claude/gat')
import numpy as np; from PIL import Image
from scipy import ndimage
from gem import L, orig
from rand import maak, kopmaat
from sw04 import maak as sw04
OUD='/home/claude/oud/karakters/amir/mkuki'; MK='/home/claude/mkb/karakters/amir/mkuki'
rows=json.load(open('/home/claude/lijn/kopinfo.json'))
def kopset(p):
    st=p.rsplit('/',1)[0]; return float(np.median([r[1] for r in rows if r[0].rsplit('/',1)[0]==st]))
# alles eerst terug naar de toestand van voor de eerste fix
for p in L:
    for suf in ['.png','_zones.png','_vuist.png','_vuist_zones.png']:
        src=OUD+'/'+p[:-4]+suf
        if os.path.exists(src): shutil.copy(src, MK+'/'+p[:-4]+suf)
log={}
# speerworp 4: vuist en voorhoofd uit frame 3 (zelfde houding), daarna gewoon mee in de lijn-stap
d=MK+'/speerworp/'
M4=np.array(Image.open(d+'speerworp_04.png').convert('RGBA')); M3=np.array(Image.open(d+'speerworp_03.png').convert('RGBA'))
F=sw04(M4,M3); Image.fromarray(F).save(d+'speerworp_04.png', optimize=True)
yy,xx=np.mgrid[0:F.shape[0],0:F.shape[1]]
hand=(M3[...,3]>0)&(xx<=239)&(yy>147)&(yy<300)
V=np.zeros_like(M3); hs=np.roll(np.roll(hand,-3,0),-2,1); V[hs]=np.roll(np.roll(M3,-3,0),-2,1)[hs]
Image.fromarray(V).save(d+'speerworp_04_vuist.png', optimize=True)
Image.fromarray(np.zeros_like(V)).save(d+'speerworp_04_vuist_zones.png', optimize=True)
Z=np.array(Image.open(d+'speerworp_04_zones.png').convert('RGBA')); Z[F[...,3]==0]=0; Z[(xx<260)&(yy>140)&(yy<314)]=0
Image.fromarray(Z).save(d+'speerworp_04_zones.png', optimize=True)
for p in L:
    O=np.array(Image.open(orig(p)).convert('RGBA')); M=np.array(Image.open(MK+'/'+p).convert('RGBA'))
    ks=kopset(p)
    F,info=maak(O,M,'synth',kop_set=ks)
    if F is None: log[p]='geen hoofd'; continue
    verh=info['kop']/ks
    ch=(np.abs(F.astype(int)-M.astype(int)).max(-1)>3)
    log[p]=dict(kop=info['kop'],verh=round(verh,2),bron=info['bron'],gem=round(info['gem'],2),D=info['D'],px=int(ch.sum()),
                ver=int((ch&(ndimage.distance_transform_edt(~info['h'])>0.6*ks)).sum()))
    np.save('/home/claude/lijn/nieuw/'+p.replace('/','__')+'.npy',F)
json.dump(log,open('/home/claude/lijn/log.json','w'),indent=0)
print(len(log))
