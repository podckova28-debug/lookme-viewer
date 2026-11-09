"""Эп. 27 «Спускать ли шины зимой?» — клипы Wan на каждый план. python build_tl.py → words.py timeline.json → python build_tl.py"""
import sys; sys.path.insert(0, '..'); sys.path.insert(0, '../../spare/code')
from short_common import *
beats = [
 hook('vo/f01.wav', 'Спускать\nшины\nзимой?'),
 dict(voice='vo/f02.wav', pad=PAD, shots=[still('kf/k2_sipes.png', 'in', (0.5, 0.55)), clip('clips/c2_sipes.mp4', to=3.0)]),
 dict(voice='vo/f03.wav', pad=PAD, shots=[clip('clips/c3_squashed.mp4', to=2.5, speed=0.57, fixed=True), still('kf/k3_squashed.png', 'left', (0.5, 0.55))]),
 dict(voice='vo/f04.wav', pad=PAD, shots=[clip('clips/c4_rut.mp4')], sfx=[dict(file='sfx/fall.mp3', at=0.6, gain=0.35)]),
 dict(voice='vo/f05.wav', pad=PAD, shots=[clip('clips/c5_deep.mp4'), still('kf/k6_pump.png', 'in', (0.62, 0.7), 0.12)]),  # клип c6: Wan утаскивает шланг в центр колеса
 dict(voice='vo/f06.wav', pad=PAD, shots=[still('kf/k7_gauge.png', 'in', (0.5, 0.72), 0.16), still('kf/k7_gauge.png', 'out', (0.45, 0.45), 0.14)]),  # клип c7: манометр съезжает к ступице
 outro('vo/f07.wav', 'Давно\nпроверял\nдавление?'),
]
def extras(x):
    x['split'](1, 'резина')
    x['tag'](1, 'ламели', 'ламел', [300, 560], [520, 820], angle=-5)
    x['split'](2, 'тормозной')
    x['sticker'](2, 'Тормозной путь длиннее', 'ламели сминаются', RED, 0.3)
    x['split'](4, 'асфальт')
    x['split'](5, 'примерно')
    x['sticker'](5, 'Минус 0,1 атм', 'на каждые 10 градусов мороза', BLUE, 0.4)
build('tirep_final.mp4', beats, ['шины', 'ламели', 'ламелями', 'тормозной', 'диска', 'асфальте', 'давление', 'атмосферы', 'инструкции'], extras)
