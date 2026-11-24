# Канал «Еда и напитки» — полный бриф (на 24.11.2026)

Ветка с файлами: `claude/clever-keller-n0ul3i` репозитория podckova28-debug/lookme-viewer. Всё ниже — пути в этой ветке.

## Решения пользователя
- Канал про историю напитков и еды, на английском. Старый канал Catching History (@catchinghistories) бросаем: по аналитике там
  ±13–19 тыс. подписок/отписок в день и 1 428 просмотров с внешней ссылки за один день (похоже на накрутку/сервис раскрутки),
  из-за этого ролики не проходят первую пробу алгоритма. Пользователь создаёт НОВЫЙ канал и начинает с абсента.
- Никакой накрутки, взаимных подписок, сервисов раскрутки. Ничего не публиковать самим — только готовить пакеты.
- Ключевые слова канала задаются один раз, общие для ниши; под каждый продукт меняются только название/описание/теги ролика.

## Оформление нового канала
Аватар: `handoff/avatars/food_1_glass.png` (бокал со слоями-эпохами: янтарь, зелень, вино) или `food_2_fork_glass.png`.
Описание:
```
The entire history of the things we drink and eat, told in a few minutes.

Why was absinthe banned for 95 years? How did a waste product of sugar become the drink of navies and pirates? What did Vikings really drink? Every episode takes one drink or dish and follows it through wars, empires, scandals, myths and the people who made it famous.

Hand-drawn animated history, real sources, no boring lectures.
New episodes every week: drinks, food, and the strange stories behind them.

Subscribe and pour yourself something.
```
Ключевые слова канала (через запятую):
```
food history, history of food, drink history, history of drinks, history of alcohol, alcohol history, food and drink history, history documentary, history explained, animated history, history facts, history of everyday things, origin of food, food documentary, drinks explained
```
Данные vidIQ (поисков/мес, конкуренция): food history 227K/58, history of coffee 116K/63, history of food 113K/58,
american food history 65K/**37**, history of alcohol 34K/53, history of wine 30K/47, pirate history 26K/45, age of sail 15K/**32**,
history of beer 12.5K/50, coffee facts 11.5K/40, history of absinthe 3.9K/**34**; «history of rum» < 750 → ром продавать через пиратов.
Настройки: Education, английский, «не для детей» (алкоголь), раскрытие ИИ = ДА, 3 хэштега, первый #history.

## Готовые ролики
| Ролик | Файлы | Статус |
|---|---|---|
| The ENTIRE History of Absinthe (The Drink That Drove Paris Mad?) 6:38 | `drinks/absinthe/upload/` (mp4 84 МБ, thumbnail, README с описанием/таймкодами/тегами) | готов, первый на новом канале |
| The ENTIRE History of Rum (From Trash to Empire) 7:27 | `drinks/rum/upload/` | готов; для нового канала название лучше «…Rum: The Drink of Pirates and Navies»; кадр 60 (лишняя рука) уже исправлен |
| The ENTIRE History of Mead 5:27 | `drinks/mead/upload/` | готов (старый формат) |
План выкладки на новом канале: абсент → ром (через 2–3 дня) → медовуха → кофе (следующий новый, анонсирован в конце абсента).
На старом канале ром и медовуху сделать приватными.

## Как делается ролик (конвейер)
- Сценарий: `drinks/<тема>/script.md`, 9 частей p0–p8, ~1300 слов (≈7 мин). Хук = сцена от 2-го лица («You are in a café in Paris, 1890…»)
  + парадокс + большое число + вопрос; каждая часть кончается крючком; в конце «Would you…? Tell me in the comments. Next time: …».
  В тексте для TTS не писать «often» (писать «offen»); сложные имена — фонетически (см. `drinks/absinthe/` TTS-замены в истории сессии:
  Pernod→Pair-noh, louche→loosh, thujone→thoo-jone и т. п.).
- Кадры: `shots.py` (≈120 кадров, (part, line, prompt, note)), стиль: «White background; detailed ink-line illustration, fine cross-hatching,
  soft muted watercolour, … accents; cut out on white», белый человечек-«you», рукописные пометки с цифрами/датами.
  Генерация Higgsfield gpt_image_2_6 16:9 партиями по 12, `frames/jobs.txt` + `urls.txt`, скачивание `dl.sh`, jpg-копии в git.
  ВСЕГДА проверять кадры листами 4×3: лишние руки/пальцы, анахронизмы (флаги, асфальт, современные башни), кривые надписи.
- Голос: Chatterbox, референс Kokoro bm_fable (`refs/kokoro_bm_fable.wav`), exaggeration 0.5, cfg 0.5, temp 0.7; проверка faster-whisper,
  плохие фразы перезаписываются 4 сидами, выбор в `picks.txt`. Higgsfield на озвучку не тратить.
- Монтаж: `drinks/absinthe/absinthe_video.py` (медленный наезд/отъезд на каждом кадре), музыка `drinks/music/mix_music.py` + `tavern_bed_90s.mp3`,
  финал перекодировать ≤ 100 МБ (GitHub), громкость ≈ −15 LUFS.
- Обложки: 3 варианта в `thumbs/`, стиль как у рома («made from TRASH») — рисунок + крупная рукописная фраза.

## Следующие темы (по данным vidIQ)
Coffee (116K поисков), Wine («the drink safer than water»), Beer, Tea, Gin («nearly destroyed London»), Vodka, Chocolate,
американская еда/газировка (низкая конкуренция: Pepsi, Coca-Cola, Ketchup, Hamburger), Hot Sauce, Sushi.

## Ускоренная проверка формата (предложено пользователю)
Shorts из готовых роликов (ответ за 24–48 ч), правило остановки: через 48 ч CTR < 3 % или досмотр < 30 % → менять обложку/начало;
5 роликов подряд < 1 000 просмотров за неделю → менять формат. Платный тест Google Ads ($20–30) — по желанию.
