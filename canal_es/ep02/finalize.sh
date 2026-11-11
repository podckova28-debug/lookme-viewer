#!/bin/bash
# usage: finalize.sh VO_DIR [WORK_DIR]
# Re-times the episode to a new voice, re-renders every scene, mixes, assembles, cuts Shorts and rewrites the upload pack.
set -e
VO=$(realpath "$1"); W=${2:-/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/ep02/final}; mkdir -p $W
PY=/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/tts/venv/bin/python
cd "$(dirname "$0")"
[ -d ../anim3d/node_modules/three ] || (cd ../anim3d && npm install --no-audit --no-fund)   # three.js for the 3D shots
$PY layout.py "$VO"
./render_all.sh $W/render
node probe.js $W/probe.json 8
$PY mix.py "$VO" $W/probe.json $W/mix.wav
./assemble.sh $W/render $W/mix.wav $W/ep02_final.mp4
$PY shorts.py $W/ep02_final.mp4 $W/shorts
python3 upload_pack.py > /dev/null
python3 srt.py
echo "final: $W/ep02_final.mp4"
