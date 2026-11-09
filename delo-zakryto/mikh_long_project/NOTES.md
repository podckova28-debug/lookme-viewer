# Он искал себя: Геннадий Михасевич (длинный ролик, 16:9)

- 6:35, 1920x1080, 30 fps. Pipeline from popkov_project (render/plan/audio), 14 chapters,
  Harrison TTS, music m1–m3. Sandbox root /home/user/mk; setup.sh fetches font/music/VO and runs whisper.
- Cheap plan: 14 Wan 3.0 480p clips x 5 s (70 credits) + 15 seedream 2k images (~37.5) + TTS.
- Chapter 9 re-recorded (first take garbled «Патриоты Витебщины»); final take d30932a0.
- v2 (accent fix): HQ 1080p (385 MB) media fa0f44ae-78a2-40d3-9d13-ca4db91f6c70, web 27f0b5ea-6a2d-4f0a-a5d8-7ce34abf3acb
- v1 (superseded): HQ d483273c-ab4c-44a3-8543-3319f6ee11a3, web 6fb5a7d5-772b-4f2a-ad4a-e57584a42829
- Accent check: whisper detect_language on 2-word windows (accent.py/scan.py approach). Real accent =
  garbled transcript + 'en' over several consecutive windows. Ch2 «Май семьдесят первого» and ch9
  «Патриоты Витебщины» were accented; fixed with takes k22 (5f3cfa61) and k93 (91632377, stress marks
  Патрио́ты Ви́тебщины). Isolated 'сам' -> 'en' flags are false positives.
- Covers: man with crimson armband (A), roadside bus stop (B); text «36 УБИЙСТВ / ОН ИСКАЛ / САМ СЕБЯ».
- Image job ids (usable as Wan refs): 100 f230bd77, 101 a1c168d7, 201 b45f3990, 301 527d46ef, 401 11e6cbaa,
  501 f5b49dac, 601 e017891b, 701 409276b8, 801 d7da1e07, 901 87f936fc, 1001 deca6f55, 1101 9464598b,
  1201 51e4e7b4, 1301 c9e32815, 1401 bf064a56.

YouTube title: Маньяк-дружинник искал сам себя: как поймали Михасевича | Дело закрыто
(description with timecodes and tags: RU artifact page, LONG section)
