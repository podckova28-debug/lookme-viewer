#!/usr/bin/env python3
"""Strict arrow placement (ep8 on). Usage: label_arrow.py <ep_dir> [targets.json]
For every label WITH an arrow: the target point T must lie INSIDE the named object. Searches text positions where
 - the text box + 20 px margin is pure white (min(R,G,B) >= 228), inside 6%..94% of the frame;
 - the arrow (same curve as assemble_ep.draw_arrow) runs over white only until it first touches ink;
 - that first ink hit belongs to the same connected drawing as T (so the arrow ends on the edge of the named object, not on something in between);
 - arrow length (start to the first ink hit) is 6.5%..25% of the frame width; qa_check fails arrows under 6%.
Picks the shortest such arrow closest to the wish position; the tip is set to the first ink hit (object edge).
Labels with no clean arrow keep their text without an arrow (strict white placement) or are dropped; all choices are reported."""
import sys, os, json, math, numpy as np
from PIL import Image, ImageFont
D=sys.argv[1]; TG=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
F=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"pilot","fonts","PatrickHand.ttf"); M=0.06; PAD=20
def curve(x1,y1,x2,y2,k=1,n=60):
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; cx,cy=mx-k*dy*0.18,my+k*dx*0.18
    return [((1-t)**2*x1+2*(1-t)*t*cx+t**2*x2,(1-t)**2*y1+2*(1-t)*t*cy+t**2*y2) for t in [i/n for i in range(n+1)]]
def edge_point(x0,y0,x1,y1,tx,ty):
    cx,cy=(x0+x1)/2,(y0+y1)/2; dx,dy=tx-cx,ty-cy
    if dx==0 and dy==0: return cx,cy
    tX=((x1 if dx>0 else x0)-cx)/dx if dx else 1e9; tY=((y1 if dy>0 else y0)-cy)/dy if dy else 1e9
    t=min(tX,tY); return cx+dx*t+(6 if dx>0 else -6)*(abs(tX)<=abs(tY)), cy+dy*t+(6 if dy>0 else -6)*(abs(tY)<abs(tX))
def place(name,text,wx,wy,tx,ty,size,k=1):
    im=Image.open(os.path.join(D,"frames",f"{name}.png")).convert("RGB"); w,h=im.size; a=np.asarray(im).min(2)
    white=a>=228; ink=a<200; T=(tx*w,ty*h)
    if not ink[min(h-1,int(T[1])),min(w-1,int(T[0]))]:
        # nudge T onto the nearest ink within 40 px (target must be inside the object)
        ys,xs=np.nonzero(ink[max(0,int(T[1])-40):int(T[1])+40,max(0,int(T[0])-40):int(T[0])+40])
        if not len(xs): return None,"target not on ink"
        i=((xs+max(0,int(T[0])-40)-T[0])**2+(ys+max(0,int(T[1])-40)-T[1])**2).argmin(); T=(xs[i]+max(0,int(T[0])-40),ys[i]+max(0,int(T[1])-40))
    # the named object = the connected ink region containing T (BFS on a 2x downsampled mask)
    from collections import deque
    m=ink[::2,::2]; hh,ww=m.shape; comp=np.zeros_like(m,bool); q=deque([(int(T[1])//2,int(T[0])//2)])
    if not m[q[0]]: q=deque()
    while q:
        y,x=q.popleft()
        if y<0 or x<0 or y>=hh or x>=ww or comp[y,x] or not m[y,x]: continue
        comp[y,x]=True; q.extend(((y+1,x),(y-1,x),(y,x+1),(y,x-1)))
    def on_object(px,py):
        y,x=int(py)//2,int(px)//2
        return comp[max(0,y-2):y+3,max(0,x-2):x+3].any()
    best=None
    for sz in (size,int(size*0.85),int(size*0.72)):
        f=ImageFont.truetype(F,int(sz*w/1536)); b=f.getbbox(text)
        for gy in np.arange(0.0,1.0,0.01):
            for gx in np.arange(0.0,1.0,0.01):
                x0,y0,x1,y1=gx*w+b[0],gy*h+b[1],gx*w+b[2],gy*h+b[3]
                if x0/w<M or y0/h<M or x1/w>1-M or y1/h>1-M: continue
                if not white[max(0,int(y0)-PAD):int(y1)+PAD, max(0,int(x0)-PAD):int(x1)+PAD].all(): continue
                sx,sy=edge_point(x0-8,y0-8,x1+8,y1+8,*T)
                L=math.hypot(T[0]-sx,T[1]-sy)
                if not (0.05*w <= L <= 0.27*w): continue
                pts=curve(sx,sy,T[0],T[1],k); hit=None; ok=True
                for (px,py) in pts:
                    ix,iy=int(px),int(py)
                    if not (0<=ix<w and 0<=iy<h): ok=False; break
                    # 4 px wide corridor around the line must be clean until the first ink
                    win=a[max(0,iy-3):iy+4,max(0,ix-3):ix+4]
                    if (win<200).any(): hit=(px,py); break
                    if (win<228).mean()>0.5: ok=False; break
                if not ok or hit is None: continue
                if not on_object(*hit) or math.hypot(hit[0]-T[0],hit[1]-T[1])>110: continue
                L2=math.hypot(hit[0]-sx,hit[1]-sy)
                if L2<0.065*w: continue
                score=L2/w+0.6*math.hypot(gx-wx,gy-wy)+(size-sz)/size*0.3
                if best is None or score<best[0]: best=(score,[text,[round(float(gx),3),round(float(gy),3)],[round(sx/w,4),round(sy/h,4)],[round(hit[0]/w,4),round(hit[1]/h,4)],sz,k])
        if best: break
    return (best[1] if best else None),("ok" if best else "no clean arrow")
p=json.load(open(os.path.join(D,"plan.json"))); out={}
for fr,labs in p["labels"].items():
    for lab in labs:
        text,(tx0,ty0),A,B=lab[0],lab[1],lab[2],lab[3]
        if A==B: out.setdefault(fr,[]).append(lab); continue
        tgt=TG.get(f"{fr}|{text}",B)
        r,why=place(fr,text,tx0,ty0,tgt[0],tgt[1],lab[4],lab[5] if len(lab)>5 else 1)
        if r: out.setdefault(fr,[]).append(r); print(f"OK   {fr} '{text}' tip {r[3]} size {r[4]}")
        else:
            out.setdefault(fr,[]).append([text,[tx0,ty0],[tx0,ty0],[tx0,ty0],lab[4]]); print(f"TEXT {fr} '{text}': {why}; arrow removed, text only (re-place with label_strict.py)")
p["labels"]=out; json.dump(p,open(os.path.join(D,"plan.json"),"w"),indent=1)
