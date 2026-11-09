import sys
from PIL import Image, ImageDraw, ImageFont
f=ImageFont.truetype('/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf',30)
out=sys.argv[1]; ns=sys.argv[2:]; cols=2; rows=(len(ns)+1)//2
W=Image.new('RGB',(cols*960,rows*560),'white')
for i,n in enumerate(ns):
    im=Image.open(f'kf/{n}.png').convert('RGB').resize((960,540)); x,y=(i%cols)*960,(i//cols)*560+20
    W.paste(im,(x,y)); ImageDraw.Draw(W).text((x+8,y-22),n,fill='red',font=f)
W.save(out,quality=86)
