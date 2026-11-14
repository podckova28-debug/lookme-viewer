import sys, os
D = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.join(D, '..', 'qa'))
import voiceqa as Q
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4, download_root=Q.WHISPER_DIR)
for f in sys.argv[1:]:
    x = Q.load_audio(f)
    for bs in (5, 1):
        s, _ = m.transcribe(x, language='ru', beam_size=bs, vad_filter=False)
        print(os.path.basename(f), bs, '→', ' '.join(t.text.strip() for t in s), flush=True)
