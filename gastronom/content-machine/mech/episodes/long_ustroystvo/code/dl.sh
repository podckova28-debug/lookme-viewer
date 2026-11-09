#!/bin/bash
# dl.sh <dir> <prefix> then lines "index url" on stdin
d=$1; p=$2; mkdir -p $d
while read i u; do [ -z "$u" ] && continue; ext=${u##*.}; f=$(printf "%s/%s%02d.%s" $d $p $i $ext); [ -s $f ] || curl -sS -o $f "$u"; done
