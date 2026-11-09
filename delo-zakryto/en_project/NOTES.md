# How They Got Caught — английская версия «Дела закрыто»
- Канал: How They Got Caught, @howtheygotcaught. Аватар тот же (без текста), шапка `htgc_banner.jpg` (2560×1440).
- Голос: Harrison (voice_id 573e5163-59b3-4926-aab1-951ef2985f81), мать в шортсе про Спесивцева — Helena (3c2b83c0-2e0a-5ae8-998a-a5fe71b7eccd).
- Конвейер: видеоблоки русских шортсов (без текста в кадре) + английская озвучка + `burn_en.py` (карточки привязаны к словам по whisper, субтитры audio_to_captions --language en).
- Spesivtsev EN: HQ https://d2ol7oe51mr4n9.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/4d614a45-9f03-423c-8dc8-0d0ea03caeea.mp4
- Английская озвучка уже записана и для Пичушкина (101–108), Михасевича (201–208), Чикатило (301–306), Банди (401–406): hf_20261102_1045* в Higgsfield. Короткие дубли (<7.2 с) надо перезаписать: 104, 107, 202, 204, 304.
- Страница: https://claude.ai/artifact/FYBUfGqVLd3EhYUoT9jBqR
- Popkov EN (7:13): HQ https://d2ol7oe51mr4n9.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/19f6381d-70dd-40de-a081-43643f6c9cbd.mp4
  Сборка в песочнице /home/user/pk_en: копия pk с английскими TITLE/STK в plan.py (regex слов расширен до a-z), английскими строками в render.py (CHAPTER, HOW THEY GOT CAUGHT, MANIAC IN UNIFORM, CASE CLOSED), ch16 = v1601,1602,101, script.json на английском.
