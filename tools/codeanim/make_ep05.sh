#!/bin/bash
# Ep5 (Iron Man, "don't snap") code-drawn build: render scenes -> synth soundtrack -> end card -> final mp4 (1080p + 720p).
# usage: tools/codeanim/make_ep05.sh TMPDIR [skip-render]   (run from the repo root)
set -e
TMP=$1; mkdir -p $TMP out
if [ "$2" != "skip-render" ]; then
  (cd tools/codeanim && for id in 01 02 03 04 05 06 07 08 09 10 11 12 13; do node render_scene.js ep05.html $id $TMP/s$id.mp4; done)
fi
for id in 01 02 03 04 05 06 07 08 09 10 11 12 13; do echo "file '$TMP/s$id.mp4'"; done > $TMP/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $TMP/list.txt -c copy $TMP/video.mp4
python3 tools/codeanim/ep05_audio.py assets/ep05/vo2 $TMP/audio.wav
ffmpeg -v error -y -i $TMP/video.mp4 -i $TMP/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest $TMP/body.mp4
ffmpeg -v error -y -sseof -0.5 -i $TMP/body.mp4 -frames:v 1 $TMP/end_bg.png
python3 tools/end_subscribe.py $TMP/end_bg.png $TMP/end.mp4 --vo assets/ep05/vo2/end.wav --hold 5.2 --title "NEXT WEEK: SOMETHING SMALL"
ffmpeg -v error -y -i $TMP/body.mp4 -i $TMP/end.mp4 -filter_complex "[0:v]setsar=1[v0];[1:v]scale=1920:1080,fps=24,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a0c];[a0c]loudnorm=I=-15:TP=-1.5:LRA=11[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/e5_ironman_code.mp4
ffmpeg -v error -y -i out/e5_ironman_code.mp4 -vf scale=1280:720 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 128k -movflags +faststart out/e5_ironman_code_720.mp4
echo done
