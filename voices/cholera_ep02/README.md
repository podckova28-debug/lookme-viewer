# The ENTIRE History of Cholera — ep02, полная озвучка

64 реплики, 9,2 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + Kokoro bm_george), exaggeration 0.45, cfg 0.5, temperature 0.7.
CHOLERA — C4_fable_wet: `voices/refs/role_cholera_fable.wav` (bm_fable +1,5 полутона), exaggeration 0.85, cfg 0.4, temperature 0.75,
затем эффект «влажности» (ffmpeg chorus + aphaser + lowpass 7,5 кГц, команда в `voices/cholera_trial/README.md`).
Сухие версии реплик CHOLERA без эффекта: `_dry/{id}.wav`.

Для синтеза годы и десятилетия написаны словами, трудные имена — по транскрипциям сценариста
(Vibrio cholerae, Jessore, Bazalgette, Pacini, Pettenkofer, Mahalanabis, Altona, Sulawesi, Tchaikovsky, copepods).
Длинные реплики разбиты по предложениям (до 180 знаков), пауза 0,3 с.

## Whisper (`qa_whisper.tsv`)
Переозвучены (3 дубля, взят лучший): L02 «Streamlined», L10 «killer kind / slipped», L15 «for decent transport»,
L20c «Presidents. Composers.», L23 «I am offended».
Оставшиеся расхождения — цифры вместо слов (C02, L05, L43, L51) и L02: whisper не слышит «-d» в первом «Streamlined»
(влажный эффект + британское произношение), второе слово распознано верно.
