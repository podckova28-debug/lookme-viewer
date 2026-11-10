#!/usr/bin/env python3
"""TTS QA: automatic check of generated narration against the script.

Catches:
  * ACCENT    - stretches where the voice stops sounding Russian (language-ID per word window)
  * GARBLED   - words the recogniser hears as something else (mispronounced / mangled words)
  * MISSING   - script words that are not spoken
  * EXTRA     - spoken words that are not in the script (inserted / hallucinated phrases)
  * REPEAT    - phrase spoken twice although the script says it once
  * LOWCONF   - words recognised with very low confidence (mumbled)
  * PAUSE     - long silence inside the line (glitch / lost words)
  * CLIP      - clipping / distortion
  * DURATION  - line longer/shorter than the allowed window (optional)

Usage:
  python3 tts_qa.py check manifest.json [--out report.json] [--max-dur 9.5] [--min-dur 7.2]
      manifest = [{"id": "v01", "audio": "vo/v01.mp3", "text": "script text ..."}, ...]
      (text may contain <#0.3#> pause tags and U+0301 stress marks - they are stripped)
  python3 tts_qa.py pick --text "script text" cand1.mp3 cand2.mp3 ...
      checks every candidate take of one line and prints the best one (lowest penalty)

Exit code: 0 = all PASS, 1 = at least one FAIL.
Runs where faster-whisper is installed (Higgsfield sandbox has it preinstalled).
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile

import numpy as np

SR = 16000
SLAVIC = {"ru", "uk", "be", "bg", "pl", "sr", "hr", "mk", "sl", "cs", "sk", "bs"}
# words whose short windows are often mislabelled as English even when spoken fine
FALSE_FRIENDS = {"сам", "сама", "само", "сами", "самых", "самого", "самой", "самим", "самом", "самый", "сума"}

# --------------------------------------------------------------------------- text

def clean_script(t):
    t = re.sub(r"<#[\d.]+#>", " ", t)
    t = t.replace("\u0301", "")
    return t

def norm_word(w):
    w = w.lower().replace("ё", "е")
    return re.sub(r"[^a-zа-я0-9]", "", w)

_E = r"(ь|и|ью|ый|ого|ом|ому|ая|ой|ую|ые|ых|ым|ыми)"
NUM_RE = re.compile(
    r"^(ноль|нол[яюе]|нул\w*|од(ин|на|но|ного|ной|ном|ному|ну|ним)|перв\w*|дв(а|е|ух|ум|умя)|втор\w*|тр(и|ех|ем|емя)|трет\w*"
    r"|четыр(е|ех|ем|ьмя)|четверт\w*|пят" + _E + r"|шест" + _E + r"|сем(ь|и|ью)|седьм\w*|восем(ь|и|ью)|восьм\w*"
    r"|девят" + _E + r"|десят" + _E + r"|\w+надцат\w*|двадцат\w*|тридцат\w*|сорок\w*|пятьдесят\w*|пятидесят\w*"
    r"|шестьдесят\w*|шестидесят\w*|семьдесят\w*|семидесят\w*|восемьдесят\w*|восьмидесят\w*|девяност\w*"
    r"|сто|ста|сотый|сотого|сотом|двест\w*|двухсот\w*|трист\w*|трехсот\w*|четырест\w*|четырехсот\w*"
    r"|(пять|шесть|семь|восемь|девять|пяти|шести|семи|восьми|девяти)сот\w*|тысяч\w*|миллион\w*)$")

def is_num_word(w):
    return bool(NUM_RE.match(w))

def tokens_script(text):
    out = []
    for w in clean_script(text).split():
        n = norm_word(w)
        if not n:
            continue
        out.append(n)
    # collapse runs of number words into one <NUM> token
    res = []
    for w in out:
        if is_num_word(w) or w.isdigit():
            if res and res[-1] == "<num>":
                continue
            res.append("<num>")
        else:
            res.append(w)
    return res

def tokens_heard(words):
    """words: list of dicts {w, s, e, p}; returns tokens with index map back to words."""
    toks, idx = [], []
    for i, wd in enumerate(words):
        n = norm_word(wd["w"])
        if not n:
            continue
        if re.search(r"\d", n) or is_num_word(n):
            # '85', '1985', '47м', '85й' -> <num>; suffix tokens like 'й', 'м' after digits are dropped
            if toks and toks[-1] == "<num>":
                idx[-1].append(i)
                continue
            toks.append("<num>"); idx.append([i])
        elif toks and toks[-1] == "<num>" and n in {"й", "м", "го", "х", "е", "я", "ю", "ми", "му", "ом", "ый", "ой"}:
            idx[-1].append(i)
        else:
            toks.append(n); idx.append([i])
    return toks, idx

# --------------------------------------------------------------------------- audio

def load_audio(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768.0

def audio_checks(a, max_gap=1.4):
    issues = []
    dur = len(a) / SR
    peak = float(np.max(np.abs(a))) if len(a) else 0
    clip = int(np.sum(np.abs(a) > 0.995))
    if clip > 30:
        issues.append({"type": "CLIP", "t": None, "detail": f"{clip} clipped samples (peak {peak:.3f})", "sev": 2})
    # silence gaps inside speech (20 ms frames)
    fr = 320
    n = len(a) // fr
    if n:
        rms = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
        db = 20 * np.log10(rms)
        voiced = db > -42
        if voiced.any():
            first, last = int(np.argmax(voiced)), int(n - 1 - np.argmax(voiced[::-1]))
            run = 0
            for k in range(first, last + 1):
                if not voiced[k]:
                    run += 1
                else:
                    if run * fr / SR > max_gap:
                        issues.append({"type": "PAUSE", "t": round((k - run) * fr / SR, 2),
                                       "detail": f"silence {run * fr / SR:.1f}s inside the line", "sev": 2})
                    run = 0
            if first * fr / SR > 1.2:
                issues.append({"type": "PAUSE", "t": 0.0, "detail": f"leading silence {first * fr / SR:.1f}s", "sev": 1})
    return dur, issues

# --------------------------------------------------------------------------- whisper

_MODEL = None
def model():
    global _MODEL
    if _MODEL is None:
        from faster_whisper import WhisperModel
        _MODEL = WhisperModel(os.environ.get("TTS_QA_MODEL", "small"), device="cpu", compute_type="int8")
    return _MODEL

def transcribe(a, lang="ru"):
    segs, _ = model().transcribe(a, language=lang, word_timestamps=True, vad_filter=False, beam_size=5)
    return [{"w": w.word.strip(), "s": float(w.start), "e": float(w.end), "p": float(w.probability)}
            for s in segs for w in s.words]

def lang_probs(chunk):
    _, _, allp = model().detect_language(chunk)
    d = dict(allp)
    top = max(d, key=d.get)
    return d.get("ru", 0.0), top

# --------------------------------------------------------------------------- checks

def accent_scan(a, words, garbled_idx):
    """Language-ID on sliding 3-word windows. Returns list of issues."""
    issues, flags = [], []
    dur = len(a) / SR
    for i in range(0, max(0, len(words) - 1)):
        j = min(len(words) - 1, i + 2)
        st, en = max(0.0, words[i]["s"] - 0.05), min(dur, words[j]["e"] + 0.05)
        if en - st < 0.9:
            en = min(dur, st + 0.9)
        r, top = lang_probs(a[int(st * SR):int(en * SR)])
        flags.append((i, j, st, en, r, top))
    # merge consecutive non-Russian windows into stretches
    k = 0
    while k < len(flags):
        i, j, st, en, r, top = flags[k]
        bad = r < 0.35 and top not in SLAVIC
        if not bad:
            k += 1; continue
        m = k
        while m + 1 < len(flags) and flags[m + 1][4] < 0.35 and flags[m + 1][5] not in SLAVIC:
            m += 1
        span_words = list(range(flags[k][0], flags[m][1] + 1))
        texts = [norm_word(words[x]["w"]) for x in span_words]
        n_win = m - k + 1
        minr = min(f[4] for f in flags[k:m + 1])
        garbled_here = any(x in garbled_idx for x in span_words)
        only_ff = all(t in FALSE_FRIENDS or len(t) <= 2 for t in texts if t)
        # decide severity: real accent = several windows, or garbled words, or very strong single window
        if only_ff and not garbled_here:
            sev = 0
        elif garbled_here and minr < 0.35:
            sev = 3
        elif n_win >= 3 and minr < 0.2:
            sev = 3
        elif n_win >= 2 and minr < 0.15:
            sev = 2
        elif minr < 0.05 and n_win >= 1 and not only_ff:
            sev = 1
        else:
            sev = 0
        if sev:
            issues.append({"type": "ACCENT", "t": round(flags[k][2], 2),
                           "detail": f"non-Russian sound ({flags[k][5]}, ru={minr:.2f}, {n_win} win): "
                                     + " ".join(words[x]["w"] for x in span_words), "sev": sev})
        k = m + 1
    return issues

def text_checks(script_text, words, dur):
    issues, garbled_idx = [], set()
    exp = tokens_script(script_text)
    heard, idx = tokens_heard(words)
    sm = difflib.SequenceMatcher(a=exp, b=heard, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            continue
        e_txt, h_txt = " ".join(exp[a1:a2]), " ".join(heard[b1:b2])
        widx = [i for g in idx[b1:b2] for i in g]
        t = round(words[widx[0]]["s"], 2) if widx else None
        if op == "replace":
            ratio = difflib.SequenceMatcher(a=e_txt.replace(" ", ""), b=h_txt.replace(" ", "")).ratio()
            if ratio >= 0.75:
                continue  # spelling variant (names, cases) - fine
            sev = 1 if ratio >= 0.55 else (2 if ratio >= 0.35 else 3)
            if len(e_txt) <= 3 and len(h_txt) <= 3:
                sev = min(sev, 1)
            garbled_idx.update(widx)
            issues.append({"type": "GARBLED", "t": t, "detail": f"script «{e_txt}» heard «{h_txt}» (sim {ratio:.2f})", "sev": sev})
        elif op == "delete":
            NEG = {"не", "ни", "нет", "без"}
            if all(len(x) <= 2 and x not in NEG for x in exp[a1:a2]):
                continue  # dropped tiny function word - recogniser noise
            if any(x in NEG for x in exp[a1:a2]):
                issues.append({"type": "MISSING", "t": t, "detail": f"NEGATION not heard: «{e_txt}» (meaning flips!)", "sev": 3})
                continue
            sev = 2 if (a2 - a1) >= 2 else 1
            issues.append({"type": "MISSING", "t": t, "detail": f"not heard: «{e_txt}»", "sev": sev})
        elif op == "insert":
            ws = [words[i] for i in widx]
            # whisper hallucinations at the very end with zero length are not in the audio
            if ws and (all(w["e"] - w["s"] < 0.05 for w in ws) or len({round(w["s"], 2) for w in ws}) == 1) \
                    and ws[0]["s"] >= dur - 1.0 and b2 == len(heard):
                continue
            if all(len(x) <= 2 for x in heard[b1:b2]):
                continue
            garbled_idx.update(widx)
            sev = 2 if (b2 - b1) >= 2 else 1
            issues.append({"type": "EXTRA", "t": t, "detail": f"extra words: «{h_txt}»", "sev": sev})
    # repeated phrase (3+ words) heard more often than in the script
    for n in (5, 4, 3):
        seen = {}
        for i in range(len(heard) - n + 1):
            g = tuple(heard[i:i + n])
            if "<num>" in g:
                continue
            seen.setdefault(g, []).append(i)
        for g, pos in seen.items():
            if len(pos) > 1:
                exp_cnt = sum(1 for i in range(len(exp) - n + 1) if tuple(exp[i:i + n]) == g)
                if len(pos) > max(1, exp_cnt):
                    t = round(words[idx[pos[1]][0]]["s"], 2)
                    issues.append({"type": "REPEAT", "t": t, "detail": "repeated: «" + " ".join(g) + "»", "sev": 3})
        if any(i["type"] == "REPEAT" for i in issues):
            break
    # low-confidence real words
    for i, w in enumerate(words):
        n = norm_word(w["w"])
        if len(n) >= 4 and not re.search(r"\d", n) and w["p"] < 0.35 and i not in garbled_idx:
            issues.append({"type": "LOWCONF", "t": round(w["s"], 2), "detail": f"mumbled? «{w['w']}» p={w['p']:.2f}", "sev": 1})
    return issues, garbled_idx

def check_one(item, max_dur=None, min_dur=None):
    a = load_audio(item["audio"])
    dur, issues = audio_checks(a)
    words = transcribe(a)
    t_issues, garbled = text_checks(item["text"], words, dur)
    issues += t_issues
    issues += accent_scan(a, words, garbled)
    if max_dur and dur > max_dur:
        issues.append({"type": "DURATION", "t": None, "detail": f"{dur:.2f}s > max {max_dur}s", "sev": 3})
    if min_dur and dur < min_dur:
        issues.append({"type": "DURATION", "t": None, "detail": f"{dur:.2f}s < min {min_dur}s", "sev": 2})
    issues.sort(key=lambda x: (-(x["sev"]), x["t"] if x["t"] is not None else -1))
    penalty = sum({1: 1, 2: 4, 3: 10}[i["sev"]] for i in issues)
    verdict = "FAIL" if any(i["sev"] >= 2 for i in issues) else ("WARN" if issues else "PASS")
    return {"id": item.get("id", os.path.basename(item["audio"])), "audio": item["audio"], "dur": round(dur, 2),
            "verdict": verdict, "penalty": penalty, "issues": issues,
            "heard": " ".join(w["w"] for w in words)}

def print_report(results):
    for r in results:
        print(f"[{r['verdict']}] {r['id']}  {r['dur']}s  penalty={r['penalty']}")
        for i in r["issues"]:
            t = f"{i['t']:.1f}s" if i["t"] is not None else "  -  "
            print(f"    {'!' * i['sev']:<3} {i['type']:<8} {t:>6}  {i['detail']}")
    fails = [r["id"] for r in results if r["verdict"] == "FAIL"]
    print(f"\nSUMMARY: {len(results)} checked, {len(fails)} FAIL" + (": " + ", ".join(fails) if fails else ""))
    return fails

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("manifest"); c.add_argument("--out")
    c.add_argument("--max-dur", type=float); c.add_argument("--min-dur", type=float)
    p = sub.add_parser("pick"); p.add_argument("--text", required=True); p.add_argument("files", nargs="+")
    p.add_argument("--max-dur", type=float); p.add_argument("--min-dur", type=float); p.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "check":
        items = json.load(open(args.manifest))
    else:
        items = [{"id": os.path.basename(f), "audio": f, "text": args.text} for f in args.files]
    results = []
    for it in items:
        r = check_one(it, args.max_dur, args.min_dur)
        results.append(r)
        print(f"... {r['id']}: {r['verdict']} (penalty {r['penalty']})", file=sys.stderr, flush=True)
    fails = print_report(results)
    if args.cmd == "pick":
        best = min(results, key=lambda r: (r["verdict"] == "FAIL", r["penalty"]))
        print(f"BEST: {best['audio']} ({best['verdict']}, penalty {best['penalty']})")
    if args.out:
        json.dump(results, open(args.out, "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if (fails and args.cmd == "check") else 0)

if __name__ == "__main__":
    main()
