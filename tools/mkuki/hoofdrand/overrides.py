import sys; sys.path.insert(0,'/home/claude/lijn')
import numpy as np, json; from PIL import Image
from handkop import HAND, handkop
from gem import orig
from rand import maak
from rolfix import vul_kop; from rolcirkels import CIRK
rows=json.load(open('/home/claude/lijn/kopinfo.json'))
MK='/home/claude/mkb/karakters/amir/mkuki'
def kopset(p):
    st=p.rsplit('/',1)[0]; return float(np.median([r[1] for r in rows if r[0].rsplit('/',1)[0]==st]))
OUDD='/home/claude/oud/karakters/amir/mkuki'
def laadM(p): return np.array(Image.open(OUDD+'/'+p).convert('RGBA'))
for p in HAND:
    M=laadM(p); O=np.array(Image.open(orig(p)).convert('RGBA')); h=handkop(p,M)
    F,_=maak(O,M,'synth',h=h,keep=np.zeros_like(h),kop_set=kopset(p)); np.save('/home/claude/lijn/nieuw/'+p.replace('/','__')+'.npy',F)
for n in CIRK:
    p=f'beweging/rol/met/rol_{n}.png'; M=laadM(p); O=np.array(Image.open(orig(p)).convert('RGBA'))
    A,head,onb=vul_kop(M,n)
    F,_=maak(O,A,'synth',h=head,keep=np.zeros_like(head),kop_set=kopset(p)); np.save('/home/claude/lijn/nieuw/'+p.replace('/','__')+'.npy',F)
p='aanval/combo/combo_05.png'; np.save('/home/claude/lijn/nieuw/'+p.replace('/','__')+'.npy',laadM(p))
print('overrides klaar')
