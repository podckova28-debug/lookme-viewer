# Озвучка эпизода 01, версия 3: лицензии и пробы рассказчика

## Модели

| Что | Модель | Версия | Лицензия | Источник |
|---|---|---|---|---|
| Синтез и клонирование | Chatterbox Multilingual, файнтюн для латиноамериканского испанского (es-419 / es-MX) | `t3_es_mx_latam.safetensors` (шаг 138 500), декодер `s3gen_v3`, токенизатор `grapheme_mtl_merged_expanded_v1.json` | MIT | huggingface.co/ResembleAI/Chatterbox-Multilingual-es-mx-latam |
| Энкодер голоса и встроенный голос | Chatterbox base: `ve.pt`, `conds.pt` | ResembleAI/chatterbox, main | MIT | huggingface.co/ResembleAI/chatterbox |
| Код | chatterbox-tts из GitHub, main | 0.1.7 + V3 | MIT | github.com/resemble-ai/chatterbox |
| Опорные голоса для клонирования | Kokoro-82M, голоса em_alex, em_santa, am_michael | 0.9.4 | Apache-2.0 | huggingface.co/hexgrad/Kokoro-82M |

OmniVoice (CC-BY-NC) и его выходы, включая прежние якоря `vo_trial/anchor_*`, в этой версии не используются. Голоса реальных людей не используются.

Каждый файл Chatterbox содержит неслышимый водяной знак Perth, это встроенная функция модели.

## Опорные голоса (`refs/`)

Сгенерированы Kokoro-82M из фразы «Todo empieza un martes. Suena la alarma, tomas el desayuno y sales a la calle, y nada parece raro, nada.» (для am_michael английский вариант). В испанской фразе нет «c» перед e/i и нет «z», поэтому кастильское [θ] в опорный тембр попасть не может.

## Пробы рассказчика (`trial_narrador/`)

Реплики s00_01–s00_03 (exaggeration 0.45) и s16_16–s16_17 (exaggeration 0.35, теплее), cfg_weight 0.4, temperature 0.7. Файл `*_ALL.wav` склеивает пять реплик с паузой 0,45 с.

| Кандидат | Опорный голос | Медиана F0 | Диапазон F0 (p10–p90) | Whisper (es) |
|---|---|---|---|---|
| A_builtin | встроенный голос Chatterbox (`conds.pt`) | 146 Гц | 93–214 Гц | все 5 реплик дословно |
| B_alex | Kokoro em_alex | 131 Гц | 107–171 Гц | все 5 реплик дословно |
| C_santa | Kokoro em_santa | 124 Гц | 83–158 Гц | все 5 реплик дословно |
| D_michael | Kokoro am_michael (английский тембр) | 125 Гц | 101–163 Гц | все 5 реплик дословно |
