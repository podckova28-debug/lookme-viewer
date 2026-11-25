# Enlarge the "simple" gag frames: crop to the drawing (+ padding) and re-pad to 16:9 on white, so they don't float small.
import sys
from PIL import Image, ImageOps
ids=[int(x) for x in open(sys.argv[1]).read().split()]
for n in ids:
    f=f"frames/f{n:02d}.png"; im=Image.open(f).convert("RGB")
    g=ImageOps.invert(im.convert("L")).point(lambda v:255 if v>18 else 0)
    x0,y0,x1,y1=g.getbbox(); w,h=x1-x0,y1-y0; p=int(max(w,h)*0.05)
    x0,y0,x1,y1=max(0,x0-p),max(0,y0-p),min(im.width,x1+p),min(im.height,y1+p)
    c=im.crop((x0,y0,x1,y1)); W,H=c.size
    if W/H<16/9: W=int(H*16/9)
    else: H=int(W*9/16)
    can=Image.new("RGB",(W,H),"white"); can.paste(c,((W-c.width)//2,(H-c.height)//2))
    can=can.resize((im.width,im.height),Image.LANCZOS); can.save(f)
    can.save(f"frames/jpg/f{n:02d}.jpg",quality=90)
    print(n, round(im.width/W,2))
