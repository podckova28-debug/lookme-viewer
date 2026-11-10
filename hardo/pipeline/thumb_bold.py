import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
F="/home/user/lookme-viewer/hardo/pilot/fonts/PatrickHand.ttf"
RED=(222,30,30); YEL=(255,214,0); BLK=(15,15,15)
def arrow(d,a,b,col,wid,k=1):
    (x1,y1),(x2,y2)=a,b; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; cx,cy=mx-k*dy*0.25,my+k*dx*0.25
    pts=[((1-t)**2*x1+2*(1-t)*t*cx+t**2*x2,(1-t)**2*y1+2*(1-t)*t*cy+t**2*y2) for t in [i/30 for i in range(31)]]
    d.line(pts,fill=col,width=wid,joint="curve"); tx,ty=x2-cx,y2-cy; L=math.hypot(tx,ty); tx,ty=tx/L,ty/L; hl=wid*3.5
    for s in (1,-1):
        an=math.radians(30)*s; d.line([(x2,y2),(x2-hl*(tx*math.cos(an)-ty*math.sin(an)),y2-hl*(tx*math.sin(an)+ty*math.cos(an)))],fill=col,width=wid)
def make(src,crop,lines,out,arr=None):
    s=Image.open(src).convert('RGB'); W,H=s.size; s=s.crop((int(crop[0]*W),int(crop[1]*H),int(crop[2]*W),int(crop[3]*H))).resize((1280,720),Image.LANCZOS)
    im=s.copy(); d=ImageDraw.Draw(im)
    for t,x,y,size,col,hl in lines:
        f=ImageFont.truetype(F,size); b=f.getbbox(t,stroke_width=size//22)
        if hl: d.rectangle([x+b[0]-14,y+b[1]+int((b[3]-b[1])*0.35),x+b[2]+14,y+b[3]+6],fill=YEL)
        d.text((x,y),t,font=f,fill=col,stroke_width=size//22,stroke_fill=col)
        print(out,t,'box',(x+b[0],y+b[1],x+b[2],y+b[3]))
    if arr: arrow(d,arr[0],arr[1],RED,16,arr[2] if len(arr)>2 else 1)
    im.save(out,quality=93); return im
