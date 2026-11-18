"""Writes out/subida_youtube.md: everything needed to publish episode 6 (title, thumbnails, description with
chapters from timing.json, tags, upload settings, end screen, card, pinned comment, Shorts, translations).
Notes for the person uploading are in Russian; everything to paste into YouTube is Spanish/English/Portuguese in code blocks."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH_SHORT = [('s00', 'Inicio'), ('s03', 'El lunes'), ('s05', 'El portero'), ('s07', 'Una semana sin dolor'), ('s09', 'Los problemas'), ('s12', 'El viernes'), ('s14', 'El sábado'), ('s15', 'Pepe'), ('s16', '¿Algo de esto es real?')]
CH_EN = ['Intro', 'Monday', 'The goalkeeper', 'A week without pain', 'The problems', 'Friday', 'Saturday', 'Pepe', 'Is any of this real?']
CH_PT = ['Início', 'A segunda-feira', 'O goleiro', 'Uma semana sem dor', 'Os problemas', 'A sexta-feira', 'O sábado', 'Pepe', 'Algo disso é real?']
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
starts = [T['scenes'][s]['start'] for s, _ in CH_SHORT]
chap = '\n'.join(f"{mmss(a)} {n}" for a, (_, n) in zip(starts, CH_SHORT))
chap_en = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_EN))
chap_pt = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_PT))
total = T['total']; end_card = total - 5          # the dark «Ponle que… / Próximo episodio / Suscríbete» card fills the last ~5.5 s
card_at = T['scenes']['s17']['start']              # after the story and the science, when the outro asks the viewer

TITLE = '¿Qué pasaría si dejaras de sentir dolor?'
TITLE_B = '¿Qué pasaría si no pudieras sentir dolor?'
TAGS = ('qué pasaría si dejaras de sentir dolor, que pasaria si dejaras de sentir dolor, no sentir dolor, sin dolor, insensibilidad al dolor, '
        'qué pasaría si no sintieras dolor, para qué sirve el dolor, qué pasaría si, que pasaria si, historias animadas, historia animada, '
        'animación en español, qué harías si, ponle que, pepe la paloma, chile picante, capsaicina')
assert len(TITLE) <= 100 and len(TAGS) <= 500, (len(TITLE), len(TAGS))

DESC = f"""¿Qué pasaría si un día dejaras de sentir dolor? Ni golpes, ni chile, ni el dedo chiquito contra la cama. Una historia animada sobre lo divertido que es no sentir nada… y lo que pasa cuando algo sí debería dolerte. Al final, la ciencia real detrás del dolor.

{chap}

Animación original.

#quepasariasi #animacion"""

SHORTS = [
    ('short1_dedo.mp4', 'El dedo chiquito contra la cama… y nada 🦶 #shorts #quepasariasi'),
    ('short2_salsa.mp4', 'La salsa de tu abuela, sin sentir dolor 🌶️ #shorts #quepasariasi'),
    ('short3_portero.mp4', 'El portero que no siente nada ⚽ #shorts #quepasariasi'),
    ('short4_profe.mp4', 'Se cayó tres veces. Sonrió tres veces 📓 #shorts #quepasariasi'),
    ('short5_semana.mp4', 'Una semana sin sentir dolor 🦷 #shorts #quepasariasi'),
    ('short6_palmada.mp4', 'Cuando no sabes cuánto duele un golpe 👋 #shorts #quepasariasi'),
    ('short7_extrañar.mp4', 'Lo que sí debería doler 💜 #shorts #quepasariasi'),
    ('short8_ciencia.mp4', '3 cosas reales sobre el dolor 🧠 #shorts #ciencia'),
]
# publishing order: the strongest hooks first; the emotional one late (it spoils the climax), the science short last
ORDER = [1, 0, 2, 3, 5, 4, 6, 7]
shorts_rows = '\n'.join(f"| {i + 1} | `{SHORTS[k][0]}` | `{SHORTS[k][1]}` |" for i, k in enumerate(ORDER))

md = f"""# Эпизод 6 · всё для загрузки на YouTube

Видео: `ep06_final.mp4` (1080p, {mmss(total)}). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
{TITLE}
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
{TITLE_B}
```

Тема обещана в конце эпизода 5. Ролик с почти таким же названием «¿Qué pasaría si dejaras de sentir dolor?» у Giro Imposible набрал 876 тыс. просмотров, больше всех в нише, поэтому основное название совпадает с этим запросом. Запасное — другая формулировка того же вопроса. Проверить названия в vidIQ не удалось: кредиты обновятся 21 ноября.

## 2. Обложки (1280×720, JPEG < 2 МБ)

| Файл | Надпись | Что на картинке |
|---|---|---|
| `miniatura_A.jpg` — **основная** | NO ME DUELE | Герой весь в пластырях и с шишкой улыбается и показывает «класс»; шкала боли на нуле |
| `miniatura_B.jpg` | ¿PICA? ¡NADA! | Герой ест бабушкину сальсу ложкой, из ушей пар, мама в ужасе |
| `miniatura_C.jpg` | ESTO SÍ DUELE | Остановка утром: Рената у автобуса, герой с забинтованной лодыжкой |

YouTube Studio → «Проверить и сравнить»: загрузить **A, B и C**. YouTube сам выберет лучшую по времени просмотра (обычно за 1–2 недели).
Арт без текста — в `miniaturas_arte/`, надпись перекладывается через `../../marca/miniatura.py`.

## 3. Описание

```
{DESC}
```

Когда эпизод 5 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si tuvieras 500 de IQ? → <ссылка>`.

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

- **Слева:** «Видео» → эпизод 5 (или «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на {mmss(end_card)}: раньше элементы закроют последнюю фразу «Pepe dice que no te va a alcanzar».

## 8. Подсказка

Одна, в {mmss(card_at)} (история и наука закончились, начинается финал): видео → эпизод 5, текст подсказки:

```
Episodio 5: 500 de IQ
```

В начале ролика подсказки не ставь: они уводят зрителя раньше времени.

## 9. Закреплённый комментарий

Опубликуй от имени канала сразу после выхода и закрепи:

```
Pepe dijo «Mañana vas a tener todo el dinero del mundo. Y no te va a alcanzar». 🐦 ¿Cómo puede no alcanzar?
Y tú, ¿qué harías si no pudieras sentir dolor un día?
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
What if you couldn't feel pain?
```
```
What if one day you stopped feeling pain? No bumps, no hot sauce, no little toe against the bed. An animated story about how fun it is to feel nothing… and what happens when something should hurt. At the end, the real science behind pain.

{chap_en}

Original animation.

#whatif #animation
```

**Português**

```
E se você não sentisse dor?
```
```
E se um dia você parasse de sentir dor? Nem pancadas, nem pimenta, nem o dedinho na quina da cama. Uma história animada sobre como é divertido não sentir nada… e o que acontece quando algo deveria doer. No final, a ciência real por trás da dor.

{chap_pt}

Animação original.

#esevoce #animacao
```

---
Длительность {mmss(total)} · голос: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
