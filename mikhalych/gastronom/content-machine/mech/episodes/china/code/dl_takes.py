"""dl_takes.py '<index> <stamp_jobid>' ... — индекс = номер реплики (1000+ = дубль b) → vo_takes3/<id>_a|b.mp3"""
import sys, json, urllib.request
ids = [k for k, _ in json.load(open('work/lines.json'))]
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/hf_20261105_'
for arg in sys.argv[1:]:
    n, s = arg.split(); n = int(n); tk = 'b' if n >= 1000 else 'a'; lid = ids[(n % 1000) - 1]
    urllib.request.urlretrieve(B + s + '.mp3', f'vo_takes3/{lid}_{tk}.mp3')
print(len(sys.argv) - 1, 'ok')
