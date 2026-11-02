# yt-* skills

Скопированы без изменений из https://github.com/Jakeschincariol/youtube-agent-skill
(коммит a2feb21, лицензия MIT, текст лицензии в `YOUTUBE-AGENT-LICENSE`).

Перед установкой прочитаны все файлы: инструкции только пишут тексты и ничего не публикуют,
шесть скриптов на Python используют только стандартную библиотеку, читают переданные им
файлы и не ходят в сеть, не запускают программы и ничего не записывают.

Профиль голоса канала для этих навыков лежит в `.claude/youtube/voice.md`.
Навыки ищут его по пути `~/.claude/youtube/voice.md`: в новой сессии скопируйте
командой `mkdir -p ~/.claude/youtube && cp .claude/youtube/voice.md ~/.claude/youtube/`.
