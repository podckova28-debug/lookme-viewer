#!/bin/bash
# frames/urls.txt: "<n> <result_url>" lines; download missing/changed frames to fNNN.png + jpg/ copies
cd "$(dirname "$0")/frames"; mkdir -p jpg
grep -v '^#' urls.txt | while read n u; do f=$(printf "f%03d.png" $n)
  if [ ! -f "$f" ] || ! grep -qF "$u" .got 2>/dev/null; then curl -s -o "$f" "$u" && echo "$u" >> .got
    python3 -c "from PIL import Image; Image.open('$f').convert('RGB').save('jpg/${f%.png}.jpg',quality=90)"; fi
done
