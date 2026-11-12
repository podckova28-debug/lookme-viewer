"""Writes out/subida_youtube.md: everything needed to publish episode 3 (title, thumbnails, description with
chapters from timing.json, tags, upload settings, end screen, card, pinned comment, Shorts, translations).
Notes for the person uploading are in Russian; everything to paste into YouTube is Spanish/English/Portuguese in code blocks."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH_SHORT = [('s00', 'Inicio'), ('s03', 'Croqueta'), ('s05', 'Todos los perros'), ('s09', 'Los problemas'), ('s12', 'Canela'), ('s15', 'Pepe'), ('s16', '¿Algo de esto es real?')]
CH_EN = ['Intro', 'Croqueta', 'Every dog', 'The problems', 'Canela', 'Pepe', 'Is any of this real?']
CH_PT = ['Início', 'Croqueta', 'Todos os cachorros', 'Os problemas', 'Canela', 'Pepe', 'Algo disso é real?']
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
starts = [T['scenes'][s]['start'] for s, _ in CH_SHORT]
chap = '\n'.join(f"{mmss(a)} {n}" for a, (_, n) in zip(starts, CH_SHORT))
chap_en = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_EN))
chap_pt = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_PT))
total = T['total']; end_card = total - 5          # the dark «Ponle que… / Próximo episodio / Suscríbete» card fills the last ~5.5 s
card_at = T['scenes']['s17']['start']              # after the story and the science, when the outro asks the viewer

TITLE = '¿Qué pasaría si pudieras hablar con los animales?'
TITLE_B = '¿Qué pasaría si tu gato pudiera hablar?'
TAGS = ('qué pasaría si pudieras hablar con los animales, que pasaria si pudieras hablar con los animales, hablar con los animales, '
        'y si los animales hablaran, si los animales pudieran hablar, qué pasaría si, que pasaria si, y si pudieras, historias animadas, '
        'historia animada, animación en español, qué harías si, ponle que, pepe la paloma, perritos de la pradera, gatos, perros')
assert len(TITLE) <= 100 and len(TAGS) <= 500, (len(TITLE), len(TAGS))

DESC = f"""¿Qué pasaría si pudieras hablar con los animales, y ellos contigo? Una historia animada sobre lo que te contarían y lo que preferirías no saber. Al final, la ciencia real detrás de la idea.

{chap}

Animación original.

#quepasariasi #animacion"""

SHORTS = [
    ('short1_croqueta.mp4', '¿Y si tu gato pudiera hablar? 🐱 #shorts #quepasariasi'),
    ('short2_perros.mp4', 'Lo que dicen TODOS los perros 🐶 #shorts #quepasariasi'),
    ('short3_hamster.mp4', 'El hámster de la clase lo sabe todo 🐹 #shorts #quepasariasi'),
    ('short4_palomas.mp4', 'Cuando entiendes a las palomas 🐦 #shorts #quepasariasi'),
    ('short5_noche.mp4', '¿Por qué ladran los perros a las 3 a. m.? #shorts #quepasariasi'),
    ('short6_pepe.mp4', 'La paloma que nunca habla… habló 🐦 #shorts #quepasariasi'),
    ('short7_ciencia.mp4', '3 cosas reales sobre hablar con animales 🧠 #shorts #ciencia'),
]
# publishing order: the strongest hooks first; the science short last (it works on its own)
ORDER = [0, 1, 4, 3, 2, 5, 6]
shorts_rows = '\n'.join(f"| {i + 1} | `{SHORTS[k][0]}` | `{SHORTS[k][1]}` |" for i, k in enumerate(ORDER))

md = f"""# Эпизод 3 · всё для загрузки на YouTube

Видео: `ep03_final.mp4` (1080p, {mmss(total)}). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
{TITLE}
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
{TITLE_B}
```

Тема обещана в конце эпизода 2. Точного запроса почти не ищут (<750 в месяц): эту серию будут смотреть из рекомендаций, а не из поиска, поэтому название держит формат канала. Запасное конкретнее и короче. Проверить их в vidIQ не удалось: кредиты кончились (обновятся 21 ноября).

## 2. Обложки (1280×720, JPEG < 2 МБ)

| Файл | Надпись | Что на картинке |
|---|---|---|
| `miniatura_A.jpg` — **основная** | MI GATO HABLA | Croqueta крупно, смотрит в камеру с осуждающим прищуром и говорит; герой за ним в шоке |
| `miniatura_B.jpg` | PEPE HABLÓ | Пепе крупно открыл клюв, впервые за три серии; герой на лавочке застыл |
| `miniatura_C.jpg` | ¡TODOS ME HABLAN! | Герой зажал уши, вокруг собаки, кот, голуби и комар говорят одновременно |

YouTube Studio → «Проверить и сравнить»: загрузить **A, B и C**. YouTube сам выберет лучшую по времени просмотра (обычно за 1–2 недели).
Арт без текста — в `miniaturas_arte/`, надпись перекладывается через `../../marca/miniatura.py`.

## 3. Описание

```
{DESC}
```

Когда эпизод 2 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si pudieras ver el futuro 5 segundos antes que todos? → <ссылка>`.

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

- **Слева:** «Видео» → эпизод 2 (или «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на {mmss(end_card)}: раньше элементы закроют последнюю фразу «Pepe ya te vio».

## 8. Подсказка

Одна, в {mmss(card_at)} (история и наука закончились, начинается финал): видео → эпизод 2, текст подсказки:

```
Episodio 2: ver el futuro
```

В начале ролика подсказки не ставь: они уводят зрителя раньше времени.

## 9. Закреплённый комментарий

Опубликуй от имени канала сразу после выхода и закрепи:

```
Pepe dijo «Mañana, nadie te va a ver». 🐦 ¿Qué crees que pasa en el próximo episodio?
Y tú, ¿qué le preguntarías a tu mascota?
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
What if you could talk to animals?
```
```
What if you could talk to animals, and they could talk back? An animated story about what they'd tell you, and what you'd rather not know. At the end, the real science behind the idea.

{chap_en}

Original animation.

#whatif #animation
```

**Português**

```
E se você pudesse falar com os animais?
```
```
E se você pudesse falar com os animais, e eles com você? Uma história animada sobre o que eles te contariam e o que você preferiria não saber. No final, a ciência real por trás da ideia.

{chap_pt}

Animação original.

#esevoce #animacao
```

---
Длительность {mmss(total)} · голос: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
