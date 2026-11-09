#!/usr/bin/env python3
"""Vision QA for Hardo episodes (numpy + PIL only, no models).

Detectors:
  clip_report(path)        -> morphing / phantom objects / object multiplication inside a Wan clip
  pair_score(a_png, b_png) -> can this first/last frame pair be animated without drifting?
  read_clocks(png)         -> list of (cx, cy, r, hour_angle, minute_angle, time_str) for round clocks
  script_times(text)       -> times mentioned in narration ("Nine fourteen p.m.", "Three thirty", "Five p.m.")
  hero_clusters(png, hsv)  -> number of separate blobs of the hero's signature colour (duplicate-hero check)
  isolated_marks(png)      -> black strokes standing alone on white (baked-in arrows, symbols)

CLI:
  qa_vision.py clip <mp4> [...]          per-clip metrics and verdicts
  qa_vision.py pair <a.png> <b.png>      pair score
  qa_vision.py frames <dir> [--hero H,S,V,H2,S2,V2]   clocks, marks, hero clusters for every F*.png
"""
import sys, os, re, glob, json, math, subprocess, tempfile
from collections import deque
import numpy as np
from PIL import Image

# ---------------------------------------------------------------- basics
def load_gray(path, size=(320, 180)):
    return np.asarray(Image.open(path).convert("L").resize(size, Image.BILINEAR)).astype(np.int16)

def load_rgb(path, size=None):
    im = Image.open(path).convert("RGB")
    if size: im = im.resize(size, Image.BILINEAR)
    return np.asarray(im)

def ink_mask(rgb):
    """non-background pixels: dark or saturated."""
    r, g, b = rgb[..., 0].astype(int), rgb[..., 1].astype(int), rgb[..., 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    gray = (r * 299 + g * 587 + b * 114) // 1000
    sat = (mx - mn)
    return (gray < 200) | (sat > 45)

def changed_frac(a, b, thr=40, shifts=range(-8, 9, 4)):
    """fraction of pixels that differ, tolerant to a whole-frame shift."""
    best = 1.0
    for dx in shifts:
        for dy in shifts:
            best = min(best, float((np.abs(a - np.roll(np.roll(b, dy, 0), dx, 1)) > thr).mean()))
    return best

def components(mask, min_area=0):
    """4-connected components of a boolean mask -> list of dicts (area, bbox, pixels idx)."""
    h, w = mask.shape; labels = np.zeros((h, w), np.int32); comps = []; cur = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if labels[y0, x0]: continue
        cur += 1; q = deque([(y0, x0)]); labels[y0, x0] = cur; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not labels[ny, nx]:
                    labels[ny, nx] = cur; q.append((ny, nx))
        if len(pts) >= min_area:
            py = np.array([p[0] for p in pts]); px = np.array([p[1] for p in pts])
            comps.append({"id": cur, "area": len(pts), "bbox": (px.min(), py.min(), px.max(), py.max()), "py": py, "px": px})
    return labels, comps

def dilate(mask, r):
    out = mask.copy()
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out |= np.roll(np.roll(mask, dy, 0), dx, 1)
    return out

# ---------------------------------------------------------------- clips
def clip_frames(path, fps=2, size=(320, 180)):
    d = tempfile.mkdtemp(prefix="qav_")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", f"fps={fps},scale={size[0]}:{size[1]}", os.path.join(d, "f%03d.png")], check=True)
    files = sorted(glob.glob(os.path.join(d, "*.png")))
    return [load_rgb(f) for f in files]

def clip_report(path):
    frames = clip_frames(path)
    if len(frames) < 3: return {"file": os.path.basename(path), "error": "too short"}
    grays = [((f[..., 0].astype(int) * 299 + f[..., 1].astype(int) * 587 + f[..., 2].astype(int) * 114) // 1000).astype(np.int16) for f in frames]
    first, last = grays[0], grays[-1]
    d_se = changed_frac(first, last)
    # 1. morphing: a middle frame that is far from BOTH endpoints
    dev = [min(changed_frac(g, first), changed_frac(g, last)) for g in grays[1:-1]]
    morph = max(dev) - max(d_se, 0.05) if dev else 0.0
    # 2. phantom objects: ink that exists in a middle frame but in neither endpoint
    m_first, m_last = ink_mask(frames[0]), ink_mask(frames[-1])
    allowed = dilate(m_first | m_last, 6)
    area = m_first.size; phantom = 0.0; phantom_t = None
    for i, f in enumerate(frames[1:-1], 1):
        m = ink_mask(f) & ~allowed
        _, comps = components(m, min_area=int(0.004 * area))
        tot = sum(c["area"] for c in comps) / area
        if tot > phantom: phantom, phantom_t = tot, i
    # 3. object multiplication: count of sizeable ink components over time
    counts = []
    for f in frames:
        _, comps = components(ink_mask(f), min_area=int(0.002 * area)); counts.append(len(comps))
    mult = max(counts) / max(1, min(counts))
    verdict = []
    if morph > 0.10: verdict.append(f"morphing: mid-frame leaves both endpoints by {morph*100:.0f}%")
    if phantom > 0.012: verdict.append(f"phantom object: {phantom*100:.1f}% of frame appears mid-clip (sample {phantom_t})")
    if mult >= 1.6 and max(counts) - min(counts) >= 3: verdict.append(f"objects multiply: components {min(counts)} -> {max(counts)}")
    return {"file": os.path.basename(path), "d_start_end": round(d_se, 3), "morph": round(morph, 3), "phantom": round(phantom, 4),
            "components": counts, "ok": not verdict, "issues": verdict}

# ---------------------------------------------------------------- first/last pairs
def pair_score(a_png, b_png):
    a, b = load_gray(a_png, (160, 90)), load_gray(b_png, (160, 90))
    diff = changed_frac(a, b, thr=40, shifts=range(-4, 5, 2))
    # structure: compare ink layouts coarsely (blocks of 10x10)
    ma, mb = ink_mask(load_rgb(a_png, (160, 90))), ink_mask(load_rgb(b_png, (160, 90)))
    ba = ma.reshape(9, 10, 16, 10).mean(axis=(1, 3)); bb = mb.reshape(9, 10, 16, 10).mean(axis=(1, 3))
    layout = float(np.abs(ba - bb).mean())
    ok = diff < 0.30 and layout < 0.20   # calibrated on ep4: good pairs 0.04/0.03, 0.22/0.18, 0.15/0.10; bad 0.33/0.25, 0.32/0.15, 0.51/0.44, 0.34/0.28
    return {"a": os.path.basename(a_png), "b": os.path.basename(b_png), "pixel_diff": round(diff, 3), "layout_diff": round(layout, 3), "animatable": ok}

# ---------------------------------------------------------------- clocks
def read_clocks(png):
    rgb = load_rgb(png); h, w, _ = rgb.shape
    gray = (rgb[..., 0].astype(int) * 299 + rgb[..., 1].astype(int) * 587 + rgb[..., 2].astype(int) * 114) // 1000
    dark = (gray < 120)
    sc = 2; small = dark[::sc, ::sc]
    _, comps = components(small, min_area=int(0.0008 * small.size))
    clocks = []
    for c in comps:
        x0, y0, x1, y1 = c["bbox"]; bw, bh = x1 - x0 + 1, y1 - y0 + 1
        if bw < 0.03 * small.shape[1] or bw > 0.22 * small.shape[1]: continue
        if abs(bw - bh) > 0.18 * max(bw, bh): continue
        if c["area"] > 0.55 * bw * bh: continue  # filled disc, not a ring
        cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, (bw + bh) / 4
        rad = np.hypot(c["px"] - cx, c["py"] - cy)
        ring = ((rad > 0.72 * r) & (rad < 1.08 * r)).mean()
        if ring < 0.75: continue
        ang = np.degrees(np.arctan2(c["py"] - cy, c["px"] - cx)) % 360
        if len(set((ang // 20).astype(int))) < 16: continue
        CX, CY, R = cx * sc, cy * sc, r * sc
        yy, xx = np.mgrid[max(0, int(CY - R)):min(h, int(CY + R)), max(0, int(CX - R)):min(w, int(CX + R))]
        rr = np.hypot(xx - CX, yy - CY); inside = (rr < 0.70 * R) & (rr > 0.08 * R)
        d2 = (gray[yy, xx] < 110) & inside
        if d2.sum() < 10: continue
        a = (np.degrees(np.arctan2(-(yy[d2] - CY), xx[d2] - CX)) ) % 360  # 0 = 3 o'clock, ccw
        clock_ang = (90 - a) % 360  # 0 = 12 o'clock, clockwise
        rn = rr[d2] / R
        hist = np.zeros(72); lens = np.zeros(72)
        for ca, rv in zip(clock_ang, rn):
            b = int(ca // 5) % 72; hist[b] += 1; lens[b] = max(lens[b], rv)
        order = np.argsort(-hist); peaks = []
        for b in order:
            if hist[b] < 0.08 * hist.max(): break
            if all(min(abs(b - p) * 5, 360 - abs(b - p) * 5) >= 25 for p, _ in peaks):
                peaks.append((b, lens[b]))
            if len(peaks) == 2: break
        if len(peaks) < 2:
            clocks.append({"cx": CX / w, "cy": CY / h, "r": R / w, "time": None, "note": "hands not separable"}); continue
        # longer hand is the minute hand; if lengths are close, the thinner one is the minute hand
        (b1, l1), (b2, l2) = peaks
        if abs(l1 - l2) < 0.12:
            t1, t2 = hist[b1] / max(l1, 1e-6), hist[b2] / max(l2, 1e-6)
            mb, hb = (b1, b2) if t1 <= t2 else (b2, b1)
        elif l1 >= l2: mb, hb = b1, b2
        else: mb, hb = b2, b1
        def refine(b):
            c0 = b * 5 + 2.5
            sel = np.abs(((clock_ang - c0 + 180) % 360) - 180) <= 12
            if sel.sum() == 0: return c0
            d = ((clock_ang[sel] - c0 + 180) % 360) - 180
            return (c0 + d.mean()) % 360
        ma, ha = refine(mb), refine(hb)
        minute = int(round(ma / 6)) % 60
        hour = (ha / 30) % 12
        hour_int = int(math.floor(hour + 1e-6))
        if abs(((hour - hour_int) * 60) - minute) > 30 and minute > 30: hour_int = (hour_int - 1) % 12
        clocks.append({"cx": round(CX / w, 3), "cy": round(CY / h, 3), "r": round(R / w, 3), "hour_angle": round(ha, 1), "minute_angle": round(ma, 1),
                       "time": f"{(hour_int if hour_int else 12)}:{minute:02d}", "hour": hour_int if hour_int else 12, "minute": minute})
    return clocks

WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
           "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
           "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}
HOURS = "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
TENS = "twenty|thirty|forty|fifty"
UNITS = "one|two|three|four|five|six|seven|eight|nine"
TEENS = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"
MIN_RE = rf"(?:(?:{TENS})(?:[- ](?:{UNITS}))?|{TEENS}|oh[- ](?:{UNITS}))"
TIME_RE = re.compile(rf"\b({HOURS})(?:[ -]({MIN_RE}))?\s*(?:(a\.?m\.?|p\.?m\.?|o'clock|in the morning)|(?=[.,;:!]|$))", re.I)

def script_times(text):
    """times mentioned in a narration block -> list of (hour12, minute)."""
    out = []
    for m in TIME_RE.finditer(text):
        hour = WORDNUM[m.group(1).lower()]; mins = m.group(2); marker = m.group(3)
        if mins:
            parts = re.split(r"[- ]", mins.lower()); minute = 0
            for p in parts:
                if p == "oh": continue
                minute += WORDNUM.get(p, 0)
        else:
            minute = 0
            if not marker: continue  # "one" alone without a.m./p.m./o'clock is not a time
        out.append((hour, minute))
    for m in re.finditer(r"\b(\d{1,2}):(\d{2})\b", text):
        h, mi = int(m.group(1)), int(m.group(2))
        if 1 <= h <= 24 and mi < 60: out.append((h % 12 or 12, mi))
    return out

def clock_matches(clock, times, tol_min=12, tol_hour_deg=22):
    """does a read clock agree with any time from the script? Accepts swapped hands (similar lengths)."""
    if not clock.get("time"): return None
    cands = [(clock["hour_angle"], clock["minute_angle"]), (clock["minute_angle"], clock["hour_angle"])]
    for h, mi in times:
        exp_hour_angle = ((h % 12) * 30 + mi * 0.5) % 360; exp_min_angle = (mi * 6) % 360
        for ha, ma in cands:
            dh = abs(((ha - exp_hour_angle + 180) % 360) - 180); dm = abs(((ma - exp_min_angle + 180) % 360) - 180)
            if dh <= tol_hour_deg and dm <= tol_min * 6: return (h, mi)
    return False

# ---------------------------------------------------------------- hero duplicates
def hero_clusters(png, hsv_lo, hsv_hi, min_area=0.003, merge_dist=0.12):
    im = Image.open(png).convert("RGB").resize((320, 180)); hsv = np.asarray(im.convert("HSV")).astype(int)
    m = np.ones(hsv.shape[:2], bool)
    for k in range(3):
        lo, hi = hsv_lo[k], hsv_hi[k]
        if lo <= hi: m &= (hsv[..., k] >= lo) & (hsv[..., k] <= hi)
        else: m &= (hsv[..., k] >= lo) | (hsv[..., k] <= hi)
    _, comps = components(dilate(m, 2), min_area=int(min_area * m.size))
    centers = [(((c["bbox"][0] + c["bbox"][2]) / 2) / 320, ((c["bbox"][1] + c["bbox"][3]) / 2) / 180, c["area"]) for c in comps]
    clusters = []
    for cx, cy, a in centers:
        for cl in clusters:
            if math.hypot(cl[0] - cx, (cl[1] - cy) * 180 / 320) < merge_dist:
                cl[0] = (cl[0] * cl[2] + cx * a) / (cl[2] + a); cl[1] = (cl[1] * cl[2] + cy * a) / (cl[2] + a); cl[2] += a; break
        else: clusters.append([cx, cy, a])
    return [(round(c[0], 2), round(c[1], 2), round(c[2] / m.size, 4)) for c in clusters]

# ---------------------------------------------------------------- isolated black marks (baked arrows, symbols)
def isolated_marks(png):
    rgb = load_rgb(png, (480, 270)); h, w, _ = rgb.shape
    gray = (rgb[..., 0].astype(int) * 299 + rgb[..., 1].astype(int) * 587 + rgb[..., 2].astype(int) * 114) // 1000
    sat = rgb.max(axis=2).astype(int) - rgb.min(axis=2).astype(int)
    black = (gray < 60) & (sat < 60)
    other = ((gray >= 60) & (gray < 215)) | (sat >= 60)   # coloured fills / grey lines (characters, objects)
    _, comps = components(black, min_area=int(0.0006 * black.size))
    marks = []
    for c in comps:
        area = c["area"] / black.size
        if area > 0.03: continue
        x0, y0, x1, y1 = c["bbox"]; bw, bh = x1 - x0 + 1, y1 - y0 + 1
        fill = c["area"] / (bw * bh)
        cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, (bw + bh) / 4
        rad = np.hypot(c["px"] - cx, c["py"] - cy)
        if abs(bw - bh) < 0.2 * max(bw, bh) and ((rad > 0.7 * r) & (rad < 1.1 * r)).mean() > 0.7: continue  # ring (clock, wheel)
        m = np.zeros_like(black); m[c["py"], c["px"]] = True
        ring = dilate(m, 5) & ~dilate(m, 1)
        neighbour_other = other[ring].mean() if ring.any() else 0
        if neighbour_other < 0.06 and (fill < 0.45 or max(bw, bh) / max(1, min(bw, bh)) > 2.2):
            marks.append({"bbox": (round(x0 / w, 2), round(y0 / h, 2), round(x1 / w, 2), round(y1 / h, 2)), "area": round(area, 4), "fill": round(fill, 2), "isolation": round(1 - neighbour_other, 2)})
    return marks

# ---------------------------------------------------------------- CLI
def main():
    if len(sys.argv) < 2: print(__doc__); return
    cmd = sys.argv[1]
    if cmd == "clip":
        for p in sys.argv[2:]: print(json.dumps(clip_report(p), ensure_ascii=False))
    elif cmd == "pair":
        print(json.dumps(pair_score(sys.argv[2], sys.argv[3])))
    elif cmd == "frames":
        d = sys.argv[2]; hero = None
        if "--hero" in sys.argv:
            v = [int(x) for x in sys.argv[sys.argv.index("--hero") + 1].split(",")]; hero = (v[:3], v[3:])
        for f in sorted(glob.glob(os.path.join(d, "F*.png"))):
            row = {"frame": os.path.basename(f), "clocks": [c.get("time") for c in read_clocks(f)], "marks": len(isolated_marks(f))}
            if hero: row["hero_clusters"] = len(hero_clusters(f, *hero))
            print(json.dumps(row))

if __name__ == "__main__": main()
