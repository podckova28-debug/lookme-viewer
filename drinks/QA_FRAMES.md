# Frame QA: how frames are checked for mutations (hands, fingers, extra limbs)

Reference files: `drinks/STYLE.md` (Picture rules), `drinks/hamburger/shots.py` (prompt template), `sheet.py`, `dl.sh`, `batch.py`.

## 1. Prevention in the prompt (most important)
- Every frame with people gets: "Anatomically correct people: every person has exactly two arms, two hands and five fingers per hand; no extra or floating limbs."
- Always: "Only what is described: do not add extra people or objects." (otherwise the model adds people and their hands break).
- Object frames: "objects only, no people, no hands, no faces". Do not add "all people drawn realistically" to object frames: it invites people.
- Fewer people = fewer errors. When hands are not needed: "visible only from the chest up, both hands hidden behind the podium".
- Every prompt is self-contained: never "the same man", describe him again.
- Stick figure: "simple white round-headed stick figure with dot eyes, exactly two arms and two legs; it is the only stick figure".
- Serious scenes (death, crime): a separate non-cartoon style, otherwise objects get smiling faces.

## 2. First look (by eye)
- Contact sheets 6×6, 480×270 per frame, number in the corner.
- Catch composition, extra people or animals, anachronisms, wrong dates or text. Hands are often missed here, hence step 3.

## 3. Strict audit by a separate agent (mandatory)
- Every frame with people is viewed one at a time at full size.
- Hands and arms are cropped with PIL into zoomed pieces and viewed.
- Brief: "For every person trace each arm shoulder→hand: flag 3+ arms/hands, two left or two right hands, a hand not attached to an arm, an arm without upper arm, extra/missing/fused fingers, hands merged into objects, broken limbs, duplicated heads. Also flag impossible objects (liquid through a closed cap), garbled big text, anachronisms. Previous audits missed obvious errors (a man with two left hands, a forearm growing from the shoulder) — be strict, when in doubt flag. Output: BAD: NN – reason, then OK: list."
- Long runs lose notes and check the first third less carefully: split into 2 agents of ~70 frames.

## 4. Fix
- Regenerate each bad frame with a rewritten prompt: fewer people, hands out of frame, or object-only.
- Optionally 2 variants (0.75 credits each) and pick by eye.
- Update the prompt in shots.py, the id in frames/urls.txt, run dl.sh.
- Build the video only after this.

Typical result: out of 120–140 frames the audit finds 4–8 more bad frames than the contact sheets do.
