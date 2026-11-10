# Ep14 QA report — The Worst Jobs in History

Final: out/The_Worst_Jobs_In_History.mp4 — 444.5 s, 1920x1080, 108 shots (3 clips), 93 labels + 4 arrows, 130 subtitle cues.
qa_check.py: 26 checks, 0 FAIL. Loudness −16.1 LUFS. Video/audio 444.63/444.5 s; speech starts 0.1–0.3 s after each block cut, no drift.

## Blind frame QA (2 reviewers, 108 frames, crops 2–8x) and fixes
- F01 boy instead of the elderly knocker-upper → edited. F02 12th extra person → removed.
- F213 two fused boys in the chimney → redrawn twice (final: one large boy, re-checked OK).
- F221 three students with a third hand → redrawn with hands hidden behind the railing.
- F421 impossible cart → redrawn. F411 six-legged table → redrawn as desk top only.
- F203 smeared waving hand → edited; then dark mouth like a moustache → edited.
- F212 letter-like pseudo-writing → wavy lines. F406 grey half-transparent leg → fixed. F403 ghost walkers → solid.
- F425 logo smudge → painted out (again after a later bed edit); bed undercarriage → edited.
- Every fixed frame re-checked blind (2 rounds) → OK.

## Final video still check (2 reviewers + A/V reviewer)
- F105 one leg under the skirt → redrawn with two legs. F106 rosette in pail → clear leeches. F10 paper scrap → small dropping.
- Labels moved to match pictures/narration: "Cuba, 1860s" (block 23 shot order changed), "still exists today", "the privy", "up into the dark", "your pick?", "your job feels bad?", "10 jobs + a bonus"; "no sewers" dropped; "master sweep" arrow re-aimed; "a leech" arrow removed (covered drawing).
- F407 clip clouded over after 2.5 s → trimmed to 2.5 s. F216 clip darkened → still image used.
- Zoom touching edges: F02 recentred, F213 shrunk 7 %, F122 and F226 shifted down.
- Audio/cut drift (atempo lost ~30 ms per block, 0.8 s by the end) → fixed in assemble_ep.py.
- Subtitles were whole paragraphs → split into ≤2 lines of ≤42 chars.
- Leading silence (1.2 s in some blocks) trimmed to 0.3 s.

Voice ASR (asr.txt): all blocks match; only differences are digits vs. words.
