# History on the Menu — style bible (v1, from the Ketchup vs Gin v2 comparison, 25.11)

Ketchup is the reference episode. Gin v2 was rebuilt in the same format, then both were measured.

## Measured comparison

| Parameter | Ketchup (reference) | Gin v2 | Target for new episodes |
|---|---|---|---|
| Length | 5:21 | 5:39 | 5–6 min |
| Frames | 122 | 139 | one frame per script line |
| Seconds per frame | 2.6 | 2.4 | 2.3–2.8 |
| Speech pace | 191 wpm | 190 wpm | 185–195 wpm |
| Short punchlines (≤3 words) | 22 % of lines | 19 % | 20–25 % |
| Questions to the viewer | 5 | 7 | 4–7 |
| Second-person "you" lines | 12 | 5 | 10+ |
| Stick-figure "you" frames | 17 | 7 | 12–18 |
| Frames with a handwritten note | 61 % | 62 % | 55–65 % |
| Simple frames (lots of white) | 20 % | 20 % | ~20 % |
| Busy frames (dense scene) | 27 % | 54 % | 25–35 % |
| Warm colours in the drawing | 97 % | 72 % | warm-dominant |
| Colour saturation (0–1) | 0.48 | 0.18 | 0.4–0.5 |
| Loudness | −15.1 LUFS | −15.3 LUFS | −15 ± 0.5 LUFS |

What matched: pace, cut rate, notes, simple/detailed rhythm, loudness, running gag + callbacks + teaser.
Where Gin v2 is weaker: half its frames are dense crowd scenes (inherited from v1), colours are muted grey-blue,
and the stick-figure "you" almost disappears after the first minute.

## The rules

**Script**
- Cold open in second person: "You are …" + year + place, a paradox, a big number, the question of the episode.
- One sentence per line = one frame. Dry humour; a punchline line of ≤3 words every 4–5 lines.
- One running gag that returns 3–5 times (ketchup: "where are the tomatoes?", gin: the GIN : PARLIAMENT scoreboard),
  plus 2 callbacks to the opening. Serious events (crimes, deaths) are told plainly, no jokes, no cartoon faces.
- Cross-link one earlier episode in the middle; end on a question for the comments + a one-line teaser of the next episode.
- TTS: numbers spelled out, write "offen", never "often".

**Picture**
- White background, ink line + cross-hatching + soft watercolour, warm palette with one accent colour per episode.
- Big subject filling most of the frame (never a small drawing floating in white). No "wide empty margins" in prompts.
- Rhythm, not a formula: ~1 in 5 frames simple (one object / stick figure / scoreboard), ~1 in 4 dense scenes,
  the rest medium (1–3 characters, close-up, expressive faces).
- The stick figure "you" (thin black line body, round white head, dot eyes, simple hands) appears at least once a minute.
- Handwritten marker note + arrow on ~60 % of frames; dates and numbers go into the notes.
- Every frame with people: strict hands check (2 arms, 2 hands, 5 fingers), no anachronisms (coins, flags, dates, modern objects).
- Object-only frames: say "objects only, no people, no hands" in the prompt.

**Edit**
- Slow push-in / pull-out, content at 92 % of the canvas so the zoom never crops anything.
- Music bed under narration, −15 LUFS, narration padded before loudnorm so the last line is never cut.
- Final check: transcribe the last 8 seconds and confirm the teaser is there.

**Shorts (vertical, from the long episodes)**
- One self-contained story, 30–45 s, the hook in the first line.
- No cropping: white margins are trimmed, the drawing fills ~60 % of the 9:16 height, the camera pans across it so every part is seen.
- Captions: Bebas Neue, white caps on an uneven red stripe, upper third (clear of the Shorts UI and faces).
