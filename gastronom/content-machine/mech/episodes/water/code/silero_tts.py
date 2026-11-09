#!/usr/bin/env python3.13
"""Бесплатная озвучка Silero v4_ru (голос eugene) с ударениями из RUAccent (поле stressed в textgate.json).

    python3.13 work/silero_tts.py qa_out/textgate.json [id ...] [--take s] [--rate 1.0]

Пишет vo_takes/<id>_<take>.wav (48 кГц). Разметка «+» перед ударной гласной у RUAccent и у Silero одинаковая,
поэтому ударение ставится ровно туда, куда сказал словарь, а не угадывается моделью.
"""
import sys, os, json, re, wave
import numpy as np, torch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(ROOT, '..', 'silero', 'v4_ru.pt')
SPEAKER, SR = 'eugene', 48000
STRESS_FIX = {'михалыч': 'мих+алыч', 'михалыча': 'мих+алыча'}   # имя персонажа: ударение на втором слоге


def prep(stressed):
    s = stressed
    for k, v in STRESS_FIX.items():
        s = re.sub(r'(?i)\b' + '\\+?'.join(k) + r'\b', lambda m, v=v: v if m.group(0).islower() else v[0].upper() + v[1:], s)
    return s.replace('«', '').replace('»', '')


def main():
    args = sys.argv[1:]; take = 's'
    if '--take' in args: i = args.index('--take'); take = args[i + 1]; del args[i:i + 2]
    rep = json.load(open(args[0], encoding='utf-8')); only = set(args[1:])
    imp = torch.package.PackageImporter(MODEL); model = imp.load_pickle('tts_models', 'model'); model.to('cpu')
    os.makedirs(os.path.join(ROOT, 'vo_takes'), exist_ok=True)
    for r in rep:
        if only and r['id'] not in only: continue
        text = prep(r['stressed'])
        a = model.apply_tts(text=text, speaker=SPEAKER, sample_rate=SR, put_accent=True, put_yo=False)
        x = (np.clip(a.numpy(), -1, 1) * 32767).astype(np.int16)
        with wave.open(os.path.join(ROOT, 'vo_takes', f"{r['id']}_{take}.wav"), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
        print(r['id'], f'{len(x) / SR:.1f} с', flush=True)


if __name__ == '__main__':
    main()
