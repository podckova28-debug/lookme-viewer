#!/usr/bin/env python3.13
"""Головы на кадрах-картинках для безопасного кадрирования в cut.py.

    python3.13 qa/heads.py <папка kf> [--out kf/heads.json]

Пишет {"KA1": {"size": [iw, ih], "heads": [[x0, y0, x1, y1], ...]}} в долях картинки. cut.py (fit_pose) по ним
сдвигает кадрирование наезда так, чтобы головы целиком оставались в кадре, и ограничивает зум. Мелкие «головы»
уже 2 % ширины кадра (фонари, пуговицы) отбрасываются.
"""
import sys, os, glob, json
from PIL import Image
from imgutils.detect import detect_heads

MIN_W = 0.02


def heads_of(path):
    im = Image.open(path).convert('RGB'); iw, ih = im.size; sc = 1280 / iw
    sm = im.resize((1280, int(ih * sc)))
    out = []
    for (x0, y0, x1, y1), _, s in detect_heads(sm, conf_threshold=0.35):
        b = [x0 / 1280, y0 / sm.height, x1 / 1280, y1 / sm.height]
        if b[2] - b[0] >= MIN_W: out.append([round(v, 4) for v in b])
    return [iw, ih], out


if __name__ == '__main__':
    args = sys.argv[1:]; out = None
    if '--out' in args: i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
    d = args[0]; out = out or os.path.join(d, 'heads.json')
    res = json.load(open(out)) if os.path.exists(out) else {}
    for f in sorted(glob.glob(os.path.join(d, '*.png'))):
        k = os.path.splitext(os.path.basename(f))[0]
        if k in res and os.path.getmtime(f) < os.path.getmtime(out): continue
        size, hs = heads_of(f); res[k] = dict(size=size, heads=hs); print(k, len(hs), flush=True)
    json.dump(res, open(out, 'w'), indent=1); print('->', out)
