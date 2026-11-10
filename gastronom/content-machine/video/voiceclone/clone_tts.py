#!/usr/bin/env python3
"""Бесплатная озвучка голосом Михалыча: локальный клон Alexey на Chatterbox Multilingual (Resemble AI, MIT).

    cbx_env/bin/python voiceclone/clone_tts.py --project water --ref voiceclone/ref_alexey.wav --take c [--ids G7 B5 ...]

Образец голоса — одна чистая реплика Alexey ~10 с (уже оплаченная, новых трат нет). Ударения ставятся сами:
берётся `stressed` из qa_out/textgate.json (RUAccent, «+» перед гласной) и переводится в знак ударения U+0301,
который модель понимает. Пишет <проект>/vo_takes/<id>_<take>.wav — дальше обычный voiceqa и vopost.
"""
import sys, os, json, re, time, argparse, importlib.util
import torch, torchaudio

VOW = 'аеиоуыэюяАЕИОУЫЭЮЯ'


ACUTE = chr(0x301)


def plus_to_acute(s):
    """«+» перед гласной → гласная + знак ударения U+0301. В словах с одной гласной знак снимается: RUAccent ставит
    его и на предлоги («н+а километр», «а н+е на воде»), и клон тогда бьёт ударение в предлог."""
    def word(m):
        w = m.group(0)
        if sum(ch in VOW for ch in w) <= 1: return w.replace('+', '')
        return re.sub(r'\+([%s])' % VOW, lambda v: v.group(1) + ACUTE, w).replace('+', '')
    return re.sub(r'[\w+]+', word, s)


def load_lines(project):
    spec = importlib.util.spec_from_file_location('script', os.path.join(project, 'script.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return list(m.LINES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--ref', required=True)
    ap.add_argument('--take', default='c')
    ap.add_argument('--ids', nargs='*')
    ap.add_argument('--exaggeration', type=float, default=0.5)
    ap.add_argument('--cfg', type=float, default=0.5)
    ap.add_argument('--temperature', type=float, default=0.8)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--no-stress', action='store_true', help='не ставить ударения из textgate')
    a = ap.parse_args()

    torch.set_num_threads(os.cpu_count() or 4)
    import chatterbox.models.tokenizers.tokenizer as tk
    tk.add_russian_stress = lambda t: t           # ударения даём сами (RUAccent), без внешнего пакета
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS

    lines = load_lines(a.project)
    tg = os.path.join(a.project, 'qa_out', 'textgate.json')
    stressed = {r['id']: r.get('stressed') for r in json.load(open(tg))} if os.path.exists(tg) else {}
    # <проект>/stress.json — ударения марок и имён, которые RUAccent угадывает неверно: {"камри": "К+амри", ...}
    sf = os.path.join(a.project, 'stress.json')
    fix = json.load(open(sf, encoding='utf-8')) if os.path.exists(sf) else {}
    def apply_fix(s):
        def w(m):
            t = m.group(0); k = t.replace('+', '').lower()
            if k not in fix: return t
            v = fix[k]; return v[0].upper() + v[1:] if t.replace('+', '')[:1].isupper() else v[0].lower() + v[1:]
        return re.sub(r'[\w+]+', w, s)
    stressed = {k: apply_fix(v) if v else v for k, v in stressed.items()}
    ids = a.ids or [i for i, _ in lines]
    out_dir = os.path.join(a.project, 'vo_takes'); os.makedirs(out_dir, exist_ok=True)

    t0 = time.time()
    model = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
    model.prepare_conditionals(a.ref, exaggeration=a.exaggeration)
    print(f'model+ref {time.time() - t0:.0f} s', flush=True)

    for lid, text in lines:
        if lid not in ids: continue
        src = text if a.no_stress or not stressed.get(lid) else plus_to_acute(stressed[lid])
        torch.manual_seed(a.seed)
        t1 = time.time()
        wav = model.generate(src, language_id='ru', exaggeration=a.exaggeration, cfg_weight=a.cfg,
                             temperature=a.temperature)
        out = os.path.join(out_dir, f'{lid}_{a.take}.wav')
        torchaudio.save(out, wav, model.sr)
        print(f'{lid}: {wav.shape[-1] / model.sr:.1f} s audio, {time.time() - t1:.0f} s -> {out}', flush=True)


if __name__ == '__main__':
    main()
