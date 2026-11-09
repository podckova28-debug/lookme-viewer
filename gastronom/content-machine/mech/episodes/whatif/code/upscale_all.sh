#!/bin/bash
cd "$(dirname "$0")/.."
while ! grep -q EXIT work/render.log; do sleep 10; done
echo "старт $(date +%T)"
for m in M_J M_A M_B M_C M_D M_E M_F M_G M_H M_I M_K M_Z; do
  extra=""; [ $m = M_J ] && extra="--to 2.3"
  python3.13 /home/user/gastronom/content-machine/video/upscale.py clips/${m}_raw.mp4 clips/ai/$m.mp4 $extra 2>&1 | grep '→'
done
echo "готово $(date +%T)"
