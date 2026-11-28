"""Final-QA fix: frames regenerated on dark backgrounds -> background removed (Higgsfield remover, raw_rb/),
placed on white; handwritten notes copied from the earlier approved frames (solid black pixels only, no glow)."""
import numpy as np
from PIL import Image
def cut(i, dx=0, dy=0, scale=1.0):
    im = Image.open(f'raw_rb/{i}.png').convert('RGBA').resize((1920, 1080), Image.LANCZOS)
    if scale != 1.0:
        w, h = int(1920 * scale), int(1080 * scale); im = im.resize((w, h), Image.LANCZOS)
    W = Image.new('RGBA', (1920, 1080), (255, 255, 255, 255)); W.alpha_composite(im, (int((1920 - im.width) / 2 + dx), int((1080 - im.height) / 2 + dy)))
    return W
def center(i):
    im = Image.open(f'raw_rb/{i}.png').convert('RGBA').resize((1920, 1080), Image.LANCZOS)
    x0, y0, x1, y1 = im.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()
    return cut(i, 960 - (x0 + x1) / 2, 540 - (y0 + y1) / 2)
def note(W, src, boxes, dx, dy, thr, s=1.0):
    g = np.asarray(Image.open(f'old_f/{src}' + ('' if '.' in src else '.jpg')).convert('L').resize((1920, 1080))).astype(np.float32)
    a = np.clip((thr + 40 - g) / 40, 0, 1)          # solid black ink only
    if thr < 0:                                     # ink on a dark gradient: strokes much darker than their surroundings
        import cv2; bg = cv2.dilate(g, np.ones((41, 41), np.uint8)); a = np.clip((bg - g - 70) / 40, 0, 1) * (g < 90)
    m = np.zeros_like(a)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = a[y0:y1, x0:x1]
    ys, xs = np.nonzero(m); X0, Y0, X1, Y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    L = Image.fromarray((m[Y0:Y1, X0:X1] * 255).astype(np.uint8))
    if s != 1.0: L = L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
    ink = Image.new('RGBA', L.size, (20, 20, 20, 255)); ink.putalpha(L)
    W.alpha_composite(ink, (int(X0 + dx), int(Y0 + dy)))
    return W
out = {}
out['b17'] = center('b17')
out['e06'] = center('e06')
def place(W, src, box):                            # a clean caption on white, scaled into box (x0, y0, x1, y1)
    g = np.asarray(Image.open(src).convert('L')).astype(np.float32); a = np.clip((150 - g) / 60, 0, 1)
    ys, xs = np.nonzero(a > .05); L = Image.fromarray((a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] * 255).astype(np.uint8))
    x0, y0, x1, y1 = box; s = min((x1 - x0) / L.width, (y1 - y0) / L.height); L = L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
    ink = Image.new('RGBA', L.size, (20, 20, 20, 255)); ink.putalpha(L); W.alpha_composite(ink, (int((x0 + x1 - L.width) / 2), int(y1 - L.height))); return W
out['c05'] = place(cut('c05'), 'old_f/vasco1.png', (1290, 50, 1790, 320))   # caption generated separately on white
out['f02'] = note(cut('f02'), 'f02', [(40, 40, 520, 320)], 0, 0, 60)
out['i07'] = note(cut('i07', dx=-170), 'i07', [(960, 30, 1860, 240)], 0, 0, 60)
for i, W in out.items(): W.convert('RGB').save(f'f/{i}.jpg', quality=93)
