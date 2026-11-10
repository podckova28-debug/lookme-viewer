#!/usr/bin/env python3
# Build per-segment render specs + audio timeline for the Pichushkin documentary.
import json, re, os
ROOT = "/home/user/hw"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "Они жили рядом", "Рецепта нет", "Миф первый", "Миф второй", "Детство", "Оговорка", "Травма", "Фантазии", "Профайлинг", "Триада", "Одиночество", "Спусковой крючок", "Психопаты", "Вменяемы", "Слепая зона", "Мелочь", "Финал"]
SHOTS = {
 1: ["a:portraits:L1,L2,L3,L4:УЧИТЕЛЬ|МИЛИЦИОНЕР|ГРУЗЧИК|ДРУЖИННИК", "a:quotes:n101:2.5,3.05,3.45:Вежливый|Тихий|Никогда бы не подумали@соседи", "n1301@потом"],
 2: ["n201", "a:list:Чего нет|Гена убийцы|Одной причины|Особого лица@ген", "n1001@биографиях"],
 3: ["a:myth:Маньяка видно сразу|Они выглядят как все", "ck100@андрей", "n100@михаил", "mk100@геннадий"],
 4: ["a:myth:Маньяками рождаются|Гены не решают", "n301@учёные", "n901@миллионы"],
 5: ["a:list:Тяжёлое детство|Насилие дома|Унижения|Отвержение", "n401@американского", "n601@агенты"],
 6: ["n101", "a:myth:Травма — это приговор|Лишь один из факторов@травма", "n701@исследователи"],
 7: ["pc100", "pc301@родные", "n501@психиатры"],
 8: ["n601", "a:list:Фантазии|Власть|Контроль|Годы до первого шага@почти"],
 9: ["n601", "n201@этих", "ck100@похожим"],
 10: ["a:list:Триада Макдональда|Поджоги|Жестокость к животным|Ночное недержание", "a:myth:Триада предсказывает убийцу|Почти не работает@позже", "n1301@жестокость#1"],
 11: ["n701", "pc301@были", "pc801@одиночество"],
 12: ["n801", "n100@михаил", "n1301@это"],
 13: ["n901", "a:dots:1:Психопат — примерно 1 из 100@оценкам", "n901@подавляющее"],
 14: ["n1001", "a:stamp:n1001:ВМЕНЯЕМ@экспертизы", "ck100@безумие"],
 15: ["n1101", "mk701@убийств", "pc801@жертв", "n1101@сша"],
 16: ["n1201", "pc1101@записка", "ck1001@фамилия", "mk1101@почерк", "n1201@пробирка", "a:board:pc1101,mk1101,ck1001,n1201@погоня"],
 17: ["n1301", "n101@почти", "a:portraits:L1,L2,L3,L4:УЧИТЕЛЬ|МИЛИЦИОНЕР|ГРУЗЧИК|ДРУЖИННИК@история"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('серийными', 0, 'ВСЕ ЧЕТВЕРО — УБИЙЦЫ', 3.4), ('заранее', 0, 'МОЖНО ЛИ ЗАМЕТИТЬ ЗАРАНЕЕ?', 3.4)],
 2: [('рецепта', 0, 'ЕДИНОГО РЕЦЕПТА НЕТ', 3.2), ('канале', 0, 'РАЗБОР НА НАШИХ ДЕЛАХ', 3.0)],
 3: [('андрей', 0, 'ЧИКАТИЛО · ОТЕЦ ДВОИХ ДЕТЕЙ', 3.4), ('михаил', 0, 'ПОПКОВ · МИЛИЦИОНЕР', 3.2), ('геннадий', 0, 'МИХАСЕВИЧ · ДРУЖИННИК', 3.2)],
 4: [('ген', 0, '«ГЕН УБИЙЦЫ»?', 3.0), ('миллионы', 0, 'МИЛЛИОНЫ НОСИТЕЛЕЙ', 3.0)],
 5: [('детство', 0, 'ТЯЖЁЛОЕ ДЕТСТВО', 3.0), ('американского', 0, 'ЭДМУНД КЕМПЕР', 3.0), ('подвале', 0, 'СПАЛ В ПОДВАЛЕ', 3.0)],
 6: [('большинство', 0, 'БОЛЬШИНСТВО НЕ УБИВАЕТ', 3.4), ('приговор', 0, 'ТРАВМА — НЕ ПРИГОВОР', 3.2)],
 7: [('травм', 0, 'ТРАВМЫ ГОЛОВЫ', 3.0), ('лобных', 0, 'ЛОБНЫЕ ДОЛИ', 3.0), ('импульсы', 0, 'КОНТРОЛЬ ИМПУЛЬСОВ', 3.0)],
 8: [('реслер', 0, 'РЕССЛЕР И ДУГЛАС · ФБР', 3.6), ('36', 0, '36 ИНТЕРВЬЮ', 3.0)],
 9: [('профайлинг', 0, 'ПРОФАЙЛИНГ', 3.0), ('бухановск', 0, 'БУХАНОВСКИЙ · ПОРТРЕТ ЧИКАТИЛО', 3.6)],
 10: [('животным', 1, 'ЖЕСТОКОСТЬ К ЖИВОТНЫМ — СИГНАЛ', 3.6)],
 11: [('изоляция', 0, 'ИЗОЛЯЦИЯ', 2.8), ('шахматы', 0, 'ДЕД И ШАХМАТЫ', 3.0)],
 12: [('спусковой', 0, 'СПУСКОВОЙ КРЮЧОК', 3.0), ('измены', 0, 'ПОПКОВ: «ИЗМЕНА ЖЕНЫ»', 3.4)],
 13: [('большинство', 0, 'БОЛЬШИНСТВО НЕ УБИВАЕТ', 3.2)],
 14: [('вменяемыми', 0, 'ПРИЗНАНЫ ВМЕНЯЕМЫМИ', 3.4), ('выбор', 0, 'ЭТО БЫЛ ВЫБОР', 3.0)],
 15: [('связи', 0, 'НЕТ СВЯЗИ МЕЖДУ ДЕЛАМИ', 3.4), ('1985', 0, '1985 · БАЗА ФБР', 3.6)],
 16: [('мелочь', 0, 'ВЫДАЁТ МЕЛОЧЬ', 3.0), ('записка', 0, 'ЗАПИСКА', 2.4), ('фамилия', 0, 'ФАМИЛИЯ', 2.4), ('письме', 0, 'ПОЧЕРК', 2.4), ('днк', 0, 'ДНК', 2.4)],
 17: [('травм', 0, 'ТРАВМЫ · ОДИНОЧЕСТВО · ФАНТАЗИИ', 3.6), ('молчали', 0, 'ЗАМЕЧАЛИ, НО МОЛЧАЛИ', 3.4)],
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
    for n in range(1, 18):
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
