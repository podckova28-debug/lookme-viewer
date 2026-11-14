# The ENTIRE History of Leprosy — ep09, полная озвучка

51 реплика (NARRATOR 38, LEPROSY 13), 7,9 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
LEPROSY, «Серый монах» — `voices/refs/role_leprosy_fenrir_monk.wav`: Kokoro am_fenrir, фраза
«Shh... there's no need to hurry, my child. Sit with me a while. I've waited a very long time... and I can wait a little longer.»,
скорость 0.8, затем −2 полутона; exaggeration 0.3, cfg 0.3 (тихо, очень медленно), temperature 0.7, без эффектов.
Отличается от am_santa (Цинга), am_onyx (Бешенство), bf_emma (Туберкулёз), bm_fable (Холера, Малярия), Lewis/Daniel (Чума, Оспа), am_puck (Испанка).

Для синтеза годы написаны словами. Подсказки произношения слитно, без дефисов:
leprae → lepree, Gerhard Armauer Hansen → Gairhard Armower Hahnsen, Hansen → Hahnsen, Kalaupapa → Kahlowpahpah, Molokai → Molokye,
Sushruta → Sooshroota, chaulmoogra → chawlmoogra, tzaraat → «tsarah aht», lazar → lazzer, Montgisard → Monzheezar, Bergen → Bairgen,
Carville → Karvil, Guy Faget → Ghee Fazhay, Promin → Prohmin. Damien, Lazarus, Baldwin, Saladin, armadillos, Alice Ball, dapsone — как есть.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. 46 из 51 ≥ 0.9, переозвучка не понадобилась.
Расхождения: C03 — только кавычки вокруг 'you lepers' / 'we lepers' (текст распознан дословно); числа цифрами (L19, L33, T01);
L19 Montgisard → «Monsiza»; L31 Carville → «Carvel», Guy Faget → «Guy Fuzz Hai», sulfa → «sulfur» (на слух близко к KAR-vil, GEE fa-ZHAY).
Kalaupapa whisper пишет «Kalapapa/Kalopapa», Molokai — «Molokie», chaulmoogra — «Cholmugra», tzaraat — «Sarah Art», dapsone — «Dapsoni».
