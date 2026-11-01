"""
edit.py: превращает исходный ролик в переработанный Shorts.

Что добавляется к каждому ролику:
  * вертикаль 1080x1920 с размытым фоном из того же кадра;
  * заголовок-хук сверху на всё время ролика;
  * субтитры по речи (faster-whisper), только если речь распознана уверенно;
    чужой язык переводится на английский, мат закрывается звёздочками;
  * реакция-панчлайн крупно по центру в последние секунды;
  * подпись канала внизу и полоса прогресса;
  * громкость выровнена под стандарт площадок (-14 LUFS).

Ничего не делается для обхода проверок YouTube: без зеркалирования,
ускорения и смены тона. Переработка здесь в том, что добавлено поверх.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
FONT_FILE = HERE / "fonts" / "Montserrat-ExtraBold.ttf"
FONT_NAME = "Montserrat ExtraBold"
MAX_SECONDS = 60

_whisper_model = None


def log(msg: str) -> None:
    import sys
    print(msg, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# probing
# --------------------------------------------------------------------------- #
def probe(src: Path) -> dict[str, Any]:
    """Длительность видеодорожки, размеры и наличие звука."""
    res = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(src)],
                         capture_output=True, text=True, check=True)
    info = json.loads(res.stdout)
    video = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    if not video:
        raise ValueError(f"в {src.name} нет видеодорожки")
    dur = float(video.get("duration") or info["format"].get("duration") or 0)
    return {"duration": min(dur, MAX_SECONDS), "width": int(video["width"]), "height": int(video["height"]),
            "has_audio": any(s.get("codec_type") == "audio" for s in info["streams"])}


def extract_frames(src: Path, out_dir: Path, count: int = 4, width: int = 512) -> list[Path]:
    """Кадры равномерно по ролику: для Claude, который пишет хук и панчлайн."""
    dur = probe(src)["duration"]
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(count):
        t = dur * (i + 0.5) / count
        path = out_dir / f"{src.stem}_f{i}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
                        "-vf", f"scale={width}:-2", "-q:v", "4", str(path)], check=True)
        frames.append(path)
    return frames


# --------------------------------------------------------------------------- #
# speech -> subtitle chunks
# --------------------------------------------------------------------------- #
PROFANITY = {
    "fuck", "fucking", "fucked", "fucker", "motherfucker", "shit", "shitty", "bullshit", "bitch",
    "bitches", "asshole", "dick", "pussy", "cunt", "bastard", "damn", "goddamn", "nigga", "slut", "whore",
}


def censor(text: str) -> str:
    """Мат в субтитрах режет монетизацию: оставляем первую букву, остальное звёздочками."""
    import re

    def repl(m: "re.Match[str]") -> str:
        w = m.group(0)
        return w[0] + "*" * (len(w) - 1) if w.lower() in PROFANITY else w
    return re.sub(r"[A-Za-z]+", repl, text)


def _split_even(start: float, end: float, text: str, max_words: int = 3) -> list[dict[str, Any]]:
    """Делит фразу на куски по 1-3 слова и раздаёт им время фразы пропорционально длине."""
    words = text.split()
    if not words:
        return []
    groups = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    total = sum(len(" ".join(g)) for g in groups)
    out, t = [], start
    for g in groups:
        seg_text = " ".join(g)
        dur = (end - start) * len(seg_text) / total
        out.append({"start": t, "end": t + dur, "text": seg_text})
        t += dur
    return out


def transcribe(src: Path, duration: float, model_size: str = "base",
               min_logprob: float = -1.0, max_no_speech: float = 0.6) -> list[dict[str, Any]]:
    """Короткие фрагменты по 1-3 слова с таймингом, всегда на английском.

    Английская речь идёт пословно, речь на другом языке переводится на английский
    (перевод Whisper). Пусто, если речи нет или она неразборчива.
    """
    try:
        import numpy as np
        from faster_whisper import WhisperModel
    except ImportError:
        log("[subs] faster-whisper не установлен, субтитры пропущены (pip install faster-whisper)")
        return []
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-t", f"{duration:.2f}", "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    if not raw:
        return []
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = _whisper_model.transcribe(audio, word_timestamps=True, vad_filter=True)
    segments = list(segments)
    foreign = info.language != "en" and info.language_probability >= 0.5
    if foreign:
        log(f"[subs] речь на языке {info.language}, делаю английский перевод")
        segments, _ = _whisper_model.transcribe(audio, task="translate", vad_filter=True)
        segments = list(segments)
    chunks: list[dict[str, Any]] = []
    for seg in segments:
        if seg.avg_logprob < min_logprob or seg.no_speech_prob > max_no_speech:
            continue
        if foreign:      # у перевода нет точных таймингов слов: делим фразу равномерно
            chunks += _split_even(seg.start, seg.end, seg.text.strip())
            continue
        words = [w for w in (seg.words or []) if w.word.strip()]
        group: list[Any] = []
        for w in words:
            group.append(w)
            text = " ".join(x.word.strip() for x in group)
            if len(group) >= 3 or len(text) > 16 or w.word.strip()[-1:] in ".,!?":
                chunks.append({"start": group[0].start, "end": w.end, "text": text})
                group = []
        if group:
            chunks.append({"start": group[0].start, "end": group[-1].end,
                           "text": " ".join(x.word.strip() for x in group)})
    for c in chunks:
        c["text"] = censor(c["text"])
    return chunks


# --------------------------------------------------------------------------- #
# ASS subtitles
# --------------------------------------------------------------------------- #
def _ts(t: float) -> str:
    t = max(t, 0.0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", "\\N")


def build_ass(duration: float, hook: str = "", punchline: str = "",
              chunks: list[dict[str, Any]] | None = None, handle: str = "") -> str:
    # цвета ASS: &HAABBGGRR
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{FONT_NAME},80,&H00FFFFFF,&H00FFFFFF,&H64000000,&H64000000,0,0,0,0,100,100,0,0,3,18,0,8,90,90,150,1
Style: Sub,{FONT_NAME},96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,7,0,2,80,80,560,1
Style: Punch,{FONT_NAME},104,&H0000D7FF,&H0000D7FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,9,0,5,70,70,0,1
Style: Handle,{FONT_NAME},38,&H59FFFFFF,&H59FFFFFF,&H80000000,&H00000000,0,0,0,0,100,100,1,0,1,3,0,2,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events: list[str] = []
    end = _ts(duration)
    if hook:
        events.append(f"Dialogue: 0,{_ts(0)},{end},Hook,,0,0,0,,{{\\fad(150,0)}}{_esc(hook)}")
    punch_start = duration
    if punchline and duration >= 3:
        punch_start = max(duration - 2.5, duration * 0.55)
        pop = r"{\fad(80,0)\fscx70\fscy70\t(0,160,\fscx112\fscy112)\t(160,300,\fscx100\fscy100)}"
        events.append(f"Dialogue: 2,{_ts(punch_start)},{end},Punch,,0,0,0,,{pop}{_esc(punchline.upper())}")
    chunks = chunks or []
    for i, c in enumerate(chunks):
        if c["start"] >= punch_start:      # в финале говорит панчлайн, субтитры не спорят с ним
            break
        next_start = chunks[i + 1]["start"] if i + 1 < len(chunks) else duration
        stop = min(c["end"] + 0.15, next_start, punch_start, duration)   # на экране всегда один фрагмент
        if stop - c["start"] < 0.2:
            continue
        text = censor(c["text"]).strip().rstrip(",;:").upper()   # запятая в конце фрагмента выглядит как ошибка
        events.append(f"Dialogue: 1,{_ts(c['start'])},{_ts(stop)},Sub,,0,0,0,,"
                      f"{{\\fad(40,0)}}{_esc(text)}")
    if handle:
        events.append(f"Dialogue: 0,{_ts(0)},{end},Handle,,0,0,0,,{_esc(handle)}")
    return header + "\n".join(events) + "\n"


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_short(src: Path, dst: Path, *, hook: str = "", punchline: str = "", subtitles: bool = True,
                 handle: str = "", bar_color: str = "0xFFD700", whisper_model: str = "base",
                 max_bitrate_k: int = 2200, manual_subs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Собирает переработанный Shorts. Возвращает сведения о результате (длительность, субтитры).

    manual_subs: свои субтитры [{"start", "end", "text"}] вместо распознавания речи;
    каждая фраза делится на куски по 1-3 слова.
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg не найден")
    info = probe(src)
    dur = info["duration"]
    if manual_subs:
        chunks = [c for ph in manual_subs for c in _split_even(float(ph["start"]), float(ph["end"]), censor(ph["text"]))]
    else:
        chunks = transcribe(src, dur, whisper_model) if (subtitles and info["has_audio"]) else []

    work = dst.parent
    work.mkdir(parents=True, exist_ok=True)
    fonts_dir = work / ".fonts"
    fonts_dir.mkdir(exist_ok=True)
    if not (fonts_dir / FONT_FILE.name).exists():
        shutil.copyfile(FONT_FILE, fonts_dir / FONT_FILE.name)
    ass_path = work / f"{dst.stem}.ass"
    ass_path.write_text(build_ass(dur, hook, punchline, chunks, handle), encoding="utf-8")

    # ffmpeg запускается из папки результата: пути в фильтрах короткие и без экранирования
    vf = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:6,"
          "eq=brightness=-0.08[bg];"
          "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[base];"
          f"color=c={bar_color}:s=1080x12:d={dur:.3f}[bar];"
          f"[base][bar]overlay=x='-w+w*t/{dur:.3f}':y=H-h:shortest=1[barred];"
          f"[barred]ass={ass_path.name}:fontsdir=.fonts[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src.resolve()), "-filter_complex", vf, "-map", "[v]"]
    if info["has_audio"]:
        cmd += ["-map", "0:a:0", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "128k",
                "-ar", "48000"]
    cmd += ["-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
            "-maxrate", f"{max_bitrate_k}k", "-bufsize", f"{max_bitrate_k * 2}k", "-pix_fmt", "yuv420p",
            "-r", "30", "-movflags", "+faststart", str(dst.resolve())]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=work)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg: {res.stderr.strip()[-500:]}")
    return {"file": str(dst), "duration": round(dur, 2), "subtitle_chunks": len(chunks),
            "size_mb": round(dst.stat().st_size / 1024 / 1024, 2)}


# --------------------------------------------------------------------------- #
# watermark / logo detection
# --------------------------------------------------------------------------- #
def _frames(src: Path, start: float, length: float, count: int, width: int) -> "Any":
    """Кадры отрезка ролика как массив (n, h, w, 3) uint8."""
    import numpy as np
    info = probe(src)
    h = int(round(info["height"] * width / info["width"] / 2) * 2)
    fps = max(count / max(length, 0.5), 0.2)
    res = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.2f}", "-t", f"{length:.2f}", "-i", str(src),
                          "-vf", f"fps={fps:.4f},scale={width}:{h},format=rgb24", "-f", "rawvideo", "-"],
                         capture_output=True)
    data = np.frombuffer(res.stdout, np.uint8)
    n = data.size // (width * h * 3)
    return data[: n * width * h * 3].reshape(n, h, width, 3)


WATERMARK_WORDS = (
    "tiktok", "instagram", "youtube", "coub", "wooglobe", "woo globe", "viralhog", "viral hog", "jukin", "failarmy",
    "fail army", "storyful", "newsflare", "caters", "swns", "heartsome", "heartbomb", "rumble", "collab", "ladbible",
    "unilad", "9gag", "memes", "subscribe", "follow", ".com", ".tv", "reels", "kennedy",
)

_ocr_engine = None


def looks_branded(text: str) -> bool:
    """Похожа ли надпись на знак площадки, агентства или ник. Терпима к ошибкам распознавания."""
    import difflib
    import re
    raw = text.strip().lower()
    if raw.startswith("@") or any(w in raw for w in WATERMARK_WORDS):
        return True
    brands = [re.sub(r"[^a-z0-9]", "", w) for w in WATERMARK_WORDS]
    brands = [b for b in brands if len(b) >= 4]
    for token in re.findall(r"[a-z0-9]+", raw) + [re.sub(r"[^a-z0-9]", "", raw)]:
        if len(token) < 4:
            continue
        for b in brands:
            if difflib.SequenceMatcher(None, token, b).ratio() >= 0.78:
                return True
            if len(token) >= 5 and token in b:      # кусок названия: GLOBE, HEART
                return True
    return False


def find_logo(src: Path, frames_per_half: int = 9, width: int = 720) -> dict[str, Any] | None:
    """Ищет водяной знак или ник в углах кадра. None, если углы чистые.

    Для каждой половины ролика строится медианный кадр: движущаяся картинка на нём
    размывается, а наложенная поверх надпись остаётся резкой. Каждый угол медианы
    вырезается, увеличивается вдвое и распознаётся (RapidOCR). Знаком считается
    надпись, похожая на бренд или @ник, или надпись, которая не двигается, пока
    движется всё вокруг. Подписи по центру и мемные заголовки не считаются знаком.
    """
    import numpy as np
    global _ocr_engine
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        log("[logo] rapidocr_onnxruntime не установлен, проверка логотипов пропущена")
        return None
    if _ocr_engine is None:
        _ocr_engine = RapidOCR()
    dur = probe(src)["duration"]
    for half in range(2):
        f = _frames(src, dur * half / 2, dur / 2, frames_per_half, width)
        if f.shape[0] < 3:
            continue
        median = np.median(f, axis=0).astype(np.uint8)
        std = f.astype(np.float32).mean(axis=3).std(axis=0)
        h, w = median.shape[:2]
        ch, cw = int(h * 0.36), int(w * 0.42)
        for vert in ("верх", "низ"):
            for horiz in ("лево", "право"):
                y_off = 0 if vert == "верх" else h - ch
                x_off = 0 if horiz == "лево" else w - cw
                crop = median[y_off:y_off + ch, x_off:x_off + cw]
                crop = np.repeat(np.repeat(crop, 2, axis=0), 2, axis=1)   # мелкие знаки читаются лучше
                result, _ = _ocr_engine(crop)
                for box, text, score in result or []:
                    clean = text.strip()
                    if float(score) < 0.5 or len(clean) < 2:
                        continue
                    xs = [pt[0] / 2 + x_off for pt in box]
                    ys = [pt[1] / 2 + y_off for pt in box]
                    x0, x1, y0, y1 = max(min(xs), 0), min(max(xs), w), max(min(ys), 0), min(max(ys), h)
                    if (x1 - x0) / w > 0.6:          # широкая строка: заголовок или субтитр, а не знак
                        continue
                    branded = looks_branded(clean)
                    inner = std[int(y0):int(y1) + 1, int(x0):int(x1) + 1]
                    pad = 12
                    ring = std[max(int(y0) - pad, 0):int(y1) + pad, max(int(x0) - pad, 0):int(x1) + pad]
                    static_over_motion = inner.size > 0 and float(ring.mean()) > 9 and \
                        float(inner.mean()) < 0.6 * float(ring.mean())
                    if branded or (static_over_motion and len(clean) >= 3):
                        return {"corner": f"{vert}-{horiz}", "text": clean, "branded": bool(branded), "half": half}
    return None
