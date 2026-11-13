import json, re, os, base64, subprocess, html, io
from PIL import Image
S='/tmp/claude-0/-home-user-lookme-viewer/e992fbdd-0cb2-5f9b-a522-ccd10e99c7b7/scratchpad'
CF='https://d2ol7oe51mr4n9.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/'
E=[ # n, dir, mp4 name, cloudfront id, thumbs, note
 (1,'ep1_qa','Why_Its_So_Hard_To_Be_A_Nurse','bd39e3d9-0b66-44d4-9f28-ee3a3eea209a',['thumb_A_saves_lives','thumb_B_room4','thumb_C_no_bathroom'],'Пилот, 2 минуты.'),
 (2,'ep2','Why_Its_So_Hard_To_Be_A_Delivery_Courier','7006c9c2-7065-47f9-8e11-c19687970552',['thumb_A_14floors','thumb_B_fivestars'],''),
 (3,'ep3','Why_Its_So_Hard_To_Be_A_Teacher','b30cd5a4-1e71-4b65-95b3-05fec314a3ff',['thumb_A_notebooks','thumb_B_markers'],''),
 (4,'ep4','Why_Its_So_Hard_To_Be_A_Line_Cook','3143d483-687d-43ac-a838-b45a0a1600ab',['thumb_A_tickets','thumb_B_salmon'],''),
 (5,'ep5','Why_Its_So_Hard_To_Be_A_Truck_Driver','5a3eb9a2-8049-4790-b6f3-f42e81320740',['thumb_A_parking','thumb_B_detention'],''),
 (6,'ep6','Why_Its_So_Hard_To_Be_A_Flight_Attendant','3fadb813-18da-4ca2-af45-08992d2c376e',['thumb_A_boarding','thumb_B_turbulence'],''),
 (7,'ep7','Why_Its_So_Hard_To_Be_A_Firefighter','74e4f162-d06d-4844-8231-74ff5f7b46e9',['thumb_A_battery','thumb_B_one_in_27'],''),
 (8,'ep8','Why_Its_So_Hard_To_Be_A_Construction_Worker','0d5306e3-b3ec-417c-ad16-2b481eb0588e',['thumb_A3_you_are_the_elevator','thumb_B3_109_ladders'],''),
 (10,'ep10','Why_Its_So_Hard_To_Be_The_President','cc1755ff-80bd-4330-a70c-4d76f26f06d2',['thumb_C_costs_2_7_years','thumb_D_lunch_11_minutes','thumb_A_all_night','thumb_B_eleven_minutes'],'Новые обложки: первые две (C и D). A и B старые.'),
 (11,'ep11','The_Weirdest_Jobs_In_The_World','de8a4c3e-9aa4-447d-9e2e-3edb14aecd28',['thumb_A3_sniff_this_punchy','thumb_B2_push','thumb_C2_milks_snakes'],''),
 (12,'ep12','Jobs_That_Will_Appear_In_10_Years','61622348-2eb0-46c1-8284-4b6ed2a07da0',['thumb_A_teach_robots','thumb_B_is_it_fake','thumb_C_300ft_up'],''),
 (13,'ep13','Why_Its_So_Hard_To_Be_An_Underwater_Welder','c573262d-77e0-47ae-9a13-2e30a8a30dd9',['thumb_A_welding_underwater','thumb_B_28_days','thumb_C_pulls_you_in'],''),
 (14,'ep14','The_Worst_Jobs_In_History','38850a93-b92b-4bff-8755-09bfc82229d2',['thumb_A_paid_to_get_bitten','thumb_B_toilets_new1','thumb_B_toilets_new2','thumb_B_toilets_new3','thumb_C_kings_toilet_guy'],'Обложка B: три новых варианта «TOILETS. By HAND.», выбери один.'),
 (15,'ep15','10_Jobs_AI_Cant_Replace','3ce03fa3-1b37-4f20-aab6-73d044158e99',['thumb_A_ai_cant_do_his_job','thumb_B_robots_still_cant','thumb_C_10_jobs_ai_cant_replace'],''),
 (16,'ep16','The_Loneliest_Jobs_On_Earth','a8b30d6c-d0e9-4bca-9aa6-0f9e533be3a1',['thumb_A_cut_off_8_months','thumb_B_paid_to_count_penguins','thumb_C_28_days_in_a_can'],'Новый.'),
]
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def meta(n,d):
    p=f'{S}/{d}/out/youtube_metadata_ep{n}.md'
    if not os.path.exists(p): p=f'/home/user/lookme-viewer/hardo/ep{n}/youtube_metadata_ep{n}.md'
    if not os.path.exists(p): return None
    t=open(p).read()
    def sec(h):
        m=re.search(r'^## '+h+r'\s*\n(.*?)(?=^## |\Z)',t,re.S|re.M); return m.group(1).strip() if m else ''
    title=sec('Title').split('\n')[0].strip()
    alts=re.search(r'Alternatives?:\s*(.*)',sec('Title')); 
    return dict(title=title,alts=alts.group(1).strip() if alts else '',desc=sec('Description'),tags=sec('Tags'),pin=sec('Pinned comment'))
def thumb(path):
    im=Image.open(path).convert('RGB'); b=io.BytesIO(); im.save(b,'JPEG',quality=84); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
eps=[]
for n,d,name,cid,th,note in E:
    mp4=f'{S}/{d}/out/{name}.mp4'; srt=f'{S}/{d}/out/{name}.srt'
    m=meta(n,d) or dict(title="Why It's So Hard to Be a Nurse",alts='',desc='',tags='',pin='')
    du=dur(mp4) if os.path.getsize(mp4)>5e6 else 119.6
    thumbs=[]
    for t in th:
        p=f'{S}/{d}/out/{t}_1280x720.jpg'
        if os.path.exists(p): thumbs.append((t.replace('thumb_',''),thumb(p),t+'_1280x720.jpg'))
    eps.append(dict(n=n,title=m['title'],alts=m['alts'],desc=m['desc'],tags=m['tags'],pin=m['pin'],note=note,
        dur=f"{int(du//60)}:{int(du%60):02d}",url=CF+cid+'.mp4',file=name+'.mp4',
        srt=open(srt).read() if os.path.exists(srt) else '',srtname=name+'.srt',thumbs=thumbs))
json.dump([{k:v for k,v in e.items() if k!='thumbs'} for e in eps],open(f'{S}/allvids/eps.json','w'),ensure_ascii=False,indent=1)
esc=html.escape
def block(label,text,cls=''):
    if not text: return ''
    return f'<div class="blk"><div class="bh"><span>{label}</span><button type="button" class="cp">Копировать</button></div><pre class="bt {cls}">{esc(text)}</pre></div>'
cards=[]
for e in reversed(eps):
    th=''.join(f'<figure><img src="{src}" alt="Обложка {esc(k)}"><figcaption>{esc(k)} · <a class="dl" download="{fn}" href="#">скачать</a></figcaption></figure>' for k,src,fn in e['thumbs'])
    srt=f'<a class="btn" download="{e["srtname"]}" href="data:text/plain;charset=utf-8;base64,{base64.b64encode(e["srt"].encode()).decode()}">Субтитры .srt</a>' if e['srt'] else ''
    cards.append(f'''<article class="ep" id="ep{e["n"]}">
<header><span class="num">Эп. {e["n"]}</span><span class="dur">{e["dur"]}</span>{f'<span class="note">{esc(e["note"])}</span>' if e["note"] else ''}</header>
<h2>{esc(e["title"])}</h2>
<div class="btns"><a class="btn main" href="{e["url"]}" target="_blank" rel="noopener">Скачать ролик 1080p</a>{srt}<span class="fn">{esc(e["file"])}</span></div>
<div class="thumbs">{th}</div>
{block('Название',e['title'])}{block('Другие варианты названия',e['alts'])}{block('Описание (с источниками и главами)',e['desc'],'long')}{block('Теги',e['tags'])}{block('Закреплённый комментарий',e['pin'])}
</article>''')
toc=''.join(f'<li><a href="#ep{e["n"]}">Эп. {e["n"]} · {esc(e["title"])}</a> <span>{e["dur"]}</span></li>' for e in reversed(eps))
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hardo — все готовые ролики</title>
<style>
:root{{--bg:#fbfbf9;--card:#fff;--ink:#1d1f22;--muted:#6a6e74;--line:#e3e4e1;--sun:#ffd65a;--sky:#cfe4f7;--skyink:#1f5c8f}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16171a;--card:#1e2024;--ink:#eceae4;--muted:#9a9ea5;--line:#2e3136;--sun:#e9bf3c;--sky:#22384d;--skyink:#9fcdf2}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px max(16px,4vw) 60px}}
.wrap{{max-width:1100px;margin:0 auto;display:grid;gap:22px}}
h1{{font-size:clamp(28px,5vw,44px);margin:0}}h1 b{{background:linear-gradient(transparent 60%,var(--sun) 60% 92%,transparent 92%)}}
.lede{{color:var(--muted);margin:4px 0 0;max-width:70ch}}
.toc{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px}}.toc ol{{margin:6px 0 0;padding-left:1.2em;columns:2;column-gap:28px}}.toc li{{break-inside:avoid;margin:2px 0}}.toc span{{color:var(--muted);font-variant-numeric:tabular-nums}}
@media (max-width:700px){{.toc ol{{columns:1}}}}
a{{color:var(--skyink)}}
.ep{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;display:grid;gap:12px}}
.ep header{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.num{{background:var(--ink);color:var(--bg);font-weight:700;font-size:13px;padding:4px 10px;border-radius:99px}}
.dur{{border:1px solid var(--line);color:var(--muted);font-size:13px;padding:3px 9px;border-radius:99px;font-variant-numeric:tabular-nums}}
.note{{background:var(--sky);color:var(--skyink);font-size:13px;padding:4px 10px;border-radius:99px}}
.ep h2{{margin:0;font-size:24px}}
.btns{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}.fn{{color:var(--muted);font-size:13px}}
.btn{{display:inline-block;font-weight:700;font-size:14px;border:1.5px solid var(--ink);border-radius:10px;padding:9px 13px;text-decoration:none;color:var(--ink)}}
.btn.main{{background:var(--ink);color:var(--bg)}}
.thumbs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}}
figure{{margin:0}}figure img{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;border:1px solid var(--line);display:block}}
figcaption{{font-size:12px;color:var(--muted);margin-top:4px}}
.blk{{border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.bh{{display:flex;justify-content:space-between;align-items:center;padding:6px 8px 6px 12px;background:var(--bg);border-bottom:1px solid var(--line)}}
.bh span{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.cp{{font:600 13px system-ui;border:1.5px solid var(--ink);background:var(--card);color:var(--ink);border-radius:8px;padding:5px 10px;cursor:pointer}}
.bt{{margin:0;padding:10px 12px;white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 system-ui}}.bt.long{{max-height:220px;overflow:auto}}
</style></head><body><div class="wrap">
<header><h1>Hardo — <b>все готовые ролики</b></h1>
<p class="lede">{len(eps)} роликов, новые сверху. Для каждого: ссылка на ролик в 1080p, обложки (картинки встроены в файл, сохраняются кнопкой «скачать»), субтитры и тексты для YouTube с кнопкой «Копировать». Ролики лежат по постоянным ссылкам, этот файл можно открыть в любом браузере.</p></header>
<nav class="toc"><b>Содержание</b><ol>{toc}</ol></nav>
{''.join(cards)}
</div>
<script>
document.querySelectorAll('a.dl').forEach(a=>{{a.href=a.closest('figure').querySelector('img').src}});
document.querySelectorAll('.cp').forEach(b=>b.addEventListener('click',async()=>{{const pre=b.closest('.blk').querySelector('pre');const t=pre.textContent;
try{{await navigator.clipboard.writeText(t);b.textContent='Скопировано'}}catch(e){{const r=document.createRange();r.selectNodeContents(pre);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Выделено: Ctrl+C'}}
setTimeout(()=>b.textContent='Копировать',1800)}}));
</script></body></html>'''
open(f'{S}/allvids/Hardo_all_videos.html','w').write(page)
print(len(eps), round(len(page)/1e6,1),'MB')
for e in eps: print(e['n'],e['dur'],e['title'][:50],len(e['thumbs']),bool(e['desc']),bool(e['srt']))
