"""stdin: «индекс хвост_URL» → vo_takes/<id>_a.mp3 (индекс = номер реплики в LINES, 1…; +1000 = дубль b)."""
import sys, json, subprocess
L = [k for k, _ in json.load(open('work/lines.json'))]
U = 'https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/'
for line in sys.stdin:
    p = line.split()
    if len(p) < 2: continue
    i = int(p[0]); tk = 'abc'[i // 1000]; k = L[(i % 1000) - 1]
    subprocess.run(['curl', '-sS', '--retry', '3', '-o', f'vo_takes/{k}_{tk}.mp3', U + p[1]], check=True)
    print(k, tk)
