#!/bin/bash
# fetch fonts, music, VO; run whisper
cd /home/user/mk; mkdir -p img vid vo mus out /home/user/tools/fonts
[ -s /home/user/tools/fonts/Oswald.ttf ] || curl -sfL -o /home/user/tools/fonts/Oswald.ttf "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/oswald/Oswald%5Bwght%5D.ttf"
B=https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/hf_20261101_
i=1; for id in 104813_9bb675c7-33c6-4707-9c6a-1a30b4cff057 104813_26bc4df5-c810-4570-b4c9-6cfb00ea746a 104813_3fee1ce4-e994-45c7-a03d-7c6a5040226c; do [ -s mus/m$i.m4a ] || curl -sfo mus/m$i.m4a $B$id.m4a; i=$((i+1)); done
while read n u; do [ -s vo/v$n.mp3 ] || curl -sfo vo/v$n.mp3 "$u"; ffmpeg -v error -y -i vo/v$n.mp3 -ar 16000 -ac 1 vo/v$n.wav; done < vo_urls.txt
: > vo/dur.txt; for f in vo/v*.mp3; do n=$(basename $f .mp3); echo "$n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)" >> vo/dur.txt; done
pip list 2>/dev/null | grep -qi faster-whisper || pip install -q faster-whisper
cd vo && python3 ../wts.py $(ls v*.wav | sed 's/.wav//' | sort) > wts.log 2> wts.err
echo SETUP_DONE > /home/user/mk/out/setup.done
