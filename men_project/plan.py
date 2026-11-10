#!/usr/bin/env python3
# Build per-segment render specs + audio timeline: «Почему маньяки — мужчины».
import json, re, os
ROOT = "/home/user/mw"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "Искали мужчину", "Цифры", "Миф", "Исследование", "Охотники", "Мотивы", "Способы", "Биология", "Воспитание", "Слепая зона", "Отравительница", "Швейная машинка", "Соцработник", "Выжившая", "Приговор", "Финал"]
P = "a:portraits:L1,L2,L3,L4:УЧИТЕЛЬ|МИЛИЦИОНЕР|ГРУЗЧИК|ДРУЖИННИК"
SHOTS = {
 1: ["w1", "w7@восемь", "w10@убивала", "n901@почему"],
 2: ["a:dots:90:9 из 10 убийц — мужчины", "a:dots:10:Женщин среди маньяков — 5–15%@американским", "n901@меньшинство"],
 3: ["a:myth:Женщины не убивают|Их просто реже замечают", "w2@исследователи", "w4@жертвы"],
 4: ["n1001", "a:list:Мужчины-убийцы|Незнакомцы — в 6 раз чаще|Выслеживали — 65%|У женщин — меньше 4%@мужчины"],
 5: ["w3", "ck1001@чик", "w2@женщина"],
 6: ["pc100", "a:list:Мотив женщин|Наследство|Страховка|Чужие сбережения@чаще", "w4@втором"],
 7: ["w3", "w2@женщины", "w4@многие"],
 8: ["w5", "a:myth:Тестостерон делает убийцей|Прямых доказательств нет@уч", "n901@миллионы"],
 9: ["w6", "a:list:Что работает вместе|Биология|Воспитание|Личная история@большинство"],
 10: ["w7", "n1301@когда"],
 11: ["w8", "w4@врачи", "a:stamp:w8:ТАЛЛИЙ@экспертиза", "w8@его"],
 12: ["w9", "n1001@следствие", "w11@суд"],
 13: ["n101", "w10@ирина", "w1@она"],
 14: ["w7", "w12@изменил"],
 15: ["w11", "a:stamp:w11:20 ЛЕТ@суд", "w11@это", "n101@родственники"],
 16: [P, "w10@но", "ck100@истории"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('восемь', 0, '8 ЛЕТ ИСКАЛИ МУЖЧИНУ', 3.4), ('убивала', 0, 'А УБИВАЛА ЖЕНЩИНА', 3.4)],
 2: [('меньшинство', 0, 'МЕНЬШИНСТВО, НО НЕ ЕДИНИЦЫ', 3.2)],
 3: [('естествен', 0, 'СМЕРТЬ «ЕСТЕСТВЕННАЯ»', 3.2)],
 4: [('сравнили', 0, '55 МУЖЧИН И 55 ЖЕНЩИН', 3.2)],
 5: [('охотники', 0, 'ОХОТНИКИ И СОБИРАТЕЛЬНИЦЫ', 3.4), ('чик', 0, 'ЧИКАТИЛО: ВОКЗАЛЫ И ЭЛЕКТРИЧКИ', 3.4), ('мужей', 0, 'МУЖЬЯ, РОДНЯ, ПАЦИЕНТЫ', 3.2)],
 6: [('власть', 0, 'МУЖЧИНЫ: ВЛАСТЬ', 3.0), ('беспомощ', 0, 'ВЛАСТЬ НАД БЕСПОМОЩНЫМИ', 3.2)],
 7: [('руками', 0, 'МУЖЧИНЫ: РУКАМИ', 2.8), ('яд', 0, 'ЖЕНЩИНЫ: ЯД', 3.0), ('медс', 0, 'МЕДСЁСТРЫ И СИДЕЛКИ', 3.0)],
 8: [('гормон', 0, 'ТЕСТОСТЕРОН', 2.8)],
 9: [('мальчиков', 0, '«СИЛА РЕШАЕТ СПОРЫ»', 3.2)],
 10: [('ищут', 0, 'ИХ ПРОСТО НЕ ИЩУТ', 3.0), ('мужчину', 0, 'ПО ПРИВЫЧКЕ ИЩУТ МУЖЧИНУ', 3.2)],
 11: [('киев', 0, 'КИЕВ · 1987', 3.0), ('тяж', 0, '«ТЯЖЁЛЫЙ ГРИПП»', 2.8), ('посудомойка', 0, 'ТАМАРА ИВАНЮТИНА', 3.2)],
 12: [('швейной', 0, 'ЯД В ШВЕЙНОЙ МАШИНКЕ', 3.2), ('годами', 0, 'ТРАВИЛА ГОДАМИ', 2.8), ('расстрел', 0, 'РАССТРЕЛ', 2.8)],
 13: [('ирина', 0, 'ИРИНА ГАЙДАМАЧУК', 3.0), ('убийств', 0, '17 УБИЙСТВ ЗА 8 ЛЕТ', 3.2)],
 14: [('переодет', 0, '«МУЖЧИНА, ПЕРЕОДЕТЫЙ В ЖЕНЩИНУ»', 3.4), ('выжила', 0, 'ОДНА ВЫЖИЛА', 3.0)],
 15: [('задержали', 0, 'ЗАДЕРЖАНА · 2010', 3.0), ('максимум', 0, 'МАКСИМУМ ДЛЯ ЖЕНЩИНЫ', 3.2), ('мягким', 0, '«СЛИШКОМ МЯГКО»', 2.8)],
 16: [('тоже', 0, 'ОНИ ТИШЕ — ИХ ДОЛЬШЕ НЕ ЗАМЕЧАЮТ', 3.6), ('истории', 0, 'ВСЕ ДЕЛА — НА КАНАЛЕ', 3.0)],
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
