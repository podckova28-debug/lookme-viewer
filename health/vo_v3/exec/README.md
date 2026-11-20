# «Why It Sucked to Be a Medieval Executioner» — озвучка H1

9 частей (`exec_p0…p8_H1_48k.mp3`), 187 фраз, 8 мин 47 с. 48 кГц моно, mp3 192k, громкость около −16,5 LUFS (двухпроходный loudnorm I=−16, TP −1,5).
Голос H1: Chatterbox (MIT), опорный голос Kokoro am_michael (Apache-2.0); exaggeration 0.4 (deadpan), cfg 0.5, temperature 0.7.
Темп 1.0 (без atempo), паузы между фразами 0,35 с. OmniVoice не используется.

В тексте для синтеза заменено: Hof → «Hohf», Margrave Albrecht → «Margrave Ahlbrekht», Heinrich → «Hynrikh» (в p1 строка 1 — «Hine rikh»),
Schmidt → «Shmit», Franz → «Frahnts», résumé → «rezoomay», «fifteen-hundreds» без дефиса.

## Whisper (`qa_whisper.tsv`, по фразам: часть_строка|сек|совпадение|распознано)
faster-whisper small, en. 172 из 187 ≥ 0.9.
Переозвучено (3 дубля, выбран верный): p1 «Your father, Heinrich» (было «Henrik», теперь «Haini Reich»), p1 «Small problem: Hof…» (было «Hope», теперь «Huff» ≈ HOHF),
p1 «Your dad never…» (было «Your dead»), p5 «You were also a doctor» (было «are»), p5 «you spent your whole career» (было «spend»),
p5 «than most real doctors» (было «wheeled»), p7 «You were the exception» (было «are»).
Проверены и распознаны верно: Nuremberg, Bavaria, Margrave Albrecht, Schmidt, Franz Schmidt (whisper: Frantz), Ferdinand the Second, résumé.
Остальные фразы ниже 0.9 — годы и числа цифрами (1500s, 1553, 1573, 361, 345, 15,000, 1617, 1634, 80), омофон patients → «patience».
