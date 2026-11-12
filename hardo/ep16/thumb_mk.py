import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
F='thumb/Anton.ttf'; BLK=(16,16,16); WHT=(255,255,255); RED=(226,28,28); YEL=(255,214,0)
def vib(im,k):
    h,s,v=[np.array(c).astype(float)/255 for c in im.convert('HSV').split()]
    s=np.clip(s*(1+k*(1-s)),0,1)
    return Image.merge('HSV',[Image.fromarray((c*255).astype('uint8')) for c in (h,s,v)]).convert('RGB')
def punch(im):
    bg=np.array(im).min(2)>245
    im=vib(im,0.40); im=ImageEnhance.Contrast(im).enhance(1.10)
    im=im.filter(ImageFilter.UnsharpMask(radius=25,percent=25,threshold=0)).filter(ImageFilter.UnsharpMask(radius=1.8,percent=140,threshold=2))
    x=np.array(im); x[bg]=255; return Image.fromarray(x)
def txt(im,xy,t,size,fill,stroke,sw):
    f=ImageFont.truetype(F,size)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(sh)
    d.text((xy[0]+6,xy[1]+8),t,font=f,fill=(0,0,0,150),stroke_width=sw,stroke_fill=(0,0,0,150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    d=ImageDraw.Draw(im); d.text(xy,t,font=f,fill=fill,stroke_width=sw,stroke_fill=stroke)
    return d.textbbox(xy,t,font=f,stroke_width=sw)
def bar_word(im,x,y,t,size):
    f=ImageFont.truetype(F,size); bb=ImageDraw.Draw(im).textbbox((x,y),t,font=f,stroke_width=10)
    bar=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(bar)
    d.polygon([(bb[0]-18,bb[1]+int(size*.25)),(bb[2]+22,bb[1]+int(size*.17)),(bb[2]+14,bb[3]+4),(bb[0]-12,bb[3]+16)],fill=YEL+(255,),outline=BLK,width=6)
    im.alpha_composite(bar); return txt(im,(x,y),t,size,RED,BLK,10)
def make(src,crop,lines,out,x0,y0,right=False):
    s=Image.open(src).convert('RGB'); W,H=s.size
    s=s.crop((int(crop[0]*W),int(crop[1]*H),int(crop[2]*W),int(crop[3]*H))).resize((1280,720),Image.LANCZOS)
    im=punch(s).convert('RGBA'); y=y0
    for t,size,kind in lines:
        f=ImageFont.truetype(F,size); w=ImageDraw.Draw(im).textbbox((0,0),t,font=f,stroke_width=10)[2]
        x=(1280-40-w) if right else x0
        b=bar_word(im,x,y,t,size) if kind=='bar' else txt(im,(x,y),t,size,BLK,WHT,10)
        y=b[3]-int(size*0.12)
    im.convert('RGB').save(out,quality=93); print(out)
make('thumb/F419m.png',(0,0,1,1),[("CUT OFF",140,"n"),("for 8",120,"n"),("MONTHS",160,"bar")],'thumb/A.jpg',40,60)
make('frames/F06.png',(0,0,1,1),[("PAID TO",110,'n'),("COUNT",170,'n'),("PENGUINS",150,'bar')],'thumb/B.jpg',0,70,right=True)
make('frames/F16.png',(0,0,1,1),[("28 DAYS",170,'n'),("IN A",110,'n'),("CAN",190,'bar')],'thumb/C.jpg',0,60,right=True)
