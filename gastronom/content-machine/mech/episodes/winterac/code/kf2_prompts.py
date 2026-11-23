"""Эп. 28 v3 — новые кадры для «больше планов, без возврата к стоп-кадру» (gpt_image_2_5 medium 2k 9:16, 1 кр).
Пользователь: «Сделай больше кадров, законченные анимации переходящие в тот же статичный кадр — ужасно».
Каждый план — свой клип Wan 3.0 480p 3 с; стоп-кадр исходника после его же клипа больше не ставим.
python3 kf2_prompts.py → kf2_req.json (запросы для generate_image_batch), clip2_req.json — промпты клипов."""
import json, importlib.util, os
_s = importlib.util.spec_from_file_location('kf', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kf_prompts.py'))
K = importlib.util.module_from_spec(_s); _s.loader.exec_module(K)
STYLE, CHAR, ARMS, CAR, END = K.STYLE, K.CHAR, K.ARMS, K.CAR, K.END
YARD, MIKH = '08996e99-8177-4b7d-8b13-c1ae3a50f7bb', '87ee183f-9089-4c8d-bbe2-f2bdaec3c14c'
KNOB_HAND = ("A man's RIGHT hand in an orange short sleeve comes from the lower left and turns the knob, holding its grip between the "
             "thumb and the bent index finger; the middle, ring and little fingers are relaxed and slightly curled. Anatomically correct "
             "hand: exactly one hand with exactly five digits, one thumb and four fingers, no extra finger. ")
CAB = f"Inside {CAR}, view from the front passenger seat toward the driver. "

F = {  # ключ: (промпт, референсы, сколько вариантов)
 'n1_puzzled': (STYLE + CAB + CHAR + "He sits in the FRONT driver's seat of the cold car; all windows are fogged up milky white. He frowns and looks "
                "doubtfully at the centre console; his right index finger hovers just above a square button with a white snowflake symbol, "
                "his left hand rests on the steering wheel; a little puff of breath steam near his mouth. " + ARMS + END, [YARD, MIKH], 2),
 'n2_rain': (STYLE + "A wet late-autumn day just above freezing: grey drizzle, puddles on the asphalt, wet yellow fallen leaves, NO snow, "
             f"grey panel apartment blocks. {CAR} seen from the driver's side; the driver's window is lowered. " + CHAR +
             "He sits in the FRONT driver's seat, smiles and gives a cheerful thumbs-up out of the open window with his left hand; "
             "his right hand is on the steering wheel. " + ARMS + END, [YARD, MIKH], 2),
 'n3_dryair': (STYLE + "Cartoon close-up of the dashboard of an old Russian car, dark-grey plastic: a fat grey rain cloud full of blue water "
               "droplets, with a grumpy cartoon face, is being sucked into a grille at the bottom of the frame; from a dashboard air vent at "
               "the top come out clean white wavy lines of dry air with small sparkles. Nobody, no hands, exactly one cartoon face." + END,
               [YARD], 1),
 'n4_drops': (STYLE + "Macro cartoon cutaway, filling the whole frame: the thin silver fins of a cold car air-conditioning radiator covered "
              "with blue frost; big round water drops form on the fins, slide down and gather in a channel at the bottom that leads into "
              "a thin black rubber drain tube. Dark blue background, bold outlines." + END, [YARD], 1),
 'n5_drip': (STYLE + f"Low view at ground level under the front of {CAR}, parked on packed snow in a winter courtyard: from a thin black "
             "rubber tube sticking down from under the car, clear water drips onto the snow and has melted a small round hole with a "
             "little puddle in it. Cold winter daylight. Nobody." + END, [YARD], 1),
 'n6_frostnight': (STYLE + f"Night, hard frost: {CAR} parked in a snowy courtyard of grey panel apartment blocks, its whole body covered "
                   "with thick white hoarfrost, little icicles hanging from the bumper and mirrors, snow sparkling under a street lamp, a "
                   "frosty full moon. Nobody." + END, [YARD], 1),
 'n7_ecu': (STYLE + "Cartoon scene under the open bonnet of a car on a freezing night: a small black electronic control unit box with a "
            "green circuit-board pattern and a strict cartoon face (frowning eyebrows) pulls a big lever of a knife switch down to the off "
            "position; a thick cable runs from the switch to a frosty round air-conditioning compressor with a pulley, covered with "
            "hoarfrost, its eyes closed in sleep. Small blue sparks, cold blue light, snowflakes. Exactly two cartoon faces." + END,
            [YARD], 1),
 'n8_thermo': (STYLE + "Close-up of an old outdoor window thermometer fixed on the frosty wooden frame of a panel-block window: a glass tube "
               "with red liquid on a white plastic plate with plain tick marks only (NO digits, no letters); one longer tick in the "
               "middle is marked with a small blue snowflake symbol; the red liquid stands exactly at that middle tick. Frost patterns "
               "on the window glass, snow falling outside." + END, [YARD], 1),
 'n9_heatknob': (STYLE + "Close-up of the centre console of an old Russian car with a plain dark-grey plastic panel: a big round heater "
                 "temperature knob with a colour scale arc from blue on the left to red on the right (no numbers). " + KNOB_HAND +
                 "The knob points to the red side." + END, [YARD], 1),
 'n10_glass': (STYLE + "Close-up of the inside of a fogged car windshield covered with tiny water droplets; warm orange air streams blow "
               "up from the defroster slot on top of the dashboard below; where the warm air touches the glass the droplets shrink and "
               "rise as thin white wisps of vapour, and a clear patch spreads, showing a snowy courtyard outside. Nobody, no hands." + END,
               [YARD], 1),
 'n11_modeknob': (STYLE + "Close-up of the centre console of an old Russian car with a plain dark-grey plastic panel: a round air-direction "
                  "knob with simple white symbols around it (a windshield symbol at the top, a seated-person symbol on the side, no "
                  "text). " + KNOB_HAND + "The knob's pointer turns to the windshield symbol." + END, [YARD], 1),
 'n13_point': (STYLE + CAB + "All windows are now perfectly clear, the snowy courtyard is visible outside, sunny frosty morning. " + CHAR +
               "He sits in the FRONT driver's seat, turns to the viewer with a sly friendly grin and points his right index finger straight "
               "at the viewer; his left hand rests on the steering wheel. " + ARMS + END, [YARD, MIKH], 2),
 'n14_drive': (STYLE + f"{CAR} seen from behind at a three-quarter angle drives out of the snowy courtyard of grey panel apartment blocks "
               "on a sunny frosty morning; all its windows are perfectly clear; a light puff of white exhaust steam; snow sparkles. "
               "Nobody visible." + END, [YARD], 1),
}

CLIPS = {  # ключ кадра: промпт клипа (Wan 3.0 480p, 3 с, без звука)
 'n1_puzzled': "He slowly moves his finger toward the snowflake button, hesitates and squints at it doubtfully; breath steam drifts; static camera.",
 'n2_rain': "Light drizzle falls, rain ripples in the puddles; he grins and shakes his thumbs-up hand cheerfully; static camera.",
 'n3_dryair': "The grumpy rain cloud is sucked into the bottom grille and shrinks; dry white air lines and sparkles flow out of the upper vent; static camera.",
 'n4_drops': "Water drops grow on the frosty fins, slide down and run into the drain tube; static camera.",
 'n5_drip': "Water drops drip from the rubber tube one after another into the little melted hole in the snow, small ripples; static camera.",
 'n6_frostnight': "Snow sparkles under the street lamp, a few snowflakes fall, frosty haze drifts slowly; slow push-in camera.",
 'n7_ecu': "The control unit box pulls the knife switch lever down with a little blue spark; the frosty compressor stays asleep; static camera.",
 'n8_thermo': "The red liquid in the thermometer slowly sinks to the middle tick with the snowflake; frost patterns grow on the glass; static camera.",
 'n9_heatknob': "The hand turns the knob from blue toward red; the hand stays in frame, five fingers; static camera.",
 'n10_glass': "Warm orange air streams blow on the glass; droplets shrink into rising wisps and the clear patch spreads wider; static camera.",
 'n11_modeknob': "The hand turns the knob until the pointer stops at the windshield symbol; the hand stays in frame, five fingers; static camera.",
 'n13_point': "He turns to the viewer, grins and points his finger at the viewer, then winks; his left hand stays on the wheel; static camera.",
 'n14_drive': "The car drives slowly away out of the courtyard, a light puff of exhaust steam, snow sparkles; static camera.",
 'k5_btnfrost': "Frost patterns slowly grow across the side window, the green lamp on the snowflake button keeps glowing, a tiny icicle glints; static camera.",
}
TAIL = " Clean bold outlines, flat cartoon colours, no text."

if __name__ == '__main__':
    reqs, i = [], 0
    for k, (p, refs, n) in F.items():
        for v in range(n):
            reqs.append(dict(index=i, key=f'{k}{"ab"[v] if n > 1 else ""}', params=dict(model='gpt_image_2_5', quality='medium', resolution='2k',
                        aspect_ratio='9:16', use_unlim=False, medias=[dict(role='image_references', value=r) for r in refs], prompt=p)))
            i += 1
    json.dump(reqs, open('kf2_req.json', 'w'), ensure_ascii=False, indent=1)
    json.dump({k: v + TAIL for k, v in CLIPS.items()}, open('clip2_req.json', 'w'), ensure_ascii=False, indent=1)
    print(len(reqs), 'кадров,', len(CLIPS), 'клипов')
