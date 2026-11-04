# Серия 1 · Shorts

Файлы: `out/shorts_ep01/short_1.mp4` … `short_4.mp4`, 1080×1920, 24 к/с, H.264 + AAC 48 кГц, звук рассказчика из оригинала (подъём 0,12 с в начале, затухание 0,4 с в конце).

Как сделаны: горизонтальный кадр целиком (1080×608) по центру, фон из того же кадра, размытый и затемнённый. Сверху маленькая строка `What If You Woke Up As... · Ep 1` и жёлтый заголовок Bangers, под кадром крупные субтитры рассказчика (по словам из faster-whisper, исправлены «Spider-Man», «9:31»). Кадр не обрезан по бокам, потому что в левом верхнем углу оригинала стоят плашки времени («DAY 1 · 7:02 AM», «9:44 AM») и паутина часто летит от края кадра. Субтитры стоят выше нижней зоны, которую перекрывает интерфейс Shorts.

Границы проверены по словам whisper и по громкости: ни один Short не начинается и не заканчивается посреди слова.

| Short | Источник в `e01_full_v3.mp4` | Длина | Первое слово / последнее слово |
|---|---|---|---|
| 1 | 0:00.00 - 0:36.80 | 36,8 с | «Today» 0:00.6 / «throw it.» 0:35.7 |
| 2 | 1:08.70 - 1:40.40 | 31,7 с | «Oh, right» 1:09.1 / «technically.» 1:39.8 (следующее слово «Say» с 1:40.5 не попадает) |
| 3 | 2:06.46 - 2:44.10 | 37,6 с | «Coffee» 2:08.0 / «looked up.» 2:39.0, дальше звук паутины до 2:44 |
| 4 | 3:31.42 - 4:03.60 | 32,2 с | «The bus» 3:31.9 / «still there.» 4:02.4, дальше тишина |

Порядок публикации: Short 1 за 1-2 дня до серии (тизер), Short 4 в день серии, Shorts 2 и 3 в следующие дни. В каждом Short в поле «Связанное видео» (Related video) выбрать полную серию 1: под Short появится ссылка на неё.

Скрипт сборки (для пересборки или следующих серий): `/tmp/claude-0/-home-user-lookme-viewer/15230ea4-cf3a-58b7-8157-8e72db0a2b22/scratchpad/agent_ep01/build_shorts.py` (временная папка; при желании перенести в `tools/`).

---

## Short 1 · «You woke up on the ceiling»

Пробуждение на потолке, телефон прилип к потолку до вечера, паучье чутьё срабатывает на муху, в ванной всё прилипает к рукам. Крючок с первой секунды: перевёрнутое лицо и «Today you woke up as Spider-Man».

Заголовок:
```
You Woke Up as Spider-Man. You're on the Ceiling.
```
Описание:
```
Day one with spider powers. Your phone is on the ceiling. Your spider-sense is warning you about a fly.
Full episode: "What If You Woke Up as SPIDER-MAN for a Day?" (linked above)

#shorts #spiderman #whatifyouwokeupas #animation #superheroparody
```

## Short 2 · «Rule #3: let Dave tie it»

Собеседование в десять, правила дня: никто не должен знать, галстук (прилипает к пальцам), галстук завязывает Дэйв, Дэйв молча даёт самодельную маску, дверная ручка остаётся в руке. Крючок: календарь с обведённой датой и «Oh, right. At ten you have a job interview».

Заголовок:
```
Spider-Man Can't Tie a Tie. Dave Can.
```
Описание:
```
Rule one: nobody can know. Rule two: wear a tie. Rule three: let Dave tie it.
Nothing surprises Dave.

#shorts #spiderman #dave #animatedcomedy #whatifyouwokeupas
```

## Short 3 · «Sorry, ma'am. I'm late.»

Кофейня: ловит паутиной падающие кружки, «запомни этот стакан». На улице пытается помочь старушке и приклеивает её к фонарю, смотрит на часы и уходит «потом вернусь». Финал: не глядя ловит вора с сумкой паутиной на остановке, «и в этот раз кто-то поднял глаза».

Заголовок:
```
He Glued a Grandma to a Lamppost. He's Late.
```
Описание:
```
Good news: nobody in this city looks up from their phone. Remember this lady. You'll see her again.

#shorts #spiderman #funnyanimation #superheroparody #whatifyouwokeupas
```

## Short 4 · «Nobody is driving the bus»

Кульминация: автобус без водителя катится с горы, герой в самодельном костюме едет за ним на «водных лыжах», красный свет, автобус останавливается в паутине, кофе не пролит ни капли, а старушка внизу всё ещё приклеена к фонарю. Крючок: «The bus is rolling down the hill. Nobody is driving it.» с первой секунды.

Заголовок:
```
Nobody Is Driving the Bus. Spider-Man Has a Coffee.
```
Описание:
```
In the movies he swings. You water-ski. And not a single drop.
The lady at the bottom of the hill? You glued her there this morning.

#shorts #spiderman #animation #superhero #whatifyouwokeupas
```
