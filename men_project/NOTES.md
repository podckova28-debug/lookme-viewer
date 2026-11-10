# Почему маньяки — почти всегда мужчины (объяснялка, 16:9)

- Sandbox root /home/user/mw (render.py/plan.py/audio.py/pipe.sh point there). Code copied from howto_project
  (portraits, quotes, word-anchored shots, corner callouts only over pictures).
- 16 chapters (script.json, ~4000 chars). Voice: Qwen TTS Flash Harrison (~1.9 cr), QA via tools/tts_qa.
- New images w1–w12 (GPT Image 2.6 low 2k, style ref): stairwell door, kitchen + bottle, railway platform,
  hospital trolley, hormone diagram, schoolyard, police board with male identikit, Soviet canteen, sewing machine,
  woman "social worker" at a door, courtroom cage, elderly witness at police. Reused hw images + L1–L4.
- Covers: cover.py (face shifted right, text block left): A «8 ЛЕТ ИСКАЛИ / МУЖЧИНУ» (torn identikit → woman),
  B «ПОЧЕМУ НЕ / ЖЕНЩИНЫ?» (split man/woman face). Bases: hf_20261110_143813_09d4405d…, 143812_33c8cfe3….
- Facts: UNODC ~90% of homicide suspects are men; female SK share 5–15% (Radford/FGCU, Harrison 2015 «1 in 6»);
  Harrison, Hughes & Gott 2019 (55+55 US SKs): men ~6x more likely to kill strangers, stalking 65.4% vs 3.6%;
  Ivanyutina (Kyiv 1987, thallium, 9 murders per court, death sentence); Gaidamachuk (2002–2010, posed as social
  worker, 17 murders, police assumed a man, survivor said a woman, 20 years = max for women in RF, 2012).
- Delivered: 5:43, HQ 1080p (347 MB) media 6b337042-0f45-4c0c-954b-4cf67e516290; web 720p 2b527478-afa6-49f0-a176-d9c3e3981421.
- QA: 16/16 pass; WARNs are false positives («90 %» digits, «грипп»/«гриб» homophone, «жизней»/«жизни»).
- Spend: 12 images 6 cr + 2 cover bases 1 cr + TTS ~1.9 cr ≈ 9 cr.
- v2 (user feedback): long callouts were cut off at the frame edge → callout_img now wraps into two balanced lines /
  shrinks to ≤1100 px; stamps (ТАЛЛИЙ, 20 ЛЕТ) barely visible → solid cream stamp card, darkened picture, shake.
  Images repeated → 21 new images x1–x21 (~10.5 cr), ~55 shots, almost every picture used once.
  w10 had three hands → replaced with v10b (woman on stairs, two hands checked).
