#!/bin/bash
# download frames listed in frames/urls.txt that are missing (or listed newer), make jpg copies
cd "$(dirname "$0")/frames"; mkdir -p jpg
B=https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI
grep -v '^#' urls.txt | while read n s; do f=$(printf "f%02d.png" $n)
  if [ ! -f "$f" ] || ! grep -q "$s" .got 2>/dev/null; then curl -s -o "$f" "$B/hf_$s.png" && echo "$s" >> .got
    python3 -c "from PIL import Image; Image.open('$f').convert('RGB').save('jpg/${f%.png}.jpg',quality=90)"; fi
done
