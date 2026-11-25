# Канал «Болезни» — полный бриф (на 24.11.2026)

Основная работа по сценариям и монтажу — в отдельном чате болезней (ветка `claude/compassionate-thompson-rzoaqf`).
Озвучка делалась здесь, в ветке `claude/clever-keller-n0ul3i`, папка `voices/`.

## Формат
«The ENTIRE History of <болезнь>»: рассказчик + сама болезнь как персонаж-злодей со своим голосом (King Cholera, Plague и т. д.).
Новый пилот «What Happens If You Catch <болезнь>?» — от второго лица, рассказ о самом зрителе; первая серия — холера.

## Озвучено (voices/, Chatterbox, только синтетические опорные голоса Kokoro; голоса реальных людей не клонируются, OmniVoice не используется)
plague_ep01 (v1–v3), cholera_ep02, smallpox_ep03, spanishflu_ep04, scurvy_ep05, rabies_ep06, tb_ep07, malaria_ep08, leprosy_ep09,
polio_ep10, typhus_ep11, yellowfever_ep12, measles_ep13, **whatif01_cholera** (34 реплики, 3:48, whisper ≥ 0.89, README и _qa.tsv в папке).
Рассказчик: George (`refs/kokoro_bm_george.wav`), exaggeration 0.45 (в What If 0.5 — живее), cfg 0.5.
Злодеи: role_*.wav в `voices/refs` (cholera — role_cholera_fable, exaggeration 0.85, cfg 0.4 + chorus/phaser/lowpass).
Правила текста: числа и годы словами, «often» не использовать, трудные слова — фонетически (Vibrio cholerae → «Vibree-oh koler-eye»,
diarrhoea → «diarrhea»).

## Данные vidIQ (поисков/мес, конкуренция)
black death 150K/58, plague 66K/71, infection 32K/58, pandemic 31K/52, disease 28K/69, malaria 21K/56 (растёт +43 %),
tuberculosis 18K/49, bubonic plague 15K/51, smallpox 11K/52, what happens if you 94K/64, dark history 551K/57, world history 376K/52.
«history of diseases» почти не ищут → в названиях ставить само название болезни, а не «history of diseases».

## Оформление канала
- Аватар: `handoff/avatars/disease_1_hourglass.png` (песочные часы, где песок — микробы) или `disease_2_lens.png` (лупа и вирус-корона).
Описание:
```
The diseases that shaped history, and what they would do to you.

The Black Death, cholera, smallpox, the Spanish flu: every episode tells the whole story of one disease, from the first victims to the cure, and the strange, brave and terrible things people did to survive it. In our "What Happens If" series, you catch it yourself, and find out what your body would go through, then and now.

Animated, science-checked, with real sources in every description.
New episodes every week.
```
Ключевые слова:
```
history of medicine, disease history, black death, plague, bubonic plague, pandemic, pandemics in history, cholera, smallpox, tuberculosis, malaria, spanish flu, what happens if you, what happens if you catch, dark history, medical history, history documentary, animated history, science explained, epidemics
```
Настройки: Education, английский, «не для детей», раскрытие ИИ = ДА. Не давать медицинских советов; лечение — только как история.

## Состояние
- Пилот What If (холера): голоса готовы и переданы чату болезней; дальше — кадры и монтаж там.
- Следующие What If: rabies (анонсирован в E02 пилота), plague, smallpox, scurvy, malaria.

## Проверка перед рендером
Обязательно: `channel/diseases/tools/QC.md` и `qc.py` (синхронизация, одно место — одна обстановка, листы для ручного просмотра).
