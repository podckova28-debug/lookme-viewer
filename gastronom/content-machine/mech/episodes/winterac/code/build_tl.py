"""Эп. 28 «Кондиционер зимой» — клипы Wan на каждое действие, очищение стекла — кодом (defog.py).
python build_tl.py → words.py timeline.json → python build_tl.py"""
import sys; sys.path.insert(0, '..')
import short_common as SC
from short_common import hook, outro, clip, still, RED, BLUE, GREEN
SC.TEMPO = 1.04         # бесплатный клон после vopost: паузы уже ужаты, чуть бодрее (≈43 → 41 с)
PAD = SC.PAD
beats = [
 hook('vo/F01.wav', 'Кондиционер\nот\nзапотевания?'),
 dict(voice='vo/F02.wav', pad=PAD, shots=[clip('clips/c2_button.mp4'), still('kf/k2_button.png', 'in', (0.5, 0.4))]),   # v2: лампа горит весь клип, 5 пальцев
 dict(voice='vo/F03.wav', pad=PAD, shots=[clip('clips/c3_evap.mp4', to=1.3), still('kf/k3_evap.png', 'down', (0.5, 0.6), 0.1)],
      sfx=[dict(file='sfx/drip.mp3', at=1.6, gain=0.3)]),
 dict(voice='vo/F04.wav', pad=PAD, shots=[clip('clips/c4_clear.mp4', fixed=True)]),
 dict(voice='vo/F05.wav', pad=PAD, shots=[still('kf/k5_btnfrost.png', 'in', (0.55, 0.55), 0.12), clip('clips/c6_comp.mp4', to=1.8)],
      sfx=[dict(file='sfx/brr.mp3', at=0.2, gain=0.3)]),
 dict(voice='vo/F06.wav', pad=PAD, shots=[clip('clips/c6_comp.mp4', ss=1.8), still('kf/k6_comp.png', 'out', (0.45, 0.45), 0.1)],
      sfx=[dict(file='sfx/snore.mp3', at=0.3, gain=0.25)]),
 dict(voice='vo/F07.wav', pad=PAD, shots=[clip('clips/c7_heater.mp4', to=2.8), still('kf/k7_heater.png', 'in', (0.5, 0.4), 0.1)]),
 dict(voice='vo/F08.wav', pad=PAD, shots=[dict(still('kf/k8_recirc.png', 'in', (0.45, 0.3), 0.12), w=1.4), clip('clips/c8_recirc.mp4', to=0.93)]),   # v2: с 0,97 с лампа загорается — не берём
 dict(voice='vo/F09.wav', pad=PAD, shots=[clip('clips/c9_breath.mp4')]),
 outro('vo/F10.wav', 'А ты\nвключаешь\nзимой?'),
]
def extras(x):
    x['split'](1, 'кондиционер')
    x['sticker'](1, 'Плюс на улице: да', 'кондиционер сушит воздух', GREEN, 0.2)
    x['split'](2, 'влага')
    x['tag'](2, 'испаритель', 'радиатор', [330, 470], [560, 760], angle=-5)
    x['split'](4, 'компрессор')
    x['split'](5, 'большинства')
    x['sticker'](5, 'Около 0 °C', 'у некоторых машин уже при +5 °C', BLUE, 0.4)
    x['split'](6, 'горячий')
    x['split'](7, 'выключи')
    x['tag'](7, 'рециркуляция', 'рециркул', [640, 250], [500, 460], angle=-5)
SC.build('winterac_final.mp4', beats, ['кондиционер', 'плюс', 'сушит', 'радиатор', 'влага', 'мороз', 'компрессор', 'электроника',
                                       'нуля', 'пяти', 'печка', 'рециркуляцию', 'дыхания', 'зимой'], extras)

# субтитры — словами сценария, а не распознавания (ASR пишет «сушат» вместо «сушит»); время слов — от words.py
import json, importlib.util
_s = importlib.util.spec_from_file_location('script', 'script.py'); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
_L = dict(_m.LINES); _tl = json.load(open('timeline.json', encoding='utf-8'))
for _b in _tl['beats']:
    _sw = _L[_b['voice'].split('/')[-1][:3]].split()
    if _b.get('words') and len(_sw) == len(_b['words']):
        for _w, _t in zip(_b['words'], _sw): _w[0] = _t
    elif _b.get('words'): print('число слов не совпало', _b['voice'])
json.dump(_tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
