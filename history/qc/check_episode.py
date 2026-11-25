# Pre-delivery check for a "Lives in Minutes" episode. Nothing is sent to the user until this passes
# AND the visual review sheets it produces have been looked at frame by frame (see history/qc/README.md).
#
# usage: python3 check_episode.py <episode dir, e.g. history/joan> [--timeline path/to/timeline.json] [--whisper /path/to/venv/python]
#
# Stage A (before generating frames):  --stage plan    -> storyboard lint only (catches unnamed recurring characters)
# Stage B (after frames are downloaded): --stage frames -> + frame files + large review sheets of every frame
# Stage C (final video):                 --stage video  -> + video/audio/package checks + review sheets of every cut
import sys, os, re, json, glob, subprocess, argparse, importlib.util
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("ep"); ap.add_argument("--stage", default="video", choices=["plan", "frames", "video"])
ap.add_argument("--timeline"); ap.add_argument("--whisper")
a = ap.parse_args()
EP = os.path.abspath(a.ep); NAME = os.path.basename(EP)
OUT = os.path.join(EP, "qc"); os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
fails, warns, oks = [], [], []
def run(c): return subprocess.run(c, capture_output=True, text=True).stdout.strip()
def dur(f): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]) or 0)

# ---------- A. storyboard lint ----------
sys.path.insert(0, EP)
spec = importlib.util.spec_from_file_location("shots", os.path.join(EP, "shots.py")); sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
S = sh.S
# words that describe a person who is probably a named recurring character -> must be tied to a character sheet
GENERIC = r"\b(king|queen|prince|princess|dauphin|emperor|tsar|bishop|cardinal|pope|girl|young woman|maiden|heroine|rider in armour|the hero)\b"
names = [n for v in getattr(sh, "WHO", {}).values() for n in v]
for k, (p, l, f, d) in enumerate(S, 1):
    has_sheet = "sheet" in d
    if re.search(GENERIC, d, re.I) and not has_sheet:
        warns.append(f"shot {k}: generic person ('{re.search(GENERIC, d, re.I).group(0)}') without a character sheet — name the character or confirm it is an extra")
    for n in names:
        if re.search(r"\b" + n + r"\b(?!'s)", d) and not has_sheet and not re.search(r"(statue|portrait|tapestry|painting) of " + n, d, re.I):
            fails.append(f"shot {k}: '{n}' appears without '(as in the sheet)' — face will drift")
# every narration line has a shot
vo = {os.path.basename(f)[:-4]: [x for x in open(f) if x.strip()] for f in glob.glob(os.path.join(EP, "vo", "c*.txt"))}
covered = {(p, l) for p, l, f, d in S}
for p, lines in sorted(vo.items()):
    miss = [i for i in range(len(lines)) if (p, i) not in covered]
    if len(miss) > 2: warns.append(f"{p}: lines {miss} have no own shot (long holds)")
    for i, t in enumerate(lines):
        if re.search(r"\boften\b", t, re.I): fails.append(f"{p}:{i} contains 'often' (write 'offen' for TTS)")
# cheap model rule
src = open(os.path.join(EP, "shots.py")).read()
if '"gpt_image_2_6"' in src: fails.append("shots.py requests gpt_image_2_6 (0.75 credits); use gpt_image_2_5 variant flare quality low (0.25)")
oks.append(f"storyboard: {len(S)} shots linted")

# ---------- B. frames ----------
if a.stage in ("frames", "video"):
    FR = os.path.join(EP, "frames"); missing = []
    for k in range(1, len(S) + 1):
        f = os.path.join(FR, f"f{k:03d}.png")
        if not os.path.exists(f): missing.append(k); continue
        w, h = Image.open(f).size
        if abs(w / h - 16 / 9) > .05: fails.append(f"frame {k}: aspect {w}x{h} is not 16:9")
    if missing: fails.append(f"missing frames: {missing}")
    # large review sheets: 4 frames per sheet (960x540 each) so faces, hands and eyes are readable
    for s in range(1, len(S) + 1, 4):
        c = Image.new("RGB", (1920, 1080), "white")
        for j, k in enumerate(range(s, min(s + 4, len(S) + 1))):
            f = os.path.join(FR, f"f{k:03d}.png")
            if not os.path.exists(f): continue
            im = Image.open(f).convert("RGB").resize((960, 540)); d = ImageDraw.Draw(im)
            d.text((8, 6), str(k), font=FONT, fill="red", stroke_width=4, stroke_fill="white")
            c.paste(im, ((j % 2) * 960, (j // 2) * 540))
        c.save(os.path.join(OUT, f"frames_{s:03d}.jpg"), quality=86)
    oks.append(f"frames: review sheets written to {OUT}/frames_*.jpg")

# ---------- C. video + package ----------
if a.stage == "video":
    up = os.path.join(EP, "upload"); mp4 = (glob.glob(os.path.join(up, "*.mp4")) or [None])[0]
    if not mp4: fails.append("upload/: no mp4")
    else:
        mb = os.path.getsize(mp4) / 1e6
        (fails if mb > 100 else oks).append(f"video size {mb:.1f} MB (limit 100)")
        st = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", mp4]))["streams"]
        v = [x for x in st if x["codec_type"] == "video"]; au = [x for x in st if x["codec_type"] == "audio"]
        if not au: fails.append("video has no audio stream")
        if v and (v[0]["width"], v[0]["height"]) != (1920, 1080): fails.append(f"video is {v[0]['width']}x{v[0]['height']}, not 1080p")
        if v and au:
            dv, da = float(v[0].get("duration", 0)), float(au[0].get("duration", 0))
            (fails if abs(dv - da) > .3 else oks).append(f"video {dv:.2f}s vs audio {da:.2f}s")
        D = dur(mp4); (warns if not 480 <= D <= 660 else oks).append(f"duration {int(D // 60)}:{int(D % 60):02d} (format 8-11 min)")
        # music bed audible: every 3-s window sampled across the video (outside the first/last 10 s) must not be near-silent
        quiet = []
        for t0 in range(10, int(D) - 10, 20):
            e = subprocess.run(["ffmpeg", "-v", "info", "-ss", str(t0), "-t", "3", "-i", mp4, "-vn", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
            m = re.search(r"mean_volume: (-?[\d.]+) dB", e)
            if m and float(m.group(1)) < -45: quiet.append((t0, float(m.group(1))))
        (warns if quiet else oks).append(f"near-silent windows (music bed missing?): {quiet}" if quiet else "no near-silent 3-s windows (music bed present)")
        # ending not cut off: last narration line must be heard in the last 20 s
        last = sorted(vo.items())[-1][1][-1].strip() if vo else ""
        if a.whisper and last:
            code = ("import sys,subprocess,numpy as np\nfrom faster_whisper import WhisperModel\n"
                    "m=WhisperModel('small',device='cpu',compute_type='int8')\n"
                    f"a=np.frombuffer(subprocess.run(['ffmpeg','-v','quiet','-sseof','-20','-i',{mp4!r},'-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)\n"
                    "print(' '.join(s.text for s in m.transcribe(a,language='en')[0]))")
            heard = subprocess.run([a.whisper, "-c", code], capture_output=True, text=True).stdout.lower()
            want = re.sub(r"[^a-z ]", "", last.lower()).split()[-3:]
            (oks if all(w in heard for w in want) else fails).append(f"ending: last words {' '.join(want)!r} {'heard' if all(w in heard for w in want) else 'NOT heard'} in the last 20 s")
        else: warns.append("ending not checked by ear (pass --whisper <venv python>)")
        # review sheets of every cut of the FINAL file (captions included)
        if a.timeline:
            cuts = json.load(open(a.timeline))["cuts"]
            for i, (t, c) in enumerate(cuts):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t + .4), "-i", mp4, "-frames:v", "1", "-vf", "scale=960:540", os.path.join(OUT, f"_cut{i:03d}.jpg")])
            for s in range(0, len(cuts), 4):
                cs = Image.new("RGB", (1920, 1080))
                for j in range(4):
                    f = os.path.join(OUT, f"_cut{s + j:03d}.jpg")
                    if os.path.exists(f): cs.paste(Image.open(f), ((j % 2) * 960, (j // 2) * 540))
                cs.save(os.path.join(OUT, f"cuts_{s:03d}.jpg"), quality=86)
            for f in glob.glob(os.path.join(OUT, "_cut*.jpg")): os.remove(f)
            oks.append(f"final video: {len(cuts)} cuts, review sheets in {OUT}/cuts_*.jpg")
        else: warns.append("no --timeline: cut review sheets of the final file not made")
    # package
    thumb = os.path.join(up, "thumbnail_1280x720.jpg")
    if not os.path.exists(thumb) or Image.open(thumb).size != (1280, 720): fails.append("upload/thumbnail_1280x720.jpg missing or not 1280x720")
    rd = os.path.join(up, "README.md")
    if not os.path.exists(rd): fails.append("upload/README.md missing")
    else:
        t = open(rd).read()
        for need, msg in [("## Название", "title"), ("## Описание", "description"), ("## Теги", "tags"), ("ИИ", "AI-disclosure line"), ("0:00", "chapters")]:
            if need not in t: fails.append(f"README: no {msg}")
        if "·" in t: warns.append("README contains '·'")
        if a.timeline:   # chapter timestamps in README must match the chapter cards in the timeline
            cards = [x for x in json.load(open(a.timeline))["cuts"] if str(x[1]).startswith("card")]
            for tc, c in cards:
                stamp = f"{int(tc // 60)}:{int(tc % 60):02d}"
                if stamp not in t: warns.append(f"README: chapter {c} starts at {stamp}, not found in description")

# ---------- report ----------
rep = [f"# QC {NAME} — stage {a.stage}", "", "## Автоматические проверки"]
rep += [f"- ❌ {x}" for x in fails] + [f"- ⚠️ {x}" for x in warns] + [f"- ✅ {x}" for x in oks]
rep += ["", "## Ручной просмотр (обязательно, каждый лист, крупно)",
        "Открыть каждый `frames_*.jpg` и `cuts_*.jpg` и отметить номера кадров с проблемой:",
        "- [ ] главный герой узнаваем в каждом кадре (лицо, причёска, одежда по возрасту из листа)",
        "- [ ] второстепенные персонажи (король, враг, судья) одинаковы во всех сценах",
        "- [ ] в сцене нет лишних персонажей с листа (епископ на коронации и т. п.)",
        "- [ ] глаза, руки, пальцы, лица без мутаций",
        "- [ ] нет анахронизмов (подзорные трубы, современные воротнички, здания, флаги не той стороны)",
        "- [ ] надписи в кадре написаны верно и не повторяются подписью",
        "- [ ] подписи не закрывают лица",
        "- [ ] по звуку: послушать начало, середину, последние 20 с; музыка слышна; нет посторонних звуков",
        "", "Пользователю отправлять только при нуле ❌ и всех отмеченных пунктах."]
open(os.path.join(OUT, "QC_REPORT.md"), "w").write("\n".join(rep) + "\n")
print("\n".join(rep[:3 + len(fails) + len(warns) + len(oks)]))
sys.exit(1 if fails else 0)
