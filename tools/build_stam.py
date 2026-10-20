#!/usr/bin/env python3
"""Stapel de paal (stam) tot een gewenste hoogte: top + mid herhaald + bottom.
Gebruik: python3 build_stam.py <hoogte_in_px> <uitvoer.png>
Het middenstuk (stam_mid.png) is naadloos, dus de kopieen sluiten op elkaar aan.
"""
import sys, os
import numpy as np
from PIL import Image

HERE=os.path.dirname(os.path.abspath(__file__))
ASSETS=os.path.join(HERE,"..","design","takelwiel","stam")

def load(name): return Image.open(os.path.join(ASSETS,name)).convert("RGBA")

def stack(parts, ov=14):
    parts=[np.array(p).astype(np.float32) for p in parts]
    w=parts[0].shape[1]
    total=sum(p.shape[0] for p in parts)-ov*(len(parts)-1)
    canv=np.zeros((total,w,4),np.float32); wt=np.zeros((total,1),np.float32); y=0
    for i,p in enumerate(parts):
        ph=p.shape[0]; win=np.ones((ph,1),np.float32)
        if i>0: win[:ov,0]=np.linspace(0,1,ov)
        if i<len(parts)-1: win[ph-ov:,0]*=np.linspace(1,0,ov)
        canv[y:y+ph]+=p*win[...,None]; wt[y:y+ph]+=win; y+=ph-ov
    wt[wt==0]=1
    return Image.fromarray(np.clip(canv/wt[...,None],0,255).astype(np.uint8))

def build(height_px, ov=14):
    top,mid,bottom=load("stam_top.png"),load("stam_mid.png"),load("stam_bottom.png")
    fixed=top.height+bottom.height-2*ov
    n=max(1, round((height_px-fixed)/(mid.height-ov)))
    return stack([top]+[mid]*n+[bottom], ov)

if __name__=="__main__":
    h=int(sys.argv[1]) if len(sys.argv)>1 else 1500
    out=sys.argv[2] if len(sys.argv)>2 else "stam_out.png"
    img=build(h); img.save(out)
    print("stam gebouwd:", img.size, "->", out)
