# Озвучка эпизода 03 (животные и Pepe)

Тот же набор, что в `../../ep01/vo_v3/` и `../../ep02/vo/`: Chatterbox Multilingual LatAm (MIT), опорные голоса из Kokoro-82M (Apache-2.0). OmniVoice и голоса реальных людей не используются. В каждом файле есть неслышимый водяной знак Perth (встроен в Chatterbox).

147 файлов. WAV mono 24 кГц, тишина по краям обрезана, один файл на id; хоровые реплики по три дубля (`_1`, `_2`, `_3`).
Список реплик: `lines.txt` (id|роль|текст). Скрипт: `es_ep03.py`, загрузчик `cbload.py`. temperature 0.7.

Опорные голоса людей лежат в `../../ep01/vo_v3/refs/`, новые голоса этого эпизода — в `refs/`. Голоса животных сделаны так: Kokoro читает испанскую фразу, затем высота сдвигается на указанное число полутонов.

| Роль | Опорный голос | exaggeration / cfg |
|---|---|---|
| narrador | kokoro_em_alex | 0.45 / 0.4; тёплые s13_01–03, s15_01–03: 0.35; s16_*: 0.6; s15_09: 0.3 / 0.3; s08_04: 0.3 / 0.25 |
| valeria (Renata) | kokoro_af_heart | 0.55 / 0.4; s14_06–07: 0.4 |
| mama | kokoro_ef_dora | 0.4 / 0.4 |
| tu | role_tu | 0.35 / 0.4 |
| nacho | role_nacho | 0.7 / 0.4 |
| profe | role_profe | 0.3 / 0.3 |
| croqueta (кошка) | role_croqueta: Kokoro am_onyx −2 | 0.3 / 0.25 |
| perro1 | role_perro1: am_fenrir +2 | 0.9 / 0.5 |
| perro2 | role_perro2: af_bella +1 | 0.9 / 0.5 |
| хор perros | es_am_michael, kokoro_am_adam, es_af_sarah | 0.8 / 0.4 |
| firulais | role_firulais: am_eric −1 | 0.6 / 0.35 |
| bigotes (Señor Bigotes) | role_bigotes: am_liam +1 | 0.7 / 0.5 |
| canela | role_canela: af_jessica +2 | 0.85 / 0.5 |
| хор palomas | role_paloma1: bf_isabella −1.5; role_paloma2: af_kore −1.5; role_paloma3: bf_emma −2 | 0.6 / 0.4; s08_07: 0.3 |
| mosquito | role_mosquito: bm_fable +1.5 | 0.3 / 0.25 |
| pepe (попугай) | role_pepe: bm_lewis −2 | 0.35 / 0.3 |

## Проверка whisper (`qa_whisper.tsv`)

faster-whisper small, язык es, 16 кГц; совпадение = доля совпавших слов без ударений и пунктуации.

Первый прогон нашёл 15 настоящих ошибок: s00_03 («Pilota»), s03_05, s03_06, s04_04 («elijo»), s04_05, s05_06 («Cactero»), s05_09 («perviendo»), s06_02 («fisos»), s08_07_3 («PP»), s10_07 («Navidad»), s10_08, s12_03 («de nata»), s14_01 («Brenata»), s14_04 («¿La picaron?»), s15_07. Для каждой сделано 4 новых дубля, оставлен лучший по whisper. 13 из 15 теперь распознаются верно.

Ещё не исправлены (идёт третья попытка с другой расстановкой пауз):
- s04_05 «Miras a Croqueta.» — whisper: «Mire esa croqueta»;
- s15_07 «¿…Qué?» — whisper: «Ok».

Итог: 124 из 147 файлов ≥ 0.9. Остальные просмотрены по тексту распознавания:
- числа whisper пишет цифрами: s00_01, s06_04, s06_07, s06_08, s07_05, s14_09, s16_02, s16_07, s16_08;
- «rizos» распознан как «risos» (z/s в латиноамериканском произношении одинаковы): s00_04_1–3, s06_02 («Psst» → «esté»);
- слияние на стыке слов: s08_03 «despacio» → «de espacio», s10_04_1 и s10_06_1 «anda ahí» → «andai», s11_06 «Dijo Renata» → «Dijorenata», s12_02 «te ve» → «TV»;
- s04_04: whisper потерял первое «¿Qué?», остальное верно;
- короткие возгласы: s10_05 «¡No sé!» (whisper: «Nose»), s15_12 «Ruu».
