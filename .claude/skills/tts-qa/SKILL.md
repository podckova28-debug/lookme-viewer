---
name: tts-qa
description: Automatic QA of TTS narration (accent, garbled/missing/extra words, repeats, mumbling, pauses, clipping, duration). Use after EVERY TTS generation for Shorts or long videos, before rendering or delivering anything, and to pick the best of several takes.
---

# TTS QA — no manual listening

The user does not want to check voice-overs by ear. Every narration line goes through
`tools/tts_qa/tts_qa.py` before it is used in a render. A line that FAILs is never delivered.

## What it catches

| Type | Meaning | How |
|---|---|---|
| ACCENT | voice stops sounding Russian (English-like accent) | whisper language-ID on sliding 3-word windows; stretches where P(ru) < 0.35 and the top language is not Slavic |
| GARBLED | mispronounced / mangled word | transcript aligned to the script; replaced span with low character similarity |
| MISSING / EXTRA | skipped or inserted words | same alignment |
| REPEAT | phrase spoken twice | n-gram count heard vs script |
| LOWCONF | mumbled word | whisper word probability < 0.35 |
| PAUSE | silence > 1.4 s inside the line (glitch) | RMS frames |
| CLIP | distortion | samples at full scale |
| DURATION | line outside the window (Shorts: `--max-dur 9.5 --min-dur 7.2`) | ffprobe length |

Severity: `!` minor (WARN), `!!`/`!!!` = FAIL. Numbers are normalised (`1985`, `85-й` ≡ "восемьдесят пятый"),
stress marks and `<#0.3#>` pause tags are ignored. Isolated "сам/самых/самого" accent flags are known
false positives and are suppressed unless the word is also garbled.

Calibrated on the Mikhasevich long video (Nov 2026): the accented takes («Май семьдесят первого» → "Сэмди Сад",
«Патриоты Витебщины» → English) FAIL, the clean takes PASS.

## Workflow (do this automatically, never ask the user to listen)

1. Generate TTS (Harrison, `text2speech_v2`, minimax). Download into the Higgsfield sandbox.
2. Write a manifest `[{"id": "v01", "audio": "vo/v01.mp3", "text": "<exact TTS prompt>"}, ...]`.
3. Copy `tools/tts_qa/tts_qa.py` into the sandbox (upload as zip via media_upload, or heredoc) and run in background:
   `python3 tts_qa.py check manifest.json --out qa.json` (add `--max-dur/--min-dur` for Shorts).
   ~25 s per 25-s line on a standard sandbox; use `size: "xl"` and `background: true` for 10+ lines.
4. For every FAIL line generate 3–4 alternative takes in ONE batch (TTS is cheap) using the fixes below, then
   `python3 tts_qa.py pick --text "<text of the variant>" k1.mp3 k2.mp3 ...` — use the BEST one.
   If texts differ between variants, run `check` with a manifest instead and take the lowest penalty PASS.
5. Only PASS/WARN lines go into the render. Re-run whisper word timestamps for replaced lines (card anchors).
6. In the delivery message, say in one line that the voice passed automatic QA (and what was re-recorded).

## Fixes that work for this voice

- Years / numbers at the START of a sentence get an accent. Do NOT start with «Май семьдесят первого года».
  Put a normal phrase first and spell years fully: «Витебская область, Белоруссия. Май тысяча девятьсот
  семьдесят первого года.» or a separate short sentence «Восемьдесят пятый год.»
- Proper names / unusual words in «quotes» drift to English. Remove the quotes and the pause tag inside the name;
  add stress marks on non-«е» vowels: «Патрио́ты Ви́тебщины».
- NEVER put U+0301 over «е» (the voice then says «э»). Use only а/о/у/ы/и/я/ю.
- Replace a word that keeps failing with a synonym or reorder the sentence.
