# Бесплатный апскейл Wan 480p → 1080p (Real-ESRGAN animevideov3, CPU bf16). Не запускать вместе с рендером.
cd "$(dirname "$0")"
for f in clips/*_raw.mp4; do n=$(basename "${f%_raw.mp4}"); o=clips/ai/$n.mp4; [ -f "$o" ] && [ "$o" -nt "$f" ] && continue
  python3.13 /home/user/gastronom/content-machine/video/upscale.py "$f" "$o" 1920x1080 2>&1 | tail -1; done
echo DONE
