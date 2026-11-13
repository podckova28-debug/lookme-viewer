# The ENTIRE History of Scurvy — ep05, полная озвучка

59 реплик, 9,2 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
SCURVY — `voices/refs/role_scurvy_santa_low.wav`: Kokoro am_santa (пожилой мужской), фраза
«Ah, there you are, sailor. Long way from home, aren't we?…», скорость 0.82, затем −2 полутона (ffmpeg asetrate 0.89);
exaggeration 0.55, cfg 0.3 (медленнее), temperature 0.7, без эффектов.
Отличается от Lewis (Чума), C4_fable_wet (Холера), daniel_low (Оспа), am_puck (Испанка).

Для синтеза годы и десятилетия написаны словами (1500 → fifteen hundred, 1840s → eighteen forties, 1907 → nineteen oh seven).
Подсказки произношения слитно, без дефисов: Jacques Cartier → Zhahk Kartyay, St. Lawrence → Saint Lawrence, Iroquoian → Irokwoyan,
HMS Salisbury → «H M S Salisbury», Theodor Frølich → Tayodor Frolik, Casimir → Kazimeer, Szent-Györgyi → Sent Jurjee, Szeged → Seged.
Остальные имена (Anson, Cape Horn, Vasco da Gama, Domagaya, Lancaster, Lind, Blane, Limeys, Falcon, Holst, ascorbic) модель читает верно сама.

## Whisper (`qa_whisper.tsv`)
55 из 59 ≥ 0.9, переозвучка не понадобилась.
Расхождения: цифры вместо слов (C01, L22), «treasure ships» слитно (C01), «pair» → «pear» (L20, омофон),
L34 «Szent-Györgyi» whisper пишет как «St. Georgie» — это и есть SENT JUR-jee, «Szeged» → «Seged».

## Новое холодное открытие (сценарий 042f9fd)
Переозвучены C01, C02, C03: NARRATOR George, exaggeration 0.55 (живее и напряжённее), 2–3 дубля, выбран лучший по whisper (см. qa_whisper.tsv). Прежние версии заменены.
