#!/usr/bin/env python3.11
"""Текстовый фильтр ДО синтеза: блокирует озвучку, пока в репликах есть то, на чём Alexey ошибается.

    python3.11 textgate.py <script.py | lines.json> [--json out.json]

Блок (код возврата 1): слово со ЗВУКОМ «ё» (по RUAccent, даже если написано через «е»), слово из lexicon.json avoid/replace,
цифры, латиница, тире между словами, знак %, аббревиатуры капсом. Предупреждение: вопрос без «ли» и вопросительного слова
(интонация не поднимется), слово не из словаря RUAccent (ударение угадано — проверить после синтеза), слова lexicon.check,
знак препинания за закрывающей кавычкой, фраза длиннее 28 слов. Рискованные слова (check + не из словаря) выводятся
списком RISK — их потом проверяет voiceqa.py по звуку. Омографы из словаря RUAccent (за́мок/замо́к, сто́ишь/стои́шь,
ча́сти/части́) без предупреждения уходят в поле omographs: voiceqa сверяет их ударение с выбором RUAccent по контексту
со строгим порогом (детектор ударения шумный, а омографов в сценарии десятки).
"""
import sys, json, re, os, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = json.load(open(os.path.join(HERE, 'lexicon.json'), encoding='utf-8'))
QWORDS = {'ли', 'что', 'как', 'какой', 'какая', 'какое', 'какие', 'какую', 'каким', 'где', 'когда', 'почему', 'зачем', 'сколько',
          'кто', 'куда', 'откуда', 'чей', 'чья', 'чье', 'неужели', 'разве', 'чем', 'кого', 'кому', 'чего', 'которую', 'который'}


def load_lines(path):
    if os.path.basename(path).startswith('jobs') and path.endswith('.txt'):          # шортсы: «vo m01 <uuid> текст»
        return [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^vo\s+(\S+)\s+\S+\s+(.+)$', open(path, encoding='utf-8').read(), re.M)]
    if path.endswith('.json'):
        return [tuple(x) for x in json.load(open(path, encoding='utf-8'))]
    spec = importlib.util.spec_from_file_location('script_mod', path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return list(m.LINES)


def lex_match(word, table):
    w = word.lower()
    for k, v in table.items():
        if k.startswith('_'): continue
        if (k.endswith('*') and w.startswith(k[:-1])) or w == k: return k, v
    return None


def ruaccent():
    from ruaccent import RUAccent
    acc = RUAccent(); acc.load(omograph_model_size='turbo3.1', use_dictionary=True, tiny_mode=False)
    for name in ('accent_model', 'omograph_model', 'yo_homograph_model', 'stress_usage_predictor'):
        m = getattr(acc, name, None)
        if m is None or not hasattr(m, 'session'): continue
        sess = m.session; orig = sess.run; need = {i.name for i in sess.get_inputs()}
        def run(names, feed, *a, _o=orig, _n=need, **kw):   # у части моделей лишний/недостающий token_type_ids
            feed = {k: v for k, v in dict(feed).items() if k in _n}
            if 'token_type_ids' in _n and 'token_type_ids' not in feed: feed['token_type_ids'] = np.zeros_like(feed['input_ids'])
            return _o(names, feed, *a, **kw)
        sess.run = run
    guessed = set(); orig_put = acc.accent_model.put_accent
    def put(word):
        guessed.add(word.lower()); return orig_put(word)
    acc.accent_model.put_accent = put
    return acc, guessed


def check(lines):
    acc, guessed = ruaccent()
    report = []
    for lid, text in lines:
        issues = []; risk = set()
        def add(level, code, word, msg, fix=''):
            issues.append(dict(level=level, code=code, word=word, msg=msg, fix=fix))
        guessed.clear()
        stressed = acc.process_all(text)
        for m in re.finditer(r"[\w+]*ё[\w+]*", stressed.replace('+ё', 'ё'), flags=re.I):
            add('block', 'ё', m.group(0).replace('+', ''), 'звук «ё»: Alexey прочитает как «е»', 'переписать без этого слова')
        words = re.findall(r"[А-Яа-яЁёA-Za-z0-9-]+", text)
        low = text.lower()
        for k, v in LEX['replace'].items():
            if k.startswith('_'): continue
            if re.search(r'(?<![а-яё])' + re.escape(k) + r'(?![а-яё])', low): add('block', 'replace', k, v['why'], f"заменить на «{v['to']}»")
        for w in words:
            wl = w.lower()
            hit = lex_match(wl, LEX['avoid'])
            if hit: add('block', 'avoid', w, hit[1]['why'], hit[1].get('fix', ''))
            hit = lex_match(wl, LEX['check'])
            if hit: add('warn', 'check', w, hit[1]['why']); risk.add(wl)
            if re.search(r'\d', w): add('block', 'digits', w, 'цифры: синтез читает непредсказуемо', 'написать словами')
            if re.search(r'[A-Za-z]', w): add('block', 'latin', w, 'латиница', 'написать кириллицей, как произносится')
            if re.fullmatch(r'[А-ЯЁ]{2,}', w): add('block', 'abbr', w, 'аббревиатура капсом', 'расшифровать словами')
        if re.search(r'\s[—–-]\s|[—–]', text): add('block', 'dash', '—', 'тире: пауза непредсказуема, фразы слипаются', 'точка, запятая или двоеточие')
        if '%' in text: add('block', 'percent', '%', 'знак процента', '«процентов» словом')
        for g in sorted(guessed):
            if len(re.findall('[аеёиоуыэюя]', g)) >= 2:
                add('warn', 'not_in_dict', g, 'нет в словаре RUAccent, ударение угадано', 'проверить по звуку после синтеза'); risk.add(g)
        for s in re.split(r'(?<=[.!?])\s+', text):
            if s.endswith('?'):
                ws = set(re.findall(r'[а-яё]+', s.lower()))
                if not ws & QWORDS: add('warn', 'question', s[:40], 'вопрос без «ли» и вопросительного слова: интонация не поднимется', 'добавить «ли» или вопросительное слово')
            if len(s.split()) > 28: add('warn', 'long', s[:40], f'фраза из {len(s.split())} слов', 'разбить на две')
        if re.search(r'[»"][.,:;!?]', text): add('warn', 'quote_punct', '»', 'знак после кавычки: паузу ставить вручную (gapfix NATURAL)')
        omo = {w.lower() for w in words if (w.lower() in acc.omographs or w.lower() in acc.yo_homographs)
               and len(re.findall('[аеёиоуыэюя]', w.lower())) >= 2} - risk
        report.append(dict(id=lid, text=text, stressed=stressed, issues=issues, risk=sorted(risk), omographs=sorted(omo)))
    return report


if __name__ == '__main__':
    args = sys.argv[1:]; out = None
    if '--json' in args: i = args.index('--json'); out = args[i + 1]; del args[i:i + 2]
    rep = check(load_lines(args[0]))
    nb = sum(1 for r in rep for x in r['issues'] if x['level'] == 'block'); nw = sum(1 for r in rep for x in r['issues'] if x['level'] == 'warn')
    for r in rep:
        for x in r['issues']:
            print(f"{'БЛОК' if x['level'] == 'block' else 'внимание'} {r['id']}: «{x['word']}» — {x['msg']}" + (f" → {x['fix']}" if x['fix'] else ''))
    print(f"\nИтог: {len(rep)} реплик, блокирующих {nb}, предупреждений {nw}. Рискованные слова для проверки по звуку: "
          + ', '.join(f"{r['id']}:{'/'.join(r['risk'])}" for r in rep if r['risk']))
    if out: json.dump(rep, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if nb else 0)
