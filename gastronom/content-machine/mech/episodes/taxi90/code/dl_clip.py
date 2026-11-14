"""dl_clip.py '<имя> <url>' ... — скачать клип в clips/<имя>_raw.mp4 и лист 8 кадров qa/c_<имя>.jpg."""
import sys, subprocess, urllib.request
for arg in sys.argv[1:]:
    n, url = arg.split(maxsplit=1); f = f'clips/{n}_raw.mp4'; urllib.request.urlretrieve(url, f)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', f, '-vf', f'fps=8/{d},scale=240:-2,tile=8x1', '-frames:v', '1', f'qa/c_{n}.jpg'])
    print(n, round(d, 1))
