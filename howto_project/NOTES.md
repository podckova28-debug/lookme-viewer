# Они жили рядом: как появляются маньяки (объяснялка, 16:9)

- 7:01, 1920x1080, 30 fps. 17 chapters (script.json), procedural animations (anim.py: Lineup, Myth, Checklist,
  Dots + the pich_long_project set). Cards anchored to whisper word timestamps (plan.py STK).
- Voice: FREE — OmniVoice (k2-fsa/OmniVoice) voice clone of Harrison on the Higgsfield sandbox CPU
  (gen.py, gen_takes.py; 7.25 s reference, num_step 16, sentence by sentence). 0 credits.
  All 17 chapters passed tools/tts_qa. Re-recorded: ch3 («не» was dropped → NEGATION rule added to tts_qa,
  text rephrased) and ch13 (accent on «А что с психопатами?» → «Теперь о психопатах.»); 2 takes each, `pick`.
- Images: GPT Image 2.6 low 2k with style ref (14 new, 0.5 cr each) + reused pc/mk/ck images; cover bases 3×1 cr.
  Total spend ≈ 10 credits.
- HQ 1080p (429 MB): media d9d4a60b-d540-4bc2-9233-7cdde9342819; web 720p: 0d0e892f-3969-4730-b0ca-accd8746294d.
- Cover: preview_howto/cover_A.jpg (split face, «ОН БЫЛ ТВОИМ СОСЕДОМ»).

## Sandbox gotchas
- After a sandbox replacement /home/user is restored lazily: importing torch from /home/user/ov/lib (50k files)
  took >15 min and the job was killed. Copy the env to local disk first (parallel cp, ~10 min):
  `cd /home/user/ov/lib && ls | xargs -P 24 -I{} cp -rn {} /tmp/fast/ov/lib/`, `cp -r /home/user/hf /tmp/fast/hf`,
  then run with `OVLIB=/tmp/fast/ov/lib OVHF=/tmp/fast/hf`. Model load is then ~35 s, ~4 min per 20-s take.
- Never `pkill -f "cp -r"` inside sandbox_exec — it matches and kills its own shell.
