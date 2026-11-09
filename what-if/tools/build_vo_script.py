"""Narration script for recording, from tools/ep01_data.py -> vo_script_ep01.md"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from ep01_data import B, INSERTS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
acts = {'01': 'Act 1. Home', '14': 'Act 2. The city', '34': 'Act 3. The bus', '48': 'Act 4. Evening'}
L = ['# Серия 1: текст рассказчика для записи', '',
     'Собирается из `tools/ep01_data.py` скриптом `tools/build_vo_script.py`.', '',
     '## Как читать', '',
     '- Голос: мужской, американский, 30 - 40 лет. Сухой, спокойный, чуть усталый, как диктор документального фильма о природе, который видит всё это не впервые.',
     '- Обращение на «you». Шутку не подчёркивать голосом: смешно от того, что рассказчик серьёзен.',
     '- Темп около 2,3 слова в секунду. Каждая реплика должна уложиться в свои 10 секунд, с паузой в начале около полсекунды.',
     '- Многоточие и новая строка значат паузу. Время («Nine twenty-two») читать отдельно и коротко.',
     '- Записывать каждую реплику отдельным дублем, 2 - 3 дубля, с секундой тишины до и после. Файлы называть по номеру блока: `vo_01.wav`.',
     '- Комната тихая, без эха; телефон в шкафу с одеждой подходит лучше, чем пустая комната.', '',
     '| Блок | Время в серии | Слов | Секунд при 2,3 сл/с |', '|---|---|---|---|']
rows, body = [], []
t = 4  # cold open hook is about 4 s
for b in B:
    w = len(b['vo_en'].split()) if b['vo_en'] else 0
    if b['id'] in acts:
        body += ['', f"## {acts[b['id']]}", '']
    if b['vo_en']:
        rows.append(f"| {b['id']} | {t//60}:{t%60:02d} | {w} | {w/2.3:.1f}{' ⚠' if w/2.3 > 9 else ''} |")
        body += [f"**{b['id']}** · {t//60}:{t%60:02d} · {b['title']}", '', '> ' + b['vo_en'].replace('. ', '.  \n> '), '', f"_{b['vo_ru']}_", '']
    t += 10
hook = [x for a, x in INSERTS if a == 'после 00'][0]
m = re.search(r'«(.+?)»', hook)
L += rows + ['', '## Крючок, 0:00', '', '> ' + (m.group(1) if m else ''), ''] + body
open(os.path.join(ROOT, 'vo_script_ep01.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('lines', len(rows) + 1)
