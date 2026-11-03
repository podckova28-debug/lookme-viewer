"""Build every episode 1 artifact from tools/ep01_data.py.

Outputs (paths relative to the repo root):
  ep01_ready/e01_bNN.txt   full prompt per block, paste as is
  ep01_ready/README.md     reference images per block, in order
  ep01_blocks_web.md       human-readable block list
  script_ep01_spider.md    script v2: logline, looks, narration per block
  board/blocks.json        data for the production board page
"""
import json, os, sys
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
         "frame 1. ONE action per shot. Static camera unless a shot says otherwise.")
NEG = ("NEGATIVE: opening on a reference sheet, leading freeze, dissolves, new colors, recolored clothes, "
       "{extra}full superhero suit, face mask, extra people, duplicated characters, morphing faces, extra "
       "fingers, twisted limbs, a second phone, a landline phone, any object that is not in the references, "
       "talking, lip-sync, on-screen text, captions, photorealism, 3D render, watermark.")
NIGHTSTAND = 'The nightstand holds only a lamp, a white mug and the one black phone. '
DIRECTION = ('SCREEN DIRECTION LOCK: the yellow school bus always faces and moves from screen LEFT to screen RIGHT, '
             'seen from the side; it never drives toward the camera, away from the camera or backwards.')
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
    if b.get('chain_from'):
        extra_rules.append(START)
    return '\n'.join([
        STYLE, LOCK, 'REFERENCES: ' + ' '.join(refs), RULES, *extra_rules,
        pre + b['shots'],
        'AUDIO: ' + b['audio'] + ' No voice, no narration, no music.',
        NEG.format(extra=(extra + ', ') if extra else ''),
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
