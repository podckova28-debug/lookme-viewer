"""Страница скачивания длинного ролика: режет mp4 на куски по 14 МБ (лимит файла артефакта 15 МБ) и собирает страницу."""
import json, os, re, sys, subprocess
D = '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/mechanic90/'
OUT = D + 'dlpage/site/'
src = sys.argv[1] if len(sys.argv) > 1 else D + 'mechanic90_1080p.mp4'
os.makedirs(OUT + 'v', exist_ok=True)
for f in os.listdir(OUT + 'v'): os.remove(OUT + 'v/' + f)
CH = 14 * 1024 * 1024
parts = []
with open(src, 'rb') as f:
    i = 0
    while True:
        b = f.read(CH)
        if not b: break
        p = f'v/part_{i:02d}.mp4'
        open(OUT + p, 'wb').write(b); parts.append(dict(path=p, size=len(b))); i += 1
# проверка: склейка кусков = исходник
import hashlib
h1 = hashlib.md5(open(src, 'rb').read()).hexdigest()
h2 = hashlib.md5(b''.join(open(OUT + p['path'], 'rb').read() for p in parts)).hexdigest()
assert h1 == h2, 'склейка не совпала'
md = open(D + 'YOUTUBE.md', encoding='utf-8').read()
sec = {m.group(1).strip(): m.group(2).strip() for m in re.finditer(r'^## (.+?)\n(.*?)(?=^## |\Z)', md, re.S | re.M)}
alts = [l[2:].strip() for l in sec['Название'].splitlines() if l.startswith('- ')]
title = sec['Название'].splitlines()[0].strip()
texts = [['Название', title]] + [[f'Запасное название {k+1}', a] for k, a in enumerate(alts)] + \
        [['Описание', sec['Описание']], ['Теги', sec['Теги']], ['Закреплённый комментарий', sec['Закреплённый комментарий']]]
t = open(D + 'dlpage/template.html', encoding='utf-8').read()
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
t = t.replace('%%DUR%%', f'{int(dur // 60)}:{int(dur % 60):02d}')
M = json.load(open(D + 'dlpage/meta.json', encoding='utf-8'))
th = [[f"thumb_{n}.jpg", lab, str(k + 1) + (' — главная' if k == 0 else ''), 'thumbs'] for k, (n, lab) in enumerate(M['thumbs'])]
t = t.replace('%%TITLE%%', M['title']).replace('%%H1%%', M['h1']).replace('%%POSTER%%', th[0][0]).replace('%%POSTER_ALT%%', M['poster_alt'])
t = t.replace('%%FILENAME%%', json.dumps(M['filename'])).replace('%%THUMBS%%', json.dumps(th, ensure_ascii=False))
t = t.replace('%%PARTS%%', json.dumps(parts)).replace('%%TEXTS%%', json.dumps(texts, ensure_ascii=False))
assert '</script' not in json.dumps(texts, ensure_ascii=False)
open(OUT + 'index.html', 'w', encoding='utf-8').write(t)
for n, _ in M['thumbs']: subprocess.run(['cp', f'{D}thumb/out4/thumb_{n}.jpg', OUT])   # v4: наклейка шортсов, плотный кадр
print(len(parts), 'кусков', sum(p['size'] for p in parts) / 1048576, 'МБ; md5 ok')
for k, v in texts: print('-', k, len(v))
