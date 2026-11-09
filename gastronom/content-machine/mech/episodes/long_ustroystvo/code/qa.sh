#!/bin/bash
# qa.sh clips/A03.mp4 -> qa/A03.jpg : 8 кадров равномерно, 480x270 каждый, 4x2
f=$1; n=$(basename $f .mp4); mkdir -p qa
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)
fps=$(python3 -c "print(8/$d)")
ffmpeg -v error -y -i $f -vf "fps=$fps,scale=480:270,tile=4x2" -frames:v 1 qa/$n.jpg
