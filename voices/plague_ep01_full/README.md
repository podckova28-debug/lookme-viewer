# The ENTIRE History of the Plague — ep01, полная озвучка

72 реплики, 9,4 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — Chatterbox (MIT) + Kokoro bm_george (Apache-2.0), exaggeration 0.45, cfg 0.5.
PLAGUE — Chatterbox + Kokoro bm_lewis −2 полутона (`voices/refs/role_plague_m_lewis.wav`), exaggeration 0.6, cfg 0.4.
Длинные реплики разбиты по предложениям (до 180 знаков) и склеены с паузой 0,3 с.

## Проверка whisper (`qa_whisper.tsv`)
faster-whisper small, en. Пять реплик переозвучены (3 дубля, взят лучший):
- L06b «I travel light» (было «by travel light»);
- L08b «Rattus» (было «ratas»);
- L24 «1347» (было «3047»; для синтеза год написан словами);
- L36 «quaranta giorni» (для синтеза написано «kwaranta jornee»);
- L50 «Yersin / Yersinia pestis» (для синтеза «Yersan»; whisper слышит «Alexandra», на слух французское «Alexandre»).

Остальные расхождения — только цифры вместо слов (L12b, L17, L19, L36P, L43, L44, L53, L57)
и «Simond» → «Simon» (L52, произношение верное, d немая).
