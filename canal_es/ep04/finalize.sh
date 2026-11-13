#!/bin/bash
# usage: finalize.sh VO_DIR [WORK_DIR]
# Re-times the episode to a new voice, re-renders every scene, mixes, assembles, cuts Shorts and rewrites the upload pack.
# VO_DIR holds one WAV per line id (run prep_vo.py on a delivered folder first); voicefx.py colours the animals here.
set -e
VO=$(realpath "$1"); W=${2:-/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/ep04/final}; mkdir -p $W/probe
PY=/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/tts/venv/bin/python
cd "$(dirname "$0")"
[ -d ../anim3d/node_modules/three ] || (cd ../anim3d && npm install --no-audit --no-fund)   # three.js for the 3D shots
# no animal voices in ep04: lines go straight to the layout
$PY layout.py "$VO"
ORDER=$(python3 -c "import json; print(' '.join(json.load(open('timing.json'))['order']))")
# ep04's mixer needs no probe (no frozen or ghost state to sample): just render
./render_all.sh $W/render
for s in $ORDER; do [ -s $W/render/$s.mp4 ] || { echo "render missing: $s"; exit 1; }; done
echo '{}' > $W/probe.json
$PY mix.py "$VO" $W/probe.json $W/mix.wav
./assemble.sh $W/render $W/mix.wav $W/ep04_final.mp4
$PY shorts.py $W/ep04_final.mp4 $W/shorts
python3 upload_pack.py > /dev/null
python3 srt.py
echo "final: $W/ep04_final.mp4"
