#!/usr/bin/env python3
"""Strict label placement (ep8 on). Usage: label_strict.py <ep_dir>
For every label WITHOUT an arrow in plan.json, find the position nearest to its current (wish) position where the text box plus a
20 px margin contains no non-white pixel (min(R,G,B) < 228), inside 6%..94% of the frame (visible at 6% zoom). Tries the size, then
85% and 72% of it. Labels with no clean spot are dropped and reported. Arrow labels are left to label_place.py.
Run it AFTER label_place.py, never before: label_place accepts up to 4% ink and misses light lines (rain, heat shimmer, sketches)."""
import sys, os, json, numpy as np
from PIL import Image, ImageFont
D=sys.argv[1]; F=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"pilot","fonts","PatrickHand.ttf"); M=0.06; PAD=20
def fits(a,x0,y0,x1,y1,w,h):
    if x0/w<M or y0/h<M or x1/w>1-M or y1/h>1-M: return False
    return not a[max(0,int(y0)-PAD):int(y1)+PAD, max(0,int(x0)-PAD):int(x1)+PAD].any()
def find(name,text,wx,wy,size):
    im=Image.open(os.path.join(D,"frames",f"{name}.png")).convert("RGB"); w,h=im.size; a=np.asarray(im).min(2)<228
    for sz in (size,int(size*0.85),int(size*0.72)):
        f=ImageFont.truetype(F,int(sz*w/1536)); b=f.getbbox(text); best=None
        for gy in np.arange(0.0,1.0,0.01):
            for gx in np.arange(0.0,1.0,0.01):
                if fits(a,gx*w+b[0],gy*h+b[1],gx*w+b[2],gy*h+b[3],w,h):
                    dd=(gx-wx)**2+(gy-wy)**2
                    if best is None or dd<best[0]: best=(dd,round(float(gx),3),round(float(gy),3))
        if best: return [text,[best[1],best[2]],[best[1],best[2]],[best[1],best[2]],sz]
    return None
p=json.load(open(os.path.join(D,"plan.json"))); out={}
for fr,labs in p["labels"].items():
    for lab in labs:
        text,(tx,ty),A,B,size=lab[:5]
        if A!=B: out.setdefault(fr,[]).append(lab); continue
        r=find(fr,text,tx,ty,size)
        if r: out.setdefault(fr,[]).append(r); print(f"{fr} '{text}' at {r[1]} size {r[4]}")
        else: print(f"DROPPED {fr} '{text}': no clean white spot")
p["labels"]=out; json.dump(p,open(os.path.join(D,"plan.json"),"w"),indent=1)
