"""ytsearch.py — поиск YouTube без API: ytInitialData со страницы результатов. Фильтры: год/месяц + 4–20 мин или >20 мин, сортировка по просмотрам."""
import json, re, sys, urllib.parse, urllib.request, base64
SP = {  # protobuf: 08 03 = сортировка по просмотрам; 12 xx: 08 = дата (4 месяц, 5 год), 18 = длина (3 = 4–20 мин, 2 = >20 мин)
 'year_mid': bytes([8, 3, 0x12, 4, 8, 5, 0x18, 3]), 'year_long': bytes([8, 3, 0x12, 4, 8, 5, 0x18, 2]),
 'month_mid': bytes([8, 3, 0x12, 4, 8, 4, 0x18, 3]), 'month_long': bytes([8, 3, 0x12, 4, 8, 4, 0x18, 2]), 'year_any': bytes([8, 3, 0x12, 2, 8, 5])}
def views(t):
    t = (t or '').replace('\xa0', ' ').lower()
    m = re.search(r'([\d\s,\.]+)\s*(тыс|млн|млрд)?', t)
    if not m: return 0
    n = float(m.group(1).replace(' ', '').replace(',', '.') or 0)
    return int(n * {'тыс': 1e3, 'млн': 1e6, 'млрд': 1e9}.get(m.group(2), 1))
def search(q, mode):
    sp = urllib.parse.quote(base64.b64encode(SP[mode]).decode())
    url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(q)}&sp={sp}&hl=ru&gl=RU'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'ru-RU,ru;q=0.9'})
    html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if not m: return []
    data = json.loads(m.group(1)); out = []
    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                v = o['videoRenderer']
                out.append(dict(id=v.get('videoId'), title=''.join(r.get('text', '') for r in v.get('title', {}).get('runs', [])),
                                ch=''.join(r.get('text', '') for r in v.get('ownerText', {}).get('runs', [])),
                                views=views(v.get('viewCountText', {}).get('simpleText') or ''.join(r.get('text','') for r in v.get('viewCountText', {}).get('runs', []))),
                                len=v.get('lengthText', {}).get('simpleText', ''), when=v.get('publishedTimeText', {}).get('simpleText', '')))
            else:
                for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(data); return out
if __name__ == '__main__':
    mode = sys.argv[1]; res = {}
    for q in sys.argv[2:]:
        try: res[q] = search(q, mode)
        except Exception as e: res[q] = [{'err': str(e)}]
    print(json.dumps(res, ensure_ascii=False))
