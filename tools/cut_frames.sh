#!/bin/bash
# cut.sh IN OUT "f0-f1 f0-f1 ..." : keep frame ranges (24 fps), audio follows, upscale to 1080
IN=$1; OUT=$2; RANGES=$3; fc=""; cat=""; i=0
for r in $RANGES; do a=${r%-*}; b=${r#*-}; ta=$(python3 -c "print($a/24)"); tb=$(python3 -c "print($b/24)")
 fc="$fc[0:v]trim=start_frame=$a:end_frame=$b,setpts=PTS-STARTPTS[v$i];[0:a]atrim=$ta:$tb,asetpts=PTS-STARTPTS[a$i];"; cat="$cat[v$i][a$i]"; i=$((i+1)); done
ffmpeg -v error -y -i $IN -filter_complex "${fc}${cat}concat=n=$i:v=1:a=1[v0x][a];[v0x]scale=1920:1080:flags=lanczos,unsharp=5:5:0.8:5:5:0.0[v]" -map "[v]" -map "[a]" -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac $OUT
