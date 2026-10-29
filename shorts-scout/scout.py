#!/usr/bin/env python3
"""
shorts-scout: ежедневный сборщик готовых приколов для YouTube Shorts.

Источники (включаются в config.json, часть требует бесплатный ключ):
  reddit       топ видеопостов за сутки в сабреддитах            REDDIT_CLIENT_ID/SECRET
  youtube      самые просматриваемые свежие Shorts по запросам   YOUTUBE_API_KEY
  telegram     публичные каналы с видео (превью t.me/s/...)      без ключа
  dailymotion  трендовые короткие видео и поиск                   без ключа
  coub         горячие и тематические луп-видео                   без ключа
  imgur        viral-галерея за сутки, только видео               IMGUR_CLIENT_ID
  twitch       самые просматриваемые клипы за сутки               TWITCH_CLIENT_ID/SECRET
  bluesky      посты с видео по поисковым запросам                без ключа

Результат: reports/YYYY-MM-DD.md и .json с отранжированным списком.
Опционально: --download скачивает ролики через yt-dlp, --vertical приводит
их к 1080x1920 через ffmpeg.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import requests

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config.json"
STATE_PATH = HERE / "state" / "seen.json"
REPORTS_DIR = HERE / "reports"
DOWNLOADS_DIR = HERE / "downloads"
USER_AGENT = "shorts-scout/0.2 (candidate collector for a Shorts channel)"
TIMEOUT = 30
NOW = dt.datetime.now(dt.timezone.utc)

Item = dict[str, Any]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def load_json(path: Path, default: Any) -> Any:
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1, sort_keys=isinstance(data, dict))


def get(url: str, retries: int = 2, **kw: Any) -> requests.Response:
    """GET с повтором: площадки иногда рвут соединение на первом запросе."""
    headers = {"User-Agent": USER_AGENT, **kw.pop("headers", {})}
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=TIMEOUT, **kw)
            resp.raise_for_status()
            return resp
        except (requests.ConnectionError, requests.Timeout):
            if attempt == retries:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("unreachable")


def parse_ts(value: Any) -> dt.datetime:
    """Принимает unix time, ISO-строку или None. Возвращает aware datetime."""
    if value in (None, "", 0):
        return NOW - dt.timedelta(days=1)
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc)
    try:
        ts = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return NOW - dt.timedelta(days=1)
    return ts if ts.tzinfo else ts.replace(tzinfo=dt.timezone.utc)


def hours_since(value: Any) -> float:
    return max((NOW - parse_ts(value)).total_seconds() / 3600, 1.0)


def iso8601_duration_to_seconds(value: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def clock_to_seconds(value: str) -> int:
    """'1:05' -> 65, '0:07' -> 7, '1:02:03' -> 3723."""
    parts = [int(p) for p in value.strip().split(":") if p.isdigit()]
    total = 0
    for p in parts:
        total = total * 60 + p
    return total


def human_to_int(value: str) -> int:
    """'234K' -> 234000, '1.2M' -> 1200000, '987' -> 987."""
    value = value.strip().replace(",", "")
    m = re.fullmatch(r"([\d.]+)\s*([KkMm]?)", value)
    if not m:
        return 0
    num = float(m.group(1))
    mult = {"k": 1_000, "m": 1_000_000}.get(m.group(2).lower(), 1)
    return int(num * mult)


def make_item(*, source: str, uid: str, title: str, url: str, video_url: str,
              author: str, community: str, pop: float, metric: str,
              duration_s: float = 0, width: int = 0, height: int = 0,
              published: Any = None) -> Item:
    return {
        "id": f"{source}:{uid}", "source": source, "title": title.strip()[:200],
        "url": url, "video_url": video_url, "author": author, "community": community,
        "pop": round(float(pop), 2), "metric": metric, "duration_s": round(float(duration_s), 1),
        "width": int(width or 0), "height": int(height or 0),
        "published": parse_ts(published).isoformat(),
    }


# --------------------------------------------------------------------------- #
# Reddit
# --------------------------------------------------------------------------- #
def fetch_reddit(cfg: dict[str, Any]) -> list[Item]:
    client_id, client_secret = os.environ.get("REDDIT_CLIENT_ID"), os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        log("[reddit] REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET не заданы, источник пропущен")
        return []
    resp = requests.post("https://www.reddit.com/api/v1/access_token",
                         auth=(client_id, client_secret), data={"grant_type": "client_credentials"},
                         headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    resp.raise_for_status()
    headers = {"Authorization": "bearer " + resp.json()["access_token"]}

    items: list[Item] = []
    for sub in cfg["subreddits"]:
        try:
            data = get(f"https://oauth.reddit.com/r/{sub}/top", headers=headers,
                       params={"t": cfg.get("period", "day"), "limit": cfg.get("limit_per_sub", 50)}).json()
        except requests.RequestException as exc:
            log(f"[reddit] r/{sub}: {exc}")
            continue
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("over_18") or post.get("stickied"):
                continue
            media = (post.get("media") or {}).get("reddit_video") or \
                    (post.get("secure_media") or {}).get("reddit_video")
            url = post.get("url_overridden_by_dest") or post.get("url") or ""
            permalink = "https://www.reddit.com" + post["permalink"]
            if media:
                video_url, dur = permalink, media.get("duration") or 0
                w, h = media.get("width") or 0, media.get("height") or 0
            elif re.search(r"(youtube\.com|youtu\.be|streamable\.com|imgur\.com/.*\.gifv)", url):
                video_url, dur, w, h = url, 0, 0, 0
            else:
                continue
            score, ratio = int(post.get("score") or 0), float(post.get("upvote_ratio") or 0)
            items.append(make_item(
                source="reddit", uid=post["id"], title=post.get("title", ""), url=permalink,
                video_url=video_url, author="u/" + str(post.get("author")),
                community="r/" + str(post.get("subreddit")), pop=score * max(ratio, 0.5),
                metric=f"{score:,} ↑ ({int(ratio * 100)}%)", duration_s=dur, width=w, height=h,
                published=post.get("created_utc")))
    return items


# --------------------------------------------------------------------------- #
# YouTube Data API
# --------------------------------------------------------------------------- #
def fetch_youtube(cfg: dict[str, Any]) -> list[Item]:
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        log("[youtube] YOUTUBE_API_KEY не задан, источник пропущен")
        return []
    since = (NOW - dt.timedelta(days=cfg.get("days_back", 2))).replace(microsecond=0)
    since_str = since.isoformat().replace("+00:00", "Z")
    ids: list[str] = []
    for query in cfg["queries"]:
        try:
            data = get("https://www.googleapis.com/youtube/v3/search", params={
                "key": key, "part": "id", "type": "video", "videoDuration": "short",
                "order": "viewCount", "publishedAfter": since_str, "relevanceLanguage": "en",
                "maxResults": cfg.get("limit_per_query", 25), "q": query, "safeSearch": "moderate",
            }).json()
        except requests.RequestException as exc:
            log(f"[youtube] search '{query}': {exc}")
            continue
        ids += [it["id"]["videoId"] for it in data.get("items", []) if it.get("id", {}).get("videoId")]

    items: list[Item] = []
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 50):
        try:
            data = get("https://www.googleapis.com/youtube/v3/videos", params={
                "key": key, "part": "snippet,statistics,contentDetails", "id": ",".join(ids[i:i + 50])}).json()
        except requests.RequestException as exc:
            log(f"[youtube] videos: {exc}")
            continue
        for v in data.get("items", []):
            dur = iso8601_duration_to_seconds(v["contentDetails"].get("duration", ""))
            if dur == 0:
                continue
            sn, st = v["snippet"], v.get("statistics", {})
            views = int(st.get("viewCount") or 0)
            items.append(make_item(
                source="youtube", uid=v["id"], title=sn.get("title", ""),
                url=f"https://www.youtube.com/shorts/{v['id']}",
                video_url=f"https://www.youtube.com/watch?v={v['id']}",
                author=sn.get("channelTitle", ""), community="youtube",
                pop=views / hours_since(sn.get("publishedAt")), metric=f"{views:,} views",
                duration_s=dur, published=sn.get("publishedAt")))
    return items


# --------------------------------------------------------------------------- #
# Telegram: публичное превью канала t.me/s/<channel>, последние ~20 постов
# --------------------------------------------------------------------------- #
def fetch_telegram(cfg: dict[str, Any]) -> list[Item]:
    items: list[Item] = []
    max_age_h = cfg.get("days_back", 3) * 24
    for channel in cfg["channels"]:
        try:
            page = get(f"https://t.me/s/{channel}").text
        except requests.RequestException as exc:
            log(f"[telegram] {channel}: {exc}")
            continue
        blocks = re.findall(r'<div class="tgme_widget_message_wrap.*?(?=<div class="tgme_widget_message_wrap|</section>)',
                            page, re.S)
        for b in blocks:
            if "tgme_widget_message_video_player" not in b:
                continue
            post = re.search(r'data-post="([^"]+)"', b)
            when = re.search(r'<time datetime="([^"]+)"', b)
            if not post or not when:
                continue
            if hours_since(when.group(1)) > max_age_h:
                continue
            views = re.search(r'tgme_widget_message_views">([^<]+)<', b)
            dur = re.search(r'message_video_duration[^>]*>([^<]+)<', b)
            txt = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', b, re.S)
            title = htmllib.unescape(re.sub(r"<[^>]+>", " ", txt.group(1))) if txt else ""
            title = re.sub(r"\s+", " ", title).strip() or f"@{channel} video"
            v = human_to_int(views.group(1)) if views else 0
            url = "https://t.me/" + post.group(1)
            items.append(make_item(
                source="telegram", uid=post.group(1).replace("/", "_"), title=title, url=url,
                video_url=url, author="@" + channel, community="t.me/" + channel,
                pop=v / hours_since(when.group(1)), metric=f"{v:,} views",
                duration_s=clock_to_seconds(dur.group(1)) if dur else 0, published=when.group(1)))
    return items


# --------------------------------------------------------------------------- #
# Dailymotion: публичный API, без ключа
# --------------------------------------------------------------------------- #
def fetch_dailymotion(cfg: dict[str, Any]) -> list[Item]:
    items: list[Item] = []
    created_after = int((NOW - dt.timedelta(days=cfg.get("days_back", 3))).timestamp())
    base = {"limit": cfg.get("limit_per_query", 30), "shorter_than": 1, "created_after": created_after,
            "fields": "id,title,views_total,duration,url,aspect_ratio,created_time,owner.screenname"}
    requests_list = [{"channel": "fun", "sort": "trending"}] + \
                    [{"channel": "fun", "search": q, "sort": "visited-today", "languages": "en"}
                     for q in cfg.get("queries", [])]
    for params in requests_list:
        try:
            data = get("https://api.dailymotion.com/videos", params={**base, **params}).json()
        except requests.RequestException as exc:
            log(f"[dailymotion] {params}: {exc}")
            continue
        for v in data.get("list", []):
            ar = float(v.get("aspect_ratio") or 1.78)
            views = int(v.get("views_total") or 0)
            items.append(make_item(
                source="dailymotion", uid=v["id"], title=v.get("title", ""), url=v["url"],
                video_url=v["url"], author=v.get("owner.screenname", ""), community="dailymotion",
                pop=views / hours_since(v.get("created_time")), metric=f"{views:,} views",
                duration_s=v.get("duration") or 0, width=int(1000 * ar), height=1000,
                published=v.get("created_time")))
    return items


# --------------------------------------------------------------------------- #
# Coub: публичный API, без ключа (короткие лупы, часто без языка)
# --------------------------------------------------------------------------- #
def fetch_coub(cfg: dict[str, Any]) -> list[Item]:
    items: list[Item] = []
    max_age_h = cfg.get("days_back", 7) * 24
    feeds = ["https://coub.com/api/v2/timeline/hot"] + \
            [f"https://coub.com/api/v2/timeline/tag/{t}" for t in cfg.get("tags", [])]
    for feed in feeds:
        for page in range(1, cfg.get("pages", 2) + 1):
            try:
                data = get(feed, params={"page": page, "per_page": 25, "order_by": "newest_popular"}).json()
            except requests.RequestException as exc:
                log(f"[coub] {feed}: {exc}")
                break
            for c in data.get("coubs", []):
                if c.get("not_safe_for_work") or c.get("age_restricted") or c.get("banned"):
                    continue
                if hours_since(c.get("created_at")) > max_age_h:
                    continue
                dims = (c.get("dimensions") or {}).get("big") or [0, 0]
                likes, views = int(c.get("likes_count") or 0), int(c.get("views_count") or 0)
                url = "https://coub.com/view/" + c["permalink"]
                items.append(make_item(
                    source="coub", uid=c["permalink"], title=c.get("title") or "coub", url=url,
                    video_url=url, author=(c.get("channel") or {}).get("permalink", ""),
                    community="coub", pop=likes, metric=f"{likes:,} likes / {views:,} views",
                    duration_s=c.get("duration") or 0, width=dims[0], height=dims[1],
                    published=c.get("created_at")))
    return items


# --------------------------------------------------------------------------- #
# Imgur: viral-галерея за сутки (бесплатный Client-ID)
# --------------------------------------------------------------------------- #
def fetch_imgur(cfg: dict[str, Any]) -> list[Item]:
    client_id = os.environ.get("IMGUR_CLIENT_ID")
    if not client_id:
        log("[imgur] IMGUR_CLIENT_ID не задан, источник пропущен")
        return []
    items: list[Item] = []
    headers = {"Authorization": f"Client-ID {client_id}"}
    for page in range(cfg.get("pages", 2)):
        try:
            data = get(f"https://api.imgur.com/3/gallery/hot/viral/day/{page}", headers=headers,
                       params={"showViral": "true", "mature": "false", "album_previews": "false"}).json()
        except requests.RequestException as exc:
            log(f"[imgur] page {page}: {exc}")
            break
        for g in data.get("data", []):
            if g.get("nsfw"):
                continue
            media = (g.get("images") or [g])[0] if g.get("is_album") else g
            if not (media.get("mp4") or str(media.get("type", "")).startswith("video")):
                continue
            ups = int(g.get("ups") or g.get("points") or 0)
            items.append(make_item(
                source="imgur", uid=g["id"], title=g.get("title") or "imgur video", url=g["link"],
                video_url=g["link"], author=g.get("account_url") or "", community="imgur",
                pop=ups, metric=f"{ups:,} ↑ / {int(g.get('views') or 0):,} views",
                width=media.get("width") or 0, height=media.get("height") or 0,
                published=g.get("datetime")))
    return items


# --------------------------------------------------------------------------- #
# Twitch: самые просматриваемые клипы за сутки (бесплатные client credentials)
# --------------------------------------------------------------------------- #
def fetch_twitch(cfg: dict[str, Any]) -> list[Item]:
    client_id, secret = os.environ.get("TWITCH_CLIENT_ID"), os.environ.get("TWITCH_CLIENT_SECRET")
    if not client_id or not secret:
        log("[twitch] TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET не заданы, источник пропущен")
        return []
    resp = requests.post("https://id.twitch.tv/oauth2/token", timeout=TIMEOUT, data={
        "client_id": client_id, "client_secret": secret, "grant_type": "client_credentials"})
    resp.raise_for_status()
    headers = {"Client-Id": client_id, "Authorization": "Bearer " + resp.json()["access_token"]}
    started = (NOW - dt.timedelta(days=cfg.get("days_back", 1))).replace(microsecond=0)
    base = {"first": 100, "started_at": started.isoformat().replace("+00:00", "Z"),
            "ended_at": NOW.replace(microsecond=0).isoformat().replace("+00:00", "Z")}
    items: list[Item] = []
    for game_id in cfg.get("game_ids", []):
        try:
            data = get("https://api.twitch.tv/helix/clips", headers=headers,
                       params={**base, "game_id": game_id}).json()
        except requests.RequestException as exc:
            log(f"[twitch] game {game_id}: {exc}")
            continue
        for c in data.get("data", []):
            if cfg.get("language") and c.get("language") != cfg["language"]:
                continue
            views = int(c.get("view_count") or 0)
            items.append(make_item(
                source="twitch", uid=c["id"], title=c.get("title", ""), url=c["url"], video_url=c["url"],
                author=c.get("broadcaster_name", ""), community="twitch", pop=views,
                metric=f"{views:,} views", duration_s=c.get("duration") or 0,
                published=c.get("created_at")))
    return items


# --------------------------------------------------------------------------- #
# Bluesky: публичный поиск постов, без ключа (с серверных IP иногда 403)
# --------------------------------------------------------------------------- #
def fetch_bluesky(cfg: dict[str, Any]) -> list[Item]:
    items: list[Item] = []
    since = (NOW - dt.timedelta(days=cfg.get("days_back", 2))).replace(microsecond=0)
    for query in cfg.get("queries", []):
        try:
            data = get("https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts", params={
                "q": query, "sort": "top", "limit": cfg.get("limit_per_query", 50), "lang": "en",
                "since": since.isoformat().replace("+00:00", "Z")}).json()
        except requests.RequestException as exc:
            log(f"[bluesky] '{query}': {exc}")
            continue
        for p in data.get("posts", []):
            embed = p.get("embed") or {}
            if embed.get("$type") != "app.bsky.embed.video#view":
                continue
            rkey = p["uri"].rsplit("/", 1)[-1]
            handle = p.get("author", {}).get("handle", "")
            url = f"https://bsky.app/profile/{handle}/post/{rkey}"
            likes = int(p.get("likeCount") or 0)
            ar = embed.get("aspectRatio") or {}
            items.append(make_item(
                source="bluesky", uid=rkey, title=(p.get("record") or {}).get("text") or "bluesky video",
                url=url, video_url=url, author="@" + handle, community="bluesky", pop=likes,
                metric=f"{likes:,} likes / {int(p.get('repostCount') or 0):,} reposts",
                width=ar.get("width") or 0, height=ar.get("height") or 0,
                published=(p.get("record") or {}).get("createdAt")))
    return items


SOURCES: dict[str, Callable[[dict[str, Any]], list[Item]]] = {
    "reddit": fetch_reddit, "youtube": fetch_youtube, "telegram": fetch_telegram,
    "dailymotion": fetch_dailymotion, "coub": fetch_coub, "imgur": fetch_imgur,
    "twitch": fetch_twitch, "bluesky": fetch_bluesky,
}


def collect(cfg: dict[str, Any]) -> list[Item]:
    items: list[Item] = []
    for name, fn in SOURCES.items():
        scfg = cfg["sources"].get(name)
        if not scfg or not scfg.get("enabled", True):
            continue
        try:
            got = fn(scfg)
        except Exception as exc:  # один упавший источник не должен ронять остальные
            log(f"[{name}] ошибка: {exc}")
            continue
        log(f"[{name}] собрано: {len(got)}")
        items += got
    return items


# --------------------------------------------------------------------------- #
# ranking
# --------------------------------------------------------------------------- #
def heat(item: Item, cfg: dict[str, Any]) -> float:
    """0..100: популярность внутри своего источника относительно reference + поправки."""
    ref = float(cfg["sources"].get(item["source"], {}).get("reference", 1) or 1)
    value = 100.0 * min(item["pop"] / ref, 1.0)
    max_dur = cfg.get("max_duration_s", 60)
    dur = item.get("duration_s", 0)
    if dur > max_dur:
        value *= 0.4          # придётся резать
    elif 0 < dur <= 15:
        value *= 0.85         # коротко для удержания
    if item.get("width") and item.get("height") and item["height"] >= item["width"]:
        value = min(value * 1.15, 100.0)  # уже вертикальный
    return round(value, 1)


def rank(items: list[Item], cfg: dict[str, Any], seen: dict[str, str]) -> list[Item]:
    unique = {it["id"]: it for it in items}          # один ролик мог прийти из двух запросов
    fresh = [it for it in unique.values() if it["id"] not in seen]
    for it in fresh:
        it["heat"] = heat(it, cfg)
    fresh.sort(key=lambda it: it["heat"], reverse=True)
    top: list[Item] = []
    per_source: dict[str, int] = {}
    cap = cfg.get("max_per_source", 6)
    for it in fresh:               # не даём одному источнику забить весь список
        if per_source.get(it["source"], 0) >= cap:
            continue
        per_source[it["source"]] = per_source.get(it["source"], 0) + 1
        top.append(it)
        if len(top) >= cfg.get("top_n", 15):
            break
    return top


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #
def write_report(top: list[Item], day: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    save_json(REPORTS_DIR / f"{day}.json", top)
    md_path = REPORTS_DIR / f"{day}.md"
    lines = [f"# Кандидаты на Shorts, {day}", "",
             "| # | heat | источник | длит. | метрика | название | ссылка |",
             "|---|------|----------|-------|---------|----------|--------|"]
    for n, it in enumerate(top, 1):
        dur = f"{int(it['duration_s'])}s" if it.get("duration_s") else "?"
        title = it["title"].replace("|", "¦").replace("\n", " ")[:80]
        lines.append(f"| {n} | {it['heat']} | {it['community']} | {dur} | {it['metric']} | {title} | [открыть]({it['url']}) |")
    lines += ["", "Автор каждого ролика указан в JSON (поле `author`) для подписи в описании Shorts.", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


# --------------------------------------------------------------------------- #
# download / convert
# --------------------------------------------------------------------------- #
def download_one(it: Item, target: Path) -> bool:
    """Скачивает один ролик в target (.mp4). True, если файл на месте."""
    if target.exists():
        return True
    if not shutil.which("yt-dlp"):
        log("[download] yt-dlp не найден: pip install yt-dlp")
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["yt-dlp", "--quiet", "--no-warnings", "--max-filesize", "200M",
           "--retries", "5", "--extractor-retries", "5",
           "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
           "--merge-output-format", "mp4", "-o", str(target)]
    cookies = os.environ.get("YTDLP_COOKIES")  # файл cookies.txt, если площадка просит войти
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append(it["video_url"])
    log(f"[download] {target.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not target.exists():
        log(f"[download] не удалось: {res.stderr.strip()[-300:]}")
        return False
    return True


def download(top: list[Item], day: str, vertical: bool) -> None:
    out_dir = DOWNLOADS_DIR / day
    for n, it in enumerate(top, 1):
        target = out_dir / f"{n:02d}_{re.sub(r'[^A-Za-z0-9_-]', '_', it['id'])}.mp4"
        if download_one(it, target):
            it["file"] = str(target)
            if vertical:
                make_vertical(target)


FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def find_font(preferred: str | None = None) -> str | None:
    for path in ([preferred] if preferred else []) + FONT_CANDIDATES:
        if path and Path(path).exists():
            return path
    if shutil.which("fc-match"):
        res = subprocess.run(["fc-match", "-f", "%{file}", "sans:bold"], capture_output=True, text=True)
        if res.returncode == 0 and Path(res.stdout.strip()).exists():
            return res.stdout.strip()
    return None


def make_vertical(src: Path, caption: str | None = None, font: str | None = None,
                  dst: Path | None = None) -> Path | None:
    """1080x1920: оригинал по центру, сзади размытая копия, сверху подпись.

    Возвращает путь к готовому файлу (по умолчанию *_v.mp4) или None при ошибке.
    """
    if not shutil.which("ffmpeg"):
        log("[vertical] ffmpeg не найден")
        return None
    dst = dst or src.with_name(src.stem + "_v.mp4")
    vf = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "boxblur=20:5[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
    if caption:
        fontfile = find_font(font)
        if fontfile:
            # ffmpeg запускается из папки результата, поэтому шрифт и текст передаются
            # короткими относительными именами: так не нужно экранировать пути (Windows, пробелы)
            import textwrap
            local_font = dst.parent / "caption_font.ttf"
            if not local_font.exists():
                shutil.copyfile(fontfile, local_font)
            # каждая строка рисуется отдельным drawtext: так она центрируется в любой версии ffmpeg
            for i, line in enumerate(textwrap.wrap(caption, 20)[:3]):
                text_file = dst.parent / f"{dst.stem}.caption{i}.txt"
                text_file.write_text(line, encoding="utf-8")
                vf += (f",drawtext=fontfile={local_font.name}:textfile={text_file.name}"
                       ":fontsize=68:fontcolor=white:borderw=4:bordercolor=black"
                       ":box=1:boxcolor=black@0.55:boxborderw=18"
                       f":x=(w-text_w)/2:y={170 + i * 100}")
        else:
            log("[vertical] шрифт не найден, подпись пропущена")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src.resolve()), "-filter_complex", vf,
           "-t", "60", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dst.resolve())]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=dst.parent)
    if res.returncode != 0:
        log(f"[vertical] {src.name}: {res.stderr.strip()[-300:]}")
        return None
    return dst


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--download", action="store_true", help="скачать кандидатов через yt-dlp")
    ap.add_argument("--vertical", action="store_true", help="вместе с --download: привести к 9:16")
    ap.add_argument("--no-mark-seen", action="store_true", help="не запоминать показанные ролики")
    ap.add_argument("--only", help="запустить только перечисленные источники, через запятую")
    ap.add_argument("--input-json", type=Path, help="вместо API взять список из JSON (для отладки)")
    args = ap.parse_args(argv)

    cfg = load_json(CONFIG_PATH, None)
    if cfg is None:
        log(f"нет файла {CONFIG_PATH}")
        return 1
    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        for name in cfg["sources"]:
            cfg["sources"][name]["enabled"] = name in wanted
    seen = load_json(STATE_PATH, {})
    day = dt.date.today().isoformat()

    if args.input_json:
        items = json.loads(args.input_json.read_text(encoding="utf-8"))
    else:
        items = collect(cfg)

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
        save_json(STATE_PATH, seen)

    print(path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
