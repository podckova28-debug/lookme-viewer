# tts_qa — automatic voice-over check

`tts_qa.py` checks every TTS line against its script so nobody has to listen by ear:
accent (non-Russian sound), garbled / missing / extra words, repeats, mumbled words,
long pauses, clipping, and the duration window for Shorts. See `.claude/skills/tts-qa/SKILL.md`
for the full workflow and the fixes that work for the Harrison voice.

```bash
python3 tts_qa.py check manifest.json --out qa.json            # long video
python3 tts_qa.py check manifest.json --max-dur 9.5 --min-dur 7.2   # Shorts blocks
python3 tts_qa.py pick --text "текст строки" k1.mp3 k2.mp3 k3.mp3  # best of several takes
```

Needs `faster-whisper` + `ffmpeg` (preinstalled in the Higgsfield sandbox). Exit code 1 if any line FAILs.

## Calibration (2026-11-09, Mikhasevich long video)

`calibration_set.json` = the real bad and good takes (Higgsfield CDN URLs) + the 12 clean chapters.

| Take | Real problem | Result |
|---|---|---|
| BAD_old02 | «Май семьдесят первого» with English accent ("Сэмди Сад") | FAIL — ACCENT ru=0.00, 3 windows |
| BAD_old09 | «Патриоты Витебщины» mangled | FAIL — ACCENT ru=0.00 + GARBLED |
| BAD_t9a / BAD_t9b | «Витебщины» with accent | FAIL — ACCENT ru=0.03 |
| BAD_k92 / BAD_k94 | «Патриоты Витебщины» with accent | FAIL — ACCENT ru=0.00 |
| GOOD_k21 / k22 / k91 / k93 | fixed takes | PASS |
| 12 other chapters | clean | 11 PASS, 1 WARN (two low-confidence words, not a failure) |

6/6 bad takes caught, 0/16 false failures.
