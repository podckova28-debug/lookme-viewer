"""Таймлайн эп. 21 «Задняя на ходу»: python build_tl.py → words.py → python build_tl.py (теги по времени слов).
Без зацикливания: длина каждого клипа подобрана под реплику; если короче — лёгкое замедление (speed 0,9–1)."""
import json
Y = [255, 208, 40]; RED = [208, 60, 40]
keys = ['заднюю', 'назад', 'нет', 'коробки', 'автомат', 'электроника', 'синхронизатора', 'заскрежещут', 'защита', 'колечко',
        'силой', 'клочья', 'заглохнет', 'усилители', 'паркинг', 'стопор', 'трещит', 'механика']
beats = [
 dict(voice='vo/t01.wav', pad=[0.05, 0.3], shots=[dict(clip='clips/c1_hook.mp4')],
      text=[dict(kind='title', text='Задняя на ходу —\nчто будет?', size=92, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=1.9)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)]),
 dict(voice='vo/t02.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c2_think.mp4', cut=True)]),
 dict(voice='vo/t03b.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c3_auto.mp4', cut=True)]),
 dict(voice='vo/t04b.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c4_grind.mp4', cut=True)]),
 dict(voice='vo/t05.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c5_lock.mp4', cut=True)]),
 dict(voice='vo/t06.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c6_boom.mp4', cut=True)]),
 dict(voice='vo/t07.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c7_old.mp4', cut=True)]),
 dict(voice='vo/t08.wav', pad=[0.03, 0.3], shots=[dict(clip='clips/c8_pawl.mp4', cut=True)]),
 dict(voice='vo/t09.wav', pad=[0.05, 0.9], shots=[dict(clip='clips/c9_outro.mp4', cut=True)],
      text=[dict(kind='title', text='Механика\nили автомат?', size=92, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)]),
]
tl = dict(out='reverse_final.mp4', voice_tempo=1.07, xfade=0.2, music=dict(file='music/bg.m4a', gain=0.16, duck=0.6), sfx_gain=0.7,
          subs=dict(y=1330, size=100, keys={k: Y for k in keys}), beats=beats)
words = {}
try:
    old = json.load(open('timeline.json', encoding='utf-8'))
    if old.get('voice_tempo') == tl['voice_tempo']:
        words = {b['voice']: b['words'] for b in old['beats'] if b.get('words')}
except Exception: pass
for b in beats:
    if b['voice'] in words: b['words'] = words[b['voice']]
if all(b.get('words') for b in beats):
    def at(i, word):
        ws = [w for w in beats[i]['words'] if word in w[0].lower()]
        return round(ws[0][1] + beats[i]['pad'][0], 2) if ws else None
    def tag(i, text, word, pos, target, angle=-5):
        t = at(i, word)
        if t is None: print('нет слова', i, word); return
        beats[i].setdefault('text', []).append(dict(kind='tag', text=text, size=72, pos=pos, target=target, angle=angle, at=t))
        beats[i].setdefault('sfx', []).append(dict(file='sfx/pop.mp3', at=t, gain=0.28))
    tag(1, 'мимо', 'нет', [300, 760], [600, 470], angle=-6)
    tag(2, 'блокировка', 'электроника', [300, 420], [500, 660], angle=-5)
    tag(3, 'скрежет!', 'заскреж', [770, 560], [500, 860], angle=5)
    tag(4, 'колечко', 'колечко', [860, 960], [650, 1205], angle=5)
    tag(6, 'тяжёлый руль', 'усилители', [800, 600], [700, 1060], angle=4)
    tag(7, 'стопор', 'стопор', [300, 470], [560, 690], angle=-5)
json.dump(tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('слова есть' if all(b.get('words') for b in beats) else 'нужен words.py')
