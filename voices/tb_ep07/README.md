# The ENTIRE History of Tuberculosis — ep07, полная озвучка

51 реплика (NARRATOR 39, TB 12), 7,8 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
TB, «Белая дама» — `voices/refs/role_tb_emma_low.wav`: Kokoro bf_emma (британский взрослый женский), фраза
«Ah... you've come to visit me. How kind. Do sit down, my dear. Mind the candle. I'm afraid I'm rather tired this evening... but then, I always am.»,
скорость 0.84, затем −1 полутон; exaggeration 0.4, cfg 0.3 (медленно, тихо), temperature 0.7, без эффектов.
Первый женский злодей канала; отличается от Lewis (Чума), C4_fable_wet (Холера), daniel_low (Оспа), am_puck (Испанка), santa_low (Цинга), onyx (Бешенство).

Для синтеза годы написаны словами. Подсказки произношения слитно, без дефисов:
phthisis → thighsis, Koch → Kokh, Frederic Chopin → Fredrik Showpan, Bronte → Brontee, La Traviata → La Traviahta, La Boheme → La Bohem,
Calmette → Kalmet, Camille Guerin → Kameel Gairan, BCG → «B C G», Schatz → Shats, HIV → «H I V», «and 90s» → «and nineties».
Mycobacterium tuberculosis, tubercles, Hippocrates, scrofula, tuberculin, streptomycin, Waksman модель читает верно сама.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Первый прогон нашёл 4 настоящие ошибки: C04 «Vampires» → «Fumpies», L22 «His talk» → «is taught»,
L17 «La Boheme» → «Labelhem», L27 «Mountain air» слито в «mountaineer». Сделано по 2–4 новых дубля, оставлен лучший:
C04, L22 и L17 теперь распознаются верно (L17: «La Bohème»). L27 во всех дублях whisper пишет «mountaineer» — это слияние на стыке слов, на слух проверить.

Итог: 46 из 51 ≥ 0.9. Остальные: цифры вместо слов (L13, L14 «90,000», L17), L28 Calmette/Guerin whisper пишет «Kelmet»/«Guiron» — близко к kal-MET / gay-RAN.
