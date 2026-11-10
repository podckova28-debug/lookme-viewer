"""YOUTUBE.tpl.md → YOUTUBE.md: {{ID}} заменяется на время начала реплики по раскладке cut.plan()."""
import os, re, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, D); os.chdir(D)
import cut
shots, total = cut.plan()
def tc(lid):
    t = 0 if lid == 'I01' else cut.LT[lid][0]
    return f'{int(t // 60):02d}:{int(t % 60):02d}'
t = open('YOUTUBE.tpl.md', encoding='utf-8').read()
t = re.sub(r'\{\{(\w+)\}\}', lambda m: tc(m.group(1)), t)
open('YOUTUBE.md', 'w', encoding='utf-8').write(t); print('ok', round(total, 1))
