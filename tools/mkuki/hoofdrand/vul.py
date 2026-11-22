# vult gaten in het hoofd van een Mkuki-frame met de pixels van het origineel (zelfde canvas, hoofd is identiek)
import numpy as np
from PIL import Image
from scipy import ndimage
def hoofdgat(orig, mk, maxlum=150):
    o=orig.astype(int); m=mk.astype(int)
    oa,ma=o[...,3],m[...,3]
    match=(oa>200)&(ma>200)&(np.abs(o[...,:3]-m[...,:3]).max(-1)<10)
    lab,n=ndimage.label(match)
    if n==0: return None,None
    sz=ndimage.sum(match,lab,range(1,n+1)); k=int(np.argmax(sz))+1
    if sz[k-1]<400: return None,None
    head=lab==k
    cand=(oa>60)&(ma<oa-40)
    lum=(o[...,:3]*[.3,.59,.11]).sum(-1)
    cand&=lum<maxlum
    r=int(__import__("os").environ.get("R","14")); yy,xx=np.mgrid[-r:r+1,-r:r+1]; disk=yy**2+xx**2<=r*r
    dicht=ndimage.binary_closing(np.pad(ma>128,r+1),structure=disk)[r+1:-r-1,r+1:-r-1]
    cand&=dicht
    rood=(ma>128)&(m[...,0]>140)&(m[...,1]<90)&(m[...,2]<90)
    rood&=ndimage.binary_dilation(head,iterations=8)
    if rood.sum()>15:
        hy,hx=ndimage.center_of_mass(head); ry,rx=np.where(rood)
        d=np.array([ry.mean()-hy,rx.mean()-hx]); d/=np.linalg.norm(d)+1e-9
        yy2,xx2=np.mgrid[0:o.shape[0],0:o.shape[1]]
        proj=(yy2-hy)*d[0]+(xx2-hx)*d[1]
        grens=np.percentile((ry-hy)*d[0]+(rx-hx)*d[1],2)-2
        cand&=proj<grens
    # kleur moet in het palet van zijn eigen hoofd zitten (huid, schaduw, omlijning)
    q=lambda x:(x[...,:3]//12)
    pal=np.zeros((22,22,22),bool); hq=q(o)[head]; pal[hq[:,0],hq[:,1],hq[:,2]]=True
    pal=ndimage.binary_dilation(pal,iterations=1)
    oq=q(o); inpal=pal[oq[...,0],oq[...,1],oq[...,2]]
    roze=(o[...,0]-o[...,1]>18)&(o[...,2]-o[...,1]>18)
    cand&=inpal|(oa<200)|roze
    from skimage.morphology import convex_hull_image
    hull=ndimage.binary_dilation(convex_hull_image(head),iterations=int(__import__('os').environ.get('HD','2')))
    cand&=hull
    near=ndimage.binary_dilation(head,iterations=3)
    lab2,n2=ndimage.label(cand)
    keep=np.zeros_like(cand); vast=ma>128
    for i in range(1,n2+1):
        c=lab2==i
        if not (c&near).any() or c.sum()>600: continue
        ring=ndimage.binary_dilation(c)&~c
        frac=(ring&vast).sum()/max(ring.sum(),1)
        if frac>=float(__import__('os').environ.get('FR','0.4')): keep|=c
    return keep,head

def ontzoom(O,M,keep,head):
    """vulpixels van het origineel, met de paarse zoom omgekleurd naar de donkere omlijning van het hoofd"""
    F=M.copy(); o=O.astype(int)
    lum=(o[...,:3]*[.3,.59,.11]).sum(-1)
    hl=lum[head]; donker=o[head][hl<=np.percentile(hl,6)][:,:3].mean(0)
    P=O[keep].astype(int)
    roze=(P[:,0]-P[:,1]>12)&(P[:,2]-P[:,1]>12)
    P[roze,:3]=donker.round().astype(int)
    P[:,3]=np.maximum(P[:,3],M[keep][:,3])
    F[keep]=P.clip(0,255).astype(np.uint8)
    return F

def glad(O,M,maxlum=150):
    """Hele hoofdrand van het origineel: gaten erbij (hoofdgat) en losse uitsteeksels buiten de originele omtrek weg."""
    keep,head=hoofdgat(O,M,maxlum)
    if keep is None: return None,None,None
    o=O.astype(int); m=M.astype(int); oa,ma=o[...,3],m[...,3]
    # alleen echte inkepingen en gaatjes: een smalle strook langs een goede rand laten we staan
    lab,n=ndimage.label(keep); echt=np.zeros_like(keep)
    for i in range(1,n+1):
        c=lab==i
        if ndimage.binary_erosion(c,iterations=1).sum()>=2 or not ndimage.binary_dilation(c,iterations=2)[ma<30].any(): echt|=c
    keep=echt
    from skimage.morphology import convex_hull_image
    hull=ndimage.binary_dilation(convex_hull_image(head),iterations=2)
    rand=hull&ndimage.binary_dilation(head,iterations=4)&~head
    q=lambda x:(x[...,:3]//12)
    pal=np.zeros((22,22,22),bool); hq=q(o)[head]; pal[hq[:,0],hq[:,1],hq[:,2]]=True
    pal=ndimage.binary_dilation(pal,iterations=1)
    mq=q(m); mpal=pal[mq[...,0],mq[...,1],mq[...,2]]
    rood=(m[...,0]>140)&(m[...,1]<90)&(m[...,2]<90)
    # uitsteeksel: Mkuki heeft een hoofdkleurige pixel waar het origineel leeg is, vlak naast het hoofd
    weg=rand&(oa<=25)&(ma>0)&mpal&~rood
    WEGPLEK=True
    # randpixels die in beide bestaan maar anders zijn: ook van het origineel (alleen hoofdkleur, geen kralen)
    o_pal=pal[q(o)[...,0],q(o)[...,1],q(o)[...,2]]|((o[...,0]-o[...,1]>18)&(o[...,2]-o[...,1]>18))
    vervang=rand&(oa>25)&(mpal|(ma<oa-40))&o_pal&~rood&~keep
    def buiten(leeg):
        lab,n=ndimage.label(leeg); rand_ids=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
        return np.isin(lab,list(rand_ids))
    ext=buiten(oa<30)|buiten(ma<30)
    vervang&=ndimage.binary_dilation(ext,iterations=2)
    # zelfde grens bij de kralen als hoofdgat: niets onder de bovenkant van de ketting
    rk=(ma>128)&rood&ndimage.binary_dilation(head,iterations=8)
    g=None
    if rk.sum()>15:
        hy,hx=ndimage.center_of_mass(head); ry,rx=np.where(rk)
        d=np.array([ry.mean()-hy,rx.mean()-hx]); d/=np.linalg.norm(d)+1e-9
        yy,xx=np.mgrid[0:o.shape[0],0:o.shape[1]]
        proj=(yy-hy)*d[0]+(xx-hx)*d[1]
        g=np.percentile((ry-hy)*d[0]+(rx-hx)*d[1],2)-2
        weg&=proj<g; vervang&=proj<g
    weg&=buiten(oa<=25)&ndimage.binary_dilation(buiten(ma<30),iterations=2)&(ndimage.uniform_filter((ma>128).astype(float),5)<0.75)
    rozem=(m[...,0]-m[...,1]>18)&(m[...,2]-m[...,1]>18)&(ma>0)&rand
    defect=ndimage.binary_dilation(keep|weg|rozem,iterations=4)
    vervang&=defect
    F=ontzoom(O,M,keep|vervang,head)
    F[weg]=0
    # gaatjes binnen in het hoofd (rondom Mkuki-huid): opvullen vanuit de huid eromheen, niet uit het origineel
    # randafwerking: paarse zoom en halfdoorzichtige randpixels rond het hoofd krijgen de kleur van de omlijning
    lumh=(o[...,:3]*[.3,.59,.11]).sum(-1); hl=lumh[head]
    donker=o[head][hl<=np.percentile(hl,6)][:,:3].mean(0)
    Fi=F.astype(int)
    ext2=buiten(Fi[...,3]<30)
    rim=ndimage.binary_dilation(ext2,iterations=5)&~ext2&hull&ndimage.binary_dilation(head,iterations=4)
    rim&=~((Fi[...,0]>140)&(Fi[...,1]<90)&(Fi[...,2]<90))
    if g is not None: rim&=proj<g
    rz=(Fi[...,0]-Fi[...,1]>12)&(Fi[...,2]-Fi[...,1]>12)
    lfi=(Fi[...,:3]*[.3,.59,.11]).sum(-1)
    fix=rim&(rz|((Fi[...,3]<230)&(Fi[...,3]>0)&(lfi>lumh[head].mean()*0.9)&(keep|vervang)))
    F[fix,:3]=donker.round().astype(np.uint8)
    keep=keep|fix
    binnen=(keep|vervang)&~ndimage.binary_dilation(buiten(ma<30),iterations=2)
    if binnen.any():
        import cv2
        rgb=np.ascontiguousarray(M[...,:3][...,::-1])
        ip=cv2.inpaint(rgb,binnen.astype(np.uint8)*255,3,cv2.INPAINT_TELEA)[...,::-1]
        F[binnen,:3]=ip[binnen]; F[binnen,3]=255
    return F,keep|vervang|weg,head

def glad2(O,M,sigma=1.1):
    """Hoofdrand: vorm uit het origineel (glad gemaakt), kleur uit het Mkuki-frame zelf."""
    import cv2
    keep,head=hoofdgat(O,M)
    if head is None: return None,None,None
    o=O.astype(int); m=M.astype(int); oa,ma=o[...,3],m[...,3]
    from skimage.morphology import convex_hull_image
    hull=ndimage.binary_dilation(convex_hull_image(head),iterations=2)
    def buiten(leeg):
        lab,n=ndimage.label(leeg); ids=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
        return np.isin(lab,list(ids))
    rood=(m[...,0]>140)&(m[...,1]<90)&(m[...,2]<90)
    Z=hull&ndimage.binary_dilation(head|keep,iterations=2)&~ndimage.binary_erosion(head|keep,iterations=3)&~ndimage.binary_dilation(rood,iterations=2)
    rk=(ma>128)&rood&ndimage.binary_dilation(head,iterations=8)
    if rk.sum()>15:
        hy,hx=ndimage.center_of_mass(head); ry,rx=np.where(rk)
        d=np.array([ry.mean()-hy,rx.mean()-hx]); d/=np.linalg.norm(d)+1e-9
        yy,xx=np.mgrid[0:o.shape[0],0:o.shape[1]]
        proj=(yy-hy)*d[0]+(xx-hx)*d[1]
        Z&=proj<np.percentile((ry-hy)*d[0]+(rx-hx)*d[1],2)-2
    # alleen de buitenrand: de doelvorm is het origineel, glad gemaakt
    r=3; yy0,xx0=np.mgrid[-r:r+1,-r:r+1]; disk=yy0**2+xx0**2<=r*r
    v=np.pad(oa>128,r+2); v=ndimage.binary_closing(v,structure=disk); v=ndimage.binary_opening(v,structure=disk[1:-1,1:-1])
    vorm=v[r+2:-r-2,r+2:-r-2].astype(float)
    T=np.clip((ndimage.gaussian_filter(vorm,sigma)-0.5)*1.6+0.5,0,1)*255
    # niet in de rand rommelen waar het origineel iets anders dan hoofd is (speer, hand): daar alleen weghalen mag niet
    Z&=ndimage.binary_dilation(buiten(oa<30)|buiten(ma<30),iterations=3)
    paars=(m[...,0]-m[...,1]>12)&(m[...,2]-m[...,1]>12)
    vast=(ma>=235)&~paars
    onbekend=~vast
    rgb=np.ascontiguousarray(M[...,:3][...,::-1]).copy()
    inp=cv2.inpaint(rgb,(onbekend&ndimage.binary_dilation(Z|keep,iterations=6)).astype(np.uint8)*255,4,cv2.INPAINT_TELEA)[...,::-1]
    F=M.copy()
    nieuw=Z&(np.abs(T-ma)>8)
    # dekking omlaag alleen bij uitsteeksels (weinig vast lijf eromheen), nooit midden in het hoofd
    omlaag=T<ma-8
    spits=ndimage.uniform_filter((ma>128).astype(float),7)<0.62
    nieuw&=~omlaag|spits
    F[nieuw,3]=T[nieuw].round().astype(np.uint8)
    zet=(nieuw|(Z&paars&(ma>0)))&onbekend
    F[zet,:3]=inp[zet]
    # gaatjes binnenin en diepe inkepingen buiten Z: kleur uit de omgeving, dekking uit de vorm
    rest=keep&~Z
    F[rest,:3]=inp[rest]; F[rest,3]=np.maximum(F[rest,3],T[rest].round().astype(np.uint8))
    F[(F[...,3]==0)]=0
    return F,nieuw|rest|(Z&paars&(ma>0)),head
