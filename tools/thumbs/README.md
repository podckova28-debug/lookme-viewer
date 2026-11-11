# Thumbnail scripts (1280×720)

- `cover_dark.py S base.png out.jpg "LINE1|LINE2" "BLOCK" SHIFT` — dark style: cream text lines + crimson block,
  picture shifted right by SHIFT px so text never touches the face. S = folder with thumb/Oswald.ttf.
- `cover_light.py` — same on cream paper (ink text).
- `lineup.py` — four portraits row + «КТО ИЗ НИХ МАНЬЯК?».

CTR rules used (Nov 2026 redesign): one big face or one piece of evidence, dark high-contrast background,
2–4 words that do not repeat the title and open a question, readable at 246×138 (check mobile sheet).
Bases: GPT Image 2.6 medium 2k with style ref 365645de…, prompt "dramatic dark version of the reference style",
left 40% empty for text.
