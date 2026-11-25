"""Manual review gate: every frame and the final video are looked at by eye and the verdict is recorded with the file's hash.
qc.py refuses to pass while any frame used in the timeline (or the final video) has no 'ok' verdict for its CURRENT file.

Per episode: bible.json (who and what may appear) + review.json (verdicts, written by this tool).

  python3 review.py todo  <timeline.json>                 -> frames still to review: writes review/<frame>_0.jpg (whole frame, 1920x1080)
                                                              and <frame>_1..4.jpg (each quarter enlarged 2x to 1920x1080),
                                                              prints for each: the narration over it, the prompt, the bible checklist
  python3 review.py ok    <timeline.json> <frame> --who hero,mum --where room [--note "..."]
  python3 review.py fix   <timeline.json> <frame> --note "two left hands; regenerate"
  python3 review.py video <timeline.json> <final.mp4>     -> viewer sheets (a still every 2 s + the words heard at that moment)
                                                              in review/video_*.jpg and the viewer checklist
  python3 review.py video_ok <timeline.json> <final.mp4> --note "watched start to end"
  python3 review.py status <timeline.json>

Checklist for every frame (answer all before 'ok'):
  ANATOMY  every person: one head, two arms from the shoulders, two hands, two legs; no extra/merged/floating limbs;
           faces: two eyes, nothing melted; objects held are actually held
  OBJECTS  furniture and props whole and where they were (no doubled mirror, no missing door, no object passing through a body)
  BIBLE    only characters from bible.json, each looking exactly as described there (clothes, hat, hair or no hair);
           nothing from the era's banned list (phones, electric light, modern clothes, wrong buildings, readable text)
  STORY    the frame shows what the narration says at that moment, in the right place and time of day,
           and agrees with the frames before and after (who is where, what they wear, what was already broken/used)
"""
import sys, os, json, hashlib, subprocess, textwrap, wave
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONT = os.path.join(REPO, 'history/fonts/BebasNeue-Regular.ttf')


def sha(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()[:16]


def load(tl_path):
    spec = json.load(open(tl_path)); ep = os.path.dirname(os.path.abspath(tl_path))
    base = os.path.join(REPO, spec['base'])
    rv_path = os.path.join(ep, 'review.json')
    rv = json.load(open(rv_path)) if os.path.exists(rv_path) else {'frames': {}, 'video': {}}
    bible = json.load(open(os.path.join(ep, 'bible.json'))) if os.path.exists(os.path.join(ep, 'bible.json')) else None
    return spec, ep, base, rv, rv_path, bible


def frames_in_order(spec):
    seq = []
    for s in spec['shots']:
        if s['img'] not in [x for x, _ in seq]: seq.append((s['img'], s['t0']))
    return seq


def line_at(spec, t):
    """id and text of the narration playing at time t (needs lines.txt next to the VO files' parent)"""
    cur = None
    for v in spec['vo']:
        if v['t'] <= t + .05: cur = v['file']
    if not cur: return '', ''
    lid = os.path.basename(cur)[:-4]; vdir = os.path.dirname(os.path.join(REPO, cur))
    for cand in (os.path.join(vdir, 'lines.txt'), os.path.join(os.path.dirname(vdir), 'lines.txt')):
        if os.path.exists(cand):
            for l in open(cand):
                p = l.rstrip('\n').split('|', 2)
                if p[0] == lid: return lid, p[2]
    return lid, ''


def prompts(ep):
    """frame id -> prompt, from any *todo*.json / frames_*.json lists in the episode folder"""
    out = {}
    for f in os.listdir(ep):
        if not f.endswith('.json') or f in ('review.json', 'bible.json') or f.startswith('timeline'): continue
        try: d = json.load(open(os.path.join(ep, f)))
        except Exception: continue
        if isinstance(d, list):
            for x in d:
                if isinstance(x, dict) and 'id' in x and 'prompt' in x: out[x['id']] = x['prompt']
        elif isinstance(d, dict) and 'ids' in d:
            reqs = [r for k, v in d.items() if isinstance(v, list) and k != 'ids' for r in v]
            for i, r in zip(d['ids'], reqs):
                try: out[i] = r['params']['prompt']
                except Exception: pass
    return out


def review_sheet(src, dst, title):
    """big-size review: <frame>_0.jpg = the whole frame at 1920x1080, <frame>_1..4.jpg = each quarter enlarged 2x to 1920x1080.
    Look at all five, one by one, at full size: hands, fingers, faces and small objects are only visible enlarged."""
    im = Image.open(src).convert('RGB').resize((1920, 1080), Image.LANCZOS); F = ImageFont.truetype(FONT, 40)
    stem = dst[:-4]; out = []
    def tag(img, t):
        d = ImageDraw.Draw(img); d.rectangle((0, 0, 30 + int(F.getlength(t)), 54), fill='black'); d.text((14, 6), t, fill='white', font=F); return img
    tag(im.copy(), title).save(stem + '_0.jpg', quality=92); out.append(stem + '_0.jpg')
    for k in range(4):
        x, y = (k % 2) * 960, (k // 2) * 540
        q = im.crop((x, y, x + 960, y + 540)).resize((1920, 1080), Image.LANCZOS)
        tag(q, f'{title}  quarter {k + 1}: {["top left", "top right", "bottom left", "bottom right"][k]} x2').save(stem + f'_{k + 1}.jpg', quality=92)
        out.append(stem + f'_{k + 1}.jpg')
    return out


def main():
    cmd, tl = sys.argv[1], sys.argv[2]
    spec, ep, base, rv, rv_path, bible = load(tl)
    opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
    os.makedirs(os.path.join(ep, 'review'), exist_ok=True)
    seq = frames_in_order(spec)
    def path(f): return os.path.join(base, f + '.jpg')
    def state(f):
        r = rv['frames'].get(f)
        if not r: return 'todo'
        if r['sha'] != sha(path(f)): return 'changed'
        return r['verdict']

    if cmd == 'todo':
        P = prompts(ep); n = 0
        if bible: print('BIBLE:', json.dumps(bible, ensure_ascii=False, indent=1)[:4000], '\n')
        for f, t in seq:
            st = state(f)
            if st == 'ok': continue
            n += 1; lid, txt = line_at(spec, t + .5)
            review_sheet(path(f), os.path.join(ep, 'review', f + '.jpg'), f'{f}  {int(t // 60)}:{int(t % 60):02d}  {lid}  [{st}]')
            print(f'--- {f} [{st}] at {t:.1f}s  -> review/{f}_0.jpg (whole) + {f}_1..4.jpg (quarters x2)')
            print('  SAYS :', textwrap.shorten(txt, 220))
            if f in P: print('  ASKED:', textwrap.shorten(P[f], 300))
            if rv['frames'].get(f, {}).get('note'): print('  LAST :', rv['frames'][f]['note'])
        print(f'\n{n} frame(s) to review. Open all five images of each frame (review/<frame>_0..4.jpg) one by one at full size, check ANATOMY, OBJECTS, BIBLE, STORY (see review.py header), then run ok/fix.')

    elif cmd in ('ok', 'fix'):
        f = sys.argv[3]
        if f not in [x for x, _ in seq]: sys.exit(f'{f} is not in the timeline')
        if cmd == 'ok':
            who, where = opt('--who'), opt('--where')
            if who is None or where is None: sys.exit('ok needs --who (characters in the frame, or "none") and --where (location)')
            if bible:
                known = set(bible.get('characters', {})) | {'none', 'extras'}
                bad = [w for w in who.split(',') if w and w not in known]
                if bad: sys.exit(f'{bad} not in bible.json characters {sorted(known)}; add them to the bible first')
                if where not in bible.get('locations', {}) and where != 'diagram': sys.exit(f'{where} not in bible.json locations')
        rv['frames'][f] = {'verdict': cmd, 'sha': sha(path(f)), 'who': opt('--who'), 'where': opt('--where'), 'note': opt('--note') or ''}
        json.dump(rv, open(rv_path, 'w'), indent=1, ensure_ascii=False); print(f, cmd)

    elif cmd == 'video':
        video = sys.argv[3]; out = os.path.join(ep, 'review')
        for f in os.listdir(out):
            if f.startswith('vs_'): os.remove(os.path.join(out, f))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-vf', 'fps=1/2,scale=480:-1', os.path.join(out, 'vs_%04d.jpg')], check=True)
        fs = sorted(f for f in os.listdir(out) if f.startswith('vs_')); F = ImageFont.truetype(FONT, 22)
        for s in range(0, len(fs), 16):
            W = Image.new('RGB', (1920, 4 * 340), 'white'); d = ImageDraw.Draw(W)
            for k, f in enumerate(fs[s:s + 16]):
                tt = (int(f[3:7]) - 1) * 2; x, y = (k % 4) * 480, (k // 4) * 340
                W.paste(Image.open(os.path.join(out, f)), (x, y)); lid, txt = line_at(spec, tt)
                d.text((x + 4, y + 272), f'{tt // 60}:{tt % 60:02d} {lid}', fill='red', font=F)
                d.text((x + 4, y + 295), '\n'.join(textwrap.wrap(txt, 60)[:2]), fill='black', font=F)
            W.save(os.path.join(out, f'video_{s // 16:02d}.jpg'), quality=80)
        for f in fs: os.remove(os.path.join(out, f))
        print(f'review/video_*.jpg written. Look at every sheet as a viewer:\n'
              ' - every 2 s: does the picture show what is being said right now? any frame that only flashes?\n'
              ' - can a newcomer follow it: who is the hero, where and when we are, what changed since the last scene?\n'
              ' - same hero, same places, clothes and props carried over correctly; nothing appears or vanishes\n'
              ' - slow spots (one picture >6 s with nothing new), captions/cards covering faces, text overlapping\n'
              ' - the ending lands; the question for the comments is on screen\n'
              f'then: review.py video_ok {tl} {video} --note "..."')

    elif cmd == 'video_ok':
        video = sys.argv[3]; rv['video'] = {'file': os.path.basename(video), 'sha': sha(video), 'note': opt('--note') or ''}
        json.dump(rv, open(rv_path, 'w'), indent=1, ensure_ascii=False); print('video ok')

    elif cmd == 'status':
        c = {}
        for f, _ in seq: c.setdefault(state(f), []).append(f)
        for k, v in c.items(): print(k, len(v), ' '.join(v) if k != 'ok' else '')


if __name__ == '__main__':
    main()
