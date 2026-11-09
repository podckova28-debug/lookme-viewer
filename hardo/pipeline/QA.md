# QA mechanism (three tiers)

Every episode goes through all three before anything is uploaded. Nothing ships with a FAIL; every WARN is looked at on the review sheets.

## Tier 1: `qa_check.py <episode_dir> --name <basename>` (26 automatic checks, exit 1 on FAIL)
Container and sync (1080p30, AAC, video = audio, narration not clipped, faststart), SRT (count, order, text = script),
white-background rule, frozen video, black frames, loudness, silence gaps, thumbnails.
Labels: inside the safe area; <6% ink under the text; arrow tip on ink; arrow starts at the text edge and is at least 6% of the width.
Clips: first->last drift; **first/last frame pairs animatable** (same composition, otherwise Wan morphs);
**clip anomaly hints** (mid-frame far from both endpoints, phantom ink, object count jumps) as WARN;
**clocks**: round clocks are read and compared with the time the narration states for that block (WARN on mismatch; the reader is right about 80% of the time);
**isolated black marks** (baked-in arrows / symbols) as WARN; **hero colour clusters** (duplicate hero) as WARN when `hero_color` is set.

## Tier 2: `qa_review_sheets.py <episode_dir> --name <basename>` (human pass, fast and complete)
Writes `out/review/`: every label cropped at 2x from the finished video, every clip at 6 fps as a 30-frame strip,
every detected clock cropped with detector reading vs script, every scene numbered with its narration line, plus `CHECKLIST.md`.
The reviewer answers the checklist per sheet. This is what catches extra limbs, duplicated objects and "second hero" frames: pixel heuristics cannot
separate a mutation from legitimate motion (kids running in, lamps switching on), so this pass stays mandatory.

## Tier 3: `qa_semantic.py frames|clips <episode_dir>` (vision model, optional)
Asks a Claude vision model narrow JSON questions per frame (hero count, other people, extra limbs, arrows/text, clock times, style) and per clip (hands/heads/objects per sample).
Needs `ANTHROPIC_API_KEY`; without it the script exits 2 and Tier 2 remains the semantic check.

## Before generating
- `qa_vision.py pair A.png B.png` before paying for a first/last-frame clip: `animatable: false` means regenerate the end frame from the start frame as reference.
- Prompts for frames always state: hero appears exactly once, other people clearly different, no arrows/text/speech bubbles, no clocks unless the time is given with hand positions.

## Plan fields used by QA
`labels`, `clip_pairs` {clip: [startFrame, endFrame]}, `static_clips`, `hero_description`, `hero_color` [[H,S,V],[H,S,V]] (PIL 0-255), `allow_clones` (frames where several copies of the hero are intended).
