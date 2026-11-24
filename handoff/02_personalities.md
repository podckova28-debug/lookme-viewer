# Канал «Личности» — полный бриф (на 24.11.2026)

Ветка с файлами: `claude/clever-keller-n0ul3i` репозитория podckova28-debug/lookme-viewer.

## Формат
«The ENTIRE Life of <имя>» — одна жизнь от рождения до смерти за 8–11 минут, по образцу Archive in Minutes (см. `history/FORMAT.md`).
Настоящее время, третье лицо, без шуток, точные даты; холодное открытие (сцена + парадокс), 10–12 глав, каждая названа предметом
(The Placard, The Oar…) и кончается крючком; один призыв подписаться на ~3:30, совпадающий с крючком; финал возвращается к открытию.
Легенды помечаются в тексте («legend says», «according to»). Без крови и жестокости в кадре.

## Оформление канала
- Название (предложено): **Lives in Minutes** (@livesinminutes); запасные Whole Lives, The Entire Life, Legends Retold.
- Аватар: `handoff/avatars/people_1_profile.png` (профиль-линия, переходящая в линию жизни) или `people_2_book.png` (книга-лавровый венок).
Описание:
```
Whole lives, told in minutes.

Rasputin, Miyamoto Musashi, and the people history could not forget. Every video tells one complete life story, from the first day to the last: the turning points, the enemies, the legends and the truth behind them, with hand-drawn animation, real dates and real sources.

New stories every week. Subscribe so you don't miss the next one.

Sources for every episode are listed in the video description.
```
Ключевые слова (vidIQ: life story 106K/45, biography documentary 84K/58, historical figures 56K/65, biographies 53K/55,
biography of famous people 12K/38, historical figures brought to life 10K/41):
```
biography, biography documentary, biographies, life story, biography of famous people, historical figures, famous historical figures, historical figures brought to life, history documentary, history explained, animated history, entire life, history in minutes, true story, dark history, famous people in history, world history
```
Настройки: Education, английский, «не для детей», раскрытие ИИ = ДА, 3 хэштега (#history первый). Имя героя — в начале названия ролика.

## Готовые ролики
| Ролик | Файлы | Статус |
|---|---|---|
| The ENTIRE Life of Rasputin 10:17 | `history/rasputin/upload/` (mp4, обложка, README) | готов |
| The ENTIRE Life of Miyamoto Musashi ~9:00 | `history/musashi/upload/` | собран; описание/теги ниже — дописать README |
Мусаси: сценарий `history/musashi/script.md` (c00–c09), главы 0:00 Cold open, 0:43 The Placard, 1:33 The Battlefield,
2:27 The Pine Tree, 3:44 The Wooden Sword, 4:32 The Oar, 5:36 The Stone, 6:28 The Brush, 7:17 The Cave, 8:15 The Book.
Обложки `history/musashi/thumbs/` (рекомендую №3 «HE WON WITH AN OAR» или №2 «60 DUELS / 0 DEFEATS»).

## Конвейер
- Кадры: Higgsfield gpt_image_2_6 16:9, комикс-стиль по двум референсам стиля 5d5f0d40-6d72-4644-b3e1-0f824c81becb и
  8e1e1260-e11b-4083-a4d6-5f15a0a4008c + листы персонажей (Мусаси: 3b8f7699-…, 65ea223f-…; Распутин: 1a4d1ac5-…, 589dd8e5-…).
  `shots.py` → партии по 12 → `frames/jobs.txt`/`urls.txt` → `dl.sh`. Проверять листами: лишние конечности, анахронизмы
  (флаги, современные башни/асфальт), неверные иероглифы, чужие костюмы.
- Голос: Chatterbox, референс Kokoro am_echo, exaggeration 0.4, cfg 0.5; японские/русские имена писать фонетически в `cNN.txt`;
  проверка faster-whisper, перезапись 3 сидами (`hist_redo.py`).
- Монтаж: `history/<герой>/make_video.py` (титры глав Bebas Neue, подписи-факты `captions.py` с авторазмещением best_spot,
  звуки `history/sfx` + `mythology/sfx`), музыка `history/music/secret_underscore_90s.mp3` через `drinks/music/mix_music.py`, crf 23 ≤ 100 МБ.
- Подписи: Bebas Neue, белые заглавные, красная полоса снизу, без «·»; не дублировать текст, уже нарисованный в кадре.

## Идеи следующих героев (по данным vidIQ, каналы до 30K)
Miyamoto Musashi (сделан), Frederick Douglass, Lord Byron, Napoleon (побег с Эльбы), Cleopatra («Your life as…» не трогать — это канал Life As),
Nikola Tesla, Genghis Khan, Joan of Arc, Ivan the Terrible, Hernán Cortés, Mata Hari.
