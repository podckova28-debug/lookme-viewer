# The ENTIRE History of the Spanish Flu — ep04, полная озвучка

55 реплик, 8,0 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
FLU — `voices/refs/role_flu_am_puck.wav`: Kokoro am_puck (американский, молодой, лёгкий), фраза
«Oh, don't look at me like that! I'm only passing through, darling…», скорость 1.05; exaggeration 0.7, cfg 0.45, temperature 0.8, без эффектов.
Отличается от Lewis (Чума), C4_fable_wet (Холера) и daniel_low (Оспа).

Для синтеза годы написаны словами; подсказки произношения слитно, без дефисов и заглавных внутри слова
(иначе модель читает по буквам): Gitchell → Gitchul, Funston → Funstun, H1N1 → «H one N one», Hultin → Hoolteen,
Brevig → Breevig, Mohandas Gandhi → Mohundas Gahndee, Munch → Moonk. Heliotrope cyanosis, Alfonso, Samoa модель читает верно сама.
Длинные реплики разбиты по предложениям (до 180 знаков), пауза 0,3 с.

## Whisper (`qa_whisper.tsv`)
53 из 55 ≥ 0.9.
Переозвучены (3 дубля, взят лучший): L20 «war bonds» звучало как «war bombs»; L24c (FLU) терялось первое слово «Onions».
Оставшиеся расхождения — цифры вместо слов (L11b) и «harbour» → «harbor» (L26).

## Новое холодное открытие (сценарий 042f9fd)
Переозвучены C01: NARRATOR George, exaggeration 0.55 (живее и напряжённее), 2–3 дубля, выбран лучший по whisper (см. qa_whisper.tsv). Прежние версии заменены.
