# The ENTIRE History of Rabies — ep06, полная озвучка

50 реплик (NARRATOR 39, RABIES 11), 7,6 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
RABIES — `voices/refs/role_rabies_onyx.wav`: Kokoro am_onyx (низкий американский мужской), фраза
«Good evening. Do come closer... I promise I don't bite. Well. Not usually. Not until you've stopped trusting water.», скорость 0.88,
затем −1,5 полутона; exaggeration 0.65, cfg 0.35, temperature 0.75, без эффектов.
Отличается от Lewis (Чума), C4_fable_wet (Холера), daniel_low (Оспа), am_puck (Испанка), santa_low (Цинга).

Для синтеза годы и числа написаны словами. Подсказки произношения слитно, без дефисов:
Joseph Meister → Zhozef Myster, Lyssavirus → Lissavirus, Lyssa → Lissa, Eshnunna → Eshnoona, mina → myna, Celsus → Selsus,
Hubert → Hewbert, Alsace → Alzass, Jean-Baptiste Jupille → Zhahn Bateest Zhoopee, Jura → Zhoora, Smolensk → Smolyensk,
Jeanna Giese → Jeena Geesee. Длинные реплики разбиты по предложениям (до 180 знаков), пауза 0,3 с.

## Whisper (`qa_whisper.tsv`)
faster-whisper small, en, 16 кГц. Первый прогон нашёл 3 настоящие ошибки:
L13 «Saint Hubert» → «St. Helberg» (подсказка Hyoobert), L31 оборванное «hospital», L35 потеряно «I've».
Для каждой сделано 4 новых дубля (для L13 ещё 4 с подсказкой Hewbert), оставлен лучший; теперь все три распознаются верно.

Итог: 47 из 50 ≥ 0.9. Оставшиеся три — только цифры вместо слов (L22, L32) и французское имя Jupille,
которое whisper пишет как «John Bates Jupey» (L24): по звучанию это Жан-Батист Жюпий.

## Новое холодное открытие (сценарий 042f9fd)
Переозвучены C01, C02: NARRATOR George, exaggeration 0.55 (живее и напряжённее), 2–3 дубля, выбран лучший по whisper (см. qa_whisper.tsv). Прежние версии заменены.
