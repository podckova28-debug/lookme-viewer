#!/usr/bin/env python3
# Build per-segment render specs + audio timeline for the Popkov documentary.
import json, re, os
ROOT = "/home/user/pk"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "Холодное открытие", "Город", "Кто он", "Почерк", "Страх", "Выжившая", "Свой", "Уход",
         "Следствие буксует", "Тишина", "Пробирка", "Задержание", "Признание", "Суды", "Итог", "Финал"]
SHOTS = {
 1: ["v101", "102", "103"],
 2: ["v201", "202", "203"],
 3: ["301", "302", "303", "304"],
 4: ["v401", "402", "403"],
 5: ["501", "502", "503"],
 6: ["601", "602", "604", "603"],
 7: ["701", "702"],
 8: ["801", "802", "803"],
 9: ["901", "902", "903"],
 10: ["1001", "1002", "1003"],
 11: ["v1101", "1102", "1103"],
 12: ["v1201", "1202", "1203"],
 13: ["1301", "1302"],
 14: ["1401", "1402", "1403", "902"],
 15: ["1501", "1502"],
 16: ["v1601", "1602", "v101"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [("91", 0, "91 ЖЕРТВА", 3.6), ("14", 0, "14 ЛЕТ ПОИСКОВ", 3.2), ("михаил", 0, "МИХАИЛ ПОПКОВ", 3.5)],
 2: [("ангарск", 0, "АНГАРСК · ИРКУТСКАЯ ОБЛАСТЬ", 4.0), ("90", 0, "1990-е", 3.0)],
 3: [("7", 0, "7 МАРТА 1964 · НОРИЛЬСК", 4.5), ("миша", 0, "«МИША-УЛЫБКА»", 3.5), ("нива", 0, "«НИВА»", 2.6)],
 4: [("кто", 0, "КТО ОТКАЖЕТ МИЛИЦИОНЕРУ?", 3.2)],
 5: [("декабре", 0, "ДЕКАБРЬ 1998", 3.5), ("неизвестным", 0, "24 ЖЕРТВЫ", 3.0)],
 6: [("28", 0, "28 ЯНВАРЯ 1998", 4.0), ("жива", 0, "ВЫЖИЛА", 2.6)],
 7: [("убийца", 0, "УБИЙЦА БЫЛ СВОИМ", 3.5)],
 8: [("98", 0, "1998 · УВОЛЬНЕНИЕ", 3.5)],
 9: [("2000", 0, "2000 · НОВАЯ ГРУППА", 3.5), ("15", 0, "15 ДЕЛ — НЕКАЧЕСТВЕННО", 3.5), ("марте", 0, "МАРТ 2001", 3.0), ("улик", 0, "УЛИК НЕТ", 2.6)],
 10: [("2011", 0, "ДО 2011 ГОДА", 3.2), ("иркутск", 0, "ИРКУТСК · УСОЛЬЕ-СИБИРСКОЕ", 3.5)],
 11: [("2012", 0, "2012", 3.0), ("образцами", 0, "ТЫСЯЧИ ОБРАЗЦОВ ДНК", 3.5), ("совпадение", 0, "СОВПАДЕНИЕ", 3.0)],
 12: [("23", 0, "23 ИЮНЯ 2012 · ВЛАДИВОСТОК", 4.5)],
 13: [("каждой", 0, "У КАЖДОЙ БЫЛО ИМЯ", 4.0)],
 14: [("22", 0, "22 УБИЙСТВА", 3.0), ("195", 0, "195 ТОМОВ · 300+ ЭКСПЕРТИЗ", 4.0), ("14", 0, "14.01.2015 — ПОЖИЗНЕННОЕ", 4.0),
      ("59", 0, "ЕЩЁ 59 УБИЙСТВ", 3.0), ("10", 0, "10.12.2018 — ВТОРОЕ ПОЖИЗНЕННОЕ", 4.0)],
 15: [("шести", 0, "6 ПРИГОВОРОВ · 91 ЖЕРТВА", 4.0), ("выжили", 0, "ВЫЖИЛИ ТРОЕ", 3.0)],
 16: [("апреле", 0, "АПРЕЛЬ 2026 · МОРДОВИЯ", 4.0), ("миша", 0, "«МИША-УЛЫБКА»", 3.5)],
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
        vid_d = sum(10.0 for s in items if s.startswith("v"))
        n_img = sum(1 for s in items if not s.startswith("v"))
        used = sum(s["dur"] for s in shots)
        k = len(shots) + len(items)
        remain = total - used + (k - 1) * XF - vid_d
        img_d = remain / max(1, n_img)
        for s in items:
            if s.startswith("v"): shots.append({"kind": "vid", "id": s[1:], "dur": 10.0})
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
