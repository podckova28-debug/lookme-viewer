"""dl_vo.py '<индекс> <url>' ... — скачать реплики по номеру в script.py в vo/<id>.mp3 и сжать паузы в vo/<id>.wav."""
import sys, subprocess, json, urllib.request
ids = [i for i, _ in json.load(open('work/lines.json'))]
for arg in sys.argv[1:]:
    n, url = arg.split(maxsplit=1); lid = ids[int(n) - 1]
    urllib.request.urlretrieve(url, f'vo/{lid}.mp3')
    subprocess.run([sys.executable, '/home/user/gastronom/content-machine/video/pauses2.py', f'vo/{lid}.mp3', f'vo/{lid}.wav'])
