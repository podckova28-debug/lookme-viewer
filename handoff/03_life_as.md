# Канал «Life As» — полный бриф (на 24.11.2026)

Ветка с файлами: `claude/clever-keller-n0ul3i` репозитория podckova28-debug/lookme-viewer. Код и эпизоды — папка `hardo/`.

## Формат
Анимированные объяснялки от второго лица: «Your Life as a <профессия/роль>» / «Why It's So Hard to Be a …» (стиль Dinzo):
белый фон, рисованные кадры с подписями-стрелками, Ken Burns, короткие клипы, рассказчик обращается к зрителю на «you».
Уже сделаны эпизоды 1–4 (ep3 Teacher, ep4 Line Cook — `hardo/ep3`, `hardo/ep4`: plan.json, blocks.json, script.md с источниками,
youtube_metadata, qa_report). Сборка `hardo/pipeline/assemble_ep.py`, проверка `hardo/pipeline/qa_check.py` (22 пункта),
хаб с ссылками `hardo/hub/`. Эпизоды 1–2 — только в хабе.

## Данные vidIQ (поисков/мес, конкуренция)
your life as 750K/57, your life as a 352K/55, why it sucks to be born as 241K/71, your life as every rank 201K/49,
in their shoes 182K/46, why it sucks 125K/69, pov story 100K/43, why it sucked to be 38K/74, your life as alexander the great 36K/46,
your life as nikola tesla 25K/47, your life as a north korean 22K/44, immersive history 8K/41.
Вывод: «Your Life as …» больше и легче, чем «Why it sucks …»; хорошо идут роль + эпоха («Every Rank in …», «in Samurai Japan»).
По outliers: «Your Life as Every Rank in Delta Force» (5K подп., 124K), «Your Life at Every Level of a 75th Ranger Career» (1K, 60K),
RU «Твоя жизнь на каждом ранге в самурайской Японии» (2,6K, 489K).

## Оформление канала
- Название: **Life As** (сохранить). Handle: @lifeas / @lifeas.tv / @yourlifeas.
- Аватар: `handoff/avatars/lifeas_2_door.png` (приоткрытая дверь и шаг внутрь — «войти в чужую жизнь») или `lifeas_1_totem.png`.
Описание:
```
Step into someone else's life for ten minutes.

What is it really like to be a line cook on a Friday night, a teacher in October, a medieval peasant, a Roman legionary or a deep-sea diver? Every video puts YOU in their shoes: the hours, the money, the dangers, the small wins and the reasons almost nobody lasts.

Animated, honest and based on real data and real stories.
New lives every week.
```
Ключевые слова:
```
your life as, your life as a, your life as every rank, in their shoes, pov story, why it sucks to be, why it's so hard to be, a day in the life, life as a, hardest jobs, worst jobs, jobs explained, animated story, animated explainer, immersive history, what it's like to be
```
Настройки: Education (или Entertainment), английский, «не для детей», раскрытие ИИ = ДА, хэштеги #yourlifeas #animation #jobs.
Публикация по прежнему решению пользователя — каждый день в 15:00 МСК (по данным лучше 22:00 МСК = 14:00 Нью-Йорк, см. `SCHEDULE.md`).

## Идеи
Every Rank in a Samurai Army, Every Rank in the Roman Legion, Life as a Medieval Peasant, Life as a Victorian Chimney Sweep,
Life as a Deep-Sea Fisherman, Life as an Air Traffic Controller, Life as a North Korean Soldier, Life as a Pirate (связка с каналом напитков).
