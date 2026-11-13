#!/bin/bash
# renders every scene of ep04 to $OUT/sXX.mp4 (3 in parallel), durations from timing.json
HYBQ=${HYBQ-&hyb=1}; export HYBQ   # painted look by default; HYBQ= render_all.sh for the vector look
OUT=${1:-/tmp/claude-0/-home-user-lookme-viewer/1113b656-b6bf-5891-bb3b-6c7738b841c9/scratchpad/ep04/render}; mkdir -p $OUT
cd "$(dirname "$0")"
python3 -c "
import json; T=json.load(open('timing.json'))
for s in T['order']: print(s, T['scenes'][s]['dur'])" | xargs -P 3 -n 2 sh -c 'node ../anim/render.js "ep04.html?scene=$0$HYBQ" $1 '"$OUT"'/$0.mp4 > '"$OUT"'/$0.log 2>&1 && echo "done $0"'
