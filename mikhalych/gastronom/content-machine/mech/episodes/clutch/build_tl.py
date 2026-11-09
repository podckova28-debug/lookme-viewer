"""Таймлайн эп. 24 «Нужно ли выжимать сцепление в мороз?»: python build_tl.py → words.py timeline.json → python build_tl.py.
Клипы Wan 3.0 480p, растянуты до 1080p в prep.sh. В бите 5 два плана (склейка на «стартеру»)."""
import json, sys
sys.path.insert(0, '/home/user/gastronom/content-machine/video')
import animatic as A

Y = [255, 208, 40]; RED = [208, 60, 40]; BLUE = [40, 110, 190]; GREEN = [46, 140, 76]
TEMPO = 1.07
keys = ['сцепление', 'сцепления', 'стартер', 'шестерни', 'коробки', 'мёд', 'легче', 'проще', 'места', 'плавно', 'выжимаешь']
PAD = [0.02, 0.14]  # было [0.04, 0.3]: между репликами 0,34 с тишины — «паузки»
beats = [
 dict(voice='vo/f01.wav', pad=[0.05, 0.14], shots=[dict(clip='clips/c1_hook.mp4')],
      text=[dict(kind='title', text='Выжимать\nсцепление?', size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=2.8)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)]),
 dict(voice='vo/f02.wav', pad=PAD, shots=[dict(clip='clips/c2_pfff.mp4', cut=True)]),
 dict(voice='vo/f03.wav', pad=PAD, shots=[dict(clip='clips/c3_cutaway.mp4', cut=True)]),
 dict(voice='vo/f04.wav', pad=PAD, shots=[dict(clip='clips/c4_honey.mp4', cut=True)]),
 dict(voice='vo/f05.wav', pad=PAD, shots=[dict(clip='clips/c5a_pedal.mp4', cut=True), dict(clip='clips/c5b_exhaust.mp4', cut=True)]),
 dict(voice='vo/f06.wav', pad=PAD, shots=[dict(clip='clips/c6_lurch.mp4', cut=True)]),
 dict(voice='vo/f07.wav', pad=PAD, shots=[dict(clip='clips/c7_release.mp4', cut=True, speed=0.88)]),
 dict(voice='vo/f08.wav', pad=[0.02, 0.9], shots=[dict(clip='clips/c8_outro.mp4', cut=True)],
      text=[dict(kind='title', text='А ты\nвыжимаешь?', size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)]),
]
tl = dict(out='clutch_final.mp4', voice_tempo=TEMPO, xfade=0.2, music=dict(file='music/bg.m4a', gain=0.16, duck=0.6), sfx_gain=0.7,
          subs=dict(y=1330, size=100, keys={k: Y for k in keys}), beats=beats)

FIX = {'ровно': 'ровно —', 'сцепление': 'сцепление', 'мед.': 'мёд.', 'вперед': 'вперёд', '-плавно': 'плавно', 'густое': 'густое,'}
def fix_words(ws, voice):
    out = [[FIX.get(w, w), s, e] for w, s, e in ws]
    for k, wd in enumerate(out):
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
    # бит 3: стартер крутит и коробку
    tag(2, 'стартер', 'стартер', [260, 500], [300, 690], angle=-5)
    tag(2, 'коробка', 'шестерни', [860, 1010], [700, 1215], angle=5)
    # бит 5: педаль → мотор завёлся
    t5 = split(4, 'стартеру')
    beats[4]['text'] = [dict(kind='sticker', big='Коробка отключена', small='стартер крутит только мотор', color=GREEN, pos=[540, 330],
                             at=0.5, until=round(t5 - 0.08, 2))]
    beats[4].setdefault('sfx', []).append(dict(file='sfx/ding.mp3', at=round(at(4, 'проще') or 5.8, 2), gain=0.3))
    # бит 6: рывок без сцепления
    beats[5]['text'] = [dict(kind='sticker', big='На передаче?', small='без сцепления — рывок', color=RED, pos=[540, 330], at=0.3,
                             until=round(beat_len(5) - 0.02, 2))]
    beats[5].setdefault('sfx', []).append(dict(file='sfx/fall.mp3', at=0.25, gain=0.35))

json.dump(tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('слова есть' if all(b.get('words') for b in beats) else 'нужен words.py')
