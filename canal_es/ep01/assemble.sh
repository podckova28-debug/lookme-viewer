#!/bin/bash
# usage: assemble.sh RENDER_DIR MIX.wav OUT.mp4  -> concatenates scene videos in order and muxes the mix (loudness -14 LUFS)
R=$1; A=$2; O=$3; cd "$(dirname "$0")"
python3 -c "import json; [print(f\"file '$R/{s}.mp4'\") for s in json.load(open('timing.json'))['order']]" > $R/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $R/list.txt -c copy $R/video.mp4
ffmpeg -v error -y -i $R/video.mp4 -i $A -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart $O
ffprobe -v error -show_entries format=duration -of csv=p=0 $O
