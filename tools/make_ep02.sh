#!/bin/bash
# Ep2 (Hulk) full build: cut -> comic FX -> narration -> end card.  usage: tools/make_ep02.sh STILLS_DIR VO_DIR END_BG_TMP
set -e
ST=$1; VO=$2; TMP=$3
python3 tools/build_ep02.py $ST
python3 tools/ep02_fx.py
python3 tools/fx_overlay.py out/e2_cut.mp4 out/e2_fx.mp4 assets/ep02/fx_ep02.json
cp out/e2_cut.timeline.json out/e2_fx.timeline.json
python3 tools/mix_vo.py out/e2_fx.mp4 out/e2_vo.mp4 $VO
ffmpeg -v error -y -sseof -0.1 -i out/e2_vo.mp4 -frames:v 1 $TMP/end_bg.png
python3 tools/end_subscribe.py $TMP/end_bg.png $TMP/end.mp4 --vo $VO/end.wav --hold 4.4 --title "NEXT WEEK: THE FLASH"
ffmpeg -v error -y -i out/e2_vo.mp4 -i $TMP/end.mp4 -filter_complex "[0:v]setsar=1[v0];[1:v]scale=1920:1080,fps=24,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out/e2_hulk_v1.mp4
rm -f out/e2_cut.mp4 out/e2_fx.mp4 out/e2_vo.mp4
