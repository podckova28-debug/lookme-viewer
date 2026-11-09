"""Cut vertical Shorts from the ep03 master with blurred fill, top title and narration captions."""
import json, os, re, subprocess, sys

ROOT = "/home/user/lookme-viewer"
SRC = f"{ROOT}/out/e2_hulk_v1.mp4"
OUT = f"{ROOT}/out/shorts_ep02"
FONTS = f"{ROOT}/assets/fonts"
HERE = os.path.join(ROOT, "assets/ep02/shorts")
WORDS = json.load(open(f"{HERE}/words.json"))

# (start, end, title line 1, title line 2)
SHORTS = [
    (0.00, 23.95, "YOU STUBBED YOUR TOE.", "NOW THERE'S NO BED."),
    (43.70, 71.00, "ROAD RAGE,", "BUT YOU'RE THE HULK"),
    (104.90, 142.30, "TOO CALM TO HULK OUT?", "DAVE HAS A TRICK"),
]

FIX = {}
# whisper misreads of SFX: "It's now or never" (~0:48), "Slash" whooshes
# word timings corrected from the loudness curve (whisper squeezed them to ~0.05 s)
RETIME = {}

DROP = set()


def words_in(t0, t1):
    out = []
    for seg in WORDS:
        for s, e, w in seg["words"]:
            w = w.strip()
            if s < t0 - 0.05 or e > t1 + 0.05:
                continue
            if (round(s, 1), w) in DROP:
                continue
            s, e = RETIME.get((round(s, 1), w), (s, e))
            out.append([s, e, FIX.get(w, w)])
    # merge "water-" "ski."
    merged = []
    for x in out:
        if merged and merged[-1][2].endswith("-"):
            merged[-1][2] += x[2]
            merged[-1][1] = x[1]
        else:
            merged.append(x)
    return merged


def chunks(ws, maxw=4):
    """Split into phrases at punctuation/pauses, then balance long phrases into <=maxw-word pieces."""
    phrases, cur = [], []
    for w in ws:
        if cur and w[0] - cur[-1][1] > 0.8:
            phrases.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.,?!]$", w[2]):
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    res = []
    for ph in phrases:
        n = -(-len(ph) // maxw)
        size = -(-len(ph) // n)
        for k in range(0, len(ph), size):
            res.append(ph[k:k + size])
    # merge flash-length chunks (mis-timed words) into the following chunk
    out = []
    for c in res:
        if out and out[-1][-1][1] - out[-1][0][0] < 0.35 and c[0][0] - out[-1][-1][1] < 0.5:
            out[-1] = out[-1] + c
        else:
            out.append(c)
    return out


def ts(t):
    t = max(t, 0)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def make_ass(i, t0, t1, l1, l2, path):
    dur = t1 - t0
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Kicker,Comic Neue,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,1,0,1,4,0,8,60,60,280,1
Style: Title,Bangers,118,&H0000E1FF,&H0000E1FF,&H00000000,&H90000000,0,0,0,0,100,100,3,0,1,9,5,8,50,50,350,1
Style: Cap,Bangers,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,2,0,1,8,4,8,80,80,1310,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [
        f"Dialogue: 1,{ts(0)},{ts(dur)},Kicker,,0,0,0,,What If You Woke Up As... · Ep 2",
        f"Dialogue: 1,{ts(0)},{ts(dur)},Title,,0,0,0,,{l1}\\N{l2}",
    ]
    cs = chunks(words_in(t0, t1))
    for k, c in enumerate(cs):
        s = c[0][0] - t0 - 0.05
        e = c[-1][1] - t0 + 0.25
        if k + 1 < len(cs):
            e = min(e, cs[k + 1][0][0] - t0 - 0.05)
        e = min(e, dur)
        txt = " ".join(w[2] for w in c).upper()
        ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\fad(40,40)}}{txt}")
    open(path, "w").write(hdr + "\n".join(ev) + "\n")
    return cs


def build(i, t0, t1, l1, l2):
    ass = f"{HERE}/short_{i}.ass"
    cs = make_ass(i, t0, t1, l1, l2, ass)
    dur = t1 - t0
    VY = 640  # top of the video window
    fc = (
        "[0:v]split=2[a][b];"
        "[a]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.12:saturation=1.1[bg];"
        "[b]scale=1080:608:flags=lanczos[fg];"
        f"[bg][fg]overlay=0:{VY},"
        f"drawbox=x=0:y={VY-6}:w=1080:h=6:color=black@0.9:t=fill,"
        f"drawbox=x=0:y={VY+608}:w=1080:h=6:color=black@0.9:t=fill,"
        f"ass={ass}:fontsdir={FONTS},format=yuv420p[v];"
        f"[0:a]afade=t=in:d=0.12,afade=t=out:st={dur-0.4:.2f}:d=0.4[aout]"
    )
    out = f"{OUT}/short_{i}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", SRC,
           "-filter_complex", fc, "-map", "[v]", "-map", "[aout]", "-r", "24",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(f"short_{i}: {t0:.2f}-{t1:.2f} ({dur:.1f}s)")
    for c in cs:
        print(f"   {c[0][0]-t0:5.2f}  {' '.join(w[2] for w in c)}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sel = [int(a) for a in sys.argv[1:]] or range(1, len(SHORTS) + 1)
    for i in sel:
        build(i, *SHORTS[i - 1])
