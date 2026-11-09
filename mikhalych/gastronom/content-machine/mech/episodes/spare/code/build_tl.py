"""Эп. 25 «Можно ли гнать на докатке?» — клипы Wan на каждый план. python build_tl.py → words.py timeline.json → python build_tl.py"""
import sys; sys.path.insert(0, '..'); sys.path.insert(0, '.')
from short_common import *
beats = [
 hook('vo/f01.wav', 'Ехать на\nдокатке\nкак обычно?'),
 dict(voice='vo/f02.wav', pad=PAD, shots=[still('kf/k2_compare.png', 'in', (0.55, 0.55), 0.1), clip('clips/c1_hook.mp4', zoom=1.3, focus=(0.45, 0.7))]),
 dict(voice='vo/f03.wav', pad=PAD, shots=[clip('clips/c3_speedo.mp4')]),
 dict(voice='vo/f04.wav', pad=PAD, shots=[still('kf/k4_wet.png', 'left', (0.55, 0.5)), clip('clips/c4_wet.mp4', to=2.6)]),
 dict(voice='vo/f05.wav', pad=PAD, shots=[clip('clips/c1_hook.mp4', ss=1.5, zoom=1.8, focus=(0.6, 0.75)), clip('clips/c5_dash.mp4')]),
 dict(voice='vo/f06.wav', pad=PAD, shots=[still('kf/k6_gauge.png', 'in', (0.68, 0.45), 0.14)]),  # клип c6: манометр съезжает с ниппеля внутрь диска
 outro('vo/f07.wav', 'Давно\nпроверял\nдокатку?'),
]
def extras(x):
    t = x['at'](1, 'почти'); t2 = x['split'](1, 'временное'); u = round((t2 or 5.0) - 0.1, 2)
    x['tag'](1, 'докатка', 'докатка', [790, 520], [790, 900], angle=5, until=u)
    x['tag'](1, 'обычное', 'обычного', [300, 480], [420, 900], angle=-5, until=u)
    x['sticker'](1, 'Почти в 1,5 раза уже', 'а по высоте почти такая же', BLUE, round(t or 1.5, 2), until=round((t2 or 5.0) - 0.1, 2))
    t5 = x['split'](4, 'электроника')
    beats[4].setdefault('sfx', []).append(dict(file='sfx/ding.mp3', at=round(t5 or 3.0, 2), gain=0.3))
    t = x['split'](3, 'торможении')
    beats[3].setdefault('sfx', []).append(dict(file='sfx/whoosh.mp3', at=round(t or 4.0, 2), gain=0.25))
    x['sticker'](2, 'Не быстрее 80 км/ч', 'так пишут производители', RED, 0.3)
    x['sticker'](5, 'Почти вдвое выше', 'давление в докатке', BLUE, 0.4)
build('spare_final.mp4', beats, ['докатку', 'докатка', 'докатке', 'восьмидесяти', 'полтора', 'сцепление', 'давление', 'вдвое', 'шиномонтаж'], extras)
