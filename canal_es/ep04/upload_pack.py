"""Writes out/subida_youtube.md: everything needed to publish episode 4 (title, thumbnails, description with
chapters from timing.json, tags, upload settings, end screen, card, pinned comment, Shorts, translations).
Notes for the person uploading are in Russian; everything to paste into YouTube is Spanish/English/Portuguese in code blocks."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH_SHORT = [('s00', 'Inicio'), ('s03', 'El espejo'), ('s05', 'La conciencia de Nacho'), ('s09', 'Los problemas'), ('s12', 'El sábado'), ('s15', 'Pepe'), ('s16', '¿Algo de esto es real?')]
CH_EN = ['Intro', 'The mirror', "Nacho's conscience", 'The problems', 'Saturday', 'Pepe', 'Is any of this real?']
CH_PT = ['Início', 'O espelho', 'A consciência do Nacho', 'Os problemas', 'O sábado', 'Pepe', 'Algo disso é real?']
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
starts = [T['scenes'][s]['start'] for s, _ in CH_SHORT]
chap = '\n'.join(f"{mmss(a)} {n}" for a, (_, n) in zip(starts, CH_SHORT))
chap_en = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_EN))
chap_pt = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_PT))
total = T['total']; end_card = total - 5          # the dark «Ponle que… / Próximo episodio / Suscríbete» card fills the last ~5.5 s
card_at = T['scenes']['s17']['start']              # after the story and the science, when the outro asks the viewer

TITLE = '¿Qué pasaría si fueras invisible?'
TITLE_B = '¿Qué pasaría si nadie pudiera verte?'
TAGS = ('qué pasaría si fueras invisible, que pasaria si fueras invisible, y si fueras invisible, ser invisible, que pasaria si pudieras volverte invisible, '
        'volverse invisible, invisibilidad, qué pasaría si, que pasaria si, historias animadas, historia animada, animación en español, qué harías si, '
        'ponle que, pepe la paloma, rana de cristal, capa de invisibilidad')
assert len(TITLE) <= 100 and len(TAGS) <= 500, (len(TITLE), len(TAGS))

DESC = f"""¿Qué pasaría si un día despertaras y nadie pudiera verte? Ni tu mamá, ni las cámaras, ni el espejo. Una historia animada sobre lo divertido que es ser invisible… y lo que pasa cuando nadie te ve. Al final, la ciencia real detrás de la idea.

{chap}

Animación original.

#quepasariasi #animacion"""

SHORTS = [
    ('short1_espejo.mp4', '¿Y si despertaras invisible? 👻 #shorts #quepasariasi'),
    ('short2_tostada.mp4', 'Desayunar siendo invisible 🍞 #shorts #quepasariasi'),
    ('short3_conciencia.mp4', 'Cuando eres la conciencia de tu mejor amigo #shorts #quepasariasi'),
    ('short4_libreta.mp4', 'Lo que el profe escribe sobre ti 📓 #shorts #quepasariasi'),
    ('short5_torta.mp4', 'Lo primero que harías si fueras invisible 🥪 #shorts #quepasariasi'),
    ('short6_maquinas.mp4', 'Las puertas automáticas no te ven 🚪 #shorts #quepasariasi'),
    ('short7_ciencia.mp4', '3 cosas reales sobre ser invisible 🧠 #shorts #ciencia'),
    ('short8_renata.mp4', 'Si nadie te ve, di que estás ahí 💜 #shorts #quepasariasi'),
]
# publishing order: the strongest hooks first; the emotional one late (it spoils the climax), the science short last
ORDER = [0, 1, 4, 2, 5, 3, 7, 6]
shorts_rows = '\n'.join(f"| {i + 1} | `{SHORTS[k][0]}` | `{SHORTS[k][1]}` |" for i, k in enumerate(ORDER))

md = f"""# Эпизод 4 · всё для загрузки на YouTube

Видео: `ep04_final.mp4` (1080p, {mmss(total)}). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
{TITLE}
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
{TITLE_B}
```

Тема обещана в конце эпизода 3. По исследованию канала запрос «que pasaria si fueras invisible» ищут ~7,1 тыс. раз в месяц, поэтому основное название совпадает с запросом слово в слово. Запасное — про чувство, а не про силу. Проверить их в vidIQ не удалось: кредиты кончились (обновятся 21 ноября).

## 2. Обложки (1280×720, JPEG < 2 МБ)

| Файл | Надпись | Что на картинке |
|---|---|---|
| `miniatura_A.jpg` — **основная** | NADIE ME VE | Герой — светящийся стеклянный контур, перед ним в воздухе висит надкусанный тост; мама смотрит сквозь него |
| `miniatura_B.jpg` | ESTOY AQUÍ | Рената на закате держит за руку пустоту (голубой контур героя), Канела смотрит вверх |
| `miniatura_C.jpg` | ¡LA TORTA FANTASMA! | Торта летит по столовой сама, школьники в ужасе |

YouTube Studio → «Проверить и сравнить»: загрузить **A, B и C**. YouTube сам выберет лучшую по времени просмотра (обычно за 1–2 недели).
Арт без текста — в `miniaturas_arte/`, надпись перекладывается через `../../marca/miniatura.py`.

## 3. Описание

```
{DESC}
```

Когда эпизод 3 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si pudieras hablar con los animales? → <ссылка>`.

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

- **Слева:** «Видео» → эпизод 3 (или «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на {mmss(end_card)}: раньше элементы закроют последнюю фразу «Pepe dice que no te va a gustar».

## 8. Подсказка

Одна, в {mmss(card_at)} (история и наука закончились, начинается финал): видео → эпизод 3, текст подсказки:

```
Episodio 3: hablar con los animales
```

В начале ролика подсказки не ставь: они уводят зрителя раньше времени.

## 9. Закреплённый комментарий

Опубликуй от имени канала сразу после выхода и закрепи:

```
Pepe dijo «Mañana vas a ser el más listo del mundo. No te va a gustar». 🐦 ¿Por qué no le va a gustar?
Y tú, ¿qué harías si fueras invisible un día?
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
What if you were invisible?
```
```
What if you woke up one day and nobody could see you? Not your mom, not the cameras, not the mirror. An animated story about how fun it is to be invisible… and what happens when nobody sees you. At the end, the real science behind the idea.

{chap_en}

Original animation.

#whatif #animation
```

**Português**

```
E se você fosse invisível?
```
```
E se um dia você acordasse e ninguém pudesse te ver? Nem sua mãe, nem as câmeras, nem o espelho. Uma história animada sobre como é divertido ser invisível… e o que acontece quando ninguém te vê. No final, a ciência real por trás da ideia.

{chap_pt}

Animação original.

#esevoce #animacao
```

---
Длительность {mmss(total)} · голос: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
