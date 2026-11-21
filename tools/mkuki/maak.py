from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
items=[('leeuw.jpg','Lion Warrior'),('schaduw.jpg','Shadow Hunter'),('krijg.jpg','War Chief')]
W,H=1500,820; cw=W//3
t=np.linspace(0,1,H)[:,None,None]
bg=np.array([233,201,143])*(1-t)+np.array([170,120,70])*t
out=Image.fromarray(np.repeat(bg,W,1).astype('uint8')).convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',30)
for k,(fn,name) in enumerate(items):
    a=np.asarray(Image.open(fn).convert('RGB'))[:, :968].astype(float)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=np.maximum(R,B); mn=np.minimum(R,B)
    kk=np.where(mx>0,(mn-G)/np.maximum(mx,1),0)
    al=np.clip((0.45-kk)/0.2,0,1)
    s=np.clip(mn-G,0,None)*(1-al); a[...,0]-=s; a[...,2]-=s
    im=Image.fromarray(np.dstack([np.clip(a,0,255),al*255]).astype('uint8'),'RGBA')
    ys,xs=np.where(al>0.5); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    sc=min((H-130)/im.height,(cw-40)/im.width); im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
    cx=k*cw+cw//2; foot=H-75
    sh=Image.new('RGBA',(W,H)); ImageDraw.Draw(sh).ellipse((cx-im.width*0.42,foot-12,cx+im.width*0.42,foot+12),fill=(60,30,10,110))
    out=Image.alpha_composite(out,sh.filter(ImageFilter.GaussianBlur(5)))
    out.alpha_composite(im,(cx-im.width//2,foot-im.height+6))
    ImageDraw.Draw(out).text((cx,H-30),name,fill=(42,22,8),font=f,anchor='mm')
out.convert('RGB').save('amir_concepten.png')
