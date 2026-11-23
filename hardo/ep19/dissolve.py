import numpy as np, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
F="/home/user/lookme-viewer/hardo/pilot/fonts/PatrickHand.ttf"
def figures(sheet):
    im=Image.open(sheet).convert('RGB'); a=np.asarray(im); ink=a.min(2)<235
    xs=np.where(ink.any(0))[0]; segs=[]; s=p=xs[0]
    for x in xs[1:]:
        if x-p>8: segs.append((s,p)); s=x
        p=x
    segs.append((s,p)); out=[]
    for x0,x1 in [q for q in segs if q[1]-q[0]>40]:
        rows=np.where(ink[:,x0:x1+1].any(1))[0]
        c=im.crop((x0-6,rows[0]-6,x1+7,rows[-1]+7))
        # alpha: flood background from the border on a dilated edge mask
        L=np.asarray(c.convert('L')).astype(int)
        bgm=Image.fromarray(((L>242)*255).astype('uint8'))
        d=bgm.copy(); w,h=d.size
        from PIL import ImageDraw as D
        for pt in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
            if d.getpixel(pt)==255: D.floodfill(d,pt,128)
        alpha=(np.asarray(d)!=128).astype('uint8')*255
        al=Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
        c=c.convert('RGBA'); c.putalpha(al); out.append(c)
    return out
def dissolve(fig,start=0.45,seed=1,cell=7,drift=260):
    random.seed(seed); a=np.asarray(fig).copy(); h,w,_=a.shape
    out=np.zeros((h,w+drift,4),np.uint8); out[:,:w]=a
    for y in range(0,h,cell):
        for x in range(0,w,cell):
            t=(x/w-start)/(1-start)
            if t<=0: continue
            blk=a[y:y+cell,x:x+cell]
            if blk[...,3].max()<40: continue
            if random.random()<min(1,t*1.25):
                out[y:y+cell,x:x+cell]=0
                if random.random()<0.55:
                    dx=int(random.random()*drift*t+cell); dy=int((random.random()-0.6)*60*t)
                    ny,nx=y+dy,x+dx
                    if 0<=ny<h-cell and nx<w+drift-cell:
                        b=blk.copy(); b[...,3]=(b[...,3]*max(0.25,1-t*0.7)).astype(np.uint8)
                        sub=out[ny:ny+b.shape[0],nx:nx+b.shape[1]]; m=b[...,3:]>sub[...,3:]
                        sub[:]=np.where(m,b,sub)
    return Image.fromarray(out)
def text(d,t,xy,size,fill,outline=(255,255,255),sw=None,anchor='la'):
    f=ImageFont.truetype(F,size); sw=sw or max(6,size//12)
    d.text(xy,t,font=f,fill=fill,stroke_width=sw,stroke_fill=outline,anchor=anchor)
