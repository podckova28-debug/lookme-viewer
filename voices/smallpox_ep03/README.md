# The ENTIRE History of Smallpox — ep03, полная озвучка

62 реплики, 9,3 мин чистой речи. WAV 24 кГц моно, тишина обрезана, `{id}.wav`.
NARRATOR — George (Chatterbox MIT + опорный голос Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5, temperature 0.7.
SMALLPOX — `voices/refs/role_smallpox_daniel_low.wav` (Kokoro bm_daniel, сдвиг вниз), exaggeration 0.5, cfg 0.35, temperature 0.7,
без эффектов: холодный спокойный «коллекционер».

Для синтеза годы написаны словами (в т. ч. трёхзначные: 165 → «one hundred and sixty-five»), трудные имена — по транскрипциям:
variola, variolation/variolated, Ramses, Lucius Verus, Tenochtitlan, Cuitlahuac, Huayna Capac, Wortley Montagu, Onesimus,
Phipps, Nelmes, Balmis, Isabel Zendal, Rahima Banu, Ali Maow Maalin, vacca.
Длинные реплики разбиты по предложениям (до 180 знаков), пауза 0,3 с.

## Whisper (`qa_whisper.tsv`)
57 из 62 ≥ 0.9.
Переозвучены (3–9 дублей, взят лучший):
- C04: «Blossom» звучало как «Brossum».
- L22: «variolation» (транскрипция vair-ee-oh-lat).
- L25, L27b: «variolated» без подсказки, модель сама читает VAIR-ee-oh-lay-ted; whisper во всех дублях слышит одно и то же.
- L26: «variolated» через написание `vairiolated`, «Onesimus» через `Ohnessimus` (oh-NESS-ih-mus). Подсказки с дефисами
  и заглавными (`Oh-NESS-ih-mus`, `vairy-oh-lay-ted`) модель читает по буквам или дробит, их не использовать.
Оставшиеся расхождения — цифры вместо слов (C02, L14, L27), «Ramses» → «Ram sees» (L10, так и задумано),
«favourite» → «favorite» (L15).

## Рубрики «Симптомы» и «Последствия» (дозапись)
S01–S05, A01–A03 (тексты из `tools/plague/ep03_lines.txt` ветки сценариста). Голоса и настройки те же; S05 и A03 — SMALLPOX.
Whisper: все 8 ≥ 0.92 (S03: «pustules» записано как «postules», S01: число цифрами), строки добавлены в конец `qa_whisper.tsv`.
