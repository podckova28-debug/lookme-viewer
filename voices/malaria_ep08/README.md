# The ENTIRE History of Malaria — ep08, полная озвучка

56 реплик (NARRATOR 43, MALARIA 13), 8,7 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
MALARIA, «Болотный граф» — `voices/refs/role_malaria_fable_count.wav`: Kokoro bm_fable (британский мужской), фраза
«Ah. Another evening by the marsh. How terribly dull. Do pass me my fur, would you? One gets such a chill... and then, of course, one burns.»,
скорость 0.82, затем −1 полутон; exaggeration 0.35, cfg 0.3 (лениво, медленно, вкрадчиво), temperature 0.7, без эффектов.
От Холеры (тоже bm_fable, но exaggeration 0.85 и «мокрый» эффект) отличается подачей и высотой; от am_santa, am_onyx, bf_emma и George — тембром.

Для синтеза годы и числа написаны словами. Подсказки произношения слитно, без дефисов:
falciparum → falsiparum, Anopheles → Anoffeleez, Secunderabad → Sekunderabad, tertian → tershun, quartan → kworton (в S03 — quartan),
Mala aria → Mahla ahria, Dante → Dahntay, cinchona → sinkohna, Pelletier → Pelltyay, Caventou → Kavahntoo, Alphonse Laveran → Alfonse Lavrahn,
Giovanni Battista Grassi → Jovahnee Bateesta Grahsee, Gorgas → Gorgus (в L29 — «Gorr gus»), DDT → «D D T», Tu Youyou → Too Yoyo,
artemisinin → artemissinin, anaemia → anemia. Plasmodium, Tutankhamun, Hippocrates, Febris, Jesuit, quinine, Cromwell, Ronald Ross модель читает верно сама.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Первый прогон нашёл 4 спорные реплики: C02 «Secunderabad» → «It's a Kundrabad», S03 «quartan» → «Caughton»,
L29 «Gorgas» → «gorgeous», A03 «bitter drink» → «bit of drink». Сделано по 2–4 новых дубля, оставлен лучший:
C02 → «Secunderabad», S03 → «Quartan», L29 → «Gorgas». A03 во всех дублях whisper слышит «bit of drink» (британское «bitter» с выпавшим t) — на слух проверить.

Итог: 51 из 56 ≥ 0.9. Остальные: L10 «boy pharaoh» слито в «boyfaro», L20 Pelletier/Caventou whisper пишет «Pelty I»/«Kavan II» (по звуку pel-TYAY, kah-vahn-TOO),
L35 «Tu Youyou» → «Tu Yo-Yo», T01 числа цифрами.
