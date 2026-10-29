#!/usr/bin/env python3
"""
shorts-scout: ежедневный сборщик готовых приколов для YouTube Shorts.

Источники:
  * Reddit  (топ видеопостов за сутки в заданных сабреддитах, OAuth app-only)
  * YouTube (самые просматриваемые Shorts за последние N дней по запросам)

Результат: reports/YYYY-MM-DD.md и .json с отранжированным списком кандидатов.
Опционально: --download скачивает ролики через yt-dlp, --vertical приводит
их к 1080x1920 через ffmpeg.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import requests

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config.json"
STATE_PATH = HERE / "state" / "seen.json"
REPORTS_DIR = HERE / "reports"
DOWNLOADS_DIR = HERE / "downloads"
USER_AGENT = "shorts-scout/0.1 (candidate collector for a Shorts channel)"
TIMEOUT = 30


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_seen() -> dict[str, str]:
    if STATE_PATH.exists():
        with STATE_PATH.open(encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_seen(seen: dict[str, str]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STATE_PATH.open("w", encoding="utf-8") as fh:
        json.dump(seen, fh, ensure_ascii=False, indent=1, sort_keys=True)


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def iso8601_duration_to_seconds(value: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


# --------------------------------------------------------------------------- #
# Reddit
# --------------------------------------------------------------------------- #
def reddit_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_reddit(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        log("[reddit] REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET не заданы, источник пропущен")
        return []

    token = reddit_token(client_id, client_secret)
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
    items: list[dict[str, Any]] = []
    for sub in cfg["subreddits"]:
        url = f"https://oauth.reddit.com/r/{sub}/top"
        params = {"t": cfg.get("period", "day"), "limit": cfg.get("limit_per_sub", 50)}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as exc:
            log(f"[reddit] r/{sub}: {exc}")
            continue
        for child in resp.json().get("data", {}).get("children", []):
            post = child.get("data", {})
            item = reddit_post_to_item(post)
            if item:
                items.append(item)
    log(f"[reddit] собрано видеопостов: {len(items)}")
    return items


def reddit_post_to_item(post: dict[str, Any]) -> dict[str, Any] | None:
    if post.get("over_18") or post.get("stickied"):
        return None
    media = (post.get("media") or {}).get("reddit_video") or \
            (post.get("secure_media") or {}).get("reddit_video")
    url = post.get("url_overridden_by_dest") or post.get("url") or ""
    duration = 0
    width = height = 0
    if media:
        duration = int(media.get("duration") or 0)
        width, height = int(media.get("width") or 0), int(media.get("height") or 0)
        video_url = "https://www.reddit.com" + post["permalink"]
    elif re.search(r"(youtube\.com|youtu\.be|streamable\.com|imgur\.com/.*\.gifv)", url):
        video_url = url
    else:
        return None

    return {
        "id": "reddit:" + post["id"],
        "source": "reddit",
        "title": post.get("title", "").strip(),
        "url": "https://www.reddit.com" + post["permalink"],
        "video_url": video_url,
        "author": "u/" + str(post.get("author")),
        "community": "r/" + str(post.get("subreddit")),
        "score": int(post.get("score") or 0),
        "upvote_ratio": float(post.get("upvote_ratio") or 0),
        "comments": int(post.get("num_comments") or 0),
        "duration_s": duration,
        "width": width,
        "height": height,
        "published": dt.datetime.fromtimestamp(
            post.get("created_utc", 0), tz=dt.timezone.utc).isoformat(),
    }


# --------------------------------------------------------------------------- #
# YouTube Data API
# --------------------------------------------------------------------------- #
def fetch_youtube(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        log("[youtube] YOUTUBE_API_KEY не задан, источник пропущен")
        return []

    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=cfg.get("days_back", 2)))
    since_str = since.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    video_ids: list[str] = []
    for query in cfg["queries"]:
        params = {
            "key": key, "part": "id", "type": "video", "videoDuration": "short",
            "order": "viewCount", "publishedAfter": since_str, "relevanceLanguage": "en",
            "maxResults": cfg.get("limit_per_query", 25), "q": query, "safeSearch": "moderate",
        }
        try:
            resp = requests.get("https://www.googleapis.com/youtube/v3/search",
                                params=params, timeout=TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as exc:
            log(f"[youtube] search '{query}': {exc}")
            continue
        video_ids += [it["id"]["videoId"] for it in resp.json().get("items", [])
                      if it.get("id", {}).get("videoId")]

    video_ids = list(dict.fromkeys(video_ids))
    items: list[dict[str, Any]] = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        params = {"key": key, "part": "snippet,statistics,contentDetails", "id": ",".join(chunk)}
        try:
            resp = requests.get("https://www.googleapis.com/youtube/v3/videos",
                                params=params, timeout=TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as exc:
            log(f"[youtube] videos: {exc}")
            continue
        for v in resp.json().get("items", []):
            duration = iso8601_duration_to_seconds(v["contentDetails"].get("duration", ""))
            if duration == 0 or duration > cfg.get("max_duration_s", 60):
                continue
            stats = v.get("statistics", {})
            sn = v["snippet"]
            items.append({
                "id": "youtube:" + v["id"],
                "source": "youtube",
                "title": sn.get("title", "").strip(),
                "url": f"https://www.youtube.com/shorts/{v['id']}",
                "video_url": f"https://www.youtube.com/watch?v={v['id']}",
                "author": sn.get("channelTitle", ""),
                "community": "youtube",
                "views": int(stats.get("viewCount") or 0),
                "likes": int(stats.get("likeCount") or 0),
                "comments": int(stats.get("commentCount") or 0),
                "duration_s": duration,
                "published": sn.get("publishedAt", ""),
            })
    log(f"[youtube] собрано shorts: {len(items)}")
    return items


# --------------------------------------------------------------------------- #
# ranking
# --------------------------------------------------------------------------- #
def heat(item: dict[str, Any], cfg: dict[str, Any]) -> float:
    """0..100: насколько ролик 'горячий' внутри своего источника + поправки."""
    max_dur = cfg.get("max_duration_s", 60)
    if item["source"] == "reddit":
        base = item["score"] * max(item["upvote_ratio"], 0.5)
        ref = cfg["reddit"].get("reference_score", 20000)
    else:
        age_h = max(hours_since(item["published"]), 1.0)
        base = item["views"] / age_h  # просмотров в час
        ref = cfg["youtube"].get("reference_vph", 20000)
    value = 100.0 * min(base / ref, 1.0)

    dur = item.get("duration_s", 0)
    if dur > max_dur:
        value *= 0.4          # придётся резать
    elif 0 < dur <= 15:
        value *= 0.85         # слишком коротко для удержания
    w, h = item.get("width", 0), item.get("height", 0)
    if w and h and h >= w:
        value = min(value * 1.15, 100.0)  # уже вертикальный
    return round(value, 1)


def hours_since(iso: str) -> float:
    try:
        ts = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return 24.0
    return (dt.datetime.now(dt.timezone.utc) - ts).total_seconds() / 3600


def rank(items: list[dict[str, Any]], cfg: dict[str, Any], seen: dict[str, str]) -> list[dict[str, Any]]:
    fresh = [it for it in items if it["id"] not in seen]
    for it in fresh:
        it["heat"] = heat(it, cfg)
    fresh.sort(key=lambda it: it["heat"], reverse=True)
    return fresh[: cfg.get("top_n", 15)]


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #
def write_report(top: list[dict[str, Any]], day: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS_DIR / f"{day}.json"
    md_path = REPORTS_DIR / f"{day}.md"
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(top, fh, ensure_ascii=False, indent=1)

    lines = [f"# Кандидаты на Shorts, {day}", "",
             "| # | heat | источник | длит. | метрика | название | ссылка |",
             "|---|------|----------|-------|---------|----------|--------|"]
    for n, it in enumerate(top, 1):
        if it["source"] == "reddit":
            metric = f"{it['score']:,} ↑ ({int(it['upvote_ratio'] * 100)}%)"
        else:
            metric = f"{it['views']:,} views"
        dur = f"{it['duration_s']}s" if it.get("duration_s") else "?"
        title = it["title"].replace("|", "¦")[:80]
        lines.append(f"| {n} | {it['heat']} | {it['community']} | {dur} | {metric} | {title} | [открыть]({it['url']}) |")
    lines += ["", "Автор каждого ролика указан в JSON (поле `author`) для подписи в описании Shorts.", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


# --------------------------------------------------------------------------- #
# download / convert
# --------------------------------------------------------------------------- #
def download(top: list[dict[str, Any]], day: str, vertical: bool) -> None:
    if not shutil.which("yt-dlp"):
        log("[download] yt-dlp не найден: pip install yt-dlp")
        return
    out_dir = DOWNLOADS_DIR / day
    out_dir.mkdir(parents=True, exist_ok=True)
    for n, it in enumerate(top, 1):
        stem = f"{n:02d}_{it['id'].replace(':', '_')}"
        target = out_dir / f"{stem}.mp4"
        if target.exists():
            continue
        cmd = ["yt-dlp", "--quiet", "--no-warnings", "--max-filesize", "200M",
               "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
               "--merge-output-format", "mp4", "-o", str(target)]
        cookies = os.environ.get("YTDLP_COOKIES")  # файл cookies.txt, если YouTube просит войти
        if cookies:
            cmd += ["--cookies", cookies]
        cmd.append(it["video_url"])
        log(f"[download] {stem}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not target.exists():
            log(f"[download] не удалось: {res.stderr.strip()[-300:]}")
            continue
        it["file"] = str(target)
        if vertical:
            make_vertical(target)


def make_vertical(src: Path) -> None:
    """1080x1920: оригинал по центру, сзади размытая копия. Файл *_v.mp4."""
    if not shutil.which("ffmpeg"):
        log("[vertical] ffmpeg не найден")
        return
    dst = src.with_name(src.stem + "_v.mp4")
    vf = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "boxblur=20:5[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter_complex", vf,
           "-t", "60", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dst)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        log(f"[vertical] {src.name}: {res.stderr.strip()[-300:]}")


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--download", action="store_true", help="скачать кандидатов через yt-dlp")
    ap.add_argument("--vertical", action="store_true", help="вместе с --download: привести к 9:16")
    ap.add_argument("--no-mark-seen", action="store_true", help="не запоминать показанные ролики")
    ap.add_argument("--input-json", type=Path, help="вместо API взять список из JSON (для отладки)")
    args = ap.parse_args(argv)

    cfg = load_config()
    seen = load_seen()
    day = dt.date.today().isoformat()

    if args.input_json:
        items = json.loads(args.input_json.read_text(encoding="utf-8"))
    else:
        items = fetch_reddit(cfg["reddit"]) + fetch_youtube(cfg["youtube"])

    top = rank(items, cfg, seen)
    if not top:
        log("Кандидатов нет: проверьте ключи API и config.json")
        return 1

    if args.download:
        download(top, day, args.vertical)

    path = write_report(top, day)
    if not args.no_mark_seen:
        for it in top:
            seen[it["id"]] = day
        save_seen(seen)

    print(path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
