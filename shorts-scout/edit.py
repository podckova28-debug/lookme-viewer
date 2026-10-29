"""
edit.py: превращает исходный ролик в переработанный Shorts.

Что добавляется к каждому ролику:
  * вертикаль 1080x1920 с размытым фоном из того же кадра;
  * заголовок-хук сверху на всё время ролика;
  * субтитры по речи (faster-whisper), только если речь распознана уверенно;
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
def transcribe(src: Path, duration: float, model_size: str = "base",
               min_logprob: float = -1.0, max_no_speech: float = 0.6) -> list[dict[str, Any]]:
    """Короткие фрагменты по 1-3 слова с таймингом. Пусто, если речи нет или она неразборчива."""
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
    segments, _ = _whisper_model.transcribe(audio, word_timestamps=True, vad_filter=True)
    chunks: list[dict[str, Any]] = []
    for seg in segments:
        if seg.avg_logprob < min_logprob or seg.no_speech_prob > max_no_speech:
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
    for c in chunks or []:
        if c["start"] >= punch_start:      # в финале говорит панчлайн, субтитры не спорят с ним
            break
        stop = min(c["end"] + 0.15, punch_start, duration)
        if stop - c["start"] < 0.2:
            continue
        text = c["text"].strip().rstrip(",;:").upper()   # запятая в конце фрагмента выглядит как ошибка
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
                 max_bitrate_k: int = 2200) -> dict[str, Any]:
    """Собирает переработанный Shorts. Возвращает сведения о результате (длительность, субтитры)."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg не найден")
    info = probe(src)
    dur = info["duration"]
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
