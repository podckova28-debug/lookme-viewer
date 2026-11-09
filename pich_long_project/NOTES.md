# Шахматист: Александр Пичушкин (длинный ролик, 16:9) — минимальная себестоимость

- 6:05, 1920x1080, 30 fps. NO AI video: all motion is procedural (`anim.py`): chessboard filling with
  counter, park map with pins, timeline, newspaper slam, note being written + circled, metro ticket scan,
  CCTV look with timecode, evidence board with red string, number counter, rubber stamp.
- Voice: Qwen Audio 3.0 TTS Flash (`qwen_audio_tts`, voice Harrison preset 573e5163…, language ru,
  instruction for documentary tone) — 0.13 credits per ~340 chars vs 1.05 for minimax. Plain text only
  (no `<#0.3#>` pause tags — those are minimax syntax). Passed tools/tts_qa (no accent, no garbled words).
  Rate limit: ~11 parallel requests, then 429 → resubmit the rest.
- Images: GPT Image 2.6, quality low, 2k, 16:9, style ref 365645de… — 0.5 credits each (17 images).
- Real spend: ~2.2 (voice, 16 ch) + 8.5 (images) + ~0.5 (samples) ≈ 11 credits.
- HQ 1080p (351 MB): media 39c2ee9b-8bd9-4d8e-81b9-7e272d28c4b0; web 720p: a114885f-b4cf-4dd7-a9a4-dbf5841faa8b.
- Sandbox: /home/user/pc; render.py reads PC_ROOT/PC_FONT env. Background jobs are capped at 15 min —
  split runall / pipe / QA into separate jobs.
