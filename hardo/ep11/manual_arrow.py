import json, sys
from PIL import Image, ImageFont
F="/home/user/lookme-viewer/hardo/pilot/fonts/PatrickHand.ttf"
def lab(frame,text,tx,ty,bx,by,size=88,k=1):
    w,h=Image.open(f'frames/{frame}.png').size; f=ImageFont.truetype(F,int(size*w/1536)); b=f.getbbox(text)
    x0,y0,x1,y1=tx*w+b[0],ty*h+b[1],tx*w+b[2],ty*h+b[3]; cx,cy=(x0+x1)/2,(y0+y1)/2; dx,dy=bx*w-cx,by*h-cy
    tX=((x1 if dx>0 else x0)-cx)/dx if dx else 1e9; tY=((y1 if dy>0 else y0)-cy)/dy if dy else 1e9; t=min(abs(tX),abs(tY))
    sx,sy=cx+dx*t,cy+dy*t; L=(dx*dx+dy*dy)**0.5; sx+=dx/L*12; sy+=dy/L*12
    return [text,[tx,ty],[round(sx/w,4),round(sy/h,4)],[bx,by],size,k]
