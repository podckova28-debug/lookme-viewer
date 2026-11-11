# Дело закрыто / How They Got Caught — production rules

- Voice: Harrison (voice_id 573e5163-59b3-4926-aab1-951ef2985f81). Cheapest engine: `qwen_audio_tts`
  (Qwen TTS Flash, language ru, plain text, no `<#..#>` tags) — 0.13 cr per ~340 chars, 8x cheaper than
  `text2speech_v2`/minimax. Never put the stress mark U+0301 over «е».
- Do NOT use the free OmniVoice clone (howto_project/gen.py) for Russian narration: the user hears a
  non-native accent/stress that whisper language-ID does not detect (P(ru)≈0.97, same as Qwen). Use Qwen.
- **Every TTS line must pass `tools/tts_qa/tts_qa.py` (skill `tts-qa`) before it goes into a render.**
  FAIL lines are re-recorded automatically (3–4 variants in one batch, then `pick`). The user does not
  listen to check voice-overs; never ask them to.
- Cheapest first: GPT Image 2.6 quality low 2k (0.5 cr) with style ref 365645de…; motion via the procedural
  animations in `pich_long_project/anim.py` (0 cr). Wan 3.0 480p (1 cr/s) only if asked. A long video costs ~11–15 cr.
  Ask before any plan over ~110 credits.
- Style: cream paper collage, B/W halftone, single crimson accent. No gore. Big on-screen cards.
- Send previews as soon as they exist. Don't touch already-delivered videos unless asked.
- Don't ask the user for approvals or confirmations for routine steps; just do the work.
- Long videos: chapter cards only at 4–6 big sections (a card per chapter kills the pace). Full-screen stamps must
  auto-fit (cure_project/anim.py Stamp wraps to 2 lines). After a render, check a frame of every stamp/list/callout.
