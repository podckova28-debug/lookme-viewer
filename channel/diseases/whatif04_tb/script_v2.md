# What If #4: What Happens If You Get Consumption in 1850? Сценарий v2

Один герой, один век (Лондон, пик эпидемии), три года болезни. Рассказчик George + White Lady (голос role_tb_emma_low).
Каждый этап — одна и та же схема из четырёх частей:
  1) ЗЕРКАЛО (тот же кадр, герой меняется) 2) ПЛАТОК 3) АТЛАС (та же страница, лёгкие меняются) 4) ВРАЧ 1850-го.
Плашка этапа в углу: MONTH 1 → MONTH 6 → YEAR 1 → YEAR 2. Карточка YOUR BODY в конце этапа.
Около 900 слов, после ускорения ~5:30. Модель картинок: gpt_image_2_5 (low, 1k), проверка каждого кадра через review.py.

`N` — рассказчик, `W` — White Lady. [ЭКРАН] — что видим.

---

## 0. Холодное открытие
**C01 N:** In eighteen fifty, the deadliest disease in the world was also the most fashionable. Pale skin, a thin waist, bright eyes and pink cheeks. People called it the look of consumption.
[ЭКРАН] Салон 1850: бледные худые гости. Дама пудрит лицо у зеркала. Стрелка «THE LOOK».

**C02 N:** Lord Byron said he'd like to die of it, so the ladies would say, how interesting he looks in dying.
[ЭКРАН] Байрон у окна в позе. Подпись «AN ACTUAL QUOTE».

**C03 W:** Darling. Everyone who's anyone has me.
[ЭКРАН] White Lady у камина. Стрелка «TUBERCULOSIS (yes, the disease herself)».

**C04 N:** Today, you're a twenty-year-old clerk in London, eighteen fifty. You've just caught it. Let's see the next three years.
[ЭКРАН] Герой-клерк выходит из конторы на туманную улицу, кашляет. Заголовок.

## 1. Как это работает
**P01 N:** Here's how you caught it. Someone in your crowded office coughs. Tiny droplets hang in the air for hours. You breathe in a few bacteria, and that's enough.
[ЭКРАН] Контора: ряд клерков за конторками, один кашляет, облачко. Схема: капли с палочками → вдох.

**P02 N:** Your immune cells swallow them, but they can't kill them. So your body builds a prison around them, a small hard lump in your lung.
[ЭКРАН] Атлас: здоровые лёгкие → бугорок. Стрелка «THE PRISON».

**P03 N:** In eighteen fifty London, most adults have one of these prisons. For most of them, the prisoner never gets out.
[ЭКРАН] Улица Лондона, толпа. Подпись «MOST ADULTS».

**P04 W:** I'm very patient.

**P05 N:** But you're overworked, underfed, and you sleep in a cold, damp room. The prisoner breaks out.
[ЭКРАН] Комната героя ночью, герой за счетами при свече, холодный пар изо рта.

## 2. MONTH 1
**M1A N:** Month one. A cough that won't go away. You're tired all the time, and a little thinner. In the mirror, you look fine. Just tired.
[ЭКРАН] ЗЕРКАЛО-1: герой поправляет галстук, лицо усталое.

**M1B N:** Your handkerchief is still clean.
[ЭКРАН] Крупно: чистый платок в руке.

**M1C N:** Inside, the bacteria are multiplying, eating into the soft tissue around the prison.
[ЭКРАН] АТЛАС-1: бугорок с расползающимся пятном. Стрелка «BREAKING OUT».

**M1D N:** Your doctor's prescription is new and very modern. Cod liver oil, a spoonful three times a day. It tastes terrible. And to be fair, it might actually help a little.
[ЭКРАН] Врач с ложкой, герой морщится. Подпись «COD LIVER OIL». Стрелка «(it has vitamin D)».

[КАРТОЧКА] WEIGHT −2 KG, FEVER: SLIGHT, COUGH: DRY, MOOD: TIRED.

## 3. MONTH 6
**M6A N:** Month six. Every afternoon, a fever comes. Two bright pink spots burn on your cheeks. Doctors called it the hectic flush.
[ЭКРАН] ЗЕРКАЛО-2: розовые пятна на щеках. Стрелка «THE HECTIC FLUSH».

**M6B N:** At night, you sweat so much you wake up in soaked sheets. You've lost your appetite, and your collar is getting loose.
[ЭКРАН] Ночь, герой садится в мокрой постели. Стрелка «SOAKED».

**M6C N:** And one morning, there's a pink speck on your handkerchief.
[ЭКРАН] Платок с розовой точкой.

**M6D N:** Your doctor says your blood is too rich. So he puts leeches on your chest.
[ЭКРАН] Врач ставит пиявки (банка с пиявками, без натурализма). Зачёркивание «STEP 2: LEECHES».

**M6E W:** Leeches. Lovely. Take more blood. I'll wait.

[КАРТОЧКА] WEIGHT −6 KG, FEVER: EVERY AFTERNOON, COUGH: WET, MOOD: ANXIOUS.

## 4. YEAR 1
**Y1A N:** Year one. You cough, and your mouth fills with bright red blood.
[ЭКРАН] Платок с алым пятном. Герой в ужасе.

**Y1B N:** Here's why. The bacteria have eaten a hole right through your lung, and broken a blood vessel on the way.
[ЭКРАН] АТЛАС-2: дыра в лёгком. Стрелка «A HOLE».

**Y1C N:** And now, every time you cough, you spray bacteria into the room. Your landlady's little boy has started coughing too.
[ЭКРАН] Лестница доходного дома: мальчик кашляет. Стрелка «NEXT».

**Y1D N:** The strangest symptom is in your head. You feel hopeful. Full of plans. Doctors called it spes phthisica, the hope of the consumptive. Nobody knows why.
[ЭКРАН] Герой у окна мечтательно улыбается, строит планы. Подпись «SPES PHTHISICA».

**Y1E N:** Your doctor's advice: go south, to the warm air of Madeira or Italy. On a clerk's wages, that's like being told to go to the moon.
[ЭКРАН] Плакат-иллюстрация пароход/пальмы vs герой пересчитывает монеты.

[КАРТОЧКА] WEIGHT −11 KG, FEVER: DAILY, COUGH: BLOOD, MOOD: STRANGELY HOPEFUL.

## 5. YEAR 2
**Y2A N:** Year two. In the mirror, a stranger. Grey skin, hollow cheeks, huge shining eyes. Your coat hangs on you like on a coat hook.
[ЭКРАН] ЗЕРКАЛО-3. Стрелка «THE LOOK. FASHIONABLE.»

**Y2B N:** You're short of breath on the stairs. Your voice has turned to a whisper.
[ЭКРАН] Герой держится за перила, задыхается.

**Y2C N:** Inside, both lungs are full of holes.
[ЭКРАН] АТЛАС-3: дыры в обоих лёгких.

**Y2D N:** Now there are three ways this can go.
[ЭКРАН] Три двери/развилка.

**Y2E N:** Path one. Galloping consumption. It speeds up, and it's over in weeks. About half of untreated people were dead within a few years.
[ЭКРАН] Пустая постель, свеча гаснет.

**Y2F N:** Path two. You drag on for years, half alive, coughing the disease into everyone around you.
[ЭКРАН] Герой в постели, вокруг семья/соседи кашляют.

**Y2G N:** Path three. Your body builds new walls around the holes, and the disease goes quiet. Some people really did recover, with scars in their lungs for life.
[ЭКРАН] АТЛАС-4: шрамы, дыры зарубцованы. Герой гуляет в парке, бледный, но живой.

**Y2H W:** I'll take any of the three.

## 6. Тот же кашель сегодня
**T01 N:** Today, the same cough, three weeks long. A doctor sends you for a chest X-ray, and a test of what you cough up.
[ЭКРАН] Клиника, рентген со светлым пятном.

**T02 N:** The treatment is four drugs, every day, for six months. You feel better in weeks, but you have to finish it, or the bacteria learn to resist.
[ЭКРАН] Таблетница, календарь из 180 клеток. Подпись «DON'T STOP».

**T03 N:** And yet, tuberculosis still kills more than a million people every year. Mostly where the medicine is too far away.
[ЭКРАН] Карта мира. Подпись «1.2 MILLION A YEAR».

**T04 W:** Still here, darling. Still in fashion.

**E01 N:** So, which path would you have got in eighteen fifty? Tell me in the comments.

---

## Проверка фактов
- Романтизация чахотки, «consumptive look»: Sontag, *Illness as Metaphor* (1978); Day, *Consumptive Chic* (2017). Байрон — цитата по Т. Муру (1830).
- XIX век: туберкулёз — около четверти всех смертей в Европе; в Англии в 1850-е — крупнейшая причина смерти взрослых (Registrar General; Dubos, *The White Plague*, 1952). Большинство взрослых горожан были инфицированы (туберкулиновые пробы начала XX в. — >90% городских взрослых).
- Рыбий жир: введён для лечения чахотки в 1840-х (C.J.B. Williams, Brompton Hospital, 1849, отчёт о 400 случаях); содержит витамин D, который влияет на иммунный ответ (Martineau et al., 2007/2011).
- Пиявки и кровопускание при чахотке и кровохарканье применялись в первой половине XIX в. (Laennec, Louis — критика кровопускания 1835).
- Hectic fever / hectic flush, ночные поты, похудение, кровохарканье — классические признаки (Laennec 1819; WHO).
- Spes phthisica — описанная в XIX в. эйфория/оптимизм чахоточных (Dubos; Bynum, *Spitting Blood*, 2012).
- Лечение «тёплым климатом» (Мадейра, Италия) — для состоятельных; Бромптонская больница для чахоточных основана в 1841.
- Без лечения: ~70% умирают за 10 лет при активной форме с бактериовыделением, медиана ~3 года; часть выздоравливает спонтанно (Tiemersma et al., PLoS One 2011) → «about half … within a few years», «some recovered».
- Кровохарканье — эрозия сосуда стенкой каверны (в т.ч. аневризмы Расмуссена).
- Сегодня: WHO Global TB Report 2024 — 1,25 млн смертей (2023); стандартный режим 6 мес (4 препарата 2 мес + 2 препарата 4 мес).
