import json
D='/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/mihalych_cost/'
s=open(D+'page_template.html',encoding='utf-8').read()
d=json.load(open(D+'demo_answer.json',encoding='utf-8'))
rules=open(D+'prompt.md',encoding='utf-8').read().strip()
dc=json.dumps({"where":["Спереди","Справа"],"facts":["Lada Granta, 2017","118 000 км","Казань"]},ensure_ascii=False)
demo=json.dumps(d,ensure_ascii=False)
assert '</script' not in rules+demo
t=s.replace('%%RULES%%',rules).replace('%%DEMO%%',demo).replace('%%DEMOCASE%%',dc)
open(D+'page/mihalych_cost.html','w',encoding='utf-8').write(t)
print('built', len(t))
