# QC tut — stage video

## Автоматические проверки
- ❌ shot 75: Ankhesenamun age 20 must have ['white mourning clothes'] here (continuity plan 75-88)
- ❌ shot 78: Ankhesenamun age 20 must have ['white mourning clothes'] here (continuity plan 75-88)
- ⚠️ shot 28: generic person ('queen') without a character sheet — name the character or confirm it is an extra
- ⚠️ shot 62: generic person ('girl') without a character sheet — name the character or confirm it is an extra
- ⚠️ shot 77: generic person ('king') without a character sheet — name the character or confirm it is an extra
- ⚠️ shot 85: generic person ('prince') without a character sheet — name the character or confirm it is an extra
- ⚠️ 'Egypt' appears in shots [13, 76, 84, 119] but has no sheet/anchor — if it is a person, add it to WHO or ANCHOR
- ⚠️ 'Prince Tutankhaten' appears in shots [20, 24] but has no sheet/anchor — if it is a person, add it to WHO or ANCHOR
- ⚠️ 'Egyptian' appears in shots [22, 33, 45, 50, 51, 56, 66, 70] but has no sheet/anchor — if it is a person, add it to WHO or ANCHOR
- ⚠️ 'Russian' appears in shots [62, 128] but has no sheet/anchor — if it is a person, add it to WHO or ANCHOR
- ⚠️ 'Hittite' appears in shots [77, 83, 84, 85, 86] but has no sheet/anchor — if it is a person, add it to WHO or ANCHOR
- ⚠️ ending not checked by ear (pass --whisper <venv python>)
- ⚠️ no --timeline: cut review sheets of the final file not made
- ✅ storyboard: 150 shots linted
- ✅ frames: review sheets written to /home/user/lookme-viewer/history/tut/qc/frames_*.jpg
- ✅ video size 97.9 MB (limit 100)
- ✅ video 606.80s vs audio 606.80s
- ✅ duration 10:06 (format 8-11 min)
- ✅ no near-silent 3-s windows (music bed present)

## Ручной просмотр (обязательно, каждый лист, крупно)
Открыть каждый `frames_*.jpg` и `cuts_*.jpg` и отметить номера кадров с проблемой:
- [ ] главный герой узнаваем в каждом кадре (лицо, причёска, одежда по возрасту из листа)
- [ ] второстепенные персонажи (король, враг, судья) одинаковы во всех сценах
- [ ] в сцене нет лишних персонажей с листа (епископ на коронации и т. п.)
- [ ] глаза, руки, пальцы, лица без мутаций
- [ ] нет анахронизмов (подзорные трубы, современные воротнички, здания, флаги не той стороны)
- [ ] надписи в кадре написаны верно и не повторяются подписью
- [ ] подписи не закрывают лица
- [ ] по звуку: послушать начало, середину, последние 20 с; музыка слышна; нет посторонних звуков

Пользователю отправлять только при нуле ❌ и всех отмеченных пунктах.
