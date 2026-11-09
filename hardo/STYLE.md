# Hardo — locked style guide

This is the channel look from episode 7 on. Episodes 2 (courier) and 4 (cook) are the reference; episode 7 (firefighter) is the
first episode built to this guide. Do not change any item here without the owner's explicit OK.

## 1. Drawing
- Reference images (pass BOTH as image references in every frame prompt):
  - the episode's own hero character sheet (made first, from the cook sheet as a style reference),
  - the cook character sheet: Higgsfield job `49f55c6b-4f18-438d-a011-7ffb378e91e0` (`style/ref_cook_charsheet.jpg`).
- Thin clean dark line, realistic proportions (normal head size), soft flat colour fills with light shading, small simple face,
  muted palette. NOT thick cartoon outlines, NOT big heads or dot eyes (that was ep3/ep6), NOT semi-real painted shading.
- See `style/ref_*.jpg` for what is right.

## 2. Composition and background
- Wide shots: hero (and at most one or two other people) plus a LIGHT partial setting drawn in the same line: part of a wall,
  a door, a piece of the vehicle, a few pieces of furniture. The setting fades into white; no full rooms, no sky fill.
- Close-ups (hands, objects) and diagrams: on pure white.
- Measured target: white share (pixels with min(R,G,B) > 235) 0.50–0.65 on wide shots, 0.60–0.70 on the episode average.
  No frame below 0.30 (no dark or full-colour backgrounds). Night is shown by a dark window or lamp, never a dark frame.
- Recurring props keep one design and colour for the whole episode (the hero's vehicle, bag, clothes).

## 3. Frame prompt template
```
Illustration in EXACTLY the style of the first reference sheet (and the second sheet, the cook, for line quality):
thin clean line, realistic proportions, soft flat colour fills, small simple face, no thick cartoon outline.
White background with a light partial setting: <one line of setting>. The hero is <hero description>; draw her/him exactly ONCE
with exactly two arms and two hands. Any other person must look clearly different. No text, no letters, no numbers, no labels,
no arrows, no speech bubbles, no logos; no clocks unless the scene gives one with hand positions. SCENE: <action, one sentence>.
```
If a frame comes back too empty or too dark, fix it by an edit pass with the frame itself as the only reference
("keep everything, only add a light background: ..."), 0.25 credit, instead of a new generation.

## 4. Edit rhythm
- NO punch-in crops: the owner said crops cut off too much of the frame (ep8). Every shot is its own generated frame.
- A cut about every 3.5 s (ep8: 136 shots in 7:53). Per block: a wide shot, a close-up, and 1–4 more distinct shots of the same
  moment (a face, a detail, another person, an object, a different angle), 0.25 credit each, each with the block's wide shot as a
  reference so outfits, people and props match. Count per block = round(block length / 3.5 s).
- Length is set only by the narration; more cuts never make the video longer.

### Hook, motion and sound (from the cook analytics, applied from ep7)
- No empty start: the voice begins at 0:00 and a sound effect plays at 0:00 (ep7: the station alarm tone, quiet under the voice, then loud in the first pause).
- The first block cuts faster than the rest: 4 shots, the first one about 4 s.
- Every still moves, slowly and evenly (linear, no easing): a 4% push-in or pull-out on ordinary shots (`zoom`) and 6% on stat and label frames (`zoom_strong_amount`, frames listed in `zoom_strong`, default = all labelled frames). Never more: the owner flagged that bigger zooms cut off too much of the frame (ep7 used 6% and 12%).
- Informative stretches (stats, money, health) never hold one picture: a label pop sound (`label_pop`) marks each number as it appears.
- Sound effects are synthesized in `assemble_ep.py` (`sfx` in plan.json: block, offset, "alert" or "pop", amplitude) and cost nothing. Keep them sparse: an opening cue, a callback cue, pops on numbers.

## 5. Voice
- ElevenLabs preset "Grady" (`e2a2d2e6-9ed2-59cd-82af-feaa27f8a678`) via text2speech_v2, variant elevenlabs, 0.6–0.75 credit per block.
- Tempo 1.1 in the assembler (about 150 words per minute). Never Piper or another voice without the owner's OK.

## 6. Labels
- Hand-lettered (PatrickHand), black, only on white, never touching a face or a drawing. The owner wants MORE text inserts (ep8 on):
  70–90 per episode (ep8: 82): on most shots, especially object and detail shots. Use ARROWS from short words to the thing
  they name ("new." -> the hard hat, "80 lb each." -> the sacks); no empty pictures: every number, every time of day ("5:15 a.m."), short punchlines and quotes
  ("looking good.", "yours."). If a wide shot has no white spot, put the insert on the block's close-up.
- Labels write themselves on: `assemble_ep.py` reveals the label pixels left to right between 0.15 s and 0.9 s of the shot
  (REVEAL), with the pop sound at the start of the writing. Free.
- Auto-placed by `pipeline/label_place.py`; the author sets only the wish position and the arrow TARGET, and must re-check targets
  after any frame is redrawn.

## 7. Animation
- The owner wants more animation (ep8 on): 3–5 Wan clips per episode, 5 credits each, on shots WITHOUT people where only one
  small thing moves (rain, steam, a needle, a light). Prompt: "static camera, the illustration stays exactly as drawn, only X moves".
- Optional beyond that, 5 credits per clip. Only first/last-frame pairs with the same composition (`qa_vision.py pair` animatable),
  or scenes without people. Never animate from a single frame of a person.

## 8. Checks before delivery
`qa_check.py` (0 FAIL), white-share numbers, `qa_review_sheets.py`, then two independent checkers on full-resolution frames:
mutations (limbs, fingers, duplicates) and continuity (picture vs narration, props, clocks, labels).
