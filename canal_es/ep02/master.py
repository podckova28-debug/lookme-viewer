"""Master the episode mix to YouTube loudness: -14 LUFS integrated, true peak under -1 dBTP.
usage: python3 master.py MIX.wav OUT.wav
Gentle bus compression, then gain, then a limiter; the gain is searched until the measured loudness lands
within 0.3 LU of the target (a single loudnorm pass undershoots: the raw mix is ~-24 LUFS with sharp SFX peaks)."""
import json, re, subprocess, sys

SRC, OUT = sys.argv[1], sys.argv[2]
TARGET = -14.0

def chain(gain):
    # the limiter runs 4x oversampled so inter-sample peaks are caught too
    return (f'acompressor=threshold=0.063:ratio=3:attack=8:release=160:knee=4,'
            f'volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.72:attack=2:release=60:level=false,aresample=48000')

def measure(af):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', SRC, '-af', af + ',ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    s = r[r.rindex('Summary:'):]
    return float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1)), float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))

gain = 8.0
for _ in range(5):
    I, tp = measure(chain(gain))
    print(f'gain {gain:+.2f} dB -> {I:.2f} LUFS, true peak {tp:.2f} dBFS')
    if abs(I - TARGET) < .3: break
    gain += TARGET - I
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-af', chain(gain), '-ar', '48000', '-c:a', 'pcm_s16le', OUT], check=True)
print(json.dumps({'gain_db': round(gain, 2), 'lufs': I, 'true_peak': tp}))
