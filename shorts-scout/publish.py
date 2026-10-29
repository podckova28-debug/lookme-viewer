#!/usr/bin/env python3
"""
publish.py: превращает выбранные из отчёта ролики в готовые Shorts и загружает их на YouTube.

Пример:
    python3 publish.py reports/2026-10-29.json 1 4 7            # подготовить и загрузить №1, №4, №7
    python3 publish.py reports/2026-10-29.json 1 4 7 --no-upload # только подготовить файлы

Для каждого номера из отчёта:
  1. скачивает ролик (yt-dlp);
  2. генерирует английские заголовок, описание, теги, хук и панчлайн: Claude смотрит
     кадры ролика (нужен ключ Anthropic), иначе шаблон; можно задать вручную (--captions);
  3. перерабатывает видео (edit.py): вертикаль 1080x1920, хук сверху, субтитры по речи,
     панчлайн в финале, подпись канала, полоса прогресса, выровненная громкость;
  4. загружает на YouTube с отложенной публикацией в ближайший свободный слот
     из config.json (YouTube Data API, OAuth).

Всё, что получилось, лежит в ready/<дата>/: видео *_short.mp4 и *_meta.json.
Загруженные ролики запоминаются в state/published.json и повторно не грузятся.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import edit
import scout

HERE = Path(__file__).resolve().parent
READY_DIR = HERE / "ready"
PUBLISHED_PATH = HERE / "state" / "published.json"
TOKEN_PATH = HERE / "state" / "youtube_token.json"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

log = scout.log
Item = dict[str, Any]

DEFAULT_PUBLISH_CFG: dict[str, Any] = {
    "timezone": "America/New_York",
    "slots": ["12:00", "17:00", "21:00"],
    "privacy": "public",
    "category_id": "23",
    "default_tags": ["funny", "fails", "shorts", "comedy", "lol"],
    "claude_model": "claude-opus-5-5",
    "channel_handle": "",
    "subtitles": True,
    "whisper_model": "base",
}


# --------------------------------------------------------------------------- #
# metadata
# --------------------------------------------------------------------------- #
META_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "YouTube Shorts title, English, max 70 characters, no hashtags"},
        "hook": {"type": "string", "description": "On-screen hook shown on top for the whole clip, English, 3-7 words"},
        "punchline": {"type": "string", "description": "Big reaction text for the last seconds, English, 2-5 words"},
        "description": {"type": "string", "description": "One or two short English sentences about the clip"},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "5-10 English search tags"},
    },
    "required": ["title", "hook", "punchline", "description", "tags"],
    "additionalProperties": False,
}

META_PROMPT = """You write metadata for a YouTube Shorts channel that reposts funny clips found online.
Write in natural, casual English for a US audience, even if the source title is in another language.

The attached images are frames from the clip in order, from start to end.

Source platform: {community}
Source title or caption: {title}
Clip length: {duration}

Return:
- title: a curiosity-driven title, max 70 characters, no hashtags, no clickbait lies about what happens
- hook: on-screen text shown on top for the whole clip, 3-7 words, makes people keep watching without spoiling the ending
- punchline: a big reaction shown over the last seconds, 2-5 words, the channel's own joke about what happened
- description: one or two short sentences, no hashtags, no links
- tags: 5-10 lowercase search tags

Hook and punchline are burned into the video in a font without emoji, so do not use emoji in them.
If the frames are unclear, keep the hook generic (for example "Wait for the ending")."""


def clean_title(raw: str) -> str:
    """Убирает из исходного заголовка ссылки, @упоминания, рекламу каналов и хэштеги."""
    text = re.sub(r"https?://\S+|t\.me/\S+|@\w+|#\w+", " ", raw)
    text = re.sub(r"👉.*$", " ", text)
    text = re.sub(r"(?i)\b(shared|made) by\b.*$", " ", text)
    return re.sub(r"\s+", " ", text).strip(" .-|¦")


def template_metadata(it: Item, cfg: dict[str, Any]) -> dict[str, Any]:
    title = clean_title(it.get("title", ""))
    ascii_share = sum(ch.isascii() for ch in title) / max(len(title), 1)
    if len(title) < 4 or ascii_share < 0.8:   # пусто, эмодзи или не по-английски
        title = "Wait for the ending 😂"
    return {
        "title": title[:70],
        "hook": "Wait for the ending...",   # название часто уже вшито в сам ролик, не дублируем
        "punchline": "",
        "description": "Funny moment found online.",
        "tags": list(cfg["default_tags"]),
        "generator": "template",
    }


def claude_metadata(it: Item, cfg: dict[str, Any], frames: list[Path] | None = None) -> dict[str, Any] | None:
    """Генерирует метаданные через Claude по кадрам ролика. None, если SDK или ключ недоступны."""
    try:
        import anthropic
    except ImportError:
        return None
    try:
        client = anthropic.Anthropic()
        response = client.beta.messages.create(
            model=cfg["claude_model"],
            max_tokens=2000,
            # при отказе модели запрос автоматически повторяется на рекомендованной резервной модели
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": META_SCHEMA}},
            messages=[{"role": "user", "content": [
                *[{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                              "data": base64.b64encode(f.read_bytes()).decode()}}
                  for f in (frames or [])],
                {"type": "text", "text": META_PROMPT.format(
                    community=it.get("community", "internet"),
                    title=it.get("title", "") or "(empty)",
                    duration=f"{int(it['duration_s'])} seconds" if it.get("duration_s") else "unknown",
                )},
            ]}],
        )
    except anthropic.AuthenticationError:
        log("[meta] нет ключа Anthropic (ANTHROPIC_API_KEY), использую шаблон")
        return None
    except anthropic.RateLimitError as exc:
        log(f"[meta] лимит Claude API, использую шаблон: {exc}")
        return None
    except anthropic.APIStatusError as exc:
        log(f"[meta] Claude API вернул {exc.status_code}, использую шаблон: {exc.message}")
        return None
    except anthropic.APIConnectionError as exc:
        log(f"[meta] нет связи с Claude API, использую шаблон: {exc}")
        return None
    except TypeError as exc:
        # SDK бросает TypeError, когда не найден ни ключ, ни профиль `ant auth login`
        if "authentication" not in str(exc):
            raise
        log("[meta] нет ключа Anthropic (ANTHROPIC_API_KEY), использую шаблон")
        return None
    if response.stop_reason == "refusal":
        log("[meta] модель отказалась, использую шаблон")
        return None
    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        log("[meta] неожиданный ответ Claude, использую шаблон")
        return None
    data["title"] = data["title"].strip()[:70]
    data["tags"] = [t.strip().lower() for t in data.get("tags", []) if t.strip()][:10]
    data["generator"] = response.model
    return data


def build_metadata(it: Item, cfg: dict[str, Any], use_claude: bool, frames: list[Path] | None = None,
                   override: dict[str, Any] | None = None) -> dict[str, Any]:
    override = override or {}
    manual = {"title", "hook", "punchline"} <= override.keys()
    meta = None if manual else (claude_metadata(it, cfg, frames) if use_claude else None)
    meta = meta or template_metadata(it, cfg)
    if manual:
        meta["generator"] = "manual"
    meta.update({k: v for k, v in override.items() if k in ("title", "hook", "punchline", "description", "tags")})
    title = meta["title"]
    if "#shorts" not in title.lower() and len(title) <= 90:
        title = f"{title} #shorts"
    credit = f"Original by {it['author']}" if it.get("author") else "Original"
    if it.get("community"):
        credit += f" ({it['community']})"
    description = "\n".join([
        meta["description"].strip(),
        "",
        f"🎥 {credit}: {it['url']}",
        "All rights belong to the original creator. If this is your video and you want it",
        "removed or credited differently, leave a comment and it will be handled right away.",
        "",
        "#shorts #funny #fails",
    ])
    tags = list(dict.fromkeys(meta["tags"] + cfg["default_tags"]))
    while len(",".join(tags)) > 450:          # у YouTube лимит 500 символов на все теги
        tags.pop()
    return {"title": title[:100], "hook": meta["hook"].strip(), "punchline": meta.get("punchline", "").strip(),
            "description": description, "tags": tags, "generator": meta["generator"]}


# --------------------------------------------------------------------------- #
# schedule
# --------------------------------------------------------------------------- #
def next_free_slots(count: int, cfg: dict[str, Any], taken: set[str],
                    now: dt.datetime | None = None) -> list[dt.datetime]:
    """Ближайшие свободные слоты публикации в будущем (не раньше чем через 30 минут)."""
    tz = ZoneInfo(cfg["timezone"])
    now = (now or dt.datetime.now(dt.timezone.utc)).astimezone(tz)
    earliest = now + dt.timedelta(minutes=30)
    times = sorted(dt.time.fromisoformat(s) for s in cfg["slots"])
    result: list[dt.datetime] = []
    day = earliest.date()
    while len(result) < count:
        for t in times:
            slot = dt.datetime.combine(day, t, tzinfo=tz)
            key = slot.astimezone(dt.timezone.utc).isoformat()
            if slot >= earliest and key not in taken:
                result.append(slot)
                taken.add(key)
                if len(result) == count:
                    break
        day += dt.timedelta(days=1)
    return result


# --------------------------------------------------------------------------- #
# YouTube upload
# --------------------------------------------------------------------------- #
def youtube_client():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), YOUTUBE_SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        secrets = os.environ.get("YOUTUBE_CLIENT_SECRETS", str(HERE / "client_secret.json"))
        if not Path(secrets).exists():
            raise SystemExit(f"Нет файла OAuth-клиента {secrets}. Как его получить, написано в README.")
        flow = InstalledAppFlow.from_client_secrets_file(secrets, YOUTUBE_SCOPES)
        creds = flow.run_local_server(port=0)   # откроет браузер для входа в аккаунт канала
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def upload(youtube, video: Path, meta: dict[str, Any], cfg: dict[str, Any],
           publish_at: dt.datetime | None) -> str:
    from googleapiclient.http import MediaFileUpload

    status: dict[str, Any] = {"selfDeclaredMadeForKids": False}
    if publish_at:
        # отложенная публикация: YouTube требует privacyStatus=private вместе с publishAt
        status["privacyStatus"] = "private"
        status["publishAt"] = publish_at.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        status["privacyStatus"] = cfg["privacy"]
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"], "tags": meta["tags"],
                    "categoryId": cfg["category_id"], "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": status,
    }
    media = MediaFileUpload(str(video), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            log(f"[upload] {video.name}: {int(progress.progress() * 100)}%")
    return response["id"]


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", type=Path, help="JSON-отчёт из reports/")
    ap.add_argument("numbers", type=int, nargs="+", help="номера роликов из отчёта (колонка #)")
    ap.add_argument("--no-upload", action="store_true", help="только подготовить видео и метаданные")
    ap.add_argument("--now", action="store_true", help="публиковать сразу, без расписания")
    ap.add_argument("--no-claude", action="store_true", help="не звать Claude, только шаблон")
    ap.add_argument("--no-subtitles", action="store_true", help="не распознавать речь для субтитров")
    ap.add_argument("--captions", type=Path,
                    help="JSON с ручными текстами: {\"номер\": {\"title\", \"hook\", \"punchline\", \"subtitles\"}}")
    args = ap.parse_args(argv)

    cfg = {**DEFAULT_PUBLISH_CFG, **scout.load_json(scout.CONFIG_PATH, {}).get("publish", {})}
    report: list[Item] = json.loads(args.report.read_text(encoding="utf-8"))
    overrides: dict[str, Any] = json.loads(args.captions.read_text(encoding="utf-8")) if args.captions else {}
    published: dict[str, Any] = scout.load_json(PUBLISHED_PATH, {})

    picks: list[tuple[int, Item]] = []
    for n in args.numbers:
        if not 1 <= n <= len(report):
            log(f"номера {n} нет в отчёте (всего {len(report)})")
            return 1
        it = report[n - 1]
        if it["id"] in published and published[it["id"]].get("youtube_id"):
            log(f"№{n} уже загружен: https://youtu.be/{published[it['id']]['youtube_id']}, пропускаю")
            continue
        picks.append((n, it))
    if not picks:
        return 0

    out_dir = READY_DIR / args.report.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    taken = {v["publish_at"] for v in published.values() if v.get("publish_at")}
    slots: list[dt.datetime | None] = [None] * len(picks) if args.now else \
        list(next_free_slots(len(picks), cfg, taken))

    youtube = None
    if not args.no_upload:
        youtube = youtube_client()

    ok = 0
    for (n, it), slot in zip(picks, slots):
        stem = f"{n:02d}_{re.sub(r'[^A-Za-z0-9_-]', '_', it['id'])}"
        raw = out_dir / f"{stem}_src.mp4"
        if not scout.download_one(it, raw):
            continue
        override = overrides.get(str(n), {})
        frames = edit.extract_frames(raw, out_dir / ".frames") if not args.no_claude else []
        meta = build_metadata(it, cfg, use_claude=not args.no_claude, frames=frames, override=override)
        want_subs = cfg["subtitles"] and not args.no_subtitles and override.get("subtitles", True)
        try:
            result = edit.render_short(raw, out_dir / f"{stem}_short.mp4", hook=meta["hook"],
                                       punchline=meta["punchline"], subtitles=want_subs,
                                       handle=cfg["channel_handle"], whisper_model=cfg["whisper_model"])
        except (RuntimeError, ValueError) as exc:
            log(f"[edit] №{n}: {exc}")
            continue
        short = Path(result["file"])
        meta["subtitle_chunks"] = result["subtitle_chunks"]
        record = {"source_url": it["url"], "author": it.get("author"), "file": str(short),
                  "title": meta["title"], "publish_at": slot.astimezone(dt.timezone.utc).isoformat() if slot else None}
        (out_dir / f"{stem}_meta.json").write_text(
            json.dumps({**meta, **record}, ensure_ascii=False, indent=1), encoding="utf-8")
        when = slot.strftime("%Y-%m-%d %H:%M %Z") if slot else "сразу"
        log(f"[ready] №{n}: {meta['title']}  ({meta['generator']}, публикация: {when})")

        if youtube is not None:
            video_id = upload(youtube, short, meta, cfg, slot)
            record["youtube_id"] = video_id
            published[it["id"]] = record
            scout.save_json(PUBLISHED_PATH, published)
            log(f"[upload] №{n}: https://youtu.be/{video_id}")
        ok += 1

    log(f"Готово: {ok} из {len(picks)}. Файлы в {out_dir}")
    return 0 if ok == len(picks) else 1


if __name__ == "__main__":
    sys.exit(main())
