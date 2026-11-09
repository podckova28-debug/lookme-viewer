#!/usr/bin/env python3
"""Автопроверка ролика целиком: текст → голос → картинка → рендер → отчет и решение «можно выпускать / нельзя».

    python3 qa/run.py --project <папка ролика> [--stage text,voice,visual,render] [--takes vo_takes] [--video final.mp4]
                      [--out <папка>/qa_out] [--force]

Папка ролика (как в winter/): script.py (LINES) или jobs.txt шортса, vo_takes/<id>_<дубль>.mp3|wav (или vo/<id>.wav), kf/*.png, clips/*.mp4,
cut.py + timeline.py + gfx.py, готовый ролик *_1080p.mp4. Состав кадров — shots.json ({"frames": {имя: {"cast": [...]}}})
или prompts.json ({имя: промпт}), из которого состав строится по ключевым словам.

Порядок: text блокирует синтез (код 1, пока сценарий не чист; --force — дальше несмотря на блок). voice выбирает
дубль на каждую реплику и пишет список переозвучки. visual проверяет кадры и клипы. render проверяет плашки, шрифты, звук.
Итог — qa_out/report.md, report.json и review.json. В review.json каждый флаг «на разбор» и каждая полоса клипа
ждут вердикта: "ok", "bad" (с note) или для ошибки "waive" (с note, почему допустимо). Решение «МОЖНО» —
только когда ошибок нет (или каждая снята waive) и у каждого пункта разбора есть вердикт.
Коды выхода: 0 — можно выпускать, 1 — есть ошибки, 2 — ждет разбора.
"""
import sys, os, json, subprocess, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PY_TEXT, PY_ML = 'python3.11', 'python3.13'
CLIP_CHECK = ('предметы не появляются и не исчезают; руки и пальцы целы; физика как в сценарии (стекло, снег, вода, дым); '
              'лицо и одежда персонажа не плывут; последние кадры не ломаются — иначе вердикт bad и `to` (секунда обрезки)')


def sh(cmd, log):
    with open(log, 'w', encoding='utf-8') as f:
        return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode


def first(*paths):
    return next((p for p in paths if p and os.path.exists(p)), None)


def manifest(proj, out):
    m = first(os.path.join(proj, 'shots.json'))
    if m: return m
    p = first(os.path.join(proj, 'prompts.json'))
    if not p: return None
    code = (f"import sys,json; sys.path.insert(0,{HERE!r}); import visualqa as V; "
            f"P=json.load(open({p!r},encoding='utf-8')); M=V.make_manifest(P); "
            f"json.dump(dict(frames=M, clips={{k: v for k, v in M.items()}}), open({os.path.join(out, 'shots_auto.json')!r},'w',encoding='utf-8'), ensure_ascii=False, indent=1)")
    subprocess.run([PY_ML, '-c', code], check=True)
    return os.path.join(out, 'shots_auto.json')


def load(p):
    return json.load(open(p, encoding='utf-8')) if p and os.path.exists(p) else None


def items(out):
    """Все флаги всех этапов в одном списке: (этап, объект, уровень, текст, картинка)."""
    R = []
    tg = load(os.path.join(out, 'textgate.json')) or []
    for r in tg:
        for x in r['issues']:
            if x['level'] == 'block': R.append(('text', r['id'], 'fail', f"«{x['word']}» — {x['msg']}" + (f" → {x['fix']}" if x.get('fix') else ''), None))
    vq = load(os.path.join(out, 'voice.json'))
    if vq:
        for lid, msgs in vq['retake'].items():
            R.append(('voice', lid, 'fail', 'переозвучить: ' + ' | '.join(msgs), None))
    vis = load(os.path.join(out, 'visual.json'))
    if vis:
        for k, v in vis['frames'].items():
            for z in v['issues']:
                R.append(('frame', k, z['level'], z['msg'], f'pack/frame_{k}.jpg'))
        for k, v in vis['clips'].items():
            for z in v['issues']:
                R.append(('clip', k, z['level'], z['msg'] + (f" (обрезать до {z['to']} с)" if 'to' in z else ''), f'pack/clip_{k}.jpg'))
            R.append(('clip', k, 'review', 'полоса кадров — разбор по чек-листу', f'pack/clip_{k}.jpg'))
    rq = load(os.path.join(out, 'render.json'))
    if rq:
        for z in rq['issues']:
            R.append(('render', z.get('what', z['code']), z['level'], z['msg'], f"pack/{z['image']}" if z.get('image') else None))
    return R


def key(it): return f"{it[0]}:{it[1]}:{it[3][:60]}"


def required(proj, out, script, takes, video):
    """Этапы, без которых решение «можно» не выносится: отсутствие результата — ошибка, а не «чисто»."""
    miss = []
    tg = load(os.path.join(out, 'textgate.json'))
    if not script: miss.append(('text', '—', 'fail', 'нет сценария: script.py со списком LINES = [(id, текст), …]', None))
    elif not tg: miss.append(('text', '—', 'fail', 'текст не проверен или сценарий пуст (0 реплик)', None))
    if takes and not os.path.exists(os.path.join(out, 'voice.json')): miss.append(('voice', '—', 'fail', 'этап «голос» не выполнен', None))
    if not takes: miss.append(('voice', '—', 'fail', 'нет дублей озвучки (vo_takes/ или vo/)', None))
    if (os.path.isdir(os.path.join(proj, 'kf')) or os.path.isdir(os.path.join(proj, 'clips'))) and not os.path.exists(os.path.join(out, 'visual.json')):
        miss.append(('frame', '—', 'fail', 'этап «картинка» не выполнен', None))
    if video and not os.path.exists(os.path.join(out, 'render.json')): miss.append(('render', '—', 'fail', 'этап «рендер» не выполнен', None))
    if not video: miss.append(('render', '—', 'fail', 'нет готового ролика (*_1080p.mp4 или --video)', None))
    return miss


def decide(out, miss=()):
    R = list(miss) + items(out)
    rv_path = os.path.join(out, 'review.json'); rv = load(rv_path) or {}
    for it in R:                                      # заготовка вердиктов для новых пунктов (невыполненный этап не снимается)
        if it[0] in ('voice', 'frame', 'clip', 'render') and it[1] != '—' and key(it) not in rv:
            rv[key(it)] = dict(verdict=None, note='', level=it[2], image=it[4])
    json.dump(rv, open(rv_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fails, pending, bad = [], [], []
    for it in R:
        v = rv.get(key(it), {}).get('verdict')
        if it[2] == 'fail':
            if v == 'waive' and it[1] != '—' and it[0] != 'text' and rv[key(it)].get('note'): continue
            fails.append(it)
        elif it[2] == 'review':
            if v is None: pending.append(it)
            elif v == 'bad': bad.append(it)
    return R, fails + bad, pending


def report(out, proj, R, fails, pending, ran):
    L = [f"# Автопроверка: {os.path.basename(os.path.abspath(proj))}", '', f"{datetime.datetime.now():%d.%m.%Y %H:%M} · этапы: {', '.join(ran)}", '']
    st = 'МОЖНО ВЫПУСКАТЬ' if not fails and not pending else ('НЕЛЬЗЯ: есть ошибки' if fails else 'ЖДЕТ РАЗБОРА')
    L += [f"**Решение: {st}** — ошибок {len(fails)}, ждут разбора {len(pending)}, всего флагов {len(R)}.", '']
    names = dict(text='Текст (до синтеза)', voice='Голос', frame='Кадры', clip='Клипы', render='Рендер')
    for stage in ('text', 'voice', 'frame', 'clip', 'render'):
        f = [it for it in fails if it[0] == stage]; p = [it for it in pending if it[0] == stage]
        if not f and not p: continue
        L += [f"## {names[stage]}", '']
        if stage == 'clip' and p: L += [f"Чек-лист полосы: {CLIP_CHECK}.", '']
        for it in f: L.append(f"- **ОШИБКА {it[1]}**: {it[3]}" + (f" — `{it[4]}`" if it[4] else ''))
        for it in p: L.append(f"- разбор {it[1]}: {it[3]}" + (f" — `{it[4]}`" if it[4] else ''))
        L.append('')
    vq = load(os.path.join(out, 'voice.json'))
    if vq: L += ['## Выбранные дубли', '', ', '.join(f"{k}: {v}" for k, v in vq['picks'].items()), '']
    open(os.path.join(out, 'report.md'), 'w', encoding='utf-8').write('\n'.join(L))
    json.dump(dict(decision=st, fails=[list(x) for x in fails], pending=[list(x) for x in pending], all=[list(x) for x in R]),
              open(os.path.join(out, 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return st


def main():
    args = sys.argv[1:]
    def opt(n, d=None):
        if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    proj = os.path.abspath(opt('--project', '.')); stages = opt('--stage', 'text,voice,visual,render').split(',')
    out = os.path.abspath(opt('--out', os.path.join(proj, 'qa_out'))); force = '--force' in args
    os.makedirs(os.path.join(out, 'pack'), exist_ok=True)
    script = first(os.path.join(proj, 'script.py'), os.path.join(proj, 'jobs.txt'))   # шортсы: строки «vo m01 <uuid> текст»
    takes = first(opt('--takes'), os.path.join(proj, 'vo_takes'), os.path.join(proj, 'vo'))
    video = first(opt('--video'), *sorted(glob.glob(os.path.join(proj, '*_1080p.mp4'))), os.path.join(proj, 'final.mp4'),
                  *sorted(glob.glob(os.path.join(proj, '*_final.mp4'))), *sorted(glob.glob(os.path.join(proj, 'short_v*.mp4')))[-1:])
    ran = []
    if 'text' in stages and script:
        rc = sh([PY_TEXT, os.path.join(HERE, 'textgate.py'), script, '--json', os.path.join(out, 'textgate.json')], os.path.join(out, 'textgate.log'))
        ran.append('text'); print('текст:', 'БЛОК — исправить сценарий до синтеза' if rc else 'чисто', flush=True)
        if rc and not force:
            R, fails, pending = decide(out); print(report(out, proj, R, fails, pending, ran)); print('Отчет:', os.path.join(out, 'report.md')); sys.exit(1)
        if not rc and not (load(os.path.join(out, 'textgate.json')) or []):
            print('текст: 0 реплик — проверь script.py', flush=True)
    if 'voice' in stages and script and takes:
        sh([PY_ML, os.path.join(HERE, 'voiceqa.py'), '--lines', script, '--takes', takes, '--risk', os.path.join(out, 'textgate.json'),
            '--out', os.path.join(out, 'voice.json')], os.path.join(out, 'voice.log'))
        ran.append('voice'); print('голос: готово', flush=True)
    if 'visual' in stages:
        cmd = [PY_ML, os.path.join(HERE, 'visualqa.py'), '--out', os.path.join(out, 'visual.json'), '--pack', os.path.join(out, 'pack')]
        if os.path.isdir(os.path.join(proj, 'kf')): cmd += ['--frames', os.path.join(proj, 'kf')]
        if os.path.isdir(os.path.join(proj, 'clips')): cmd += ['--clips', os.path.join(proj, 'clips')]
        m = manifest(proj, out)
        if m: cmd += ['--manifest', m]
        sh(cmd, os.path.join(out, 'visual.log')); ran.append('visual'); print('картинка: готово', flush=True)
    if 'render' in stages and (os.path.exists(os.path.join(proj, 'cut.py')) or video):
        cmd = [PY_ML, os.path.join(HERE, 'renderqa.py'), '--project', proj, '--out', os.path.join(out, 'render.json'), '--pack', os.path.join(out, 'pack')]
        if video: cmd += ['--video', video]
        sh(cmd, os.path.join(out, 'render.log')); ran.append('render'); print('рендер: готово', flush=True)
    R, fails, pending = decide(out, required(proj, out, script, takes, video))
    st = report(out, proj, R, fails, pending, ran)
    print(f"{st}: ошибок {len(fails)}, ждут разбора {len(pending)}. Отчет: {os.path.join(out, 'report.md')}")
    sys.exit(0 if not fails and not pending else (1 if fails else 2))


if __name__ == '__main__':
    main()
