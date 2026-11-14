"""Распознать отдельные реплики прямо из итогового ролика (окно по раскладке): python3.13 asr_lines.py A2 E4 G1"""
import sys, os, wave, numpy as np
D = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, D); os.chdir(D)
import cut
cut.plan()
sys.path.insert(0, os.path.join(D, '..', 'qa')); import voiceqa as Q
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4, download_root=Q.WHISPER_DIR)
wf = wave.open('work/final_check/full.wav'); sr = wf.getframerate(); x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
L = dict(cut.LINES)
for lid in sys.argv[1:]:
    a, v, b = cut.LT[lid]
    seg = x[int((v - 0.15) * sr): int((b + 0.1) * sr)]
    s, _ = m.transcribe(seg, language='ru', beam_size=5, vad_filter=False)
    print(lid, '|', L[lid], '\n   →', ' '.join(t.text.strip() for t in s), flush=True)
