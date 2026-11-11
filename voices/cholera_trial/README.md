# King Cholera — пробы голоса

Тестовые фразы: «Kneel. Or, well... collapse. Either is fine.» / «They blamed the smell. The smell! I am offended on a personal level.» / «Twenty litres a day. I do not do things by halves.»
Chatterbox (MIT), exaggeration 0.85 (театрально), cfg 0.4, temperature 0.75. Опорные голоса Kokoro (Apache-2.0), фраза-приглашение хозяина приёма.

| Вариант | Опорный голос | F0 | Длина 3 фраз | Комментарий |
|---|---|---|---|---|
| C1_daniel | `refs/role_cholera_daniel.wav` (bm_daniel, без сдвига) | ~138 Гц | 12,4 с | неторопливый, смакующий |
| C2_fable_up | `refs/role_cholera_fable.wav` (bm_fable +1,5 полутона) | ~156 Гц | 10,1 с | живее, болтливее, дальше всех от Чумы (Lewis ~111 Гц) |
| C3_daniel_wet | C1 + эффект «влажности» (chorus + phaser + lowpass 7,5 кГц) | ~138 Гц | 12,4 с | разборчивость сохранена (whisper дословно) |
| C4_fable_wet | C2 + тот же эффект | ~156 Гц | 10,1 с | |

Whisper en: все дословно; «Kneel» распознаётся как «Neil» (омофон), «twenty» цифрами.
Эффект накладывается после синтеза одной командой ffmpeg (см. ниже), его можно менять без переозвучки:
`ffmpeg -i in.wav -af "chorus=0.6:0.85:28|35:0.25|0.2:0.3|0.4:1.8|1.2,aphaser=in_gain=0.7:out_gain=0.9:delay=2.5:decay=0.35:speed=0.6,lowpass=f=7500" out.wav`
