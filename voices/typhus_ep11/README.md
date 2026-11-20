# The ENTIRE History of Typhus — ep11, полная озвучка

42 реплики (NARRATOR 32, TYPHUS 10), 6,8 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
TYPHUS, «Генерал Вошь» — `voices/refs/role_typhus_echo_general.wav`: Kokoro am_echo (хрипловатый американский мужской), фраза
«At ease, soldier. Sit down, sit down. You look cold. Here, take my coat... it is a little crowded inside, but my men are very good company. We march at dawn.»,
скорость 0.92, затем −1 полутон; exaggeration 0.55, cfg 0.35, temperature 0.75, без эффектов. Французский акцент не делали
(в Kokoro нет мужского французского голоса). Отличается от am_santa, am_onyx, bf_emma, bm_fable, am_fenrir, am_eric, am_puck и George.

Для синтеза годы написаны словами. Подсказки произношения слитно: prowazekii → «prohvazekee eye», Brill-Zinsser → «Brill Zinser»,
Grosse Île → «Grohs Eel», Charles Nicolle → «Sharl Neekol», Stanislaus von Prowazek → «Stanislows fon Prohvazek», Lviv → «Luhveev»,
Rudolf Weigl → «Roodolf Vygul», typhos → «tyfos», DDT → «D D T».

S02 и S03 — новый текст без слова «often» (по просьбе пользователя: голос читал в нём «t»).

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Первый прогон нашёл 2 ошибки: C03 «dug up» → «stuck up», L19 «both died» → «oath died».
Переозвучены (3 дубля, выбран лучший): C03, L19, а также S02 и S03 с новым текстом. Все четыре распознаются верно.
Итог: 39 из 42 ≥ 0.9; остальные — числа цифрами (L08, L16, L21).
