#!/usr/bin/env python3
# Build per-segment render specs + audio timeline for the Pichushkin documentary.
import json, re, os
ROOT = "/home/user/pc"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "Холодное открытие", "Битцевский парк", "Кто он", "1992", "Возвращение", "Колодцы", "Выжившие", "Доска", "Охота", "Ошибка", "Записка", "Метро", "Арест", "Признание", "Приговор", "Финал"]
SHOTS = {
 1: ["a:chess:0:61", "100", "801"],
 2: ["101", "a:map:0:0", "102"],
 3: ["301", "a:timeline:1974", "201"],
 4: ["a:timeline:1992", "401", "100"],
 5: ["a:timeline:2001", "501", "201"],
 6: ["a:map:0:14", "601", "101"],
 7: ["101", "701", "100"],
 8: ["801", "a:chess:20:48", "100"],
 9: ["901", "a:headline:Битцевский маньяк: новая жертва", "101"],
 10: ["1001", "a:timeline:2006", "100"],
 11: ["1101", "a:note", "1101"],
 12: ["a:ticket", "a:cctv:1201:14:21:07", "a:board:100,1101,1201,1001"],
 13: ["a:stamp:1301:ЗАДЕРЖАН", "a:chess:55:61", "801"],
 14: ["100", "a:map:14:40", "801"],
 15: ["1401", "a:count:48:УБИЙСТВ ДОКАЗАНО", "1401"],
 16: ["a:chess:61:61", "1501", "100"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('64', 0, '64 КЛЕТКИ', 3.0), ('отпечатки', 0, 'НИ ОТПЕЧАТКОВ · НИ СВИДЕТЕЛЕЙ', 3.6), ('листок', 0, 'ЛИСТОК БУМАГИ', 3.2)],
 2: [('юг', 0, 'МОСКВА · БИТЦЕВСКИЙ ПАРК', 4.0), ('20', 0, '20+ КВ. КМ ЛЕСА', 3.2)],
 3: [('74', 0, '1974 · МЫТИЩИ', 3.5), ('дед', 0, 'ДЕД НАУЧИЛ ИГРАТЬ В ШАХМАТЫ', 3.8)],
 4: [('однокласснику', 0, 'ПЕРВАЯ ЖЕРТВА — ОДНОКЛАССНИК', 4.0), ('несчастный', 0, '«НЕСЧАСТНЫЙ СЛУЧАЙ»', 3.4), ('9', 1, '9 ЛЕТ ТИШИНЫ', 3.0)],
 5: [('могиле', 0, '«ВЫПИТЬ НА МОГИЛЕ СОБАКИ»', 3.8), ('один', 1, 'ВОЗВРАЩАЛСЯ ОДИН', 3.0)],
 6: [('колодцах', 0, 'КАНАЛИЗАЦИОННЫЕ КОЛОДЦЫ', 3.5), ('никто', 0, 'ИХ НИКТО НЕ ИСКАЛ', 3.2)],
 7: [('выживают', 0, 'ВЫЖИВШИЕ', 2.8), ('нескольких', 0, 'ИСКАЛИ НЕСКОЛЬКИХ', 3.2), ('грузчик', 0, 'ГРУЗЧИК В СУПЕРМАРКЕТЕ', 3.4)],
 8: [('64', 0, 'ЦЕЛЬ: 64 КЛЕТКИ', 3.4), ('рекорд', 1, 'РЕКОРД ЧИКАТИЛО', 3.4)],
 9: [('кинологи', 0, 'ПАТРУЛИ · КИНОЛОГИ', 3.4), ('выдало', 0, 'ЧТО ЕГО ВЫДАЛО?', 3.6), ('комментариях', 0, 'ПИШИТЕ В КОММЕНТАРИЯХ', 3.4)],
 10: [('июнь', 0, 'ИЮНЬ 2006', 3.0), ('москалев', 0, 'МАРИНА МОСКАЛЁВА', 3.4), ('ошибка', 0, 'ЕГО ОШИБКА', 2.8)],
 11: [('записку', 0, 'ЗАПИСКА ДЛЯ СЫНА', 3.2), ('телефона', 0, 'ИМЯ И ТЕЛЕФОН', 3.0)],
 12: [('метро', 0, 'ПРОЕЗДНОЙ', 2.8), ('камеры', 0, 'КАМЕРЫ МЕТРО', 3.0)],
 13: [('16', 0, '16 ИЮНЯ 2006', 3.4)],
 14: [('60', 0, '«БОЛЬШЕ 60»', 3.0), ('счет', 0, 'ЕГО ВОЛНОВАЛ ТОЛЬКО СЧЁТ', 3.4)],
 15: [('2007', 0, '2007 · ПРИСЯЖНЫЕ', 3.2), ('пожизненному', 0, 'ПОЖИЗНЕННОЕ', 3.0)],
 16: [('хода', 0, 'ОДИН ХОД', 2.8), ('записку', 0, 'ЗАПИСКА', 2.8)],
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
        vid_d = sum(5.0 for s in items if s.startswith("v"))
        n_img = sum(1 for s in items if not s.startswith("v"))
        used = sum(s["dur"] for s in shots)
        k = len(shots) + len(items)
        remain = total - used + (k - 1) * XF - vid_d
        img_d = remain / max(1, n_img)
        for s in items:
            if s.startswith("v"): shots.append({"kind": "vid", "id": s[1:], "dur": 5.0})
            elif s.startswith("a:"): shots.append({"kind": "anim", "spec": s[2:], "dur": round(img_d, 3)})
            else: shots.append({"kind": "img", "id": s, "dur": round(img_d, 3)})
        stk = []
        ws = words.get(n, [])
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
