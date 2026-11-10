"""Насколько клон похож на Alexey: косинус голосовых отпечатков (энкодер Chatterbox) к среднему отпечатку Alexey.
    cbx_env/bin/python voiceclone/similarity.py <папка Alexey> <файлы для сравнения ...>"""
import sys, glob, numpy as np, librosa, torch
from chatterbox.models.voice_encoder import VoiceEncoder
from huggingface_hub import hf_hub_download
ve = VoiceEncoder(); ve.load_state_dict(torch.load(hf_hub_download('ResembleAI/chatterbox', 've.pt'), map_location='cpu')); ve.eval()
def emb(paths):
    wavs = [librosa.load(p, sr=16000)[0] for p in paths]
    e = ve.embeds_from_wavs(wavs, sample_rate=16000)
    return e / np.linalg.norm(e, axis=1, keepdims=True)
ref = sorted(glob.glob(sys.argv[1] + '/*_a.mp3'))
R = emb(ref)
loo = [float(R[i] @ (np.delete(R, i, 0).mean(0) / np.linalg.norm(np.delete(R, i, 0).mean(0)))) for i in range(len(R))]
c = R.mean(0); c /= np.linalg.norm(c)
print(f'Alexey к своему среднему (без себя): {np.mean(loo):.3f}, мин {np.min(loo):.3f}')
for grp in sys.argv[2:]:
    paths = sorted(glob.glob(grp)); E = emb(paths)
    s = E @ c
    print(f'{grp}: {np.mean(s):.3f} (мин {np.min(s):.3f}, n={len(paths)})')
