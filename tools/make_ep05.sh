#!/bin/bash
# Ep5 (Iron Man) full build: cut -> comic FX -> narration -> end card.  usage: tools/make_ep05.sh TMPDIR
set -e
TMP=$1
python3 tools/build_cut.py assets/ep05/cut.json
python3 tools/ep05_fx.py
python3 tools/fx_overlay.py out/e5_cut.mp4 out/e5_fx.mp4 assets/ep05/fx.json
cp out/e5_cut.timeline.json out/e5_fx.timeline.json
python3 tools/mix_vo.py out/e5_fx.mp4 out/e5_vo.mp4 assets/ep05/vo
ffmpeg -v error -y -sseof -0.1 -i out/e5_vo.mp4 -frames:v 1 $TMP/end_bg.png
python3 tools/end_subscribe.py $TMP/end_bg.png $TMP/end.mp4 --vo assets/ep05/vo/end.wav --hold 5.2 --title "NEXT WEEK: SOMETHING SMALL"
ffmpeg -v error -y -i out/e5_vo.mp4 -i $TMP/end.mp4 -filter_complex "[0:v]setsar=1[v0];[1:v]scale=1920:1080,fps=24,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out/e5_ironman_v1.mp4
ffmpeg -v error -y -i out/e5_ironman_v1.mp4 -vf scale=1280:720 -c:v libx264 -crf 24 -preset fast -c:a aac -b:a 128k -movflags +faststart out/e5_ironman_v1_720.mp4
rm -f out/e5_cut.mp4 out/e5_fx.mp4 out/e5_vo.mp4
