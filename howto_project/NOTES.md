# Они жили рядом: как появляются маньяки (объяснялка, 16:9)

- 7:01, 1920x1080, 30 fps. 17 chapters (script.json), procedural animations (anim.py: Lineup, Myth, Checklist,
  Dots + the pich_long_project set). Cards anchored to whisper word timestamps (plan.py STK).
- v1 voice (REJECTED by the user: audible accent): FREE — OmniVoice (k2-fsa/OmniVoice) voice clone of Harrison on the Higgsfield sandbox CPU
  (gen.py, gen_takes.py; 7.25 s reference, num_step 16, sentence by sentence). 0 credits.
  All 17 chapters passed tools/tts_qa. Re-recorded: ch3 («не» was dropped → NEGATION rule added to tts_qa,
  text rephrased) and ch13 (accent on «А что с психопатами?» → «Теперь о психопатах.»); 2 takes each, `pick`.
- Images: GPT Image 2.6 low 2k with style ref (14 new, 0.5 cr each) + reused pc/mk/ck images; cover bases 3×1 cr.
  Total spend ≈ 10 credits.
- v1 HQ (429 MB, OmniVoice, superseded): d9d4a60b-d540-4bc2-9233-7cdde9342819.
- v2 HQ 1080p 6:35 (402 MB): media 71484077-2ccb-485b-906b-9d3077d6bfba; web 720p: 362bf8ed-51b1-42c6-92e9-d2b669716ed5.
- Cover: preview_howto/cover_A.jpg (split face, «ОН БЫЛ ТВОИМ СОСЕДОМ»).

## Sandbox gotchas
- After a sandbox replacement /home/user is restored lazily: importing torch from /home/user/ov/lib (50k files)
  took >15 min and the job was killed. Copy the env to local disk first (parallel cp, ~10 min):
  `cd /home/user/ov/lib && ls | xargs -P 24 -I{} cp -rn {} /tmp/fast/ov/lib/`, `cp -r /home/user/hf /tmp/fast/hf`,
  then run with `OVLIB=/tmp/fast/ov/lib OVHF=/tmp/fast/hf`. Model load is then ~35 s, ~4 min per 20-s take.
- Never `pkill -f "cp -r"` inside sandbox_exec — it matches and kills its own shell.

## v2 (user feedback: accent, callouts covering things, weak first shot)
- Voice re-done with Qwen TTS Flash Harrison (all 17 chapters, ~2.3 cr). QA: 17/17 pass (2 minor WARN).
  OmniVoice passed whisper language-ID (P(ru)≈0.97) but the user still heard an accent → never use it for RU.
- Callouts: bottom-right corner, 85% size, soft dark band only at the bottom; shown only over pictures
  (never over animated text cards) and cut at the end of the picture they appear on.
- plan.py: shots can be anchored to a spoken word: "ID@word" / "ID@word#k" — pictures now match the names
  (ch3 teacher→Chikatilo, militiaman→Popkov, druzhinnik→Mikhasevich).
- Opening: anim `portraits:` — 4 archival waist-up B/W portraits (L1–L4, GPT Image 2.6 low 9:16, 2 cr),
  revealed one by one with labels; reused at the end.
