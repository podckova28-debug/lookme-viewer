#!/bin/bash
# dl.sh <dir> <ext> : строки «имя хвост_URL» из stdin → <dir>/<имя>.<ext>
U=https://d8j0ntlcm91z4.cloudfront.net/user_35NOdNk1NKtyC7RbzyCbNu39KlI
while read n t; do [ -z "$n" ] && continue; curl -sS --retry 3 -o "$1/$n.$2" "$U/$t"; done
