# Чума ep01 v2 — новые реплики начала (C01, C03, C04, C05)

Голоса и настройки — как во всей серии чумы (`voices/plague_ep01_full`, скрипт `plague_full.py`):
- NARRATOR — George: Chatterbox (MIT) + опорный голос Kokoro bm_george, exaggeration 0.45, cfg 0.5, temperature 0.7.
- PLAGUE — Lewis −2 полутона (`role_plague_m_lewis`), exaggeration 0.6, cfg 0.4, temperature 0.7.
- Длинные реплики режутся на куски ≤180 символов по предложениям, между кусками 0,3 с. WAV 24 кГц моно, тишина обрезана.

Текст для синтеза: годы словами («thirteen forty-seven»), Messina → «Messeena» (muh-SEE-nuh). По 3–4 дубля (seed 0–3), выбран лучший по whisper.

| id | роль | дубль | сек | whisper |
|---|---|---|---|---|
| C01 | NARRATOR | seed 0 | 16.6 | 0.96 — «Messina» распознано верно; расхождение только в цифрах года |
| C03 | NARRATOR | seed 1 | 17.1 | 1.00 — с паузами между предложениями (seed 0 читал слитно) |
| C04 | NARRATOR | seed 0 | 10.1 | 0.86 — всё верно, whisper пишет 5,000 цифрами и «house guest» раздельно |
| C05 | PLAGUE | seed 0 | 0.8 | 1.00 «Miss me?» |
