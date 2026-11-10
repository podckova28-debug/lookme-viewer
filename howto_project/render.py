#!/usr/bin/env python3
# Render one segment (chapter / title / end) of a long documentary to a silent 1920x1080 30fps mp4.
import sys, json, math, subprocess, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
ROOT = os.environ.get("PC_ROOT", "/home/user/hw")
FONT = os.environ.get("PC_FONT", "/home/user/tools/fonts/Oswald.ttf")
CREAM = (238, 229, 210)
INK = (24, 22, 20)
CRIMSON = (178, 24, 30)
XF = 0.4  # crossfade seconds

_fc = {}
def font(sz):
    if sz not in _fc:
        f = ImageFont.truetype(FONT, sz)
        try: f.set_variation_by_name("Bold")
        except Exception: pass
        _fc[sz] = f
    return _fc[sz]

_paper = None
def paper():
    global _paper
    if _paper is None:
        rng = np.random.default_rng(7)
        base = np.ones((H, W, 3), np.float32) * np.array(CREAM, np.float32)
        noise = rng.normal(0, 6, (H // 4, W // 4)).astype(np.float32)
        noise = np.array(Image.fromarray(noise).resize((W, H), Image.BICUBIC))
        fine = rng.normal(0, 3, (H, W)).astype(np.float32)
        base += (noise + fine)[..., None]
        yy, xx = np.mgrid[0:H, 0:W]
        v = 1 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        base *= v[..., None]
        _paper = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    return _paper.copy()

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

# ---------- text cards ----------
def chapter_card(num, title, t, dur):
    im = paper(); d = ImageDraw.Draw(im)
    a = ease(t / 0.5); b = ease((dur - t) / 0.4)
    k = min(a, b)
    f1 = font(46); f2 = font(150)
    lab = f"ГЛАВА {num:02d}"
    y0 = 400 + int(30 * (1 - a))
    tw = d.textlength(lab, font=f1)
    d.text(((W - tw) / 2, y0), lab, font=f1, fill=CRIMSON)
    tt = title.upper()
    tw2 = d.textlength(tt, font=f2)
    d.text(((W - tw2) / 2, y0 + 60), tt, font=f2, fill=INK)
    lw = int(tw2 * ease((t - 0.2) / 0.6))
    d.rectangle(((W - tw2) / 2, y0 + 250, (W - tw2) / 2 + lw, y0 + 258), fill=CRIMSON)
    if k < 1:
        im = Image.blend(paper(), im, k)
    return im

def title_card(t, dur):
    im = paper(); d = ImageDraw.Draw(im)
    a = ease(t / 0.6); b = ease((dur - t) / 0.5); k = min(a, b)
    f0 = font(44); f1 = font(190); f2 = font(54)
    s0 = "ДЕЛО ЗАКРЫТО"
    d.text(((W - d.textlength(s0, font=f0)) / 2, 300), s0, font=f0, fill=CRIMSON)
    s1 = "ОНИ ЖИЛИ РЯДОМ"
    sc = 1.0 + 0.03 * (1 - a)
    d.text(((W - d.textlength(s1, font=f1)) / 2, 370), s1, font=f1, fill=INK)
    s2 = "КАК ПОЯВЛЯЮТСЯ МАНЬЯКИ"
    d.text(((W - d.textlength(s2, font=f2)) / 2, 690), s2, font=f2, fill=INK)
    lw = int(900 * ease((t - 0.4) / 0.8))
    d.rectangle((W / 2 - lw / 2, 660, W / 2 + lw / 2, 668), fill=CRIMSON)
    if k < 1: im = Image.blend(paper(), im, k)
    return im

def end_card(t, dur):
    im = paper(); d = ImageDraw.Draw(im)
    a = ease(t / 0.4); b = ease((dur - t) / 0.8)
    f = font(210)
    s = "ДЕЛО ЗАКРЫТО"
    stamp = Image.new("RGBA", (1500, 420), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
    sd.rectangle((10, 10, 1490, 410), outline=CRIMSON + (255,), width=14)
    sd.text(((1500 - sd.textlength(s, font=f)) / 2, 60), s, font=f, fill=CRIMSON + (255,))
    sc = 1.25 - 0.25 * ease(t / 0.25)
    st = stamp.rotate(-6, expand=True, resample=Image.BICUBIC)
    st = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
    al = st.split()[3].point(lambda v: int(v * min(a, 1.0) * 0.92))
    st.putalpha(al)
    im.paste(st, ((W - st.width) // 2, (H - st.height) // 2), st)
    if b < 1: im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, b)
    return im

# ---------- stickers ----------
_stk = {}
def sticker_img(text):
    if text in _stk: return _stk[text]
    f = font(64)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = int(tmp.textlength(text, font=f)); padx, pady = 38, 18
    w, h = tw + 2 * padx, 64 + 2 * pady + 14
    im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rectangle((18, 20, 18 + w, 20 + h), fill=(0, 0, 0, 90)); sh = sh.filter(ImageFilter.GaussianBlur(6))
    im.alpha_composite(sh)
    strip = Image.new("RGBA", (w, h), CREAM + (255,)); dd = ImageDraw.Draw(strip)
    rng = random.Random(hash(text) & 0xffff)
    # torn edges
    for x in range(0, w, 6):
        dd.rectangle((x, 0, x + 6, rng.randint(0, 5)), fill=(0, 0, 0, 0))
        dd.rectangle((x, h - rng.randint(0, 5), x + 6, h), fill=(0, 0, 0, 0))
    dd.rectangle((0, 0, 10, h), fill=CRIMSON + (255,))
    dd.text((padx + 6, pady - 4), text, font=f, fill=INK + (255,))
    im.alpha_composite(strip, (8, 8))
    im = im.rotate(rng.uniform(-2.5, 2.5), expand=True, resample=Image.BICUBIC)
    _stk[text] = im
    return im

import re as _re
_cal = {}
def split_callout(text):
    for sep in (" · ", " — "):
        if sep in text:
            a, b = text.split(sep, 1); return "two", a, b
    if _re.match(r"^\d+$", text): return "num", text, ""
    m = _re.match(r"^(\d[\d.,+]*)\s+([^\d]+)$", text)
    if m: return "num", m.group(1), m.group(2)
    return "one", text, ""

def callout_img(text):
    if text in _cal: return _cal[text]
    kind, a, b = split_callout(text)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    if kind == "num":
        fa, fb = font(300), font(84)
        wa, wb = tmp.textlength(a, font=fa), tmp.textlength(b, font=fb)
        bbn = tmp.textbbox((0, 0), a, font=fa); bbl = tmp.textbbox((0, 0), b or "Ж", font=fb)
        w = int(max(wa, wb)) + 160
        h = 40 + (bbn[3] - bbn[1]) + (34 + 30 + (bbl[3] - bbl[1]) + 50 if b else 50)
    elif kind == "two":
        fa, fb = font(124), font(72)
        wa, wb = tmp.textlength(a, font=fa), tmp.textlength(b, font=fb)
        w = int(max(wa, wb)) + 140; h = 124 + 72 + 150
    else:
        fa = font(120); wa = tmp.textlength(a, font=fa); fb = None; wb = 0
        w = int(wa) + 140; h = 120 + 110
    w = min(w, 1700)
    pad = 40
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rectangle((pad + 14, pad + 18, pad + w + 14, pad + h + 18), fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    card = Image.new("RGBA", (w, h), CREAM + (255,)); dd = ImageDraw.Draw(card)
    rng = random.Random(sum(map(ord, text)))
    for x in range(0, w, 7):  # torn top / bottom edges
        dd.rectangle((x, 0, x + 7, rng.randint(0, 9)), fill=(0, 0, 0, 0))
        dd.rectangle((x, h - rng.randint(0, 9), x + 7, h), fill=(0, 0, 0, 0))
    if kind == "num":
        bb = dd.textbbox((0, 0), a, font=fa)
        ytop = 40 - bb[1]
        dd.text(((w - wa) / 2, ytop), a, font=fa, fill=CRIMSON + (255,))
        ly = 40 + (bb[3] - bb[1]) + 34
        if b:
            dd.rectangle((w / 2 - 90, ly, w / 2 + 90, ly + 8), fill=INK + (255,))
            bb2 = dd.textbbox((0, 0), b, font=fb)
            dd.text(((w - wb) / 2, ly + 30 - bb2[1]), b, font=fb, fill=INK + (255,))
    elif kind == "two":
        dd.rectangle((0, 0, 16, h), fill=CRIMSON + (255,))
        dd.text((70, 32), a, font=fa, fill=INK + (255,))
        dd.rectangle((70, 196, 70 + min(wa, w - 140), 204), fill=CRIMSON + (255,))
        dd.text((70, 218), b, font=fb, fill=CRIMSON + (255,))
    else:
        dd.rectangle((0, 0, 16, h), fill=CRIMSON + (255,))
        dd.text((70, 40), a, font=fa, fill=INK + (255,))
    # two strips of tape
    tape = Image.new("RGBA", (170, 46), (226, 218, 196, 200))
    im.alpha_composite(card, (pad, pad))
    for (tx, ang) in ((pad - 40, -24), (pad + w - 130, 22)):
        tt = tape.rotate(ang, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(tt, (max(0, tx), 0))
    im = im.rotate(rng.uniform(-2.2, 2.2), expand=True, resample=Image.BICUBIC)
    _cal[text] = im
    return im

_cal_side = {}
def draw_sticker(frame, text, t, dur):
    im = callout_img(text)
    a = ease(t / 0.35); b = ease((dur - t) / 0.4); k = min(a, b)
    # lower-third: darken only the bottom band so the picture itself stays visible
    band = _band()
    shade = Image.new("RGBA", (W, band.height), (20, 18, 16, 0)); shade.putalpha(band.split()[3].point(lambda v: int(v * k)))
    frame.paste(shade.convert("RGB"), (0, H - band.height), shade)
    sc = 0.85 * (1.12 - 0.12 * ease(t / 0.35))
    s = im.resize((int(im.width * sc), int(im.height * sc)), Image.BICUBIC) if sc != 1 else im.copy()
    al = s.split()[3].point(lambda v: int(v * k))
    s.putalpha(al)
    # bottom-right corner: people in the pictures stand left of centre, animated cards are centred
    x = W - s.width - 70; y = H - s.height - 60 + int(30 * (1 - a))
    frame.paste(s, (x, y), s)

_bandc = []
def _band():
    if not _bandc:
        bh = 330
        g = Image.linear_gradient("L").resize((W, bh)).point(lambda v: int(v * 0.42))
        b = Image.new("RGBA", (W, bh), (20, 18, 16, 255)); b.putalpha(g); _bandc.append(b)
    return _bandc[0]

# ---------- shots ----------
class ImgShot:
    def __init__(self, sid, dur, mode):
        src = Image.open(f"{ROOT}/img/{sid}.png").convert("RGB")
        self.src = src.resize((2240, int(2240 * src.height / src.width)), Image.LANCZOS)
        self.dur = dur; self.mode = mode
    def frame(self, t):
        p = ease(t / self.dur) * 0.6 + (t / self.dur) * 0.4
        sw, sh = self.src.size
        z0, z1 = {"in": (1.0, 1.12), "out": (1.12, 1.0), "left": (1.08, 1.08), "right": (1.08, 1.08)}[self.mode]
        z = z0 + (z1 - z0) * p
        cw, ch = sw / z, sw / z * 9 / 16
        ch = min(ch, sh); cw = ch * 16 / 9
        cx, cy = sw / 2, sh / 2
        if self.mode == "left": cx = sw / 2 + (sw - cw) / 2 * (0.9 - 1.8 * p)
        if self.mode == "right": cx = sw / 2 - (sw - cw) / 2 * (0.9 - 1.8 * p)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        return self.src.resize((W, H), Image.BILINEAR, box=box)

class VidShot:
    def __init__(self, sid, dur):
        self.dur = dur
        p = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{ROOT}/vid/{sid}.mp4", "-t", str(dur + 0.2),
                            "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        buf = p.stdout; n = len(buf) // (W * H * 3)
        self.frames = [buf[i * W * H * 3:(i + 1) * W * H * 3] for i in range(n)]
    def frame(self, t):
        i = min(len(self.frames) - 1, int(t * FPS))
        return Image.frombytes("RGB", (W, H), self.frames[i])

class CardShot:
    def __init__(self, fn, dur): self.fn = fn; self.dur = dur
    def frame(self, t): return self.fn(t, self.dur)

def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    shots = []
    modes = ["in", "left", "out", "right"]
    mi = spec.get("mode_seed", 0)
    for s in spec["shots"]:
        k = s["kind"]
        if k == "img": shots.append(ImgShot(s["id"], s["dur"], modes[mi % 4])); mi += 1
        elif k == "vid": shots.append(VidShot(s["id"], s["dur"]))
        elif k == "chapter": shots.append(CardShot(lambda t, d, n=s["num"], ti=s["title"]: chapter_card(n, ti, t, d), s["dur"]))
        elif k == "title": shots.append(CardShot(title_card, s["dur"]))
        elif k == "end": shots.append(CardShot(end_card, s["dur"]))
        elif k == "anim":
            import anim
            shots.append(anim.AnimShot(s["spec"], s["dur"]))
    # timeline with crossfades: shot i starts at sum(prev durs) - i*XF
    starts = []; t = 0
    for i, s in enumerate(shots):
        starts.append(t); t += s.dur - (XF if i < len(shots) - 1 else 0)
    total = spec["total"]
    nfr = int(round(total * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", spec.get("preset", "veryfast"), "-crf", "18",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    stickers = []
    for st in spec.get("stickers", []):
        # a callout belongs to the picture on screen when it appears: only over pictures, cut at that shot's end
        i0 = max([i for i, s0 in enumerate(starts) if s0 <= st["t"]] or [0])
        if not isinstance(shots[i0], ImgShot): continue
        d = min(st["dur"], starts[i0] + shots[i0].dur - XF / 2 - st["t"])
        if d >= 0.9: stickers.append(dict(st, dur=d))
    for f in range(nfr):
        t = f / FPS
        act = [i for i, st in enumerate(starts) if st <= t < st + shots[i].dur] or [len(shots) - 1]
        i = act[-1]
        fr = shots[i].frame(min(t - starts[i], shots[i].dur - 1e-3))
        if len(act) > 1:
            j = act[0]
            prev = shots[j].frame(min(t - starts[j], shots[j].dur - 1e-3))
            fr = Image.blend(prev, fr, ease((t - starts[i]) / XF))
        for st in stickers:
            if st["t"] <= t < st["t"] + st["dur"]:
                draw_sticker(fr, st["text"], t - st["t"], st["dur"])
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    print("OK", out, nfr)

if __name__ == "__main__":
    main()
