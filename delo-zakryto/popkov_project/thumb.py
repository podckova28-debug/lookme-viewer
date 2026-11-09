import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, x0, maxw, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W,H=1280,720
im=Image.open(src).convert("RGB").resize((W,H),Image.LANCZOS)
FONT=sys.argv[5]
def F(sz):
    f=ImageFont.truetype(FONT,sz); f.set_variation_by_name("Bold"); return f
CR=(182,16,30); INK=(16,14,12); PAPER=(244,236,216)
def card(box,fill,rot,seed):
    x1,y1,x2,y2=box; w,h=x2-x1,y2-y1; P=30
    random.seed(seed); pts=[]
    for i in range(0,w+1,10): pts.append((P+i,P+random.randint(-5,5)))
    for i in range(0,h+1,10): pts.append((P+w+random.randint(-5,5),P+i))
    for i in range(w,-1,-10): pts.append((P+i,P+h+random.randint(-5,5)))
    for i in range(h,-1,-10): pts.append((P+random.randint(-5,5),P+i))
    sh=Image.new("RGBA",(w+2*P,h+2*P),(0,0,0,0))
    ImageDraw.Draw(sh).polygon([(x+7,y+9) for x,y in pts],fill=(0,0,0,120)); sh=sh.filter(ImageFilter.GaussianBlur(7))
    lay=Image.new("RGBA",sh.size,(0,0,0,0)); ImageDraw.Draw(lay).polygon(pts,fill=fill)
    sh.alpha_composite(lay); return sh
def block(text,sz,y,fill,ink,rot,seed,pad):
    d=ImageDraw.Draw(im)
    while d.textlength(text,font=F(sz))>maxw-2*pad[0]: sz-=2
    f=F(sz); b=d.textbbox((0,0),text,font=f); tw,th=b[2]-b[0],b[3]-b[1]
    c=card((0,0,tw+2*pad[0],th+2*pad[1]),fill,rot,seed)
    ImageDraw.Draw(c).text((30+pad[0]-b[0],30+pad[1]-b[1]),text,font=f,fill=ink)
    c=c.rotate(rot,resample=Image.BICUBIC,expand=True)
    im.paste(c,(x0-30,y-30),c); return y+th+2*pad[1]
y=95
y=block("91 ЖЕРТВА",200,y,CR+(255,),PAPER,2,1,(26,24))+26
y=block("МАНЬЯК",130,y,PAPER+(255,),INK,-1.5,2,(20,16))+18
y=block("В ПОГОНАХ",130,y,PAPER+(255,),INK,1,3,(20,16))
im.save(out,quality=93); print(out,y)
