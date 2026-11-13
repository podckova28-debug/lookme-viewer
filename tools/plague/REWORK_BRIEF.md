# Rework brief for episodes 4–7 (retention fixes)

User feedback after publishing (smallpox): retention suffers.
1. Too many frames that are just a city / a landscape / an empty room with nothing happening.
2. The slow zoom annoys → camera is now fully static (`'static': True` in beats(); do not touch).
3. The episode must pull the viewer into the story from the very first second (no "City. Date." opener, no establishing shot first).
4. More on-screen text inserts, and they must read like native human captions, not AI lists joined with " · ".

## What to change in tools/plague/epXX_spec.py (do NOT generate images, do NOT spend credits, do NOT commit)
A. **Cold open (C01–C03 only):** rewrite the narration so the first sentence drops us into a concrete moment with a person in trouble (sensation, action, stakes); place and date come after, in passing. Keep the same facts. Keep each line about the same length. The FIRST shot of the episode must show a character (stickman or villain), never an empty establishing shot. You may reorder or swap shots between C01–C03.
B. **Empty scenery → scenes with characters:** every frame whose prompt is pure scenery (contains "No people", "No people and no human figures", "People only as tiny distant figures", or is built with `sc(...)`/`sh(...)` without people) and is NOT a diagram (`d..`) must be rewritten into a scene where 1–3 simple stickmen (or the villain) are clearly doing something that matches the narration of that line. Keep the same frame id (it will be regenerated). Rules for stickmen prompts (copy the episode's own STICK/SN helper):
   - describe clothes in words for the exact era; no reference sheet for modern / ancient scenes (if the episode's helper attaches the stickman sheet, keep it only for 1600–1900 scenes);
   - at most 3 figures, standing apart; each has exactly two arms and two hands; hands empty unless ONE object is named; nothing floating; no flags; no readable text;
   - villains hold at most ONE object.
   Exceptions you may keep as-is: frames that are clearly objects with meaning (a letter, a coin, a vial) — but no more than ~6 per episode.
C. **Captions:** rewrite every caption/label so it reads naturally: short sentence-case or title phrases, no " · " separators, no lists of three words. Examples: `FEVER · HEADACHE · ACHES` → `Fever, headache, aching muscles`; `CAMP FUNSTON, KANSAS · MARCH 1918` → `Camp Funston, Kansas — March 1918`; `1 IN 3 INFECTED · MORE DEATHS THAN THE WAR` → `One in three people infected`. Then ADD more captions so that roughly every second shot that introduces a person, place, date or striking number has one (names of people, places + years, key numbers, short quotes from the narration). Use the existing `cap(...)` helper; one caption per shot.
D. Do not change any narration lines except C01–C03. Do not change ids. Keep the file runnable: after editing run `python3 tools/plague/epXX_spec.py lines`, `frames` and `beats` and make sure they succeed.

## Report back
- the new C01–C03 text;
- the list of frame ids whose prompts changed (these need regeneration);
- the count of captions before/after.
