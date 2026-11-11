#!/usr/bin/env python3
# Build per-segment render specs + audio timeline: «Почему маньяки — мужчины».
import json, re, os
ROOT = "/home/user/cw"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "", "Образцовый пациент", "На свободе", "Не диагноз", "Неизлечимы?", "Оук-Ридж", "Новые инструменты", "Мендота", "Чем раньше", "Химическая кастрация", "Цифры", "Принудительное лечение", "С 1999 года", "Главный страх", "Что работает", "Вердикт"]
SHOTS = {
 1: ["k1", "k21@эдмунд", "a:stamp:k21:«НЕ ОПАСЕН»@нет", "k25@детское", "k6@этот", "k18@вообще"],
 2: ["k2", "k3@отправили", "k26@образцовым", "k4@помогал", "k29@какие", "a:stamp:k26:IQ ОКОЛО 140@коэфф"],
 3: ["k5", "k27@именно", "k6@через", "k7@после", "k23@сдался"],
 4: ["k8", "a:stamp:k8:«МАНЬЯК» — НЕ ДИАГНОЗ@маньяк", "k28@большинство", "a:list:Что приходится лечить|Жестокость|Навязчивые фантазии|Отсутствие сочувствия@лечить"],
 5: ["k29", "k24@одно"],
 6: ["k30", "k9@радикальную", "k31@пациенты", "k38@позже", "a:list:Итог программы|Обычные пациенты — реже|Психопаты — чаще@обычные"],
 7: ["k10", "k32@но", "a:stamp:k32:НОВЫЕ ИНСТРУМЕНТЫ@терапия", "k24@после"],
 8: ["k33", "k11@подход", "k34@терпеливо", "a:list:Центр Мендота|Не наказывать за срыв|Поощрять за успехи|Насилие — заметно реже@подростки"],
 9: ["k20", "k35@черты", "a:stamp:k35:НЕТ ЧУВСТВА ВИНЫ@не", "k12@тепло", "k36@работа"],
 10: ["k13", "a:stamp:k13:ХИМИЧЕСКАЯ КАСТРАЦИЯ@это", "k14@россии", "k37@для", "k22@но"],
 11: ["k38", "a:list:Обзор Лёзеля и Шмукера|Больше 20 000 осуждённых|Рецидивов — на треть меньше@охватил", "a:myth:Минус треть рецидивов|В строгих исследованиях — несколько процентов@когда"],
 12: ["k16", "k15@новокузнецк", "k39@лежал"],
 13: ["k17", "a:stamp:k17:С 1999 ГОДА@1999", "k28@недавно", "k41@выйти"],
 14: ["k1", "k18@маньяки", "k26@кемпер", "k16@списив", "a:stamp:k6:ЦЕНА ОШИБКИ — ЖИЗНИ@ошибка"],
 15: ["k22", "a:list:Управление риском|Долгий надзор|Лекарства|Терапия: контроль импульсов|Строгий контроль после выхода@долгий", "k42@после", "k19@чтобы#1"],
 16: ["a:myth:Маньяка можно вылечить|Почти никогда — но риск можно снизить", "k12@риск", "k26@история", "a:stamp:k21:ЛУЧШЕ ВСЕХ ПРОХОДИТ ТЕСТЫ@тот"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('осень', 0, 'КАЛИФОРНИЯ · 1972', 3.0), ('эдмунд', 0, 'ЭДМУНД КЕМПЕР', 3.0), ('убил', 0, 'УЖЕ УБИЛ ТРЁХ ДЕВУШЕК', 2.6)],
 2: [('15', 0, '15 ЛЕТ', 2.6), ('бабушку', 0, 'УБИЛ БАБУШКУ И ДЕДУШКУ', 3.0), ('аскадеру', 0, 'БОЛЬНИЦА АТАСКАДЕРО', 3.2), ('ответы', 0, 'ЗНАЛ, ЧТО ХОТЯТ УСЛЫШАТЬ', 3.2)],
 3: [('21', 0, 'ВЫПУСТИЛИ В 21 ГОД', 3.0), ('против', 0, 'ВРАЧИ БЫЛИ ПРОТИВ', 3.0), ('6', 0, 'ШЕСТЬ ДЕВУШЕК', 2.8), ('сам', 0, 'САМ СДАЛСЯ ПОЛИЦИИ', 3.0)],
 4: [('суд', 0, 'СУД: ВМЕНЯЕМ', 2.6)],
 5: [('психопатии', 0, 'ПСИХОПАТИЯ', 2.6), ('невозможно', 0, '«НЕИЗЛЕЧИМО»', 2.6)],
 6: [('канад', 0, 'КАНАДА · ОУК-РИДЖ · 1960–70-е', 3.4), ('сами', 0, 'ОТДЕЛЕНИЕМ УПРАВЛЯЛИ ПАЦИЕНТЫ', 3.4)],
 7: [('понимать', 0, 'УЧИЛИСЬ ЧИТАТЬ ЧУВСТВА', 3.0), ('управлять', 0, '…ЧТОБЫ УПРАВЛЯТЬ', 2.6), ('неизлечим', 0, '«НЕИЗЛЕЧИМО»', 2.6)],
 8: [('висконсин', 0, 'ЦЕНТР МЕНДОТА · ВИСКОНСИН', 3.4), ('месяцами', 0, 'МЕСЯЦАМИ ПООЩРЯТЬ', 3.0)],
 9: [('раньше', 0, 'ЧЕМ РАНЬШЕ — ТЕМ ЛУЧШЕ', 3.2), ('безсерд', 0, 'ЧЕРТЫ БЕССЕРДЕЧИЯ', 3.0), ('ребенком', 0, 'РЕБЁНОК + СЕМЬЯ', 3.0)],
 10: [('тестостерон', 0, 'СНИЖАЮТ ТЕСТОСТЕРОН', 2.8), ('2012', 0, 'РОССИЯ · 2012', 3.0), ('практике', 0, 'ПОЧТИ НЕ ПРИМЕНЯЕТСЯ', 3.0)],
 11: [('лёзел', 0, 'ЛЁЗЕЛЬ И ШМУКЕР', 3.0)],
 12: [('принуд', 0, 'ПРИНУДИТЕЛЬНОЕ ЛЕЧЕНИЕ', 3.0), ('списив', 0, 'АЛЕКСАНДР СПЕСИВЦЕВ', 3.2), ('лучше', 0, '«ЕМУ СТАЛО ЛУЧШЕ»', 3.0)],
 13: [('15', 0, '+15 УБИЙСТВ', 3.0), ('опасен', 0, '«БОЛЬШЕ НЕ ОПАСЕН»?', 3.0)],
 14: [('риск', 0, 'ОЦЕНКА РИСКА', 2.6), ('обманул', 0, 'ОБМАНУЛ ПСИХИАТРОВ', 2.6), ('отпускали', 0, 'ОТПУСКАЛИ ИЗ БОЛЬНИЦЫ', 2.6)],
 15: [('управление', 0, 'НЕ ЛЕЧЕНИЕ — УПРАВЛЕНИЕ РИСКОМ', 3.6), ('никого', 0, 'ЧТОБЫ БОЛЬШЕ НИКОГО НЕ УБИЛ', 3.0)],
 16: [('детстве', 0, 'ДО ПЕРВОГО ПРЕСТУПЛЕНИЯ', 3.0)],
}

def load_words():
    out = {}
    for line in open(f"{ROOT}/vo/wts.log"):
        if not line.startswith("v"): continue
        parts = line.split()
        n = int(parts[0][1:]); ws = []
        for p in parts[1:]:
            w, t = p.rsplit("@", 1)
            ws.append((re.sub(r"[^а-яё0-9]", "", w.lower()), float(t)))
        out[n] = ws
    return out

def main():
    durs = {int(l.split()[0][1:3]): float(l.split()[1]) for l in open(f"{ROOT}/vo/dur.txt")}
    # refresh durations (re-recorded files)
    import subprocess
    for n in durs:
        durs[n] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        f"{ROOT}/vo/v{n:02d}.mp3"], capture_output=True, text=True).stdout)
    words = load_words()
    segs = []; t_glob = 0.0; vo_place = []
    os.makedirs(f"{ROOT}/spec", exist_ok=True)
    for n in range(1, 17):
        card = n > 1
        vo_start = (CARD + LEAD_CARD) if card else LEAD_FIRST
        total = vo_start + durs[n] + TAIL
        shots = []
        if card: shots.append({"kind": "chapter", "num": n, "title": TITLE[n], "dur": CARD + XF})
        items = SHOTS[n]
        ws = words.get(n, [])
        # shot boundaries: "ID@word" / "ID@word#k" starts the shot just before that spoken word (k-th occurrence)
        t_first = (CARD + XF - XF) if card else 0.0
        m = len(items); B = [None] * m + [total]; B[0] = t_first; ids = []
        for i, it in enumerate(items):
            sid, _, anc = it.partition("@"); ids.append(sid)
            if anc and i > 0:
                w, _, occ = anc.partition("#")
                hits = [t for x, t in ws if x.startswith(w)]
                o = int(occ or 0)
                if len(hits) > o: B[i] = round(vo_start + hits[o] - 0.3, 3)
                else: print("WARN no shot anchor", n, anc)
        known = [i for i in range(m + 1) if B[i] is not None]
        for a, b in zip(known, known[1:]):
            for i in range(a + 1, b): B[i] = B[a] + (B[b] - B[a]) * (i - a) / (b - a)
        for i in range(m):
            if B[i + 1] - B[i] < 1.5: print("WARN short shot", n, items[i], round(B[i + 1] - B[i], 2))
        for i, sid in enumerate(ids):
            d = round(B[i + 1] - B[i] + (XF if i < m - 1 else 0), 3)
            if sid.startswith("a:"): shots.append({"kind": "anim", "spec": sid[2:], "dur": d})
            else: shots.append({"kind": "img", "id": sid, "dur": d})
        stk = []
        for anchor, occ, text, d in STK.get(n, []):
            hits = [t for w, t in ws if w.startswith(anchor)]
            if len(hits) > occ:
                stk.append({"text": text, "t": round(vo_start + hits[occ] - 0.1, 2), "dur": d})
            else:
                print("WARN no anchor", n, anchor)
        spec = {"total": round(total, 3), "shots": shots, "stickers": stk, "mode_seed": n}
        json.dump(spec, open(f"{ROOT}/spec/ch{n:02d}.json", "w"), ensure_ascii=False, indent=1)
        segs.append((f"ch{n:02d}", total)); vo_place.append((n, t_glob + vo_start))
        t_glob += total
        if n == 1:
            json.dump({"total": 4.6, "shots": [{"kind": "title", "dur": 4.6}]}, open(f"{ROOT}/spec/t00.json", "w"))
            segs.append(("t00", 4.6)); t_glob += 4.6
    json.dump({"total": 4.5, "shots": [{"kind": "end", "dur": 4.5}]}, open(f"{ROOT}/spec/e99.json", "w"))
    segs.append(("e99", 4.5)); t_glob += 4.5
    json.dump({"segs": segs, "vo": vo_place, "total": t_glob}, open(f"{ROOT}/spec/timeline.json", "w"), indent=1)
    print("TOTAL", round(t_glob, 2), "sec =", f"{int(t_glob // 60)}:{int(t_glob % 60):02d}")
    for s, d in segs: print(s, round(d, 2))

main()
