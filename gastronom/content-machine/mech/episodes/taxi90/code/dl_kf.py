"""dl_kf.py '<имя> <url>' ... — скачать кадры в kf/<имя>.png и собрать лист превью qa/sheet_<первое>.jpg."""
import sys, urllib.request
from PIL import Image
names = []
for arg in sys.argv[1:]:
    n, url = arg.split(maxsplit=1); urllib.request.urlretrieve(url, f'kf/{n}.png'); names.append(n)
ims = [Image.open(f'kf/{n}.png').convert('RGB').resize((480, 270)) for n in names]
c = Image.new('RGB', (3 * 490, ((len(ims) + 2) // 3) * 280), 'white')
from PIL import ImageDraw
d = ImageDraw.Draw(c)
for k, (n, im) in enumerate(zip(names, ims)):
    x, y = (k % 3) * 490, (k // 3) * 280; c.paste(im, (x, y)); d.rectangle([x, y, x + 60, y + 22], fill='black'); d.text((x + 4, y + 4), n, fill='white')
c.save(f'qa/sheet_{names[0]}.jpg', quality=84); print('ok', names)
