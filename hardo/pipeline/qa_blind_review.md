# Tier 2b: blind checker (independent vision pass)

Why: pixel heuristics (qa_check.py, qa_vision.py) cannot see an extra arm, a duplicated hand or a
"second hero" — they only see ink and colour statistics. The author of the frames also misses these
(F34 of ep4 shipped with three arms on two characters after a full author pass). An independent
reader with no stake in the frames catches them.

How: after `qa_review_sheets.py`, start a fresh subagent (general-purpose) that has NOT seen the
episode, give it only the `out/review/` directory and the prompt below, and do not tell it what you
think is fine. Treat every finding as real until you have looked at the frame yourself at 2x.
Then fix, rebuild, regenerate the sheets and run the checker AGAIN on the new sheets (a fix can
introduce a new defect: an edited frame left a skin-coloured smudge on the counter).

Ship rule: the episode ships only when the blind checker's verdict is "ship" on the final sheets.

## Prompt (copy verbatim, fill the path and the hero description)

You are an independent quality checker for a flat-vector animated explainer video (white background,
one recurring hero: <HERO DESCRIPTION>). You have NOT seen this video before and must not assume it is
fine. Look at every review sheet listed below with the Read tool (they are images) and answer the
checklist strictly. Report every defect you see, even small ones, with the sheet name and the
cell/scene number. Do not soften findings.

Sheets directory: <EPISODE>/out/review/
- labels_XX.jpg: hand-lettered labels cropped at 2x. Text sits fully on white; the arrow starts at the
  text edge and not inside letters; the arrow is not a tiny stub; the arrow tip touches the object it names.
- clip_<name>.jpg: a 6x5 grid of consecutive frames of a 5-second animation, read left to right row by
  row. Count hands, arms and heads in EVERY cell; the count may only change when someone enters from the
  frame edge. Count repeated objects (tickets, pans, plates): they must not duplicate or vanish. Nothing
  may appear that is not in the first or last cell. No morphing of faces or objects.
- clocks.jpg: each clock crop with the time the script states. Say whether the drawn hands show that time.
- scenes_XX.jpg: every scene of the finished video, numbered, with the narration line in the header.
  For EVERY person in EVERY scene count arms and hands (exactly two each) and check that every hand
  connects to a shoulder of the same body. The hero appears exactly once per frame except where many
  outline figures are intended; other people look different from the hero; no baked-in arrows, text,
  speech bubbles or logos; the picture matches the narration line; style is flat vector on white;
  no smudges or leftover marks on plain surfaces.

Also read CHECKLIST.md in the same directory.

Output: a markdown report with one section per sheet, then a final verdict for the whole episode:
"ship", "fix by editing" (list what), or "regenerate" (list what). Be concrete: scene numbers, label
texts, cell positions (row, column).

## Calibration result (ep4, first run)
The checker found a real defect the author missed (ghost bucket in clipC_mop, frames 12-16) plus two
baked marks and two script/number mismatches, but it did NOT see the three arms in F34 on the
scenes sheet (960 px tiles, six per sheet). Limb counting needs full-resolution frames: give the
checker `frames/*.png` one by one (or 2x crops per person), not only the scenes sheets.
