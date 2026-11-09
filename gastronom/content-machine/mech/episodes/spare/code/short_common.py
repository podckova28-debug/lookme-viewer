"""Общая сборка таймлайна дешёвых шортсов эп. 25–27: кадры с движением камеры + один клип-хук петлёй в финале.
Двухпроходно: python build_tl.py → words.py timeline.json → python build_tl.py (слова для ярлыков и склеек)."""
import json, sys
sys.path.insert(0, '/home/user/gastronom/content-machine/video')
import animatic as A
Y = [255, 208, 40]; RED = [208, 60, 40]; BLUE = [40, 110, 190]; GREEN = [46, 140, 76]
TEMPO = 1.07
PAD = [0.02, 0.14]

def build(out, beats, keys, extras):
    tl = dict(out=out, voice_tempo=TEMPO, xfade=0.2, music=dict(file='music/bg.m4a', gain=0.16, duck=0.6), sfx_gain=0.7,
              subs=dict(y=1330, size=100, keys={k: Y for k in keys}), beats=beats)
    words = {}
    try:
        old = json.load(open('timeline.json', encoding='utf-8'))
        if old.get('voice_tempo') == TEMPO: words = {b['voice']: b['words'] for b in old['beats'] if b.get('words')}
    except Exception: pass
    for b in beats:
        if b['voice'] in words:
            ws = [[w, s, e] for w, s, e in words[b['voice']]]
            for k, wd in enumerate(ws):
                if k == 0 or ws[k - 1][0].endswith(('.', '?', '!', ':')): wd[0] = wd[0][:1].upper() + wd[0][1:]
            b['words'] = ws
    if all(b.get('words') for b in beats):
        def at(i, word):
            ws = [w for w in beats[i]['words'] if word in w[0].lower()]
            return round(ws[0][1] + beats[i]['pad'][0], 2) if ws else None
        def blen(i): return len(A.read_audio(beats[i]['voice'], TEMPO)) / A.SR + sum(beats[i]['pad'])
        def split(i, word):
            t = at(i, word); T = blen(i)
            if t is None: print('нет слова', i, word); return None
            beats[i]['shots'][0]['w'] = round(t - 0.05, 2); beats[i]['shots'][1]['w'] = round(T - t + 0.05, 2); return t
        def tag(i, text, word, pos, target, angle=-5, sfx='pop', until=None):
            t = at(i, word)
            if t is None: print('нет слова', i, word); return
            beats[i].setdefault('text', []).append(dict(kind='tag', text=text, size=72, pos=pos, target=target, angle=angle, at=t, **({'until': until} if until else {})))
            beats[i].setdefault('sfx', []).append(dict(file=f'sfx/{sfx}.mp3', at=t, gain=0.28))
        def sticker(i, big, small, color, at_s=0.3, until=None):
            beats[i]['text'] = beats[i].get('text', []) + [dict(kind='sticker', big=big, small=small, color=color, pos=[540, 330],
                                                                 at=at_s, until=round(until if until is not None else blen(i) - 0.02, 2))]
        extras(dict(at=at, blen=blen, split=split, tag=tag, sticker=sticker))
        fit_clips(beats, blen)
    json.dump(tl, open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('слова есть' if all(b.get('words') for b in beats) else 'нужен words.py')

def clip_len(path, c):
    import subprocess
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)
    return min(d, c.get('to', d)) - c.get('ss', 0)

def fit_clips(beats, blen):
    """Клип короче своего плана замедляется (не ниже 0,62), чтобы не замирать в конце; pingpong и явный speed не трогаем."""
    for i, b in enumerate(beats):
        T = blen(i); ws = [s.get('w', 1) for s in b['shots']]
        for s, w in zip(b['shots'], ws):
            if 'clip' not in s or s.get('pingpong'): continue
            if s.get('fixed'):
                if 'to' in s: s['to'] = round(s['to'] / s.get('speed', 1.0), 3)
                continue
            d = T * w / sum(ws) + 0.15; L = clip_len(s['clip'], s) * (2 if s.get('pingpong') else 1)
            s['speed'] = round(max(0.62, min(1.0, L / d)), 3)
            if 'to' in s: s['to'] = round(s['to'] / s['speed'], 3)  # в animatic.py to — секунды уже замедленного клипа

def clip(path, **kw):
    return dict(clip=path, cut=True, **kw)

def hook(voice, title, clip='clips/c1_hook.mp4'):
    return dict(voice=voice, pad=[0.05, 0.14], shots=[dict(clip=clip)],
                text=[dict(kind='title', text=title, size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0, until=2.8)],
                sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.25)])

def outro(voice, title, clip='clips/c1_hook.mp4'):
    return dict(voice=voice, pad=[0.02, 0.9], shots=[dict(clip=clip, cut=True)],
                text=[dict(kind='title', text=title, size=96, box=1000, plate=True, color=RED, pos=[540, 300], at=0.0)],
                sfx=[dict(file='sfx/whoosh.mp3', at=0, gain=0.2)])

def still(img, move='in', focus=(0.5, 0.5), amount=0.08):
    return dict(img=img, move=move, focus=list(focus), amount=amount, cut=True)
