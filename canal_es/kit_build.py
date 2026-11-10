import re, html, sys
md = open('/home/user/lookme-viewer/canal_es/ep01_detener_el_tiempo.md', encoding='utf-8').read()
secs = re.split(r'^### ', md, flags=re.M)[1:]
out = []
for sec in secs:
    sec = sec.split('\n---\n')[0]
    lines = sec.splitlines()
    head = lines[0]
    m = re.match(r'(\d+)\. (.+) · (\d+:\d\d)', head)
    num, name, tc = m.groups()
    pic = ''; es = []; ru = ''; card = ''
    for l in lines[1:]:
        if l.startswith('**Картинка:**'): pic = l.replace('**Картинка:**','').strip()
        elif l.startswith('> ') and l[2:].strip(): es.append(('n', l[2:].strip()))
        elif re.match(r'\*\*(VALERIA|TÚ):\*\*', l):
            who, txt = re.match(r'\*\*(VALERIA|TÚ):\*\* (.+)', l).groups(); es.append((who, txt))
        elif l.startswith('_') and l.endswith('_'): ru = l.strip('_')
        elif l.startswith('**Карточка:**'): card = l.replace('**Карточка:**','').strip()
        elif l.startswith('Карточка:'): card = l.replace('Карточка:','').strip()
    E = html.escape
    esh = ''.join(f'<p class="es">{E(t)}</p>' if w=='n' else f'<p class="es line"><b>{E(w)}</b> {E(t)}</p>' for w,t in es)
    body = (f'<p class="pic">{E(pic)}</p>' if pic else '') + (f'<div class="esbox" lang="es">{esh}</div>' if es else '') + \
           (f'<p class="ru">{E(ru)}</p>' if ru else '') + (f'<p class="card">{E(card)}</p>' if card else '')
    out.append(f'<details class="scene"><summary><span class="tc">{tc}</span><span class="sn">{num}</span><span class="st">{E(name)}</span></summary><div class="sb">{body}</div></details>')
tpl = open('/home/user/lookme-viewer/canal_es/kit_template.html', encoding='utf-8').read()
open('/home/user/lookme-viewer/canal_es/kit.html','w',encoding='utf-8').write(tpl.replace('{{SCENES}}', '\n'.join(out)))
print(len(out), 'scenes')
