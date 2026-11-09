"""Эп. 26 «Держать ли сцепление на светофоре?» — клипы Wan на каждый план. python build_tl.py → words.py timeline.json → python build_tl.py"""
import sys; sys.path.insert(0, '..'); sys.path.insert(0, '../../spare/code')
from short_common import *
beats = [
 hook('vo/f01.wav', 'Держать\nсцепление\nна светофоре?'),
 dict(voice='vo/f02.wav', pad=PAD, shots=[clip('clips/c2_pedal.mp4'), clip('clips/c3_cutaway.mp4', to=1.6, pingpong=True)]),
 dict(voice='vo/f03.wav', pad=PAD, shots=[still('kf/k3_cutaway.png', 'out', (0.65, 0.5), 0.12)]),
 dict(voice='vo/f04.wav', pad=PAD, shots=[clip('clips/c1_hook.mp4', zoom=1.6, focus=(0.95, 0.12), subs_y=1700), clip('clips/c4_bearing.mp4')]),
 dict(voice='vo/f05.wav', pad=PAD, shots=[clip('clips/c5_slip.mp4'), clip('clips/c6_lurch.mp4')]),
 dict(voice='vo/f06.wav', pad=PAD, shots=[clip('clips/c7_neutral.mp4'), still('kf/k7_neutral.png', 'punch', (0.68, 0.82), 0.2)]),
 outro('vo/f07.wav', 'А ты\nдержишь\nсцепление?'),
]
def extras(x):
    x['split'](1, 'подшипник')
    x['tag'](1, 'выжимной подшипник', 'подшипник', [430, 560], [720, 930], angle=-4)  # реплика s02b: «подшипник сцепления»
    x['sticker'](2, 'Пара секунд', 'подшипнику не страшно', GREEN, 0.3)
    x['split'](3, 'временем')
    t = x['split'](4, 'машина')
    beats[4].setdefault('sfx', []).append(dict(file='sfx/fall.mp3', at=round(t or 3.0, 2), gain=0.35))
    x['split'](5, 'машину')
    x['sticker'](5, 'Дольше 10 секунд?', 'нейтраль, а машину держи тормозом', BLUE, 0.4)
build('redlight_final.mp4', beats, ['сцепление', 'подшипник', 'нейтраль', 'тормозом', 'переход', 'секунд', 'коробку'], extras)
