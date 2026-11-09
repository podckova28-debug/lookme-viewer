"""Render board/index.html from board/template.html and board/blocks.json, listing which images exist."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
data = json.load(open('board/blocks.json', encoding='utf-8'))
need = sorted({p for b in data['blocks'] for p in b['files']})
have = [p for p in need if os.path.exists(os.path.join('assets/styleB', p))]
SHEET = ("Character model sheet in EXACTLY the same hand-drawn 2D 1990s feature animation style as the references: "
         "clean confident ink lines, soft painted cel shading, caricatured expressive faces with tired eye bags. "
         "The SAME scruffy guy as in the character sheet (same face, messy brown hair, stubble, same body), dressed "
         "for a job interview: slightly wrinkled white button-up shirt, thin dark navy tie, charcoal gray slacks, "
         "black and white sneakers, a black backpack on his back. Plain warm cream background, 16:9. Left: three "
         "full-body views side by side: front, three-quarter, side. Right: six head-and-shoulders expressions: "
         "hopeful, nervous, panicked, proud, deadpan, defeated. No text, no labels.")
html = open('board/template.html', encoding='utf-8').read()
html = (html.replace('__DATA__', json.dumps(data, ensure_ascii=False))
            .replace('__HAVE__', json.dumps(have))
            .replace('__SHEET_PROMPT__', json.dumps(SHEET)))
open('board/index.html', 'w', encoding='utf-8').write(html)
print('images needed', len(need), 'present', len(have), 'missing', [p for p in need if p not in have])
