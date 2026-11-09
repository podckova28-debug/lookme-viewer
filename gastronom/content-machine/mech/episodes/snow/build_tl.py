"""Таймлайн эп. 23 «Нужно ли счищать снег с крыши?»: python build_tl.py → words.py timeline.json → python build_tl.py.
Клипы Wan 3.0 480p, растянуты до 1080p в prep.sh. Шоты под реплику, без зацикливания; в бите 6 два плана (склейка на «номер»)."""
import json, sys
sys.path.insert(0, '/home/user/gastronom/content-machine/video')
import animatic as A

Y = [255, 208, 40]; RED = [208, 60, 40]; BLUE = [40, 110, 190]; GREEN = [46, 140, 76]
TEMPO = 1.07
keys = ['крыши', 'крыше', 'крышу', 'сугроб', 'лобовое', 'ничего', 'сзади', '100', 'килограммов', 'штрафа', 'номер', '500', 'всю']
PAD = [0.04, 0.3]
beats = [
 dict(voice='vo/t01.wav', pad=[0.05, 0.3], shots=[dict(clip='clips/c1_hook.mp4')],
      text=[dict(kind='title', text='Снег с крыши —\nсам слетит?', size=92, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=2.6)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)]),
 dict(voice='vo/t02.wav', pad=PAD, shots=[dict(clip='clips/c2_finger.mp4', cut=True)]),
 dict(voice='vo/t03.wav', pad=PAD, shots=[dict(clip='clips/c3_pov.mp4', cut=True, ss=0.7)]),  # сугроб сползает на «съехал»
 dict(voice='vo/t04.wav', pad=PAD, shots=[dict(clip='clips/c4_highway.mp4', cut=True)]),
 dict(voice='vo/t05.wav', pad=PAD, shots=[dict(clip='clips/c5_ruler.mp4', cut=True)]),
 dict(voice='vo/t06.wav', pad=PAD, shots=[dict(clip='clips/c6a_rear.mp4', cut=True), dict(clip='clips/c6b_plate.mp4', cut=True)]),
 dict(voice='vo/t07.wav', pad=PAD, shots=[dict(clip='clips/c7_sweep.mp4', cut=True)]),
 dict(voice='vo/t08.wav', pad=[0.05, 0.9], shots=[dict(clip='clips/c8_outro.mp4', cut=True)],
      text=[dict(kind='title', text='А ты чистишь\nкрышу?', size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)]),
]
tl = dict(out='snow_final.mp4', voice_tempo=TEMPO, xfade=0.2, music=dict(file='music/bg.m4a', gain=0.16, duck=0.6), sfx_gain=0.7,
          subs=dict(y=1330, size=100, keys={k: Y for k in keys}), beats=beats)

FIX = {'стекла.': 'стёкла.', 'что,': 'что', 'раз.': 'раз?'}
def fix_words(ws, voice):
    out = [[FIX.get(w, w), s, e] for w, s, e in ws]
    if voice == 'vo/t02.wav' and out and out[0][0].lower().startswith('слетит'): out[0][0] = 'Слетит.'
    for k, wd in enumerate(out):  # заглавная в начале реплики и после точки
        if k == 0 or out[k - 1][0].endswith(('.', '?', '!')): wd[0] = wd[0][:1].upper() + wd[0][1:]
    return out

words = {}
try:
    old = json.load(open('timeline.json', encoding='utf-8'))
    if old.get('voice_tempo') == tl['voice_tempo']:
        words = {b['voice']: b['words'] for b in old['beats'] if b.get('words')}
except Exception: pass
for b in beats:
    if b['voice'] in words: b['words'] = fix_words(words[b['voice']], b['voice'])

if all(b.get('words') for b in beats):
    def at(i, word):
        ws = [w for w in beats[i]['words'] if word in w[0].lower()]
        return round(ws[0][1] + beats[i]['pad'][0], 2) if ws else None
    def beat_len(i):
        v = A.read_audio(beats[i]['voice'], TEMPO)
        return len(v) / A.SR + sum(beats[i]['pad'])
    def split(i, word):
        t = at(i, word); T = beat_len(i)
        beats[i]['shots'][0]['w'] = round(t - 0.05, 2); beats[i]['shots'][1]['w'] = round(T - t + 0.05, 2)
        return t
    def tag(i, text, word, pos, target, angle=-5, sfx='pop'):
        t = at(i, word)
        if t is None: print('нет слова', i, word); return
        beats[i].setdefault('text', []).append(dict(kind='tag', text=text, size=72, pos=pos, target=target, angle=angle, at=t))
        beats[i].setdefault('sfx', []).append(dict(file=f'sfx/{sfx}.mp3', at=t, gain=0.28))
    # бит 3: сугроб съезжает на стекло
    beats[2].setdefault('sfx', []).append(dict(file='sfx/fall.mp3', at=round((at(2, 'съехал') or 2.1) - 0.1, 2), gain=0.45))
    beats[2]['text'] = [dict(kind='sticker', big='Обзор — ноль', small='предупреждает «Автодор»', color=RED, pos=[540, 330],
                             at=round(at(2, 'лобовое') or 3.0, 2), until=round(beat_len(2) - 0.02, 2))]
    # бит 4: глыба летит назад
    tag(3, 'лёд и снег', 'срывается', [300, 560], [560, 760], angle=-5)
    beats[3].setdefault('sfx', []).append(dict(file='sfx/whoosh.mp3', at=round(at(3, 'летит') or 2.5, 2), gain=0.3))
    # бит 5: вес
    beats[4]['text'] = [dict(kind='sticker', big='≈ 100 кг', small='20 см мокрого снега', color=BLUE, pos=[540, 330],
                             at=round(at(4, 'крыше') or 2.1, 2), until=round(beat_len(4) - 0.02, 2))]
    beats[4].setdefault('sfx', []).append(dict(file='sfx/ding.mp3', at=round(at(4, '100') or 3.9, 2), gain=0.3))
    # бит 6: штраф
    t6 = split(5, 'номер')
    beats[5]['text'] = [dict(kind='sticker', big='Снег на крыше', small='штрафа нет', color=GREEN, pos=[540, 330], at=0.3, until=round(t6 - 0.08, 2)),
                        dict(kind='sticker', big='500 ₽', small='за номер под снегом', color=RED, pos=[540, 330], at=round(t6 + 0.05, 2))]
    beats[5].setdefault('sfx', []).append(dict(file='sfx/ding.mp3', at=round(at(5, '500') or 5.0, 2), gain=0.3))

json.dump(tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('слова есть' if all(b.get('words') for b in beats) else 'нужен words.py')
