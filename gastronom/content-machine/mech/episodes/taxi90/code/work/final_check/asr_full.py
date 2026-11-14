"""ASR всего итогового ролика и сверка со сценарием по словам (порядок реплик — как в монтаже)."""
import sys, os, re, json, subprocess, difflib
D = '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/taxi90'
sys.path.insert(0, D); os.chdir(D)
import cut
shots, total = cut.plan()
order = []
for s in shots:
    if not order or order[-1] != s['line']: order.append(s['line'])
L = dict(cut.LINES)
norm = lambda w: re.sub(r'[^а-яa-z0-9]', '', w.lower().replace('ё', 'е'))
ref = [(lid, norm(w)) for lid in order for w in L[lid].split() if norm(w)]
wav = 'work/final_check/full.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'taxi90_1080p.mp4', '-ac', '1', '-ar', '16000', wav], check=True)
from faster_whisper import WhisperModel
sys.path.insert(0, os.path.join(D, '..', 'qa')); import voiceqa as Q
m = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4, download_root=Q.WHISPER_DIR)
import wave, numpy as np
wf = wave.open(wav); x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
segs, _ = m.transcribe(x, language='ru', word_timestamps=True, beam_size=5, vad_filter=False)
hyp = []
for s in segs:
    for w in s.words:
        if norm(w.word): hyp.append((round(w.start, 2), norm(w.word), w.word.strip()))
json.dump(hyp, open('work/final_check/asr_words.json', 'w'), ensure_ascii=False)
sm = difflib.SequenceMatcher(None, [r[1] for r in ref], [h[1] for h in hyp], autojunk=False)
out = []
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op == 'equal': continue
    lid = ref[a0][0] if a0 < len(ref) else ref[-1][0]
    t = hyp[b0][0] if b0 < len(hyp) else (hyp[-1][0] if hyp else 0)
    out.append(f"{lid:4s} {t:7.2f}s  {op:7s} сценарий: «{' '.join(r[1] for r in ref[a0:a1])}» → слышно: «{' '.join(h[2] for h in hyp[b0:b1])}»")
print('слов в сценарии', len(ref), 'распознано', len(hyp), 'совпадение', round(sm.ratio(), 4))
print('\n'.join(out))
