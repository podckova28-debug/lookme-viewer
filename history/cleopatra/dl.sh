#!/bin/bash
# download frames listed in frames/urls.txt (n  hhmmss_jobid, date 20261128 unless the line has a full stamp), jpg copies for review
cd "$(dirname "$0")/frames"; mkdir -p jpg
B=https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI
grep -v '^#' urls.txt | while read n s; do f=$(printf "f%03d.png" $n); [[ $s == *_*_* ]] || s=20261128_$s
  if ! grep -qx "$n $s" .got 2>/dev/null; then curl -sf -o "$f" "$B/hf_$s.png" && echo "$n $s" >> .got
    python3 -c "from PIL import Image; Image.open('$f').convert('RGB').save('jpg/${f%.png}.jpg',quality=90)"; fi
done
# white-out notes listed in frames/patches.txt (frames reused for a neighbouring line)
grep -v '^#' patches.txt | while read n x0 y0 x1 y1; do f=$(printf "f%03d.png" $n)
  python3 -c "from PIL import Image,ImageDraw; im=Image.open('$f').convert('RGB'); ImageDraw.Draw(im).rectangle(($x0,$y0,$x1,$y1),fill='white'); im.save('$f'); im.save('jpg/${f%.png}.jpg',quality=90)"; done
