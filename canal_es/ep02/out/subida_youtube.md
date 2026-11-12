# Эпизод 2 · всё для загрузки на YouTube

Видео: `ep02_final.mp4` (1080p, 9:08). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
¿Qué pasaría si pudieras ver el futuro 5 segundos antes que todos?
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
¿Qué pasaría si pudieras ver 5 segundos del futuro?
```

vidIQ: основное 84 балла, запасное 80, «…ver el futuro… solo 5 segundos?» 81. Основное начинается с точного запроса «qué pasaría si pudieras ver el futuro» (≈4,8 тыс. поисков в месяц), а у «5 segundos del futuro» поиска почти нет.

## 2. Обложки (1280×720, JPEG < 2 МБ)

| Файл | Надпись | Что на картинке |
|---|---|---|
| `miniatura_A.jpg` — **основная** | LO VI ANTES | Герой с хитрой улыбкой, впереди его светящийся «призрак из будущего» и кольцо отсчёта 5 |
| `miniatura_B.jpg` | PEPE VA A HABLAR | Пепе крупно с хитрым прищуром, за ним его призрак уже открыл клюв, герой в шоке |
| `miniatura_C.jpg` | ¿CÓMO LO SUPO? | Вышибалы: герой уклоняется, перед каждым мячом летит его призрак |
| `miniatura_D.jpg` — запас | ¡SÍ! ¿A QUÉ? | Рената ещё молчит, её призрак уже спросил, герой ответил слишком рано |
| `miniatura_E.jpg` — запас | PEPE VA A HABLAR | Пепе во весь рост на лавочке, над ним говорящий призрак |

YouTube Studio → «Проверить и сравнить»: загрузить **A, B и C**. YouTube сам выберет лучшую по времени просмотра (обычно за 1–2 недели).
Арт без текста — в `miniaturas_arte/`, надпись перекладывается через `../../marca/miniatura.py`.

## 3. Описание

```
¿Qué pasaría si pudieras ver el futuro, cinco segundos antes que todos? Una historia animada sobre lo que ganarías y lo que perderías. Al final, la ciencia real detrás de la idea.

0:00 Inicio
1:36 Quemados
3:35 Todo dos veces
6:01 La pregunta
7:20 Pepe
7:49 ¿Algo de esto es real?

Animación original.

#quepasariasi #animacion
```

Когда эпизод 1 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si pudieras detener el tiempo? → <ссылка>`.

## 4. Теги (352 из 500 символов)

```
qué pasaría si pudieras ver el futuro, y si pudieras ver el futuro, que pasaria si pudieras ver el futuro, ver el futuro, 5 segundos del futuro, qué pasaría si, que pasaria si, y si pudieras, historias animadas, historia animada, animación en español, qué harías si, superpoderes, ponle que, pepe la paloma, alerta sísmica, el cerebro predice el futuro
```

## 5. Настройки при загрузке

| Поле | Значение |
|---|---|
| Плейлист | Episodios |
| Аудитория | Нет, это видео не для детей |
| Изменённый или синтетический контент | Нет (мультфильм, не реалистичное видео) |
| Категория | Фильмы и анимация |
| Язык видео и названия | Испанский (Латинская Америка) |
| Автоматические главы | Выключить: главы уже есть в описании |
| Комментарии | Включены, сортировка «Популярные» |
| Публикация | По расписанию, 19:00 UTC (13:00 Мехико, 20:00 Мадрид) |

## 6. Субтитры

`subtitulos_es.srt` → Studio → Субтитры → Испанский → «Загрузить файл» → «С отметками времени».

## 7. Конечная заставка (с 9:03 до 9:08, 5 секунд)

На тёмной заставке в центре уже есть «Ponle que… / Próximo episodio / Suscríbete»; края свободны.

- **Слева:** «Видео» → эпизод 1 (пока его нет — «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на 9:03: раньше элементы закроют последнюю фразу про Пепе.

## 8. Подсказка

Одна, в 8:45 (история и наука закончились, начинается финал): видео → эпизод 1, текст подсказки:

```
Episodio 1: detener el tiempo
```

В начале ролика подсказки не ставь: они уводят зрителя раньше времени.

## 9. Закреплённый комментарий

Опубликуй от имени канала сразу после выхода и закрепи:

```
¿Qué dijo Pepe? 🐦 Escribe tu teoría: las mejores salen en el próximo episodio.
Y tú, ¿qué harías con cinco segundos de futuro?
```

## 10. Шортсы

Порядок публикации: первый — в день выхода эпизода, через 3–4 часа после него, дальше по одному в день около 15:00 UTC.
У каждого в «Связанное видео» поставь этот эпизод: из шортса появится ссылка на полную серию.

| # | Файл | Название (оно же описание) |
|---|---|---|
| 1 | `short1_taza.mp4` | `Ves el futuro… y atrapas la taza ☕ #shorts #quepasariasi` |
| 2 | `short2_quemados.mp4` | `¿Y si vieras cada balón antes de que lo lancen? #shorts #quepasariasi` |
| 3 | `short6_pepe.mp4` | `En 5 segundos, Pepe va a hablar 🐦 #shorts #quepasariasi` |
| 4 | `short5_pregunta.mp4` | `Ya sabes lo que te va a preguntar #shorts #quepasariasi` |
| 5 | `short3_cumple.mp4` | `Tu fiesta sorpresa… cinco segundos antes 🎉 #shorts #quepasariasi` |
| 6 | `short4_pizza.mp4` | `Respondes antes de que te pregunten 🍕 #shorts #quepasariasi` |
| 7 | `short7_ciencia.mp4` | `3 cosas reales sobre ver el futuro 🧠 #shorts #ciencia` |

## 11. Переводы названия и описания (по желанию)

Studio → Языки → Добавить язык. Зрители с английским и португальским интерфейсом увидят название на своём языке; само видео остаётся испанским.

**English**

```
What if you could see the future 5 seconds before everyone else?
```
```
What if you could see the future, five seconds before everyone else? An animated story about what you'd win and what you'd lose. At the end, the real science behind the idea.

0:00 Intro
1:36 Dodgeball
3:35 Everything twice
6:01 The question
7:20 Pepe
7:49 Is any of this real?

Original animation.

#whatif #animation
```

**Português**

```
E se você pudesse ver o futuro 5 segundos antes de todo mundo?
```
```
E se você pudesse ver o futuro, cinco segundos antes de todo mundo? Uma história animada sobre o que você ganharia e o que perderia. No final, a ciência real por trás da ideia.

0:00 Início
1:36 Queimada
3:35 Tudo duas vezes
6:01 A pergunta
7:20 Pepe
7:49 Algo disso é real?

Animação original.

#esevoce #animacao
```

---
Длительность 9:08 · голос: vo_final2
