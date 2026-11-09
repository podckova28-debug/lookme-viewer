"""Ударения и «ё» по всем репликам (RUAccent): слова со звуком «ё» и омографы."""
import json, re, sys
from ruaccent import RUAccent
acc = RUAccent()
acc.load(omograph_model_size='turbo3.1', use_dictionary=True, tiny_mode=False)
import numpy as np
NOT_IN_DICT = set()
def _patch(model, tag):
    sess = model.session; orig = sess.run; need = {i.name for i in sess.get_inputs()}
    def run(names, feed, *a, **kw):
        feed = {k: v for k, v in dict(feed).items() if k in need}
        if 'token_type_ids' in need and 'token_type_ids' not in feed: feed['token_type_ids'] = np.zeros_like(feed['input_ids'])
        return orig(names, feed, *a, **kw)
    sess.run = run
for name in ('accent_model', 'omograph_model', 'yo_homograph_model', 'stress_usage_predictor'):
    m = getattr(acc, name, None)
    if m is not None and hasattr(m, 'session'):
        try: _patch(m, name)
        except Exception as e: print('patch fail', name, e)
_orig_put = acc.accent_model.put_accent
def put(word):
    NOT_IN_DICT.add(word); return _orig_put(word)
acc.accent_model.put_accent = put
L = json.load(open('work/lines.json'))
out = {}
for k, t in L:
    s = acc.process_all(t); out[k] = s
    yo = re.findall(r"[\w+]*ё[\w+]*", s.replace('+ё', 'ё'), flags=re.I)
    print(k, '|', s, '| Ё:', ', '.join(yo) if yo else '-')
json.dump(out, open('work/stress.json', 'w'), ensure_ascii=False, indent=0)
print('НЕТ В СЛОВАРЕ (ударение угадано нейросетью):', sorted(NOT_IN_DICT))
