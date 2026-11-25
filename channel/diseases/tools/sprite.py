"""Cut-out animation helpers: chroma-key a sprite drawn on flat green, and composite sprites onto a background.

python3 sprite.py key in.png out.png         -> RGBA sprite, green removed, edges despilled, cropped to the figure
python3 sprite.py comp bg.jpg out.jpg sprite.png:x:y:h [...]   -> still composite (x = centre, y = feet line, h = height px at 1920x1080)
"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def key(src, dst):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    # greenness: how much green dominates the other channels
    gd = g - np.maximum(r, b)
    a = np.clip(1 - (gd - 40) / 80, 0, 1)            # gd >= 120 -> fully transparent, <= 40 -> opaque
    # despill: pull green down to the max of r/b where it still dominates
    g2 = np.where(gd > 0, np.maximum(r, b) + gd * .15, g)
    out = np.dstack([r, g2, b, a * 255]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(out, 'RGBA')
    al = img.split()[3].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.6))   # trim the green fringe
    img.putalpha(al)
    box = img.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()
    img.crop(box).save(dst)
    return img.crop(box)


def place(bg, sp, x, y, h, shadow=True):
    """paste sprite sp (RGBA) onto bg (RGBA) with its feet centre at (x, y), scaled to height h"""
    w = int(sp.width * h / sp.height); s = sp.resize((w, int(h)), Image.LANCZOS)
    if shadow:   # soft contact shadow so the figure stands on the floor
        sh = Image.new('RGBA', bg.size, (0, 0, 0, 0)); from PIL import ImageDraw
        ImageDraw.Draw(sh).ellipse((x - w * .42, y - h * .025, x + w * .42, y + h * .025), fill=(0, 0, 0, 110))
        bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(h * .02)))
    bg.alpha_composite(s, (int(x - w / 2), int(y - h)))
    return bg


if __name__ == '__main__':
    if sys.argv[1] == 'key':
        key(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'comp':
        bg = Image.open(sys.argv[2]).convert('RGBA').resize((1920, 1080))
        for spec in sys.argv[4:]:
            p, x, y, h = spec.rsplit(':', 3)
            bg = place(bg, Image.open(p).convert('RGBA'), float(x), float(y), float(h))
        bg.convert('RGB').save(sys.argv[3], quality=92)
