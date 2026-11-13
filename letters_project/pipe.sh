#!/bin/bash
cd /home/user/cw
bash runall.sh
[ -s out/mix.m4a ] || python3 audio.py > out/audio.log 2>&1
python3 -c "
import json;t=json.load(open('spec/timeline.json'))
open('out/list.txt','w').write(''.join(f\"file '{s[0]}.mp4'\n\" for s in t['segs']))"
ffmpeg -v error -y -f concat -safe 0 -i out/list.txt -c copy out/v.mp4
ffmpeg -v error -y -i out/v.mp4 -i out/mix.m4a -map 0:v -map 1:a -c:v libx264 -preset medium -b:v 8000k -maxrate 10000k -bufsize 16000k -pix_fmt yuv420p -c:a copy -shortest -movflags +faststart out/hq.mp4
ffmpeg -v error -y -i out/hq.mp4 -vf scale=1280:720 -c:v libx264 -preset medium -b:v 1800k -c:a aac -b:a 128k -movflags +faststart out/web.mp4
echo DONE > out/pipe.done
