# «Why It Sucked to Be a Pirate» — озвучка H1

9 частей (`suck_p0…p8_H1_48k.mp3`), 184 фразы, 8 мин 54 с. 48 кГц моно, mp3 192k, громкость −16,5 LUFS (двухпроходный loudnorm I=−16, TP −1,5).
Голос H1: Chatterbox (MIT), опорный голос Kokoro am_michael (Apache-2.0); exaggeration 0.4 (deadpan, на 0.1 ниже обычного H1), cfg 0.5, temperature 0.7.
Темп 1.05 — ffmpeg atempo при сборке (высота голоса не меняется); паузы между фразами 0,35 с (после ускорения). OmniVoice не используется.

В тексте для синтеза заменено: Thames → «Tems», Woodes Rogers → «Woods Rogers», Nassau → «Nassaw», «You made an X.» → «ex»,
«Mary Read» → «Mary Reed» (только p7, фраза 12: модель читала «Red»).

## Whisper (`qa_whisper.tsv`, по фразам: часть_строка|сек|совпадение|распознано)
faster-whisper small, en. 168 из 184 ≥ 0.9.
Переозвучено (3 дубля, выбран верный по whisper): p0 «Well.» (было «will»), p0 «This is why it sucked to be a pirate» (было «it's sucked»),
p1 «Pirates didn't want a fight» (было «to fight»), p4 «Because he has the saw» (было «song»), p7 «pirate careers» (было «pyroquias»),
p7 «Mary Read» (было «Red»).
Проверены и распознаны верно: quartermaster, Bartholomew Roberts, buccaneer, pieces of eight, weevils, Sabbath, Gardiners Island (whisper: Gardner's),
Nassau, Woodes Rogers, Calico Jack Rackham, Anne Bonny, Mary Read, Thames, Carolinas, Charleston, Treasure Island; годы 1718, 1699, 1883, 1720, 1722, 1726.
Остальные 16 фраз ниже 0.9 — только числа цифрами и омофоны: «No prey» → «pray», «An eye» → «and I», «Dinner time» → «dinnertime», «eye patches» → «eyepatches».
