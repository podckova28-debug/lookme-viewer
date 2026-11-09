#!/usr/bin/env python3
"""Build review sheets that make a visual pass fast and hard to get wrong.

Usage: qa_review_sheets.py <episode_dir> --name <basename>
Writes into <dir>/out/review/:
  labels_XX.jpg   every label cropped at 2x from the FINISHED video (text + arrow + target), 4 per sheet
  clip_<name>.jpg every clip at 6 fps as a strip (30 thumbnails) from the clip file
  clocks.jpg      every detected clock cropped, with the time the detector read and the time the script says
  scenes_XX.jpg   every scene of the finished video, 6 per sheet, numbered with block text excerpt
  CHECKLIST.md    what to look at on each sheet
"""
import sys, os, re, json, glob, subprocess, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_vision as qv

def main():
    d = sys.argv[1]; name = sys.argv[sys.argv.index("--name") + 1]
    out = os.path.join(d, "out"); rv = os.path.join(out, "review"); os.makedirs(rv, exist_ok=True)
    for f in glob.glob(os.path.join(rv, "*.jpg")): os.remove(f)
    mp4 = os.path.join(out, name + ".mp4"); srt = os.path.join(out, name + ".srt")
    plan = json.load(open(os.path.join(d, "plan.json"))); blocks = json.load(open(os.path.join(d, "blocks.json")))
    font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot", "fonts", "PatrickHand.ttf"), 26)
    def t(x): h, m, s = x.replace(",", ".").split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
    cues = [(t(a), t(b)) for a, b in re.findall(r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)", open(srt).read())]
    scenes = []
    for bi, (blk, (a, b)) in enumerate(zip(plan["blocks"], cues)):
        total = b - a + 0.4; fixed = sum(x[2] for x in blk if x[0] == "clip" and os.path.exists(os.path.join(d, "clips", f"{x[1]}.mp4"))); rest = total - fixed; cur = a
        for kind, nm, share in blk:
            dur = share if (kind == "clip" and os.path.exists(os.path.join(d, "clips", f"{nm}.mp4"))) else (rest if share is None else rest * share)
            scenes.append({"block": bi, "name": nm, "kind": kind, "t0": cur, "dur": dur}); cur += dur
    def grab(ts, path, w=None):
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{ts:.2f}", "-i", mp4, "-frames:v", "1", "-q:v", "2"]
        if w: cmd += ["-vf", f"scale={w}:-1"]
        subprocess.run(cmd + [path], check=True)
    checklist = ["# Review checklist", ""]
    # --- 1. labels at 2x from the finished video
    tiles = []
    for sc in scenes:
        if sc["kind"] != "still" or sc["name"] not in plan.get("labels", {}): continue
        tmp = os.path.join(rv, "_f.png"); grab(sc["t0"] + sc["dur"] * 0.6, tmp)
        im = Image.open(tmp).convert("RGB"); W, H = im.size
        for lab in plan["labels"][sc["name"]]:
            text, (tx, ty), (ax, ay), (bx, by), size = lab[:5]
            xs = [tx * W, bx * W, ax * W, tx * W + 0.35 * W]; ys = [ty * H, by * H, ay * H, ty * H + 0.12 * H]
            x0, x1 = max(0, min(xs) - 60), min(W, max(xs) + 60); y0, y1 = max(0, min(ys) - 60), min(H, max(ys) + 60)
            crop = im.crop((int(x0), int(y0), int(x1), int(y1)))
            crop.thumbnail((900, 500)); canvas = Image.new("RGB", (960, 540), "white"); canvas.paste(crop, (30, 30))
            ImageDraw.Draw(canvas).text((30, 505), f"{sc['name']}  '{text}'", font=font, fill="red")
            tiles.append(canvas)
    for k in range(0, len(tiles), 4):
        sheet = Image.new("RGB", (1920, 1080), "white")
        for i, tl in enumerate(tiles[k:k + 4]): sheet.paste(tl, ((i % 2) * 960, (i // 2) * 540))
        sheet.save(os.path.join(rv, f"labels_{k // 4 + 1:02d}.jpg"), quality=90)
    checklist += [f"## labels_XX.jpg ({len(tiles)} labels)", "- text fully on white, not touching any drawing", "- arrow starts at the text edge, not inside letters; arrow longer than a thumb; tip touches the object it names",
                  "- the label names what the narration says at that moment", ""]
    # --- 2. clips at 6 fps
    for sc in scenes:
        if sc["kind"] != "clip": continue
        cp = os.path.join(d, "clips", f"{sc['name']}.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", cp, "-vf", "fps=6,scale=384:-1,tile=6x5", "-frames:v", "1", "-vsync", "0", os.path.join(rv, f"clip_{sc['name']}.jpg")], check=True)
    rep = {sc["name"]: qv.clip_report(os.path.join(d, "clips", f"{sc['name']}.mp4")) for sc in scenes if sc["kind"] == "clip"}
    checklist += ["## clip_<name>.jpg (6 fps, read left to right, row by row)", "- count hands/arms/heads in EVERY thumbnail: the count may only change when someone enters from the frame edge",
                  "- count objects (pans, tickets, plates): no duplication, no shrinking range", "- nothing appears above/behind that was not in the first or last frame",
                  "- numeric hints: " + "; ".join(f"{k}: morph {v['morph']}, phantom {v['phantom']}, components {v['components']}" for k, v in rep.items()), ""]
    # --- 3. clocks
    rows = []
    for sc in scenes:
        if sc["kind"] != "still": continue
        fp = os.path.join(d, "frames", f"{sc['name']}.png")
        if not os.path.exists(fp): continue
        clocks = qv.read_clocks(fp)
        if not clocks: continue
        im = Image.open(fp).convert("RGB"); W, H = im.size
        times = qv.script_times(blocks[sc["block"]])
        for c in clocks:
            cx, cy, r = c["cx"] * W, c["cy"] * H, c["r"] * W
            crop = im.crop((int(cx - 1.4 * r), int(cy - 1.4 * r), int(cx + 1.4 * r), int(cy + 1.4 * r))).resize((300, 300))
            verdict = qv.clock_matches(c, times)
            rows.append((crop, f"{sc['name']}: reads {c.get('time')} | script {['%d:%02d' % x for x in times] or 'no time'} | {'OK' if verdict else ('MISMATCH' if verdict is False and times else 'check')}"))
    if rows:
        sheet = Image.new("RGB", (1920, 340 * math.ceil(len(rows) / 4)), "white"); dr = ImageDraw.Draw(sheet)
        for i, (crop, cap) in enumerate(rows):
            x, y = (i % 4) * 480, (i // 4) * 340; sheet.paste(crop, (x + 90, y + 10)); dr.text((x + 10, y + 312), cap[:60], font=font, fill="black")
        sheet.save(os.path.join(rv, "clocks.jpg"), quality=90)
    checklist += [f"## clocks.jpg ({len(rows)} clocks found)", "- every clock must show the time the narration states for that block; detector reading is a hint, trust your eyes", ""]
    # --- 4. all scenes numbered
    tiles = []
    for i, sc in enumerate(scenes):
        tmp = os.path.join(rv, "_s.jpg"); grab(sc["t0"] + sc["dur"] * 0.6, tmp, 960)
        im = Image.open(tmp).convert("RGB"); dr = ImageDraw.Draw(im)
        dr.rectangle((0, 0, 960, 34), fill="white"); dr.text((6, 2), f"{i + 1:02d} {sc['name']} \u00b7 b{sc['block'] + 1}: {blocks[sc['block']][:70]}", font=font, fill="red")
        tiles.append(im)
    for k in range(0, len(tiles), 6):
        sheet = Image.new("RGB", (1920, 1620), "white")
        for i, tl in enumerate(tiles[k:k + 6]): sheet.paste(tl, ((i % 2) * 960, (i // 2) * 540))
        sheet.save(os.path.join(rv, f"scenes_{k // 6 + 1:02d}.jpg"), quality=88)
    checklist += [f"## scenes_XX.jpg ({len(tiles)} scenes)", "- the hero appears exactly once per frame (unless the plan lists the frame under allow_clones)", "- other people look different from the hero",
                  "- no baked-in arrows, text, speech bubbles, logos", "- the picture matches the narration excerpt in the header", "- style: flat vector, white background, same hero design as the reference", ""]
    marks = {sc["name"]: qv.isolated_marks(os.path.join(d, "frames", f"{sc['name']}.png")) for sc in scenes if sc["kind"] == "still" and os.path.exists(os.path.join(d, "frames", f"{sc['name']}.png"))}
    flagged = {k: v for k, v in marks.items() if v}
    mark_lines = [f"- {k}: {len(v)} mark(s) at {[m['bbox'] for m in v]}" for k, v in flagged.items()] or ["- none"]
    checklist += ["## isolated black marks (possible baked arrows/symbols)", *mark_lines, ""]
    for f in glob.glob(os.path.join(rv, "_*")): os.remove(f)
    open(os.path.join(rv, "CHECKLIST.md"), "w").write("\n".join(checklist))
    print("\n".join(checklist)); print("sheets:", sorted(os.path.basename(x) for x in glob.glob(os.path.join(rv, "*.jpg"))))

if __name__ == "__main__": main()
