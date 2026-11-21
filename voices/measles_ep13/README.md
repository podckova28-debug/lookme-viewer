# The ENTIRE History of Measles — ep13, полная озвучка

36 реплик (NARRATOR 27, MEASLES 9). WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
MEASLES, «Красный шут» — `voices/refs/role_measles_jester.wav`: Kokoro am_adam, фраза
«Hee hee! Oh, look at all these little faces! Come here, come here, I've got a game for you. Tag! You're it! And you! And you! Hee hee hee!»,
скорость 1.1, затем +3 полутона; exaggeration 0.75, cfg 0.45, temperature 0.8, без эффектов.
Отличается от всех прошлых злодеев (am_santa, am_onyx, bf_emma, bm_fable, am_fenrir, am_eric, am_puck, am_echo, am_liam) и George.

Для синтеза годы и числа словами. Подсказки: Roald Dahl → «Rooahl Dahl», al-Razi → «al Rahzee», Kamehameha → «Kahmayhahmayhah»,
Faroe → Fairoh, Panum → Pahnum, Fiji → Feejee, Cakobau → Thahkombow, Hilleman → Hilluhmun, MMR/SSPE/BFG — по буквам; often → offen.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Переозвучена C01 (3 дубля, выбран лучший): «the writer Roald Dahl» было слито в «writer-rule Dal», теперь «Ruald Dahl».
Верно: Olivia, al-Razi, Fiji, Cakobau («Thakombo»), Enders, Peebles, Edmonston, Hilleman, MMR, Roald Dahl (L18).
Остальные расхождения — числа цифрами; rinderpest → «Rindipest», Kamehameha → «Kamahamaha» (по звуку близко).
