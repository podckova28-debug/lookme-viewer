"""Финальная склейка сегментов и звука с двухпроходной нормализацией (если parallel() упал на склейке)."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cut
P = cut.P; out = P(sys.argv[1] if len(sys.argv) > 1 else 'disposable_1080p.mp4')
subprocess.run([cut.FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', P('work/segs.txt'), '-i', P('work/mix.wav'),
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', cut.loudnorm2(P('work/mix.wav')), '-c:a', 'aac', '-b:a', '192k',
                '-ar', str(cut.SR), '-movflags', '+faststart', '-shortest', out], check=True)
print('готово:', out)
