#!/usr/bin/env python3
"""Auto-place labels: find a white area for the text near the target and snap the arrow tip to ink.
Usage: label_place.py <ep_dir>   (reads plan.json labels as wishes, writes plan.json with placed coords, previews in review/labels/)"""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
S=os.path.dirname(os.path.abspath(__file__)); FONT=os.path.join(S,"pilot","fonts","PatrickHand.ttf")
def draw_arrow(d,a,b,width,k=1):
    (x1,y1),(x2,y2)=a,b; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1
    cx,cy=mx-k*dy*0.18,my+k*dx*0.18; pts=[]
    for i in range(25):
        t=i/24; pts.append(((1-t)**2*x1+2*(1-t)*t*cx+t**2*x2,(1-t)**2*y1+2*(1-t)*t*cy+t**2*y2))
    d.line(pts,fill="black",width=width,joint="curve"); tx,ty=x2-cx,y2-cy; tl=math.hypot(tx,ty) or 1; tx,ty=tx/tl,ty/tl; hl=width*4.5
    for s in (1,-1):
        ang=math.radians(28)*s; d.line([(x2,y2),(x2-hl*(tx*math.cos(ang)-ty*math.sin(ang)),y2-hl*(tx*math.sin(ang)+ty*math.cos(ang)))],fill="black",width=width)
def place(d):
    plan=json.load(open(os.path.join(d,"plan.json"))); out=os.path.join(d,"review","labels"); os.makedirs(out,exist_ok=True); log=[]
    for name,labs in plan["labels"].items():
        im=Image.open(os.path.join(d,"frames",f"{name}.png")).convert("RGB"); w,h=im.size; a=np.array(im); ink=(a.min(axis=2)<200)
        # integral image for fast box ink sums
        I=np.pad(ink.astype(np.int32).cumsum(0).cumsum(1),((1,0),(1,0)))
        def boxink(x0,y0,x1,y1):
            x0,y0,x1,y1=[int(max(0,min(v,lim))) for v,lim in ((x0,w),(y0,h),(x1,w),(y1,h))]
            if x1<=x0 or y1<=y0: return 1.0
            return (I[y1,x1]-I[y0,x1]-I[y1,x0]+I[y0,x0])/((x1-x0)*(y1-y0))
        prev=im.copy(); dr=ImageDraw.Draw(prev); new=[]
        for lab in labs:
            text,(tx,ty),(ax,ay),(bx,by),size=lab[:5]; k=lab[5] if len(lab)>5 else 1; arrow=(ax,ay)!=(bx,by)
            f=ImageFont.truetype(FONT,int(size*w/1536)); bb=f.getbbox(text); bw,bh=bb[2]-bb[0],bb[3]-bb[1]
            # 1. snap tip to nearest ink within 70px
            if arrow:
                px,py=int(bx*w),int(by*h); best=None
                ys,xs=np.where(ink[max(0,py-70):py+70,max(0,px-70):px+70])
                if len(xs):
                    dd=(xs+max(0,px-70)-px)**2+(ys+max(0,py-70)-py)**2; i=dd.argmin(); px,py=xs[i]+max(0,px-70),ys[i]+max(0,py-70)
                bx,by=px/w,py/h
            # 2. search text position: ink < 2% in the box (+pad), inside safe area; prefer near wish, moderate distance to tip, upper half
            pad=int(14*w/1536); best=None
            for gy in np.arange(0.03,0.95-bh/h,0.015):
                for gx in np.arange(0.035,0.965-bw/w,0.015):
                    x0,y0=gx*w+bb[0]-pad,gy*h+bb[1]-pad; x1,y1=gx*w+bb[2]+pad,gy*h+bb[3]+pad
                    if x1>0.97*w or y1>0.96*h: continue
                    k_ink=boxink(x0,y0,x1,y1)
                    if k_ink>0.04: continue
                    cx,cy=(x0+x1)/2/w,(y0+y1)/2/h
                    cost=abs(gx-tx)+abs(gy-ty)  # stay close to the author's wish
                    if arrow:
                        dist=math.hypot((cx-bx)*w,(cy-by)*h)/w
                        if dist<0.12: cost+=2
                        cost+=0.6*max(0,dist-0.35)
                    cost+=0.3*gy
                    if best is None or cost<best[0]: best=(cost,gx,gy,k_ink)
            if best is None: log.append(f"{name} '{text}': NO white spot found, keeping wish"); gx,gy,k_ink=tx,ty,-1
            else: _,gx,gy,k_ink=best
            # arrow start = centre of text box (assembler snaps it to the box edge)
            cxs,cys=(gx*w+(bb[0]+bb[2])/2)/w,(gy*h+(bb[1]+bb[3])/2)/h
            new.append([text,[round(float(gx),3),round(float(gy),3)],[round(float(cxs),3),round(float(cys),3)] if arrow else [round(float(gx),3),round(float(gy),3)],[round(float(bx),3),round(float(by),3)] if arrow else [round(float(gx),3),round(float(gy),3)],size]+([k] if len(lab)>5 else []))
            dr.text((gx*w,gy*h),text,font=f,fill="black")
            if arrow:
                x0,y0,x1,y1=gx*w+bb[0]-pad,gy*h+bb[1]-pad,gx*w+bb[2]+pad,gy*h+bb[3]+pad; cx,cy=(x0+x1)/2,(y0+y1)/2; dx,dy=bx*w-cx,by*h-cy
                tX=((x1 if dx>0 else x0)-cx)/dx if dx else 1e9; tY=((y1 if dy>0 else y0)-cy)/dy if dy else 1e9; t=min(tX,tY); sx,sy=cx+dx*t,cy+dy*t
                draw_arrow(dr,(sx,sy),(bx*w,by*h),max(3,int(7*w/1536)),k)
            log.append(f"{name} '{text}': text at ({gx:.3f},{gy:.3f}) ink {k_ink:.3f}" + (f", tip ({bx:.3f},{by:.3f})" if arrow else ""))
        plan["labels"][name]=new; prev.save(os.path.join(out,f"{name}.jpg"),quality=85)
    json.dump(plan,open(os.path.join(d,"plan.json"),"w"),indent=1); print("\n".join(log))
if __name__=="__main__": place(sys.argv[1])
