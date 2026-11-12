"""Recurring scheme blocks (WHAT HE DOES TO YOU / WHAT HE LEAVES BEHIND), drawn by the builder - no image generation.

Each block is one still background (assets/plague/schemes/bg.jpg, made by make_bg()) shown as a single continuous
shot across several narration beats; items appear one by one and stay on screen ('persist') until the block ends.
"""
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

CREAM = [242, 232, 208]
BG = 'scheme_bg'   # frame id; the file is copied into each episode's frames folder

def make_bg(path, w=1920, h=1080, seed=7):
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), np.float32) + np.array([38, 29, 22], np.float32)
    n = rng.normal(0, 1, (h // 8, w // 8)).astype(np.float32)
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    base += (n[..., None] - .5) * 18 + rng.normal(0, 3, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w]; r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    base *= (1 - .45 * np.clip(r - .4, 0, 1) ** 1.5)[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for o, wdt in ((34, 3), (46, 1)):   # double gold rule frame
        d.rectangle((o, o, w - o, h - o), outline=(150, 118, 70), width=wdt)
    im.save(path, quality=93)

def _t(text, x, y, size, color=CREAM, at=.3, maxw=None, style='plate'):
    it = {'text': text, 'x': x, 'y': y, 'size': size, 'at': at, 'persist': True, 'color': color, 'style': style}
    if maxw: it['maxw'] = maxw
    return it

def header(title, accent, at=.1):
    return [_t(title, 960, 150, 74, at=at, style='title'),
            {'style': 'line', 'pts': [760, 205, 1160, 205], 'width': 3, 'color': accent, 'text': '', 'size': 1, 'x': 0, 'y': 0, 'at': at, 'persist': True}]

def axis(y=560):
    return [{'style': 'line', 'pts': [200, y, 1720, y], 'width': 5, 'color': [120, 98, 70], 'text': '', 'size': 1, 'x': 0, 'y': 0, 'at': .1, 'persist': True}]

def nodes(all_nodes, accent, idx, ats, y=560):
    """add timeline nodes idx (indices into all_nodes = [(when, [line1, line2]), ...]) fading in at the given times.
    Items persist, so each node is added once, in the beat where the narration reaches it."""
    n = len(all_nodes); xs = [260 + i * (1400 / (n - 1)) for i in range(n)]; items = []
    for i, at in zip(idx, ats):
        when, lines = all_nodes[i]
        items += [{'style': 'dot', 'x': xs[i], 'y': y, 'r': 30, 'color': accent, 'text': '', 'size': 1, 'at': at, 'persist': True},
                  _t(str(i + 1), xs[i], y + 2, 36, [24, 18, 14], at + .05, style='num'),
                  _t(when, xs[i], y - 90, 52, accent, at, maxw=270)]
        items += [_t(ln, xs[i], y + 95 + j * 56, 44, CREAM, at + .15, maxw=270) for j, ln in enumerate(lines)]
    return items

def column(side, rows, accent, ats, with_head=True, y0=380):
    """one column of the consequences scheme: side 'L' (FOR THE SURVIVOR) or 'R' (FOR THE WORLD)"""
    x, head = (560, 'FOR THE SURVIVOR') if side == 'L' else (1360, 'FOR THE WORLD')
    items = [_t(head, x, y0 - 80, 56, accent, max(.1, ats[0] - .4) if ats else .1)] if with_head else []
    items.append({'style': 'line', 'pts': [x - 260, y0 - 35, x + 260, y0 - 35], 'width': 2, 'color': accent, 'text': '', 'size': 1, 'x': 0, 'y': 0, 'at': max(.1, ats[0] - .4) if ats else .1, 'persist': True})
    return items + [_t(r, x, y0 + 50 + j * 96, 50, CREAM, at, maxw=720) for j, (r, at) in enumerate(zip(rows, ats))]
