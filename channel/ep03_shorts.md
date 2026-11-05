# Серия 3 · Shorts («What If You Woke Up as THE FLASH?»)

Файлы: `out/shorts_ep03/short_1.mp4` … `short_3.mp4`, 1080×1920, 24 к/с, H.264 + AAC 48 кГц, звук из оригинала (подъём 0,12 с в начале, затухание 0,4 с в конце).

Источник: `out/e3_full_v5.mp4`. Все три Short взяты из отрезка 0:00–1:56.4. Кусок после 1:57 сейчас переснимается, поэтому в Shorts его нет совсем (последний кадр Short 3 стоит до перехода на крышу с «Stage four»).

Оформление то же, что у серии 1: горизонтальный кадр целиком (1080×608) по центру поверх размытой и затемнённой копии, сверху маленькая строка `What If You Woke Up As... · Ep 3` и жёлтый заголовок Bangers, под кадром крупные субтитры рассказчика по словам из faster-whisper. Кадр по бокам не обрезан, потому что в углах оригинала стоят плашки («PAUSE: 3.71 S», «STAGE 1: DENIAL», «HER PAUSE: 4 SECONDS»).

Правки субтитров: звук около 0:48, который whisper слышит как «It's now or never», это не рассказчик, и в субтитрах его нет. Также убран «Slash» перед «Stage two» (это свист перехода), исправлены «questions», «Forty apology letters», «In Portugal. Stage one.». Для «Stage one», «Research», «Bargaining» тайминг подогнан по громкости (whisper сжал эти слова почти до нуля).

Границы проверены по словам whisper, по громкости и по покадровым сеткам. Ни один Short не начинается и не заканчивается посреди слова: готовые файлы ещё раз распознаны whisper, первые и последние слова совпадают с таблицей.

| Short | Источник в `e3_full_v5.mp4` | Длина | Первое слово / последнее слово |
|---|---|---|---|
| 1 | 0:00.00 – 0:38.00 | 38,0 с | «Today, you woke up as the Flash» 0:00 / «never been early.» 0:34.5, дальше занос и дымящийся кроссовок до 0:38, обрез перед переходом к SMS |
| 2 | 0:38.30 – 1:09.00 | 30,7 с | «Your girlfriend texted…» 0:38.7 (SMS уже на экране) / «Nobody can hear you scream.» 1:08.7, обрез перед переходом к «WHAT IF…» |
| 3 | 1:12.95 – 1:56.40 | 43,5 с | «She's leaving you.» 1:13.2 / «Plus one violinist.» 1:55.6, обрез перед переходом на крышу (Stage four) |

Порядок публикации: Short 2 за 1–2 дня до серии (самый сильный крючок, обрывается на «Nobody can hear you scream» и тянет на полную серию), Short 1 в день выхода серии, Short 3 через 1–2 дня после. В каждом Short в поле «Связанное видео» (Related video) выбрать полную серию 3.

Скрипт сборки: `/tmp/claude-0/-home-user-lookme-viewer/15230ea4-cf3a-58b7-8157-8e72db0a2b22/scratchpad/agent_ep03_shorts/build_shorts.py` (рядом `words.json` с таймингами слов; временная папка). Если после пересъёмки 1:58–2:21 тайминги до 1:57 не сдвинутся, Shorts пересобирать не нужно.

---

## Short 1 · «Morning person? No. The Flash.»

Утро: будильник улетает в стену, кровать застелена за мгновение («You made your bed. You have never made your bed.»), зубная щётка превращает лицо в пену, Дэйв на кухне (кружка летит, герой ловит её быстрее, чем Дэйв замечает), «You're also early. You have never been early.», занос на тротуаре и дымящийся кроссовок. Крючок: будильник врезается в стену на первой секунде и «Today, you woke up as the Flash».

Заголовок:
```
He Woke Up as The Flash and Doesn't Know It Yet
```
Описание:
```
You made your bed. You have never made your bed. Your toothbrush is not a morning person.
Full episode: "What If You Woke Up as THE FLASH?" (linked above)

#shorts #theflash #whatifyouwokeupas #animation #superheroparody
```

## Short 2 · «"We need to talk..."»

SMS от Лили «Coffee at 9? We need to talk.», кафе, «She put down the spoon. Lily never puts down the spoon.», вдох («The long kind»), «when the fastest man alive panics, the world stops», плашки «HER PAUSE: 4 SECONDS / FOR YOU: ~3 WEEKS», «Rule one of frozen time. Nobody can hear you scream.» Крючок: экран с SMS и «the four most dangerous words in the English language» с первой секунды.

Заголовок:
```
"We Need to Talk" Lasts 3 Weeks When You're The Flash
```
Описание:
```
Her pause: 4 seconds. For you: about three weeks.
Rule one of frozen time: nobody can hear you scream.
Full episode: "What If You Woke Up as THE FLASH?" (linked above)

#shorts #theflash #weneedtotalk #animatedcomedy #whatifyouwokeupas
```

## Short 3 · «Stages of panic in 4 seconds»

Мозг рисует худшее: она уходит к парню с укулеле, в Португалию. Stage 1: Denial (лупа, её телефон, а там собаки, ещё собаки). Stage 2: Research (Дэйв не помогает, гора книг об отношениях, «They all say it's you»). Stage 3: Bargaining (кольцо, починенное окно, чаевые, сорок писем с извинениями «на всякий случай», плюс один скрипач). Счётчик паузы в углу тает с 3,71 до 1,94 с. Крючок: «She's leaving you. For a guy with a ukulele.» с первой секунды.

Заголовок:
```
She's Leaving You. For a Guy With a Ukulele.
```
Описание:
```
She paused for 4 seconds. You panicked for 3 weeks. Denial, research, bargaining... and one violinist.
Full episode: "What If You Woke Up as THE FLASH?" (linked above)

#shorts #theflash #funnyanimation #relationshiphumor #whatifyouwokeupas
```
