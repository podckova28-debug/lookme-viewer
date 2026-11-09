#!/bin/bash
# qa2.sh name... : крупная сетка 4x3 (640x360) по клипам mclips/
for n in "$@"; do f=mclips/$n.mp4; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f); fps=$(python3 -c "print(12/$d)"); ffmpeg -v error -y -i $f -vf "fps=$fps,scale=640:360,tile=4x3" -frames:v 1 qa/${n}_big.jpg; done
