import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for n in sys.argv[1:]:
    segs, _ = m.transcribe(f"{n}.wav", language="ru", word_timestamps=True, vad_filter=False)
    ws = [(round(w.start,2), w.word.strip()) for s in segs for w in s.words]
    print(n, " ".join(f"{w[1]}@{w[0]}" for w in ws), flush=True)
