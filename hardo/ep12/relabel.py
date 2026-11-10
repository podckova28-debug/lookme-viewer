import sys, os, json, numpy as np
from PIL import Image, ImageFont
F="/home/user/lookme-viewer/hardo/pilot/fonts/PatrickHand.ttf"; M=0.06; PAD=20
def fits(a,x0,y0,x1,y1,w,h):
    if x0/w<M or y0/h<M or x1/w>1-M or y1/h>1-M: return False
    return not a[max(0,int(y0)-PAD):int(y1)+PAD, max(0,int(x0)-PAD):int(x1)+PAD].any()
def box(text,x,y,size,w,h):
    f=ImageFont.truetype(F,int(size*w/1536)); b=f.getbbox(text); return (x*w+b[0],y*h+b[1],x*w+b[2],y*h+b[3])
CACHE={}
def mask(name):
    if name not in CACHE: CACHE[name]=np.asarray(Image.open(f"frames/{name}.png").convert("RGB")).min(2)<228
    return CACHE[name]
def find(name,text,wx,wy,sizes,occ):
    a=mask(name).copy(); h,w=a.shape
    for x0,y0,x1,y1 in occ: a[max(0,int(y0)):int(y1)+1, max(0,int(x0)):int(x1)+1]=True
    for sz in sizes:
        f=ImageFont.truetype(F,int(sz*w/1536)); b=f.getbbox(text); best=None
        for gy in np.arange(0.0,1.0,0.01):
            for gx in np.arange(0.0,1.0,0.01):
                if fits(a,gx*w+b[0],gy*h+b[1],gx*w+b[2],gy*h+b[3],w,h):
                    dd=(gx-wx)**2+(gy-wy)**2
                    if best is None or dd<best[0]: best=(dd,round(float(gx),3),round(float(gy),3))
        if best: return [text,[best[1],best[2]],[best[1],best[2]],[best[1],best[2]],sz]
    return None
