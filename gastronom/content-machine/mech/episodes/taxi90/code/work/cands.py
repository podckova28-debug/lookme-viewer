"""Кандидаты для voiceqa: по 2 лучших дубля на реплику по баллам stress_audit (вывод pick_best_take в stdin) + принудительные."""
import ast, os, re, sys, json
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
force = {'E1': ['E1_x.wav'], 'Z4': ['Z4_x.wav'], 'G1': ['G1_x.wav', 'G1_c.wav'], 'A1': ['A1_c.wav'], 'Z2': ['Z2_x.wav'], 'A8': ['A8_c.wav', 'A8_x.wav']}
ban = {'G1_v.wav', 'A1_q.wav', 'A1_y.wav', 'Z4_q.wav', 'A8_q.wav'}
out = os.path.join(D, 'vo_cand'); os.makedirs(out, exist_ok=True)
for f in os.listdir(out): os.remove(os.path.join(out, f))
n = 0
for ln in sys.stdin:
    m = re.match(r'(\w+) → (\S+) .*было: (\{.*\})', ln.strip())
    if not m: continue
    lid, sc = m.group(1), ast.literal_eval(m.group(3))
    order = [f for f in sorted(sc, key=lambda f: sc[f]) if f not in ban]
    sel = list(dict.fromkeys(force.get(lid, []) + order[:2]))
    for f in sel:
        os.symlink(os.path.join(D, 'vo_takes', f), os.path.join(out, f)); n += 1
print('кандидатов', n)
