"""Эп. 28 v3 «Кондиционер зимой»: 24 анимированных плана, 2–3 на реплику, стоп-кадров нет.
Пользователь: «Сделай больше кадров, законченные анимации переходящие в тот же статичный кадр — ужасно».
Правило монтажа v3: каждый план — свой клип, режется на середине движения (план короче клипа) и не возвращается
к исходному кадру; никаких still() с картинкой, у которой уже был свой клип.
python build_tl3.py → words.py timeline.json → python build_tl3.py → animatic.py timeline.json"""
import sys; sys.path.insert(0, '..')
import short_common as SC
from short_common import clip, RED, BLUE, GREEN
SC.TEMPO = 1.04
PAD = SC.PAD
C = lambda name, **kw: clip(f'clips/{name}.mp4', **kw)
def hook(voice, title, shots):
    return dict(voice=voice, pad=[0.05, 0.14], shots=shots,
                text=[dict(kind='title', text=title, size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=2.8)],
                sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)])
def outro(voice, title, shots):
    return dict(voice=voice, pad=[0.02, 0.9], shots=shots,
                text=[dict(kind='title', text=title, size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
                sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)])

beats = [
 hook('vo/F01.wav', 'Кондиционер\nот\nзапотевания?', [C('c1_hook'), C('n1_puzzled')]),
 dict(voice='vo/F02.wav', pad=PAD, shots=[C('n2_rain'), C('c2_button'), C('n3_dryair')]),
 dict(voice='vo/F03.wav', pad=PAD, shots=[C('c3_evap', to=1.3), C('n4_drops'), C('n5_drip')],
      sfx=[dict(file='sfx/drip.mp3', at=3.6, gain=0.3)]),
 dict(voice='vo/F04.wav', pad=PAD, shots=[C('c4_clear', fixed=True)]),
 dict(voice='vo/F05.wav', pad=PAD, shots=[C('n6_frostnight'), C('c5_btnfrost'), C('c6_comp', to=1.8)],
      sfx=[dict(file='sfx/brr.mp3', at=0.2, gain=0.3)]),
 dict(voice='vo/F06.wav', pad=PAD, shots=[C('n7_ecu', to=2.0), C('n8_thermo'), C('c6_comp', ss=1.8)]),   # n7: после 2,0 с перчатка отрывается от рычага
 dict(voice='vo/F07.wav', pad=PAD, shots=[C('c7_heater', to=2.8), C('n9_heatknob', to=0.9), C('n10_glass')]),   # n9: после 0,9 с шкала плывёт, рука сползает
 dict(voice='vo/F08.wav', pad=PAD, shots=[C('n11_modeknob', to=1.3), C('c8b_recirc')]),   # n11: дальше пальцы слипаются; c8b — c8 без кадров с горящей лампой (0,97–1,70 с)
 dict(voice='vo/F09.wav', pad=PAD, shots=[C('c12_fogback', ss=2.3), C('c9_breath')]),     # туман возвращается → дыхание
 outro('vo/F10.wav', 'А ты\nвключаешь\nзимой?', [C('n13_point'), C('n14_drive')]),
]
# реплика → слова, на которых начинается следующий план
CUTS = {0: ['кондиционер'], 1: ['кондиционер', 'сушит'], 2: ['радиатор', 'прямо'], 4: ['лампочка', 'компрессор'],
        5: ['большинства', 'некоторых'], 6: ['горячий', 'забирает'], 7: ['обязательно'], 8: ['от'], 9: ['пиши']}

def extras(x):
    for i, words in CUTS.items():
        T = x['blen'](i); ts = [x['at'](i, w) for w in words]
        if None in ts: print('нет слова', i, words); continue
        b = [0.0] + [t - 0.05 for t in ts] + [T]
        for s, (a, e) in zip(beats[i]['shots'], zip(b, b[1:])): s['w'] = round(e - a, 2)
    x['sticker'](1, 'Плюс на улице: да', 'кондиционер сушит воздух', GREEN, 0.2)
    x['tag'](2, 'испаритель', 'холодный', [330, 470], [560, 760], angle=-5, until=round(x['at'](2, 'прямо') - 0.08, 2))   # не тянуть на план под машиной
    x['sticker'](5, 'Около 0 °C', 'у некоторых машин уже при +5 °C', BLUE, 0.4)
    x['tag'](7, 'рециркуляция', 'рециркул', [640, 250], [500, 460], angle=-5)

SC.build('winterac_final.mp4', beats, ['кондиционер', 'плюс', 'сушит', 'радиатор', 'влага', 'мороз', 'компрессор', 'электроника',
                                       'нуля', 'пяти', 'печка', 'рециркуляцию', 'дыхания', 'зимой'], extras)

# субтитры — словами сценария, а не распознавания; время слов — от words.py
import json, importlib.util
_s = importlib.util.spec_from_file_location('script', 'script.py'); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
_L = dict(_m.LINES); _tl = json.load(open('timeline.json', encoding='utf-8'))
for _b in _tl['beats']:
    _sw = _L[_b['voice'].split('/')[-1][:3]].split()
    if _b.get('words') and len(_sw) == len(_b['words']):
        for _w, _t in zip(_b['words'], _sw): _w[0] = _t
    elif _b.get('words'): print('число слов не совпало', _b['voice'])
json.dump(_tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
