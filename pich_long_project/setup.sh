#!/bin/bash
cd /home/user/pc; mkdir -p img vo mus out /home/user/tools/fonts
[ -s /home/user/tools/fonts/Oswald.ttf ] || curl -sfL -o /home/user/tools/fonts/Oswald.ttf "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/oswald/Oswald%5Bwght%5D.ttf"
B=https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI/hf_20261101_
i=1; for id in 104813_9bb675c7-33c6-4707-9c6a-1a30b4cff057 104813_26bc4df5-c810-4570-b4c9-6cfb00ea746a 104813_3fee1ce4-e994-45c7-a03d-7c6a5040226c; do [ -s mus/m$i.m4a ] || curl -sfo mus/m$i.m4a $B$id.m4a; i=$((i+1)); done
while read n u; do [ -s img/$n.png ] || curl -sfo img/$n.png "$u"; done < img_urls.txt
python3 - <<'P'
import subprocess
with open("vo/dur.txt","w") as f:
    for l in open("vo_urls.txt"):
        n,u=l.split()
        subprocess.run(["curl","-sfo",f"vo/v{n}.mp3",u],check=True)
        subprocess.run(["ffmpeg","-v","error","-y","-i",f"vo/v{n}.mp3","-ar","16000","-ac","1",f"vo/v{n}.wav"],check=True)
        d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"vo/v{n}.mp3"],capture_output=True,text=True).stdout.strip()
        f.write(f"v{n} {d}\n")
P
cat vo/dur.txt
echo SETUP_DONE
