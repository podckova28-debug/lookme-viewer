"""Слова озвучки с низкой уверенностью распознавания (кандидаты на акцент и неверное ударение) и паузы между словами.

    python wordconf.py vo/s0*.mp3   — слово[уверенность?|пауза после], «?» — ниже 0,75, «|0.48» — пауза длиннее 0,12 с

Вторая строка — распознавание без подсказки языка (латиница = прочитано по-английски)."""
import os, sys
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8', download_root=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whisper'))
for f in sys.argv[1:]:
    segs, info = m.transcribe(f, language='ru', beam_size=5, word_timestamps=True, vad_filter=False)
    ws = [w for s in segs for w in s.words]
    out = []
    for i, w in enumerate(ws):
        gap = ws[i + 1].start - w.end if i + 1 < len(ws) else 0
        mark = ('?' if w.probability < 0.75 else '') + (f'|{gap:.2f}' if gap > 0.12 else '')
        out.append(f'{w.word.strip()}[{w.probability:.2f}{mark}]')
    print(os.path.basename(f), ' '.join(out))
    segs2, info2 = m.transcribe(f, language=None, beam_size=1)
    print('   auto:', info2.language, ''.join(s.text for s in segs2)[:120])
