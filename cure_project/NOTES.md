# «Можно ли вылечить маньяка?» — long video (RU, 16:9)

Sandbox root `/home/user/cw` (same pipeline as men_project: plan.py → render.py/anim.py → audio.py → pipe.sh).

- Script: `script.json`, 16 chapters, ~4.5k chars. Voice: Qwen TTS, Harrison, all 16 lines PASS tts_qa
  (v06 re-recorded, take d; takes a–c "failed" only because whisper wrote «Oak Ridge» in Latin — false positive).
- Images: k1–k42 (GPT Image 2.6 low 2k, style ref 365645de…). k25–k42 added so shots don't repeat.
  k40 (stairwell door) is unused.
- Anchors use whisper spellings: «списив» (Спесивцев), «аскадеру» (Атаскадеро), «безсерд», «канад» (heard «Канадо»), «лёзел».
- Duration 6:15. Covers: A «ВРАЧИ СКАЗАЛИ: НЕ ОПАСЕН» (main), B «ЕГО ВЫЛЕЧИЛИ?» (tools/thumbs/cover_dark.py, SHIFT 140).
- Sources: Rice/Harris/Cormier 1992 (Oak Ridge); Caldwell et al. 2006–07 (Mendota JTC); Lösel & Schmucker 2005;
  Frick (callous-unemotional traits); 14-ФЗ 2012; Kemper and Spesivtsev case materials.

## Delivered (2026-11-11)
- HQ 1080p 381 MB: d2ol7oe51mr4n9…/5a92ab47-b588-498b-b4a5-5f85eac27caf.mp4 (first PUT returned 400, retry 200)
- Web 720p: d2ol7oe51mr4n9…/accb8fe2-7f8b-429f-bd0e-05ef3858c523.mp4
- Page: LONG entry `delo_long_cure` (version 24), covers cure_cover_A/B.jpg. Package sent to «Мозг».

## v2 (2026-11-11) — replaces v1
- User: "some lines don't fit" + "too many chapters, kills the pace".
- 5 section cards (ACTS in plan.py) instead of 15; chapters without a card flow on with 0.5 s tail. 6:15 → 5:43.
- Stamp anim auto-fits: font shrinks, long text wraps to 2 balanced lines, never starts a line with a dash.
- Callout fixes: «ОУК-РИДЖ · 1960–70-е», ЛЁЗЕЛЬ И ШМУКЕР anchored earlier, dropped the 1 s «…ЧТОБЫ УПРАВЛЯТЬ».
- HQ 348 MB: d2ol7oe51mr4n9…/6a1ad832-8621-4e0a-8d4f-dbde13698c57.mp4; web: …/e6979207-2b97-4233-b6cd-b720d3fb7e92.mp4.
  Page v25, update sent to «Мозг».

## v3 (2026-11-12) — replaces v2
- User: «Большой вопрос и маленький маньяка?» — the title card (copied from men_project) had a huge first line and a
  tiny second line. Now both lines are big; the key word «МАНЬЯКА?» is the largest, in crimson. Only t00 re-rendered.
- HQ: d2ol7oe51mr4n9…/67c77004-6238-4749-83c1-efe791867e80.mp4; web: …/824dcb31-d875-4237-80b8-eb5a03e199e4.mp4. Page v26.
