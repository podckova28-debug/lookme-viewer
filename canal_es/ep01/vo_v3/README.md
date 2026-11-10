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

## Полная озвучка (выбран B_alex)

179 файлов: 175 реплик, из них две хоровые по три дубля (`s10_06b_1/2/3`, `s13_01b_1/2/3`). Всего 7,0 минуты звука.
WAV mono 24 кГц, тишина обрезана (порог 0,008, 30 мс до и 50 мс после), один файл на id.
Список реплик: `lines.txt`. Скрипт: `full_v3.py` (загрузчик `cbload.py`), cfg_weight 0.4, temperature 0.7.

| Роль | Опорный голос (`refs/`) | Обработка опорного | Медиана F0 | exaggeration |
|---|---|---|---|---|
| narrador | kokoro_em_alex | нет | ~131 Гц | 0.45; тёплые s11_05b, s11b_06, s11b_07, s13_13b, s16_16, s16_17: 0.35; s18_*: 0.6 |
| valeria (Renata) | kokoro_af_heart (испанский текст) | нет | ~195 Гц | 0.55; s16_14–s16_15: 0.35 |
| mama | kokoro_ef_dora | нет | ~158 Гц | 0.4 |
| tu | role_tu ← kokoro_am_puck | +2 полутона (asetrate 1.12) | ~130 Гц | 0.35 |
| nacho | role_nacho ← kokoro_am_echo | +4 полутона (asetrate 1.26) | 115–156 Гц | 0.7 |
| profe | role_profe ← kokoro_em_santa | −3 полутона (asetrate 0.84) | ~109 Гц | 0.3, cfg_weight 0.3 |
| хор _1, _2 (мальчики) | role_chico1 ← am_adam, role_chico2 ← am_liam | +2,5 и +3 полутона | | 0.8 |
| хор _3 (девочка) | kokoro_af_sky | нет | | 0.8 |

Все опорные голоса синтезированы Kokoro-82M (Apache-2.0) из той же фразы без «c/z». Сдвиг высоты: ffmpeg `asetrate,aresample,atempo`.
Многоточие в начале s17_07 («…y una paloma») убрано из текста для синтеза: паузу ставить при сборке.

## Проверка whisper (`qa_whisper.tsv`)

faster-whisper small, язык es, звук пересэмплирован ffmpeg в 16 кГц. Совпадение: доля совпавших слов после снятия ударений и пунктуации.
Первый прогон: 20 реплик с настоящими ошибками («una cama» вместо «una cana», «Ya veo» → «en el país», «podría escopiar»). Для каждой сделано 4 новых дубля, оставлен лучший по whisper.

После исправлений 159 из 179 файлов ≥ 0.9. Остальные 20 проверены вручную по тексту распознавания, ошибок произношения нет:
- числа whisper пишет цифрами: s01_05, s05_03, s11_04, s11_08, s13_13, s13_13b, s16_06, s16_18, s18_06, s18_07;
- хор «¡Gooool!» (s10_06b_1/2/3) распознаётся как «GOOOL», «Go»;
- s12_04b «Ay, no…» звучит как «I know»: это та же фонетика;
- слияние слов на стыке: s09_02 «esa Renata» → «es Arenata», s14_05 «la cana» → «Lacana», s10_01 «toca patear» → «toca apatear», s11_06 «la ves» → «la vez»;
- s04_08b, s06_06b, s15_09: потеряны только междометия и пунктуация («¿Eh?», «Eh…»).

На слух стоит проверить: акцент Renata (af_heart с испанским текстом) и s09_02.
