# «You're a Pirate in 1718. This Is Your Life.» — озвучка H1

8 частей, 113 фраз, 7 мин 56 с. Файлы `pirate_p0…p7_H1_48k.mp3`: 48 кГц моно, mp3 192k, громкость −16 LUFS (loudnorm, один проход; по факту около −16,9).
Голос H1: Chatterbox (MIT), опорный голос Kokoro am_michael (Apache-2.0); exaggeration 0.5, cfg 0.5, temperature 0.7; паузы между фразами 0,45 с. OmniVoice не используется.

В тексте для синтеза заменено: Thames → «Tems», Woodes Rogers → «Woods Rogers», Nassau → «Nassaw». Остальное как в сценарии.

## Whisper (`qa_whisper.tsv`, по фразам)
faster-whisper small, en. 99 из 113 фраз ≥ 0.9.
Одна настоящая ошибка: p7 «Would you sign?» звучало как «sigh» — переозвучено (3 дубля, все верные).
Проверены: Carolinas, quartermaster, Bartholomew Roberts, buccaneer, pieces of eight, marooned, weevils, careened,
Gardiners Island (whisper: Gardner's), Nassau, Woodes Rogers, Calico Jack Rackham, Anne Bonny, Mary Read, Thames — всё верно.
Остальные расхождения: годы и числа whisper пишет цифрами (1718, 1699, 600 pieces of 8), «Eye patches» → «eyepatches»,
«An eye, one hundred» → «and I-100» (омофон).
