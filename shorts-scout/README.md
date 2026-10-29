# shorts-scout

Ежедневный сборщик готовых приколов для англоязычного канала YouTube Shorts.
Скрипт сам ходит по Reddit и YouTube, отбирает самые горячие короткие ролики
за сутки, убирает уже показанные и кладёт отчёт в `reports/ГГГГ-ММ-ДД.md`.
Вам остаётся выбрать из списка, а не искать.

## Что внутри

| Файл | Назначение |
|------|-----------|
| `scout.py` | сбор, ранжирование, отчёт, скачивание, конвертация в 9:16 |
| `config.json` | сабреддиты, поисковые запросы YouTube, размер отчёта |
| `.env.example` | какие ключи нужны |
| `reports/` | ежедневные отчёты (md + json) |
| `state/seen.json` | что уже показывалось (создаётся автоматически) |
| `downloads/` | скачанные ролики (не попадают в git) |

## Источники

| Источник | Что берёт | Ключ |
|----------|-----------|------|
| Reddit | топ видеопостов за сутки в 10 «смешных» сабреддитах | бесплатный, нужен |
| YouTube | самые просматриваемые свежие Shorts по запросам | бесплатный, нужен |
| Telegram | видео из публичных каналов (funnyvideos, funny_videos, fails) | не нужен |
| Dailymotion | трендовые ролики до 60 с из раздела Fun и поиск | не нужен |
| Coub | горячие лупы и теги funny / fail / animals | не нужен |
| Imgur | viral-галерея за сутки, только видео | бесплатный, нужен |
| Twitch | самые просматриваемые клипы за сутки (Just Chatting, Music) | бесплатный, нужен |
| Bluesky | посты с видео по запросам | не нужен, но с серверных IP бывает 403 |

Любой источник выключается в `config.json` полем `"enabled": false`.
Coub и Telegram часто дают контент без слов или на русском, отбирайте по превью.

Не вошли и почему: TikTok и Instagram без входа в аккаунт ничего не отдают,
9GAG закрыт Cloudflare, X (Twitter) API платный. Если захотите TikTok,
самый надёжный путь: yt-dlp с cookies вашего аккаунта по списку профилей.

## Ключи

1. **Reddit.** Откройте <https://www.reddit.com/prefs/apps>, создайте приложение
   типа *script*. Понадобятся `client id` (строка под названием приложения)
   и `secret`.
2. **YouTube Data API v3.** В <https://console.cloud.google.com/apis/credentials>
   создайте проект, включите *YouTube Data API v3*, создайте API key.
   Бесплатной квоты (10 000 единиц в день) хватает с запасом: скрипт тратит
   около 600 единиц за запуск.
3. **Imgur.** <https://api.imgur.com/oauth2/addclient>, тип
   *Anonymous usage without user authorization*. Нужен только Client ID.
4. **Twitch.** <https://dev.twitch.tv/console/apps>, *Register Your Application*,
   категория Other. Нужны Client ID и Client Secret.

Скопируйте `.env.example` в `.env` и заполните. Незаполненные источники
пропускаются, остальные работают.

## Запуск на своём компьютере

```bash
cd shorts-scout
pip install -r requirements.txt
set -a; source .env; set +a
python3 scout.py
```

Отчёт печатается в консоль и сохраняется в `reports/`.

Скачать кандидатов и сразу привести к вертикали 1080x1920 (нужен `ffmpeg`):

```bash
python3 scout.py --download --vertical
```

Файлы окажутся в `downloads/ГГГГ-ММ-ДД/`, вертикальные версии с суффиксом `_v`.
Если YouTube отвечает «Sign in to confirm you're not a bot», экспортируйте
cookies из браузера расширением *Get cookies.txt LOCALLY* и укажите путь
к файлу в `YTDLP_COOKIES`.

Полезные флаги:

* `--no-mark-seen` не запоминать показанные ролики (посмотреть ещё раз).
* `--only telegram,coub` запустить только часть источников.
* `--input-json файл` прогнать ранжирование на готовом списке (отладка).

## Автозапуск в GitHub Actions

Workflow `.github/workflows/shorts-scout.yml` запускается каждый день в 06:00 UTC,
собирает отчёт и коммитит его в репозиторий. Чтобы он заработал, добавьте
секреты в *Settings → Secrets and variables → Actions*:
`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `YOUTUBE_API_KEY`,
`IMGUR_CLIENT_ID`, `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`.
Без ключей отчёт всё равно соберётся из Telegram, Dailymotion и Coub.
Скачивание в Actions не делается: YouTube блокирует загрузку с серверных
адресов. Скачивайте на своём компьютере командой выше.

## Как считается `heat`

У каждого источника своя мера популярности: голоса (Reddit, Imgur), просмотры
в час (YouTube, Telegram, Dailymotion), лайки (Coub, Bluesky), просмотры клипа
(Twitch). Она делится на `reference` источника из `config.json` и даёт 0..100.
Ролики длиннее 60 с получают штраф (придётся резать), короче 15 с небольшой
штраф, уже вертикальные получают бонус. В отчёт попадает не больше
`max_per_source` роликов от одного источника.

Подкручивайте `reference`, если один источник всегда упирается в 100 или
наоборот никогда не поднимается.

## Что писать в описании Shorts

В JSON-отчёте у каждого ролика есть `author` и `url`. Указывайте их в описании
и удаляйте ролик по первой просьбе автора: это снижает риск страйка.
