#!/usr/bin/env python3
"""Semantic QA with a vision model (Claude API). Needs ANTHROPIC_API_KEY in the environment.

Usage:
  qa_semantic.py frames <episode_dir>            asks about every frames/F*.png
  qa_semantic.py clips  <episode_dir>            asks about 6 sampled frames of every clips/*.mp4
Writes <dir>/out/semantic_<mode>.md and .json; exit 1 if any frame/clip is flagged, 2 if no key.

Questions are narrow and answered as JSON so the result is machine-checkable:
  frames: hero_count, other_people, extra_limbs, arrows_or_text, clocks (list of times), style_ok, notes
  clips : per sample -> hands, heads, large_objects, anomaly; flagged if counts jump between samples or any anomaly is named
"""
import sys, os, json, glob, base64, subprocess, tempfile, urllib.request

MODEL = os.environ.get("QA_MODEL", "claude-sonnet-5-5")
KEY = os.environ.get("ANTHROPIC_API_KEY")

FRAME_Q = """You are checking a single frame of a flat-vector animated explainer. Answer ONLY with JSON:
{"hero_count": <int, how many copies of the main character (described below) are visible>,
 "other_people": <int>, "extra_limbs": <true if any person has more than two arms/hands or a limb attached to nothing>,
 "arrows_or_text": <true if the picture itself contains drawn arrows, letters, numbers, speech bubbles or logos; hand-lettered labels in a marker font with a thin curved arrow are NOT counted>,
 "clocks": [<"H:MM" for every clock or watch face visible>], "style_ok": <true if flat vector on white background>, "notes": "<one short sentence>"}
Main character: %s"""

CLIP_Q = """These are %d frames sampled in order from a 5-second animated clip (flat vector, white background). For EACH frame answer with JSON list in order:
[{"hands": <int visible hands>, "heads": <int>, "large_objects": <int count of the main repeated objects such as pans, plates, tickets>, "anomaly": "<empty string or what is wrong: extra limb, duplicated object, object morphing, body part floating>"}]
Only JSON."""

def call(content):
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST",
        headers={"content-type": "application/json", "anthropic-version": "2023-06-01", "x-api-key": KEY},
        data=json.dumps({"model": MODEL, "max_tokens": 600, "messages": [{"role": "user", "content": content}]}).encode())
    with urllib.request.urlopen(req, timeout=120) as r:
        j = json.loads(r.read()); txt = "".join(b.get("text", "") for b in j["content"])
    txt = txt.strip().strip("`"); txt = txt[txt.find("{") if "{" in txt[:5] else txt.find("["):]
    return json.loads(txt[:txt.rfind("}") + 1] if txt.startswith("{") else txt[:txt.rfind("]") + 1])

def img_block(path, maxw=1024):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    tmp = tempfile.mktemp(suffix=".jpg"); im.save(tmp, quality=85)
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(open(tmp, "rb").read()).decode()}}

def main():
    if not KEY: print("ANTHROPIC_API_KEY is not set"); sys.exit(2)
    mode, d = sys.argv[1], sys.argv[2]; out = os.path.join(d, "out"); os.makedirs(out, exist_ok=True)
    plan = json.load(open(os.path.join(d, "plan.json"))); hero = plan.get("hero_description", "the recurring main character of this episode")
    allow = set(plan.get("allow_clones", [])); rows = []; flagged = []
    if mode == "frames":
        for f in sorted(glob.glob(os.path.join(d, "frames", "F*.png"))):
            nm = os.path.basename(f)[:-4]
            try: a = call([img_block(f), {"type": "text", "text": FRAME_Q % hero}])
            except Exception as e: a = {"error": str(e)}
            a["frame"] = nm; rows.append(a)
            if a.get("error") or (a.get("hero_count", 1) > 1 and nm not in allow) or a.get("extra_limbs") or a.get("arrows_or_text") or a.get("style_ok") is False:
                flagged.append(nm)
    else:
        for cp in sorted(glob.glob(os.path.join(d, "clips", "*.mp4"))):
            if "rejected" in cp: continue
            td = tempfile.mkdtemp(); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cp, "-vf", "fps=1.2,scale=768:-1", os.path.join(td, "c%02d.jpg")], check=True)
            fr = sorted(glob.glob(os.path.join(td, "*.jpg")))[:6]
            try: a = call([*(img_block(x) for x in fr), {"type": "text", "text": CLIP_Q % len(fr)}])
            except Exception as e: a = [{"anomaly": f"error {e}"}]
            nm = os.path.basename(cp)[:-4]; rows.append({"clip": nm, "samples": a})
            hands = [s.get("hands", 0) for s in a if isinstance(s, dict)]; objs = [s.get("large_objects", 0) for s in a if isinstance(s, dict)]
            if any(s.get("anomaly") for s in a if isinstance(s, dict)) or (hands and max(hands) - min(hands) >= 2) or (objs and min(objs) and max(objs) >= 1.5 * min(objs)):
                flagged.append(nm)
    rep = [f"# Semantic QA ({mode}) · model {MODEL}", "", f"{len(rows)} items, {len(flagged)} flagged: {', '.join(flagged) or 'none'}", "", "```json", json.dumps(rows, ensure_ascii=False, indent=1), "```"]
    open(os.path.join(out, f"semantic_{mode}.md"), "w").write("\n".join(rep)); json.dump(rows, open(os.path.join(out, f"semantic_{mode}.json"), "w"), ensure_ascii=False, indent=1)
    print(rep[2]); sys.exit(1 if flagged else 0)

if __name__ == "__main__": main()
