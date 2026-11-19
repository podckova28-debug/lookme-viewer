# «Why It Sucked to Be the Mona Lisa» — озвучка H1

9 частей (`mona_p0…p8_H1_48k.mp3`), 151 фраза, 8 мин 05 с. 48 кГц моно, mp3 192k, громкость около −16,5 LUFS (двухпроходный loudnorm I=−16, TP −1,5).
Голос H1: Chatterbox (MIT), опорный голос Kokoro am_michael (Apache-2.0); exaggeration 0.4 (deadpan), cfg 0.5, temperature 0.7.
Темп 1.0 (без atempo), паузы между фразами 0,35 с. OmniVoice не используется.

В тексте для синтеза заменено: Giocondo → «Jokondo», sfumato → «sfoomahto», Fontainebleau → «Fontenbloh», Louvre → «Loovruh»,
Vincenzo Peruggia → «Vinchenzo Peroojah», Guillaume Apollinaire → «Geeyohm Apolleenair»; годы с дефисом («fifteen-oh-three») — без дефиса.

## Whisper (`qa_whisper.tsv`, по фразам: часть_строка|сек|совпадение|распознано)
faster-whisper small, en. 135 из 151 ≥ 0.9.
Переозвучено (3 дубля, выбран верный): p5 «You were famous now» (было «You are famous now»).
Проверены и распознаны верно: Mona Lisa, Leonardo da Vinci, sfumato, poplar, Fontainebleau, Louvre, Versailles, Corsica, Napoleon,
Francis the First, Louis the Fourteenth (римскими цифрами), Vincenzo Peruggia (whisper: Perugia), Guillaume Apollinaire, Pablo Picasso, Florence, Rome, Milan.
Близко по звучанию: Giocondo → «del Yocondo».
Остальные фразы ниже 0.9 — годы и числа цифрами (77 centimeters, 1503, 1516, 1911, 1913, 1956, 1974, 2009, 2024, 20,000), омофон «queued» → «cued»,
«asked» → «asks» (p2), «teacup» раздельно.
