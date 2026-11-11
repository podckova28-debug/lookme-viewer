#!/bin/bash
# usage: finalize.sh VO_DIR [WORK_DIR]
# Re-times the episode to a new voice, re-renders every scene, mixes, assembles, cuts Shorts and rewrites the upload pack.
# VO_DIR holds one WAV per line id (run prep_vo.py on a delivered folder first).
set -e
VO=$(realpath "$1"); W=${2:-/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/ep02/final}; mkdir -p $W/probe
PY=/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/tts/venv/bin/python
cd "$(dirname "$0")"
[ -d ../anim3d/node_modules/three ] || (cd ../anim3d && npm install --no-audit --no-fund)   # three.js for the 3D shots
$PY layout.py "$VO"
ORDER=$(python3 -c "import json; print(' '.join(json.load(open('timing.json'))['order']))")
# the probe (ghost opacity, cuts, events for the mix) runs scene by scene in its own browser while the renders go
( for s in $ORDER; do SCENES=$s node probe.js $W/probe/$s.json 5 > $W/probe/$s.log 2>&1 || echo "probe failed $s"; done ) &
PROBE=$!
./render_all.sh $W/render
wait $PROBE
for s in $ORDER; do [ -s $W/render/$s.mp4 ] || { echo "render missing: $s"; exit 1; }; [ -s $W/probe/$s.json ] || { echo "probe missing: $s"; exit 1; }; done
python3 -c "
import json, glob; r = {}
for f in glob.glob('$W/probe/s*.json'): r.update(json.load(open(f)))
json.dump(r, open('$W/probe.json', 'w')); print('probe', len(r), 'scenes')"
$PY mix.py "$VO" $W/probe.json $W/mix.wav
./assemble.sh $W/render $W/mix.wav $W/ep02_final.mp4
$PY shorts.py $W/ep02_final.mp4 $W/shorts
python3 upload_pack.py > /dev/null
python3 srt.py
echo "final: $W/ep02_final.mp4"
