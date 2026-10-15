#!/usr/bin/env python3
# Maakt de Duinwacht-bandiet uit de gewone bandietset.
#
#     python3 tools/bandiet_duin_kleur.py
#
# Uit enemies/bandiet/ komt enemies/bandiet_duin/: dezelfde bandiet, maar omgekleurd naar
# een woestijnwacht. Net als bij de elite (tools/bandiet_elite_kleur.js) legt een
# gradient-map de helderheid per pixel op een kleurladder, zodat de tekening, de plooien
# en de contour precies blijven. Vier vlakken, herkend aan tint/verzadiging/helderheid:
#   huid    de warme bruine huid (gezicht, handen, voeten)   -> blijft onveranderd
#   gewaad  het blauwe gewaad + bandana                       -> duinzand
#   sjerp+broek de rode sjerp en de khaki broek               -> brons
#   metaal  het felle staal                                   -> zwaard koper, ogen goud
# De diepe blauwe schaduw van het gewaad wordt opgeruimd (anders zandkleur met navy-spikkels).
# Daarnaast tekent het script grijze wenkbrauwen over de ogen (oude krijger): het zoekt de
# ogen op als de kleine felle vlekken (los van het lange zwaardblad) en tekent er net
# boven twee grijze boogjes. Op frontale frames twee, op profiel een. Een paar frames waar
# de kop wegdraait vragen handwerk achteraf.
#
# Draai hierna tools/gen-klein.py en tools/gen-offline-manifest.py.
import os, sys, colorsys
from collections import deque
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'enemies', 'bandiet')
DST  = os.path.join(ROOT, 'enemies', 'bandiet_duin')

# kleurladders (helderheid 0..1 -> rgb)
duin  = [(0,(64,54,38)),(0.40,(114,98,68)),(0.70,(164,144,102)),(1,(200,182,136))]  # duinzand gewaad
brons = [(0,(50,36,20)),(0.42,(94,68,38)),(0.72,(144,108,64)),(1,(186,148,96))]     # sjerp + broek
koper = [(0,(60,30,18)),(0.42,(120,62,36)),(0.72,(176,100,62)),(1,(216,146,104))]   # zwaardblad
goud  = [(0,(86,60,18)),(0.50,(172,130,42)),(0.80,(218,176,72)),(1,(248,224,150))]  # ogen

def mapramp(L, ramp):
    for i in range(1, len(ramp)):
        if L <= ramp[i][0]:
            a, b = ramp[i-1], ramp[i]; t = (L - a[0]) / ((b[0]-a[0]) or 1)
            return tuple(round(a[1][k] + (b[1][k]-a[1][k])*t) for k in range(3))
    return ramp[-1][1]

def hsv(r,g,b): return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def eye_clusters(px, W, H):
    # felle-metaal pixels, in componenten; compacte clusters in de bovenhelft = ogen
    bright = [[False]*W for _ in range(H)]
    ys_all = []
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            ys_all.append(y)
            h,s,v = hsv(r,g,b)
            if v > 0.50 and s < 0.38: bright[y][x] = True
    if not ys_all: return [], set()
    ymin, ymax = min(ys_all), max(ys_all); figh = ymax - ymin
    seen = [[False]*W for _ in range(H)]; eyes=[]; eyeset=set()
    for y in range(H):
        for x in range(W):
            if bright[y][x] and not seen[y][x]:
                q=deque([(x,y)]); seen[y][x]=True; pix=[]
                while q:
                    cx,cy=q.popleft(); pix.append((cx,cy))
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                        nx,ny=cx+dx,cy+dy
                        if 0<=nx<W and 0<=ny<H and bright[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx]=True; q.append((nx,ny))
                xs=[p[0] for p in pix]; yy=[p[1] for p in pix]
                w=max(xs)-min(xs)+1; hh=max(yy)-min(yy)+1; cy=(min(yy)+max(yy))/2
                # compact + in de bovenste 55% van de figuur = oog (het lange zwaardblad valt af)
                if 10<=len(pix)<=300 and w<=38 and hh<=30 and cy < ymin + figh*0.55:
                    eyes.append((min(xs),min(yy),max(xs),max(yy))); eyeset.update(pix)
    return eyes, eyeset

def recolor(im):
    im = im.convert('RGBA'); px = im.load(); W,H = im.size
    eyes, eyeset = eye_clusters(px, W, H)
    out = im.copy(); op = out.load()
    for y in range(H):
        for x in range(W):
            r,g,b,a = px[x,y]
            if a == 0: continue
            h,s,v = hsv(r,g,b); hd = h*360
            if v < 0.12:
                if 198<=hd<=262 and s>=0.25:            # diepe blauwe schaduw -> donker duin
                    op[x,y]=(duin[0][1][0],duin[0][1][1],duin[0][1][2],a)
                continue                                 # overige contour: zwart laten
            if 7<=hd<=38 and (r-g)>=14 and 0.22<=s<=0.74: continue   # huid behouden
            L = ((0.299*r + 0.587*g + 0.114*b)/255) ** 0.82
            if v>0.50 and s<0.38:
                ramp = goud if (x,y) in eyeset else koper   # ogen goud, zwaard/glans koper
            elif (hd>=344 or hd<=8) and s>=0.45: ramp = brons   # rode sjerp
            elif 198<=hd<=262 and s>=0.15:       ramp = duin    # blauw gewaad
            elif 9<=hd<=58 and s>=0.15:          ramp = brons   # khaki broek + bladlijf
            else:                                ramp = duin
            o = mapramp(L, ramp); op[x,y]=(o[0],o[1],o[2],a)
    # de originele (zwarte) wenkbrauw grijs kleuren: de vorm van de tekenaar blijft, alleen de
    # kleur verandert. Net boven elk oog (de felle vlek) liggen de donkere wenkbrauw-pixels op de
    # huid; de blauwe bandana laten we met rust (die ligt hoger en is blauw in het origineel).
    for ex0,ey0,ex1,ey1 in eyes:
        for yy in range(ey0-8, ey0):                       # net boven het oog, niet op het oog zelf
            for xx in range(ex0-2, ex1+3):
                if not (0<=xx<W and 0<=yy<H): continue
                r,g,b,a = px[xx,yy]                       # het origineel beslist of dit wenkbrauw is
                if a == 0: continue
                h,s,v = hsv(r,g,b)
                if v < 0.24 and not (198<=h*360<=262):    # donkere wenkbrauw, niet de blauwe bandana
                    gg = min(180, int(104 + v*300))       # donker -> middengrijs, lichter -> lichtgrijs
                    op[xx,yy] = (gg, int(gg*0.97), int(gg*0.92), a)   # warm grijs
    return out

def main():
    only = sys.argv[1] if len(sys.argv)>1 else None   # bv "run" om 1 set te testen
    n=kop=0
    for sub, dirs, files in os.walk(SRC):
        rel = os.path.relpath(sub, SRC)
        if only and rel!='.' and not rel.startswith(only): continue
        dd = os.path.join(DST, rel) if rel!='.' else DST
        os.makedirs(dd, exist_ok=True)
        for f in files:
            s=os.path.join(sub,f); d=os.path.join(dd,f)
            if f.lower().endswith('.png'):
                recolor(Image.open(s)).save(d); n+=1
                if n%20==0: print('\r%d frames omgekleurd'%n, end='', flush=True)
            else:
                import shutil; shutil.copyfile(s,d); kop+=1
    print('\nklaar: %d frames omgekleurd, %d bestanden gekopieerd -> %s'%(n,kop,DST))

if __name__=='__main__':
    main()
