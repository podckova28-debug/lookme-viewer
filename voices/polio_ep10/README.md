# The ENTIRE History of Polio — ep10, полная озвучка

45 реплик (NARRATOR 35, POLIO 10), 7,3 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
POLIO, «Mister Summer» — `voices/refs/role_polio_eric.wav`: Kokoro am_eric (американский мужской), фраза
«Well hello there, folks! Isn't it a swell summer day? Come on down to the pool, kids, the water's just fine! Everybody's welcome. Everybody.»,
скорость 1.0, без сдвига высоты; exaggeration 0.7, cfg 0.4, temperature 0.75 (бодро, приторно), без эффектов.
Отличается от am_santa, am_onyx, bf_emma, bm_fable, am_fenrir, am_puck (Испанка) и George.

Для синтеза годы и числа написаны словами. Подсказки произношения слитно, без дефисов:
Landsteiner → Landshtyner, Franklin Delano Roosevelt → «Franklin Dellanoh Rohzavelt», Salk → Sawlk, Sabin → Saybin,
formaldehyde → formaldahyde, Pittsburgh → Pittsburg. Остальное (March of Dimes, Harvard, Paul Alexander, Elizabeth Kenny, Cutter, Rotary, Copenhagen,
Pakistan, Afghanistan, Napoleon) модель читает верно сама.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Первый прогон нашёл 1 ошибку: C02 «breathes for him» → «breeds for him». Сделано 3 новых дубля, все верные; оставлен первый.
Итог: 41 из 45 ≥ 0.9. Остальные — только числа цифрами (L06, L10, L26, L27).
Salk whisper пишет «Sork» — это британское чтение рассказчика (sɔːlk), ударение и гласная верные. Landsteiner → «Carl Landsteiner», Sabin, Roosevelt — верно.
