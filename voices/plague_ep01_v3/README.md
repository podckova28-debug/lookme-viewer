# Чума ep01 v3 — 12 новых реплик (S01–S04, SP1, J01, B01, T01, T02, A01–A03)

Голоса и настройки как во всей серии (`plague_full.py`): NARRATOR — George (bm_george), exaggeration 0.45, cfg 0.5, temperature 0.7;
PLAGUE — Lewis −2 полутона (`role_plague_m_lewis`), exaggeration 0.6, cfg 0.4. Куски ≤180 символов, между ними 0,3 с. WAV 24 кГц моно.
Текст для синтеза: bubo → «byooboh», buboes → «byoobohz», Siena → «Seeyenna», Kitasato Shibasaburō → «Keetahsahtoh Sheebahsahbooroh»,
Yersin → «Yersan», 1959 → «nineteen fifty-nine». По 3 дубля (seed 0–2), выбран лучший; все дубли с whisper — в `qa_all_takes.tsv`.

Выбрано: S01 s0, S02 s0, S03 s0, S04 s0, SP1 s0, J01 s1, B01 s1 (whisper: «Siena»), T01 s0 (whisper: «Kitasato Shibasaburo»), T02 s0, A01 s1, A02 s1, A03 s0.
Whisper ≥ 0.91 у всех; ниже 1.00 только из-за цифр (200, 12 million, 1959), «bubo/buboes» (whisper не знает слова) и «Yersin» → «Yesan».
