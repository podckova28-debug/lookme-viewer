"""Таймлайн эп. 22 «Стоит ли переплачивать за 95-й?»: python build_tl.py → words.py timeline.json → python build_tl.py.
Шоты длиной под реплику (без зацикливания); в битах 3 и 4 — по два плана, склейка на начале второй фразы."""
import json, os, sys
sys.path.insert(0, '/home/user/gastronom/content-machine/video')
import animatic as A

Y = [255, 208, 40]; RED = [208, 60, 40]; BLUE = [40, 110, 190]; GREEN = [46, 140, 76]
TEMPO = 1.07
keys = ['95-й', '92-й', '92-м', 'переплачивать', 'мощность', 'сил', 'сжатие', 'вспыхивает', 'стучать', 'восьмиклапанной',
        'одинаковый', 'тысяч', 'поршни', 'дороже']
PAD = [0.04, 0.3]
beats = [
 dict(voice='vo/t01.wav', pad=[0.05, 0.3], shots=[dict(clip='clips/c1_hook.mp4')],
      text=[dict(kind='title', text='95-й лучше\n92-го?', size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=2.2)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)]),
 dict(voice='vo/t02c.wav', pad=PAD, shots=[dict(clip='clips/c2_myth.mp4', cut=True)]),
 dict(voice='vo/t03.wav', pad=PAD, shots=[dict(clip='clips/c_pump_n.mp4', cut=True), dict(clip='clips/c3a_cyl.mp4', cut=True)]),
 dict(voice='vo/t04.wav', pad=PAD, shots=[dict(clip='clips/c3b_knock.mp4', cut=True), dict(clip='clips/c4_listen.mp4', cut=True)]),
 dict(voice='vo/t04c.wav', pad=PAD, shots=[dict(clip='clips/c4b_piston.mp4', cut=True), dict(clip='clips/c4c_hold.mp4', cut=True)]),
 dict(voice='vo/t05b.wav', pad=PAD, shots=[dict(clip='clips/c5_flap.mp4', cut=True)]),
 dict(voice='vo/t06.wav', pad=PAD, shots=[dict(clip='clips/c6_test.mp4', cut=True)]),
 dict(voice='vo/t07.wav', pad=PAD, shots=[dict(clip='clips/c7_money.mp4', cut=True)]),
 dict(voice='vo/t08.wav', pad=[0.05, 0.9], shots=[dict(clip='clips/c8_outro.mp4', cut=True)],
      text=[dict(kind='title', text='А ты какой\nльёшь?', size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
      sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)]),
]
tl = dict(out='gas92_final.mp4', voice_tempo=TEMPO, xfade=0.2, music=dict(file='music/bg.m4a', gain=0.16, duck=0.6), sfx_gain=0.7,
          subs=dict(y=1330, size=100, keys={k: Y for k in keys}), beats=beats)

# правка слов ASR: «95» «-й» → «95-й», «8» «-клапанной» → «восьмиклапанной», ё и заглавные
FIX = {'сжатия': 'сжатие', 'рулем': 'рулём', 'гранты,': 'Гранты,', 'дает': 'даёт', 'за': 'за'}
def fix_words(ws):
    out = []
    for w, s, e in ws:
        if out and w.startswith('-') and out[-1][0].rstrip(',.').isdigit():
            prev = out[-1][0]
            joined = ('восьми' if prev == '8' else prev) + (w[1:] if prev == '8' else w)
            out[-1] = [joined, out[-1][1], e]; continue
        out.append([FIX.get(w, w), s, e])
    for i, (w, s, e) in enumerate(out):  # «За рулём» — название журнала в кавычках
        if w.lower() == 'за' and i + 1 < len(out) and out[i + 1][0].lower().startswith('рул'):
            out[i][0] = '«За'; out[i + 1][0] = 'рулём»'
    return out

words = {}
try:
    old = json.load(open('timeline.json', encoding='utf-8'))
    if old.get('voice_tempo') == tl['voice_tempo']:
        words = {b['voice']: b['words'] for b in old['beats'] if b.get('words')}
except Exception: pass
for b in beats:
    if b['voice'] in words: b['words'] = fix_words(words[b['voice']])

if all(b.get('words') for b in beats):
    def at(i, word):
        ws = [w for w in beats[i]['words'] if word in w[0].lower()]
        return round(ws[0][1] + beats[i]['pad'][0], 2) if ws else None
    def beat_len(i):
        v = A.read_audio(beats[i]['voice'], TEMPO)
        return len(v) / A.SR + sum(beats[i]['pad'])
    def split(i, word):  # два плана: склейка на начале слова
        t = at(i, word); T = beat_len(i)
        beats[i]['shots'][0]['w'] = round(t - 0.05, 2); beats[i]['shots'][1]['w'] = round(T - t + 0.05, 2)
        return t
    def tag(i, text, word, pos, target, angle=-5, sfx='pop'):
        t = at(i, word)
        if t is None: print('нет слова', i, word); return
        beats[i].setdefault('text', []).append(dict(kind='tag', text=text, size=72, pos=pos, target=target, angle=angle, at=t))
        beats[i].setdefault('sfx', []).append(dict(file=f'sfx/{sfx}.mp3', at=t, gain=0.28))
    t3 = split(2, 'она')
    beats[2]['text'] = [dict(kind='sticker', big='Октановое число', small='стойкость к детонации', color=BLUE, pos=[540, 330],
                             at=round(t3 + 0.1, 2))]
    t4 = split(3, 'он')
    tag(3, 'детонация', 'мотор', [790, 470], [560, 880], angle=5)
    beats[3]['text'][-1]['until'] = round(t4 - 0.08, 2)  # ценник только на плане с цилиндром
    for k in range(4):  # стук
        beats[3].setdefault('sfx', []).append(dict(file='sfx/chop.mp3', at=round(0.25 + k * 0.55, 2), gain=0.35))
    beats[5]['text'] = [dict(kind='sticker', big='8-клапанная Гранта', small='АвтоВАЗ разрешает 92-й', color=GREEN, pos=[540, 330],
                             at=round(at(5, 'восьми') or 2.5, 2))]
    tag(6, '92-й: 10,34 л', 'расход', [290, 560], [333, 1010], angle=-5)
    tag(6, '95-й: 10,35 л', 'обоих', [790, 760], [783, 1010], angle=5)
    beats[7]['text'] = [dict(kind='sticker', big='6 600 ₽ в год', small='при 15 000 км', color=RED, pos=[540, 330],
                             at=0.0, until=round(beat_len(7) - 0.02, 2))]
    beats[7].setdefault('sfx', []).append(dict(file='sfx/ding.mp3', at=round(at(7, 'тысяч') or 2.0, 2), gain=0.3))
    split(4, 'ремонт')
    tag(4, 'поршень', 'постепенно', [800, 520], [560, 820], angle=5)
    beats[4]['text'][-1]['until'] = round(at(4, 'ремонт') - 0.08, 2)
    beats[4]['text'].append(dict(kind='sticker', big='Мотору нужен 95-й?', small='не экономь на 92-м', color=RED, pos=[540, 330],
                                 at=round(at(4, 'ремонт') + 0.05, 2)))

json.dump(tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('слова есть' if all(b.get('words') for b in beats) else 'нужен words.py')
