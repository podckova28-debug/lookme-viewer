#!/usr/bin/env python3
# Build per-segment render specs + audio timeline: «Почему маньяки — мужчины».
import json, re, os
ROOT = "/home/user/lw"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
# chapter cards only at the 5 big sections; other chapters flow on without a card
ACTS = {2: (1, "Невесты маньяков"), 5: (2, "Что это такое"), 7: (3, "Почему они пишут"), 13: (4, "Чем это кончается"), 15: (5, "Вердикт")}
TAIL_FLOW = 0.5
SHOTS = {
 1: ["j1", "j2@он", "j3@кэрол", "a:stamp:j5:МУЖ И ЖЕНА@закону", "j4@зале", "j44@почему"],
 2: ["j7", "j6@женщины", "j17@просили", "j9@родила", "j8@хотя", "a:stamp:j7:КАЗНЁН В 1989@банд#1"],
 3: ["j10", "j11@почти", "a:stamp:j11:75 ПИСЕМ@годы", "j12@88", "j13@октябре"],
 4: ["j16", "j14@том", "j15@позже", "j27@словам", "a:stamp:j16:«В НЕГО ВЛЮБЛЯЮТСЯ ВСЕ»@сам"],
 5: ["a:stamp:j18:ГИБРИСТОФИЛИЯ", "j19@термин", "j35@так", "j20@но"],
 6: ["a:myth:Им нравятся убийства|Чаще дело совсем не в преступлении", "j21@писательница", "j22@криминальный",
     "a:list:Почему они пишут|Желание спасти|Безопасная любовь|Прошлое|Внимание|Вера в невиновность@причины"],
 7: ["j23", "j24@рамслинд", "a:stamp:j24:«Я ЕГО ИЗМЕНЮ»@другие", "j25@изменить"],
 8: ["j26", "a:stamp:j26:БЕЗОПАСНАЯ ЛЮБОВЬ@это", "j27@мужчина", "j45@как", "j15@он"],
 9: ["j28", "a:stamp:j28:ТЯЖЁЛАЯ ТРАВМА@большинства", "j14@наталья", "j29@знакомая"],
 10: ["j30", "j31@невеста", "j23@для"],
 11: ["j33", "j32@психологи", "a:stamp:j32:«ЕГО ОКЛЕВЕТАЛИ»@она"],
 12: ["j34", "a:stamp:j34:128 СТУДЕНТОК@128", "j35@холодного", "a:stamp:j35:БОЛЕЕ ПРИВЛЕКАТЕЛЕН@девушки",
      "a:myth:Женщин тянет к «плохим парням»|Поздние исследования подтвердили это не до конца@но"],
 13: ["j36", "a:stamp:j36:МУЖЧИНЫ ИМИ МАНИПУЛИРОВАЛИ@айзенберг", "j39@иногда", "j37@сотрудница", "j38@передала"],
 14: ["j13", "j40@кэрол", "j12@дорин", "j41@анализ", "j43@26", "j42@их"],
 15: ["j25", "a:list:Почему они пишут|Одиночество|Старая травма|Желание спасти|Любовь на расстоянии@чаще", "j45@настоящее"],
 16: ["j46"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('флорида', 0, 'ФЛОРИДА · 1980', 2.6), ('банди', 0, 'ТЕД БАНДИ', 2.6), ('кэрол', 0, 'КЭРОЛ ЭНН БУН', 3.0), ('женщины', 0, 'ПРИШЛИ ПОСМОТРЕТЬ НА НЕГО', 3.0)],
 2: [('писали', 0, 'ЕМУ ПИСАЛИ ЖЕНЩИНЫ', 3.0), ('родила', 0, '1982 · ДОЧЬ', 3.0), ('супружеских', 0, 'СВИДАНИЙ НЕ БЫЛО', 2.8)],
 3: [('лос', 0, 'ЛОС-АНДЖЕЛЕС · 1985', 3.0), ('ромирес', 0, 'РИЧАРД РАМИРЕС', 3.0), ('дорр', 0, 'ДОРИН ЛИОЙ', 3.0), ('поженятся', 0, 'СВАДЬБА В ТЮРЬМЕ · 1996', 3.0)],
 4: [('битцевский', 0, 'АЛЕКСАНДР ПИЧУШКИН', 3.0), ('2007', 0, 'ПОЖИЗНЕННЫЙ СРОК · 2007', 3.0), ('наталья', 0, 'НАТАЛЬЯ ИЗ НЯГАНИ', 3.0),
     ('фамилию', 0, 'ВЗЯЛА ЕГО ФАМИЛИЮ', 2.6), ('правозащитницы', 0, 'ПРАВОЗАЩИТНИЦА ЕВА МЕРКАЧЁВА', 3.0)],
 5: [('джон', 0, 'ДЖОН МАНИ · 1986', 3.0), ('диагноза', 0, 'НЕ ДИАГНОЗ', 2.6)],
 6: [('айзенберг', 0, 'ШЕЙЛА АЙЗЕНБЕРГ', 3.0), ('рамсленд', 0, 'КЭТРИН РАМСЛЕНД', 3.0)],
 7: [('спасти', 0, 'ЖЕЛАНИЕ СПАСТИ', 3.0), ('чудовище', 0, '«ВСЕ ВИДЯТ ЧУДОВИЩЕ»', 3.0), ('маленького', 0, 'МАЛЕНЬКИЙ МАЛЬЧИК', 3.0)],
 8: [('пьяным', 0, 'НЕ ПРИДЁТ ПЬЯНЫМ', 2.6), ('стирать', 0, 'НИ СТИРКИ, НИ ГОТОВКИ', 3.0)],
 9: [('прошлое', 0, 'ПРОШЛОЕ', 2.4), ('бил', 0, 'МУЖ БИЛ И ИЗМЕНЯЛ', 3.0)],
 10: [('внимание', 0, 'ВНИМАНИЕ', 2.4), ('камеры', 0, 'ИНТЕРВЬЮ И КАМЕРЫ', 2.8)],
 11: [('невиновность', 0, 'ВЕРА В НЕВИНОВНОСТЬ', 3.0), ('защитной', 0, '«ЗАЩИТНАЯ ИСТОРИЯ»', 3.0)],
 12: [('2014', 0, 'ВЕЛИКОБРИТАНИЯ · 2014', 3.0), ('холодного', 0, 'ХОЛОДНЫЙ, САМОВЛЮБЛЁННЫЙ, РАСЧЁТЛИВЫЙ', 3.6)],
 13: [('деньги', 0, 'ДЕНЬГИ · ПОСЫЛКИ · АДВОКАТЫ', 3.4), ('2015', 0, 'НЬЮ-ЙОРК · 2015', 3.0), ('джой', 0, 'ДЖОЙС МИТЧЕЛЛ', 3.0)],
 14: [('развелась', 0, 'РАЗВЕЛАСЬ · 1986', 3.0), ('дорин', 0, 'ДОРИН ЛИОЙ', 2.6), ('менсона', 0, 'НЕВЕСТА МЭНСОНА · 26 ЛЕТ', 3.0), ('истекло', 0, 'РАЗРЕШЕНИЕ НА БРАК ИСТЕКЛО', 3.0)],
 15: [('реже', 0, 'ГОРАЗДО РЕЖЕ, ЧЕМ КАЖЕТСЯ', 3.0)],
 16: [('письмо', 0, 'ПИСЬМО РАССКАЗЫВАЕТ О ТОЙ, КТО ЕГО ПИШЕТ', 4.0)],
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
        card = n in ACTS
        vo_start = (CARD + LEAD_CARD) if card else LEAD_FIRST
        total = vo_start + durs[n] + (TAIL if (n + 1 in ACTS or n == 16) else TAIL_FLOW)
        shots = []
        if card: shots.append({"kind": "chapter", "num": ACTS[n][0], "title": ACTS[n][1], "dur": CARD + XF})
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
