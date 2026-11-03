"""Build every episode 1 artifact from tools/ep01_data.py.

Outputs (paths relative to the repo root):
  ep01_ready/e01_bNN.txt   full prompt per block, paste as is
  ep01_ready/README.md     reference images per block, in order
  ep01_blocks_web.md       human-readable block list
  script_ep01_spider.md    script v2: logline, looks, narration per block
  board/blocks.json        data for the production board page
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from ep01_data import B, LOOKS, LOOK_NEG, PLATES, SHEETS, INSERTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

STYLE = ("Style: hand-drawn 2D 1990s feature animation, clean confident ink lines, soft painted cel shading, "
         "warm painted backgrounds with depth, caricatured expressive faces with tired eye bags, satirical adult "
         "webcomic edge; simple limited animation on twos. The visual style, characters, room and palette are "
         "EXACTLY as in the reference images.")
LOCK = ("PALETTE LOCK: use only the colors and background treatment of the references. Do not introduce new "
        "colors. Characters look exactly like their sheets in every shot: same face, hair, clothes.")
RULES = ("A single 10-second scene of FIVE hard-cut shots at 2.0s, 4.0s, 6.0s and 8.0s, no dissolves. Do not "
         "open on a reference image. Characters only emote and gesture, they do NOT talk. Motion starts on "
         "frame 1. ONE action per shot. Static camera unless a shot says otherwise. Anything stuck to the hero "
         "is always joined to him by a clearly visible white sticky web blob. White web blobs appear ONLY where a "
         "shot says something is stuck; never on his shirt, chest, backpack, clothes, walls or props otherwise.")
NEG = ("NEGATIVE: opening on a reference sheet, leading freeze, dissolves, new colors, recolored clothes, "
       "{extra}full superhero suit, face mask, extra people, duplicated characters, {dave}morphing faces, extra "
       "fingers, twisted limbs, rude hand gestures, a raised middle finger, a second phone, a landline phone, any phone on the kitchen counter, "
       "talking, lip-sync, on-screen text, captions, photorealism, 3D render, watermark{tail}.")
NIGHTSTAND = 'The nightstand holds only a lamp and a white mug, no phone of any kind on it. '
DIRECTION = ('SCREEN DIRECTION LOCK: the yellow school bus always faces and moves from screen LEFT to screen RIGHT, '
             'seen from the side; it never drives toward the camera, away from the camera or backwards.')
MIRROR = ('MIRROR RULE: a mirror or glass only reflects what stands in front of it. The hero is a real person standing in the '
          'room: whenever his reflection is seen, his real body (back, shoulder or side) is also in the frame in front of the glass. '
          'The camera is never inside or behind the mirror.')
START = ('START FRAME: SHOT 1 begins exactly on the provided start frame and continues its action with the same '
         'framing, position and light.')

def sheet_desc(key, look):
    if key.startswith('hero_'):
        lk = {'hero_home': 'home', 'hero_interview': 'interview', 'hero_costume': look if look.startswith('costume') else 'costume'}[key]
        return LOOKS[lk]
    return SHEETS[key]

def build_prompt(b):
    refs = [f"@Image1 = LOCATION ({PLATES[b['plate']]})."]
    for i, k in enumerate(b['sheets']):
        refs.append(f"@Image{i+2} = {sheet_desc(k, b['look'])}.")
    extra = LOOK_NEG[b['look']]
    pre = NIGHTSTAND if b['plate'] in ('01_bedroom', '12_bedroom_night') else ''
    extra_rules = []
    if b['plate'] == '10_bus_street' and 'bus' in b['shots']:
        extra_rules.append(DIRECTION)
    if re.search(r'mirror|reflection|glass door', b['shots']):
        extra_rules.append(MIRROR)
    if b.get('chain_from'):
        extra_rules.append(START)
    return '\n'.join([
        STYLE, LOCK, 'REFERENCES: ' + ' '.join(refs), RULES, *extra_rules,
        pre + b['shots'],
        'AUDIO: ' + b['audio'] + ' No voice, no narration, no music.',
        NEG.format(dave='Dave with hair, Dave looking like the hero, ' if 'dave' in b['sheets'] else '', extra=(extra + ', ') if extra else '', tail=', a reflection with nobody standing in front of the mirror' if re.search(r'mirror|reflection|glass door', b['shots']) else ''),
    ]) + '\n'

def files_for(b):
    return ['plates/' + b['plate'] + '.png'] + ['sheets/' + k + '.png' for k in b['sheets']]

os.makedirs('ep01_ready', exist_ok=True)
for f in os.listdir('ep01_ready'):
    os.remove(os.path.join('ep01_ready', f))
board = []
idx = ['# Серия 1, готовые промпты, версия 2', '',
       'Файл блока вставляется в поле промпта Seedance 2.5 целиком. Картинки прикладываются в указанном порядке. '
       'Настройки: 720p, 16:9, 10 секунд, звук включён, Unlimited включён, на кнопке 0 кредитов.', '',
       '| Блок | Сцена | Картинки по порядку |', '|---|---|---|']
for b in B:
    p = build_prompt(b)
    if b['id'] != '01':
        open(f"ep01_ready/e01_b{b['id']}.txt", 'w', encoding='utf-8').write(p)
    start = f"стартовый кадр: последний кадр блока {b['chain_from']}, " if b.get('chain_from') else ''
    idx.append(f"| {b['id']} | {b['title']} | " + start + ', '.join(f'`{x}`' for x in files_for(b)) + ' |')
    board.append({'id': b['id'], 'title': b['title'], 'files': files_for(b), 'prompt': p,
                  'vo_en': b['vo_en'], 'vo_ru': b['vo_ru'], 'accepted': b['id'] == '01',
                  'chain_from': b.get('chain_from')})
open('ep01_ready/README.md', 'w', encoding='utf-8').write('\n'.join(idx) + '\n')
os.makedirs('board', exist_ok=True)
json.dump({'blocks': board, 'inserts': INSERTS}, open('board/blocks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# human block list
L = ['# Серия 1, 54 блока для Seedance 2.5, версия 2', '',
     'Источник правды: `tools/ep01_data.py`. Этот файл, готовые промпты и доска собираются из него скриптом `tools/build_ep01.py`. Править блоки только там.', '',
     'Блоки пронумерованы в порядке монтажа. Блок 01 принят, генерация `325ac9b5`.', '']
for b in B:
    L += [f"**b{b['id']}** · {b['title']} · `{b['plate']}` · " + ', '.join(f'`{k}`' for k in b['sheets']), b['shots'], 'AUDIO: ' + b['audio'], '']
open('ep01_blocks_web.md', 'w', encoding='utf-8').write('\n'.join(L))

# script v2
acts = {'01': 'Акт 1. Дом', '14': 'Акт 2. Город', '34': 'Акт 3. Спасение', '48': 'Акт 4. Вечер'}
look_ru = {'home': 'дома: футболка, пижама', 'interview': 'на собеседование: рубашка, галстук, рюкзак',
           'costume': 'костюм поверх рубашки, капюшон, очки', 'costume_down': 'костюм, капюшон снят, очки на лбу', 'none': 'героя нет в кадре'}
S = ['# Серия 1. «What If You Woke Up as SPIDER-MAN?» · версия 2', '',
     'Собирается из `tools/ep01_data.py`. Исправлено по разбору от 3 ноября: у героя есть цель, костюм логичен, в кульминации есть выбор и ставка, гэги разнообразнее, предметы не исчезают.', '',
     '## Логлайн', '',
     'Безработный парень просыпается с силами паука в день первого за год собеседования. Он весь день пытается добраться до офиса незаметно, а у самой двери выбирает спасти от автобуса старушку, которую сам утром приклеил к фонарю. Собеседование потеряно, в новостях хвалят водителя, а ночью чутьё срабатывает снова.', '',
     '## Правила серии', '',
     '- Рассказчик говорит с героем на «ты». Персонажи не говорят.',
     '- Дэйв ничему не удивляется и всегда помогает молча.',
     '- Каждый прилипший предмет отлипает в том же блоке. Исключения: телефон на потолке до конца серии, кофе в руке героя с 19 по 46 блок.',
     '- Монтажный стык между блоками всегда меняет крупность плана, если это та же комната и тот же персонаж.',
     '- С блока 21 в руке героя только белый стакан с коричневой манжетой, маффин и банка остаются на стойке.',
     '- Погоня 34 → 36 → 37 → 38 генерируется цепочкой: последний кадр предыдущего блока идёт стартовым кадром следующего. Эти блоки запускаются по одному.',
     '- Силы показаны все: липкость, стены, чутьё (блоки 03, 20, 32, 53), реакция (07, 26), сила (13, 22, 36).', '',
     '## Вставки, которые делаю я', '']
S += [f'- {a}: {t}' for a, t in INSERTS]
S += ['']
for b in B:
    if b['id'] in acts:
        S += [f"## {acts[b['id']]}", '']
    S += [f"**{b['id']}. {b['title']}** · герой {look_ru[b['look']]}"]
    if b['vo_en']:
        S += [f"> {b['vo_en']}", f"> _{b['vo_ru']}_"]
    else:
        S += ['> без текста, только звук']
    S += ['']
open('script_ep01_spider.md', 'w', encoding='utf-8').write('\n'.join(S))
print('blocks', len(B), 'ready', len(os.listdir('ep01_ready')) - 1)

# ---- long takes: consecutive blocks in one location merged into one 20 - 30 s generation ----
NUM = {2: 'TEN', 3: 'FIFTEEN'}

def groups_of(blocks, size=3):
    out, cur = [], []
    for b in blocks:
        if cur and (b['plate'] != cur[-1]['plate'] or b['look'] != cur[-1]['look'] or len(cur) == size
                    or b.get('chain_from') or cur[-1].get('chain_from')):
            out.append(cur); cur = []
        cur.append(b)
    if cur: out.append(cur)
    return out

def build_long(g):
    if len(g) == 1:
        return None
    sheets = []
    for b in g:
        for k in b['sheets']:
            if k not in sheets: sheets.append(k)
    look = g[0]['look']
    refs = [f"@Image1 = LOCATION ({PLATES[g[0]['plate']]})."] + [f"@Image{i+2} = {sheet_desc(k, look)}." for i, k in enumerate(sheets)]
    n = len(g) * 5
    cuts = ', '.join(f'{t}.0s' for t in range(2, len(g) * 10, 2))
    rules = (f"A single {len(g)*10}-second scene of {NUM[len(g)]} hard-cut shots, a hard cut every 2 seconds at {cuts}, no dissolves. "
             "Do not open on a reference image. Characters only emote and gesture, they do NOT talk. Motion starts on frame 1. "
             "ONE action per shot. Static camera unless a shot says otherwise. Anything stuck to the hero is always joined to him "
             "by a clearly visible white sticky web blob. White web blobs appear ONLY where a shot says something is stuck; never on his shirt, chest, backpack, clothes, walls or props otherwise. Every character and every object keeps the same look in all shots.")
    shots, k = [], 0
    for b in g:
        for part in re.split(r'\s*HARD CUT\.\s*', b['shots'].strip()):
            part = re.sub(r'^SHOT \d+', '', part).strip()
            if part:
                k += 1; shots.append(f'SHOT {k} {part}')
    assert k == n, (g[0]['id'], k)
    extra_rules = []
    if any(b['plate'] == '10_bus_street' and 'bus' in b['shots'] for b in g): extra_rules.append(DIRECTION)
    mirror = any(re.search(r'mirror|reflection|glass door', b['shots']) for b in g)
    if mirror: extra_rules.append(MIRROR)
    pre = NIGHTSTAND if g[0]['plate'] in ('01_bedroom', '12_bedroom_night') else ''
    extra = LOOK_NEG[look]
    return '\n'.join([
        STYLE, LOCK, 'REFERENCES: ' + ' '.join(refs), rules, *extra_rules,
        pre + ' HARD CUT. '.join(shots),
        'AUDIO: ' + ' '.join(b['audio'] for b in g) + ' No voice, no narration, no music.',
        NEG.format(dave='Dave with hair, Dave looking like the hero, ' if 'dave' in sheets else '', extra=(extra + ', ') if extra else '', tail=', a reflection with nobody standing in front of the mirror' if mirror else ''),
    ]) + '\n', ['plates/' + g[0]['plate'] + '.png'] + ['sheets/' + s + '.png' for s in sheets]

os.makedirs('ep01_ready_long', exist_ok=True)
for f in os.listdir('ep01_ready_long'):
    os.remove(os.path.join('ep01_ready_long', f))
long_idx = []
for g in groups_of([b for b in B if b['id'] not in ('01', '02', '03', '04', '05')]):
    r = build_long(g)
    ids = f"{g[0]['id']}-{g[-1]['id']}" if len(g) > 1 else g[0]['id']
    if r:
        open(f'ep01_ready_long/e01_b{ids}.txt', 'w', encoding='utf-8').write(r[0])
        long_idx.append({'ids': ids, 'secs': len(g) * 10, 'files': r[1], 'prompt': r[0], 'blocks': [b['id'] for b in g]})
    else:
        long_idx.append({'ids': ids, 'secs': 10, 'files': files_for(g[0]), 'prompt': None, 'blocks': [g[0]['id']]})
json.dump(long_idx, open('board/long.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('long generations', len(long_idx), 'of which merged', sum(1 for x in long_idx if x['prompt']))
