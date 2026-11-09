# 480p клипы Wan 3.0 (854×480) → 1920×1080: lanczos + лёгкая резкость
for f in clips/*_raw.mp4; do o=${f%_raw.mp4}.mp4; [ -f "$o" ] && [ "$o" -nt "$f" ] && continue
  ffmpeg -y -hide_banner -loglevel error -i "$f" -an -vf "scale=1920:1080:flags=lanczos,unsharp=5:5:0.7:5:5:0,fps=30" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p "$o" && echo "$o"; done
