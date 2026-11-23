# «Why It Sucked to Be a Plague Doctor» — озвучка H1

9 частей (`plague_p0…p8_H1_48k.mp3`), 1408 слов. 48 кГц моно, mp3 192k, громкость около −16,5 LUFS (двухпроходный loudnorm I=−16, TP −1,5).
Голос H1: Chatterbox (MIT), опорный голос Kokoro am_michael (Apache-2.0); exaggeration 0.4 (deadpan), cfg 0.5, temperature 0.7.
Темп 1.1 (atempo, высота сохраняется), паузы между фразами 0,25 с (после ускорения).

В тексте для синтеза заменено: Orvieto → «Orvyehto», Matteo Angelo → «Mahteyo Ahnjeloh», Perugia → «Perooja», Charles de Lorme → «Sharl duh Lorm»,
Paulitious → «Pawlishus», Rae → «Ray», Michel de Nostredame → «Meeshel duh Nostruhdahm», Ragusa → «Ragooza» (в p8 строка 8 — «Rahgooza»),
quaranta → «kwarahnta», «fifteen-hundreds» без дефиса.

## Whisper (`qa_whisper.tsv`: часть_строка|сек|совпадение|распознано)
faster-whisper small, en. Переозвучено (по 4 дубля, выбран верный): p0 «Oh, and the famous bird mask?» (было «Oh, in»), p8 «You were underpaid» (было «you are»),
p8 «the city of Ragusa» (было «Urguza», теперь распознаётся «Ragusa»).
Проверены и распознаны верно: Orvieto, Matteo Angelo («Matteu Angelo»), Perugia, miasma, camphor, Edinburgh, George Rae («Ray»), Nostradamus, Dubrovnik, quarantine.
Остальные строки ниже 0.9 — годы и числа цифрами (1348, 1619, 1656, 1645, 1534, 1377, 18/5/12, 300, 400, 30, 40), омофоны «A long cane» → «along Kane», «patients» → «patience»,
«Paulitious» → «Paul Isius», «Michel de Nostredame» → «Michel D. Nostrudam».
