# Дело закрыто / How They Got Caught — production rules

- Voice: Harrison TTS (`text2speech_v2`, minimax, voice_id 573e5163-59b3-4926-aab1-951ef2985f81).
  Never put the stress mark U+0301 over «е».
- **Every TTS line must pass `tools/tts_qa/tts_qa.py` (skill `tts-qa`) before it goes into a render.**
  FAIL lines are re-recorded automatically (3–4 variants in one batch, then `pick`). The user does not
  listen to check voice-overs; never ask them to.
- Cheapest models first: Wan 3.0 480p (1 credit/s), seedream 2k stills with Ken Burns. Ask before any plan over ~110 credits.
- Style: cream paper collage, B/W halftone, single crimson accent. No gore. Big on-screen cards.
- Send previews as soon as they exist. Don't touch already-delivered videos unless asked.
- Don't ask the user for approvals or confirmations for routine steps; just do the work.
