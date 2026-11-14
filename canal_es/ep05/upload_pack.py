"""Writes out/subida_youtube.md: everything needed to publish episode 5 (title, thumbnails, description with
chapters from timing.json, tags, upload settings, end screen, card, pinned comment, Shorts, translations).
Notes for the person uploading are in Russian; everything to paste into YouTube is Spanish/English/Portuguese in code blocks."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH_SHORT = [('s00', 'Inicio'), ('s03', 'El lunes'), ('s05', 'Los frijoles de don Chuy'), ('s07', 'Una semana de genio'), ('s09', 'Los problemas'), ('s12', 'El viernes'), ('s15', 'Pepe'), ('s16', '¿Algo de esto es real?')]
CH_EN = ['Intro', 'Monday', "Don Chuy's beans", 'A week as a genius', 'The problems', 'Friday', 'Pepe', 'Is any of this real?']
CH_PT = ['Início', 'A segunda-feira', 'Os feijões do seu Chuy', 'Uma semana de gênio', 'Os problemas', 'A sexta-feira', 'Pepe', 'Algo disso é real?']
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
starts = [T['scenes'][s]['start'] for s, _ in CH_SHORT]
chap = '\n'.join(f"{mmss(a)} {n}" for a, (_, n) in zip(starts, CH_SHORT))
chap_en = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_EN))
chap_pt = '\n'.join(f"{mmss(a)} {n}" for a, n in zip(starts, CH_PT))
total = T['total']; end_card = total - 5          # the dark «Ponle que… / Próximo episodio / Suscríbete» card fills the last ~5.5 s
card_at = T['scenes']['s17']['start']              # after the story and the science, when the outro asks the viewer

TITLE = '¿Qué pasaría si tuvieras 500 de IQ?'
TITLE_B = '¿Qué pasaría si fueras la persona más lista del mundo?'
TAGS = ('qué pasaría si tuvieras 500 de iq, que pasaria si tuvieras 500 de iq, iq de 500, 500 de iq, coeficiente intelectual, '
        'qué pasaría si fueras un genio, la persona más inteligente del mundo, el más listo del mundo, iq de einstein, qué pasaría si, que pasaria si, '
        'historias animadas, historia animada, animación en español, qué harías si, ponle que, pepe la paloma')
assert len(TITLE) <= 100 and len(TAGS) <= 500, (len(TITLE), len(TAGS))

DESC = f"""¿Qué pasaría si un día despertaras con 500 de IQ? Lo sabes todo, lo calculas todo y aprendes cualquier cosa en segundos. Una historia animada sobre ser el más listo del mundo… y la única pregunta que no sabes contestar. Al final, la ciencia real detrás del IQ.

{chap}

Animación original.

#quepasariasi #animacion"""

SHORTS = [
    ('short1_tostadora.mp4', 'Cuando tienes 500 de IQ y tu mamá tiene una tostadora 🍞 #shorts #quepasariasi'),
    ('short2_frijoles.mp4', '¿Cuántos frijoles hay en el frasco? 🫘 #shorts #quepasariasi'),
    ('short3_profe.mp4', 'Corregir al profe con 500 de IQ 📏 #shorts #quepasariasi'),
    ('short4_pepe.mp4', 'Lo único que no puedes calcular 🐦 #shorts #quepasariasi'),
    ('short5_corregir.mp4', 'Cuando corriges a todo el mundo 🙄 #shorts #quepasariasi'),
    ('short6_torta.mp4', 'Pensar demasiado: ¿torta o quesadilla? 🥪 #shorts #quepasariasi'),
    ('short7_nose.mp4', 'La pregunta más difícil del mundo 💜 #shorts #quepasariasi'),
    ('short8_ciencia.mp4', '3 cosas reales sobre el IQ 🧠 #shorts #ciencia'),
]
# publishing order: the strongest hooks first; the emotional one late (it spoils the climax), the science short last
ORDER = [1, 0, 3, 2, 5, 4, 6, 7]
shorts_rows = '\n'.join(f"| {i + 1} | `{SHORTS[k][0]}` | `{SHORTS[k][1]}` |" for i, k in enumerate(ORDER))

md = f"""# Эпизод 5 · всё для загрузки на YouTube

Видео: `ep05_final.mp4` (1080p, {mmss(total)}). Всё, что вставляется в YouTube, лежит в блоках кода — копируй целиком.
Общие настройки канала (категория, язык, «не для детей», расписание) — в `../../marca/canal_youtube.md`, здесь только то, что касается этой серии.

## 1. Название

```
{TITLE}
```

Запасное (для теста названий в «Проверить и сравнить», если он у тебя есть):

```
{TITLE_B}
```

Тема обещана в конце эпизода 4 («¿Y si tuvieras 500 de IQ?»). Похожий ролик «IQ de 500» у Noah_Ketalsi набрал 402 тыс. просмотров, поэтому в основном названии стоит «500 de IQ», как в обещании. Запасное — для тех, кто ищет «la persona más lista del mundo». Проверить названия в vidIQ не удалось: кредиты кончились (обновятся 21 ноября).

## 2. Обложки (1280×720, JPEG < 2 МБ)

| Файл | Надпись | Что на картинке |
|---|---|---|
| `miniatura_A.jpg` — **основная** | 500 DE IQ | Герой в цвете, ухмыляется; мир вокруг — синий чертёж с меловыми стрелками и траекториями, над кудрями светится мозг |
| `miniatura_B.jpg` | ¿SÍ O NO? | Мозг перегрелся: дым из кудрей, вихрь карточек-вариантов, полоска загрузки почти пустая; в дверях ждёт Рената |
| `miniatura_C.jpg` | NO SE PUEDE CALCULAR | Пепе в цвете в красной рамке прицела на синем чертеже, герой меряет его линейкой |

YouTube Studio → «Проверить и сравнить»: загрузить **A, B и C**. YouTube сам выберет лучшую по времени просмотра (обычно за 1–2 недели).
Арт без текста — в `miniaturas_arte/`, надпись перекладывается через `../../marca/miniatura.py`.

## 3. Описание

```
{DESC}
```

Когда эпизод 4 будет опубликован, можно добавить строку перед хэштегами: `Episodio anterior: ¿Qué pasaría si fueras invisible? → <ссылка>`.

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

- **Слева:** «Видео» → эпизод 4 (или «Лучшее для зрителя»).
- **Справа:** «Подписка».

Старт ставь ровно на {mmss(end_card)}: раньше элементы закроют последнюю фразу «Pepe dice que ese es el problema».

## 8. Подсказка

Одна, в {mmss(card_at)} (история и наука закончились, начинается финал): видео → эпизод 4, текст подсказки:

```
Episodio 4: ser invisible
```

В начале ролика подсказки не ставь: они уводят зрителя раньше времени.

## 9. Закреплённый комментарий

Опубликуй от имени канала сразу после выхода и закрепи:

```
Pepe dijo «Mañana, nada te va a doler. Ni siquiera lo que debería». 🐦 ¿Qué crees que significa?
Y tú, ¿qué harías con 500 de IQ?
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
What if you had an IQ of 500?
```
```
What if you woke up one day with an IQ of 500? You know everything, you calculate everything and you learn anything in seconds. An animated story about being the smartest person in the world… and the one question you can't answer. At the end, the real science behind IQ.

{chap_en}

Original animation.

#whatif #animation
```

**Português**

```
E se você tivesse QI de 500?
```
```
E se um dia você acordasse com QI de 500? Você sabe tudo, calcula tudo e aprende qualquer coisa em segundos. Uma história animada sobre ser a pessoa mais inteligente do mundo… e a única pergunta que você não sabe responder. No final, a ciência real por trás do QI.

{chap_pt}

Animação original.

#esevoce #animacao
```

---
Длительность {mmss(total)} · голос: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
