#!/usr/bin/env python3
# Build per-segment render specs + audio timeline for the Mikhasevich documentary.
import json, re, os
ROOT = "/home/user/mk"
XF = 0.4
CARD = 3.0
LEAD_CARD = 0.15
LEAD_FIRST = 0.5
TAIL = 1.0
TITLE = ["", "Холодное открытие", "Витебщина, 1971", "Кто он", "Почерк", "Невиновные", "Дружинник", "Игнатович", "Красный «Запорожец»", "Письмо", "Почерк", "Совпадение", "Признание", "Суд", "Финал"]
SHOTS = {
 1: ["vm01", "101", "100"],
 2: ["201", "vm02", "401"],
 3: ["100", "vm03", "301"],
 4: ["401", "vm04", "101"],
 5: ["501", "vm05", "1301"],
 6: ["601", "vm06", "100"],
 7: ["701", "vm07", "501"],
 8: ["801", "vm08", "301"],
 9: ["901", "vm09", "100"],
 10: ["1001", "vm10", "801"],
 11: ["1101", "vm11", "100"],
 12: ["1201", "vm12", "701"],
 13: ["1301", "vm13", "501"],
 14: ["1401", "vm14", "1101"],
}
# sticker: (anchor word prefix, occurrence index, text, duration)
STK = {
 1: [('36', 0, '36 ДОКАЗАННЫХ УБИЙСТВ', 3.6), ('14', 1, '14 НЕВИНОВНЫХ ОСУЖДЕНЫ', 3.6), ('расстреляли', 0, 'ОДИН РАССТРЕЛЯН', 3.0), ('самого', 0, 'ОН ИСКАЛ САМОГО СЕБЯ', 3.5)],
 2: [('май', 0, 'МАЙ 1971', 3.2), ('витебская', 0, 'ВИТЕБСКАЯ ОБЛАСТЬ · БССР', 3.8), ('отдельными', 0, '«ОТДЕЛЬНЫЕ ДЕЛА»', 3.2)],
 3: [('47', 0, '1947 · ПОД ПОЛОЦКОМ', 3.5), ('механиком', 0, 'МЕХАНИК', 2.8), ('красный', 0, 'КРАСНЫЙ «ЗАПОРОЖЕЦ»', 3.5)],
 4: [('остановках', 0, 'АВТОБУСНЫЕ ОСТАНОВКИ', 3.2), ('удостоверение', 0, 'УДОСТОВЕРЕНИЕ ДРУЖИННИКА', 3.6)],
 5: [('признаются', 0, 'ПРИЗНАНИЯ ПОД ДАВЛЕНИЕМ', 3.2), ('14', 0, '14 ОСУЖДЁННЫХ', 3.2), ('расстреляют', 0, 'ОДИН РАССТРЕЛЯН', 3.0)],
 6: [('дружину', 0, 'НАРОДНЫЙ ДРУЖИННИК', 3.2), ('рейдах', 0, 'РЕЙДЫ ПО ПОИСКУ УБИЙЦЫ', 3.5), ('засады', 0, 'ЗНАЛ, ГДЕ ЗАСАДЫ', 3.2)],
 7: [('игнат', 0, 'СЛЕДОВАТЕЛЬ НИКОЛАЙ ИГНАТОВИЧ', 4.0), ('один', 1, 'УБИЙЦА ОДИН', 3.0), ('невиновны', 0, 'ОСУЖДЁННЫЕ НЕВИНОВНЫ', 3.4)],
 8: [('красный', 0, 'КРАСНЫЙ «ЗАПОРОЖЕЦ»', 3.4), ('тысячи', 0, 'ТЫСЯЧИ ВЛАДЕЛЬЦЕВ', 3.2)],
 9: [('1985', 0, '1985', 2.8), ('патриот', 0, '«ПАТРИОТЫ ВИТЕБЩИНЫ»', 3.8), ('почерк', 0, 'ГЛАВНАЯ УЛИКА — ПОЧЕРК', 3.5)],
 10: [('сотен', 0, 'СОТНИ ТЫСЯЧ ОБРАЗЦОВ', 3.6), ('вручную', 0, 'ВРУЧНУЮ', 2.6)],
 11: [('декабрь', 0, 'ДЕКАБРЬ 1985', 3.2), ('совпадение', 0, 'СОВПАДЕНИЕ', 3.0), ('задерживают', 0, 'ЗАДЕРЖАН', 2.8)],
 12: [('десятках', 0, 'ДЕСЯТКИ УБИЙСТВ', 3.2), ('расстреляны', 0, 'ЗА НИХ УЖЕ ОСУДИЛИ ДРУГИХ', 3.6)],
 13: [('36', 0, '36 УБИЙСТВ · СМЕРТНЫЙ ПРИГОВОР', 4.0), ('88', 0, '1988 · РАССТРЕЛЯН', 3.4), ('посмертно', 0, 'ОПРАВДАНЫ, НЕКОТОРЫЕ ПОСМЕРТНО', 4.0)],
 14: [('сам', 0, 'ОН ХОДИЛ В ОБЛАВЫ САМ', 3.4), ('14', 1, '14 НЕВИНОВНЫХ', 3.0), ('почерк', 0, 'ЕГО ПОЙМАЛ ПОЧЕРК', 3.5)],
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
    for n in range(1, 15):
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
