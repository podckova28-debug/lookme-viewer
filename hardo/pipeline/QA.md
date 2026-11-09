# QA mechanism (four tiers)

Every episode goes through all four before anything is uploaded. Nothing ships with a FAIL; every WARN is looked at on the review sheets; the blind checker must say "ship" on the final sheets.

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

## Tier 2b: blind checker (`qa_blind_review.md`)
A fresh subagent that has not seen the episode reads `out/review/` with the prompt in `qa_blind_review.md` and reports per sheet
(arms/hands per person in every scene, counts per clip cell, labels, clocks, smudges) with a verdict: ship / fix by editing / regenerate.
Reason: ep4 F34 shipped with three arms on two characters after an author pass and 26 green checks; pixel metrics cannot see limbs,
and the author is anchored on their own frames. After every fix: rebuild, regenerate the sheets, run the checker again.

## Tier 3: `qa_semantic.py frames|clips <episode_dir>` (vision model, optional)
Asks a Claude vision model narrow JSON questions per frame (hero count, other people, extra limbs, arrows/text, clock times, style) and per clip (hands/heads/objects per sample).
Needs `ANTHROPIC_API_KEY`; without it the script exits 2 and Tier 2 remains the semantic check.

## Before generating
- `qa_vision.py pair A.png B.png` before paying for a first/last-frame clip: `animatable: false` means regenerate the end frame from the start frame as reference.
- Prompts for frames always state: hero appears exactly once, other people clearly different, no arrows/text/speech bubbles, no clocks unless the time is given with hand positions.

## Plan fields used by QA
`labels`, `clip_pairs` {clip: [startFrame, endFrame]}, `static_clips`, `hero_description`, `hero_color` [[H,S,V],[H,S,V]] (PIL 0-255), `allow_clones` (frames where several copies of the hero are intended).

## Added for ep5
- `label_place.py <ep_dir>`: takes the author's label wishes from plan.json, snaps every arrow tip to the nearest ink and moves the text
  to the nearest white area (ink under the box < 4%, inside the safe area, arrow length 12–35% of the width). Labels with no white spot
  are dropped instead of being drawn over the artwork. Run before the build; it writes previews to review/labels/.
- Before the build the frames go to the blind checker at FULL resolution (one PNG per Read), not the scenes sheets.
- Night scenes: ask for a white background explicitly ("night shown only by a dark window / lamp cone"); a first pass with "night, dark sky"
  produced 11 frames with 0–2% white and all of them had to be redrawn.
- Hero truck colour and other recurring props must be named in every prompt (ep5: two frames came back with a white cab instead of blue).
- Narration: Piper (offline, free) `en_US-lessac-high` at tempo 1.1 gives about 197 wpm; Higgsfield seed_speech is 0.3 credits per block,
  ElevenLabs/MiniMax 0.6.

## Added for ep6
- Wan 3.0 from a SINGLE start frame on a white-background illustration invents a full background within a second and bends limbs
  (ep6: cart and turbulence clips rejected, 10 credits). Animate only first/last-frame pairs with the same composition
  (`qa_vision.py pair` says animatable) or scenes with no people and no white void (planes in the sky, a window, a sunrise).
- Two frames per narration block keep every shot under about 7 s; the second frame is a close-up (hands, object) and costs 0.25 credit.
- Real prices on this account: gpt-image-2.6 0.25 per image, Wan 5 s clip 5, ElevenLabs block 0.6–0.75, Piper 0.

## Episode 6, second pass (style and voice)
- The series look is the ep1–3 cartoon (char_ref of ep3 as a style reference in every prompt); ep5 and the first ep6 pass drifted and were rejected.
- Narration: Grady (ElevenLabs) at tempo 1.0–1.05 (about 135–140 wpm). Piper was rejected as monotone and female-sounding; never pick a voice by a metric without listening.
- Style reference: always pass a frame of the approved episode as a second image reference and write "in EXACTLY the style of the reference" first.

## Style rule (set after episode 6)
The channel look is the courier/teacher/cook look: the hero and one or two props on PURE WHITE, no room, no ceiling, no floor fill,
at most a thin ground line or a few outline buildings. Target: white share >= 0.55 per frame on average, no frame below 0.30.
Episode 6 drifted again (white 0.37 average): the prompts described full cabins, galleys and hotel rooms, so the model drew them.
Prompt rule: every scene prompt names only the hero, the one object the line is about and at most one other person; it says
"no background, no walls, no ceiling, no floor, white around" explicitly. Check the white-share numbers before building.
- Character drawing: the reference for new heroes is the COOK (ep4 char_ref, job 49f55c6b-4f18-438d-a011-7ffb378e91e0): thin
  line, realistic proportions, soft flat fills, small simple face. Not the teacher sheet (thicker outline, bigger head) and not
  the ep6 attendant. Say "thin line, realistic proportions, no thick cartoon outline" in the character prompt and check the sheet
  against the cook before generating scenes.
