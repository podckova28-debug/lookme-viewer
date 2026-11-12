"""Writes out/subida_youtube.md: everything needed to publish episode 2 (title, thumbnails, description with
chapters from timing.json, tags, upload settings, end screen, card, pinned comment, Shorts, translations).
Notes for the person uploading are in Russian; everything to paste into YouTube is Spanish/English/Portuguese in code blocks."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH_SHORT = [('s00', 'Inicio'), ('s05', 'Quemados'), ('s10', 'Todo dos veces'), ('s14', 'La pregunta'), ('s16', 'Pepe'), ('s17', '¿Algo de esto es real?')]
CH_EN = ['Intro', 'Dodgeball', 'Everything twice', 'The question', 'Pepe', 'Is any of this real?']
CH_PT = ['Início', 'Queimada', 'Tudo duas vezes', 'A pergunta', 'Pepe', 'Algo disso é real?']
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
starts = [T['scenes'][s]['start'] for s, _ in CH_SHORT]
chap = '\n'.join(f"{mmss(a)} {n}" for a, (_, n) in zip(starts, CH_SHORT))
chap_en = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_EN))
chap_pt = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_PT))
total = T['total']; end_card = total - 5          # the dark «Ponle que… / Próximo episodio / Suscríbete» card fills the last ~5.5 s
card_at = T['scenes']['s18']['start']              # after the story and the science, when the outro asks the viewer

TITLE = '¿Qué pasaría si pudieras ver el futuro 5 segundos antes que todos?'
TITLE_B = '¿Qué pasaría si pudieras ver 5 segundos del futuro?'
TAGS = ('qué pasaría si pudieras ver el futuro, y si pudieras ver el futuro, que pasaria si pudieras ver el futuro, '
        'ver el futuro, 5 segundos del futuro, qué pasaría si, que pasaria si, y si pudieras, historias animadas, '
        'historia animada, animación en español, qué harías si, superpoderes, ponle que, pepe la paloma, '
        'alerta sísmica, el cerebro predice el futuro')
assert len(TITLE) <= 100 and len(TAGS) <= 500, (len(TITLE), len(TAGS))

DESC = f"""¿Qué pasaría si pudieras ver el futuro, cinco segundos antes que todos? Una historia animada sobre lo que ganarías y lo que perderías. Al final, la ciencia real detrás de la idea.

{chap}

Animación original.

#quepasariasi #animacion"""

SHORTS = [
    ('short1_taza.mp4', 'Ves el futuro… y atrapas la taza ☕ #shorts #quepasariasi'),
    ('short2_quemados.mp4', '¿Y si vieras cada balón antes de que lo lancen? #shorts #quepasariasi'),
    ('short3_cumple.mp4', 'Tu fiesta sorpresa… cinco segundos antes 🎉 #shorts #quepasariasi'),
    ('short4_pizza.mp4', 'Respondes antes de que te pregunten 🍕 #shorts #quepasariasi'),
    ('short5_pregunta.mp4', 'Ya sabes lo que te va a preguntar #shorts #quepasariasi'),
    ('short6_pepe.mp4', 'En 5 segundos, Pepe va a hablar 🐦 #shorts #quepasariasi'),
    ('short7_ciencia.mp4', '3 cosas reales sobre ver el futuro 🧠 #shorts #ciencia'),
]
# publishing order: the strongest hooks first; the science short last (it works on its own)
ORDER = [0, 1, 5, 4, 2, 3, 6]
shorts_rows = '\n'.join(f"| {i + 1} | `{SHORTS[k][0]}` | `{SHORTS[k][1]}` |" for i, k in enumerate(ORDER))

md = f"""# Эпизод 2 · всё для загрузки на YouTube

Видео: `ep02_final.mp4` (1080p, {mmss(total)}). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
{TITLE}
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
{TITLE_B}
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
{DESC}
```

Когда эпизод 1 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si pudieras detener el tiempo? → <ссылка>`.

## 4. Теги ({len(TAGS)} из 500 символов)

```
{TAGS}
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

## 7. Конечная заставка (с {mmss(end_card)} до {mmss(total)}, 5 секунд)

На тёмной заставке в центре уже есть «Ponle que… / Próximo episodio / Suscríbete»; края свободны.

- **Слева:** «Видео» → эпизод 1 (пока его нет — «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на {mmss(end_card)}: раньше элементы закроют последнюю фразу про Пепе.

## 8. Подсказка

Одна, в {mmss(card_at)} (история и наука закончились, начинается финал): видео → эпизод 1, текст подсказки:

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
{shorts_rows}

## 11. Переводы названия и описания (по желанию)

Studio → Языки → Добавить язык. Зрители с английским и португальским интерфейсом увидят название на своём языке; само видео остаётся испанским.

**English**

```
What if you could see the future 5 seconds before everyone else?
```
```
What if you could see the future, five seconds before everyone else? An animated story about what you'd win and what you'd lose. At the end, the real science behind the idea.

{chap_en}

Original animation.

#whatif #animation
```

**Português**

```
E se você pudesse ver o futuro 5 segundos antes de todo mundo?
```
```
E se você pudesse ver o futuro, cinco segundos antes de todo mundo? Uma história animada sobre o que você ganharia e o que perderia. No final, a ciência real por trás da ideia.

{chap_pt}

Animação original.

#esevoce #animacao
```

---
Длительность {mmss(total)} · голос: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
