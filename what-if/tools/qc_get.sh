#!/bin/bash
# usage: qc_get.sh NAME URL  -> downloads, strip (fps4 8x5), cut times, loudness
S=${QC_DIR:-/tmp/qc}/$1
mkdir -p $S && cd $S && curl -sS -o $1.mp4 "$2" || exit 1
ffmpeg -v error -y -i $1.mp4 -vf "fps=4,scale=320:-1,tile=8x5" -frames:v 1 strip.png
echo "$1 cuts: $(ffmpeg -i $1.mp4 -vf "select='gt(scene,0.2)',metadata=print:file=-" -f null - 2>/dev/null | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | tr '\n' ' ')"
echo "$1 $(ffmpeg -i $1.mp4 -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tail -1)"
