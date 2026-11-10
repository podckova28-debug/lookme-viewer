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
 1: ["a:lineup:ck100,n100,pc100,mk100:УЧИТЕЛЬ|МИЛИЦИОНЕР|ГРУЗЧИК|ДРУЖИННИК", "n101", "a:headline:Никто бы не подумал"],
 2: ["n201", "a:list:Чего нет|Гена убийцы|Одной причины|Особого лица", "n201"],
 3: ["a:myth:Маньяка видно сразу|Они выглядят как все", "ck100", "n100"],
 4: ["a:myth:Маньяками рождаются|Гены не решают", "n301", "n201"],
 5: ["n401", "a:list:Тяжёлое детство|Насилие дома|Унижения|Отвержение", "n701"],
 6: ["n101", "a:myth:Травма — это приговор|Лишь один из факторов", "n701"],
 7: ["pc100", "n501", "pc301"],
 8: ["n601", "a:list:Фантазии|Власть|Контроль|Годы до первого шага", "n701"],
 9: ["n601", "n201", "ck100"],
 10: ["a:list:Триада Макдональда|Поджоги|Жестокость к животным|Ночное недержание", "n401", "a:myth:Триада предсказывает убийцу|Почти не работает"],
 11: ["n701", "pc301", "pc801"],
 12: ["n801", "n100", "n801"],
 13: ["n901", "a:dots:1:Психопат — примерно 1 из 100", "n901"],
 14: ["n1001", "a:stamp:n1001:ВМЕНЯЕМ", "ck100"],
 15: ["n1101", "mk701", "a:map:0:14"],
 16: ["a:board:pc1101,mk1101,ck1001,n1201", "n1201", "pc1101"],
 17: ["n1301", "a:lineup:ck100,n100,pc100,mk100:УЧИТЕЛЬ|МИЛИЦИОНЕР|ГРУЗЧИК|ДРУЖИННИК", "n101"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
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
