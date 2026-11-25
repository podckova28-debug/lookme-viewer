"""Pre-render QC for a What If episode. Run BEFORE every render; it exits with code 1 if anything fails.

usage: python3 qc.py <timeline.json> <groups.json> [out_dir] [--video final.mp4]

groups.json: {"room": {"master": "room_d3", "frames": ["h11a", ...]}, "market": {...}, ...}
  Put only frames shot from the SAME camera as the master in a group; close-ups of a different angle go nowhere.
  Every group is one location (or one character). Each frame is matched against the master with ORB features
  + RANSAC homography; a frame of the same place, same camera, must have many inliers and a near-identity homography.

Checks:
 1. SYNC  - every VO line starts on a cut, lines never overlap, last line ends before the video does,
            (with --video) the audio and video streams of the final file have the same length.
 2. PLACE - each frame of a location group matches its master (same furniture, same window, same camera).
 3. SHEETS - writes, for a human/visual pass: one sheet per group (master first, verdict on every tile),
            a sheet of every frame in timeline order with timecodes, and a still of every text overlay.
            Look at the sheets at full size: hands/arms, clothes, anachronisms, who is in the frame and why.
"""
import sys, os, json, wave, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
video = sys.argv[sys.argv.index('--video') + 1] if '--video' in sys.argv else None
if video in args: args.remove(video)
tl_path, groups_path = args[0], args[1]
out = args[2] if len(args) > 2 else os.path.join(os.path.dirname(os.path.abspath(tl_path)), 'qc')
os.makedirs(out, exist_ok=True)
spec = json.load(open(tl_path)); groups = json.load(open(groups_path))
base = os.path.join(REPO, spec['base'])
fails, notes = [], []

# ---------- 1. sync ----------
def wav_len(p):
    w = wave.open(os.path.join(REPO, p)); return w.getnframes() / w.getframerate()
cuts = sorted({round(s['t0'], 3) for s in spec['shots']})
vo = spec['vo']
for a, b in zip(vo, vo[1:] + [None]):
    end = a['t'] + wav_len(a['file'])
    name = os.path.basename(a['file'])
    if not any(abs(a['t'] - c) < .08 for c in cuts): fails.append(f'SYNC: {name} starts at {a["t"]:.2f}s, not on a cut')
    if b and end > b['t'] + .01: fails.append(f'SYNC: {name} overlaps the next line by {end - b["t"]:.2f}s')
    if not b and end > spec['duration']: fails.append(f'SYNC: last line {name} ends after the video ({end:.2f} > {spec["duration"]:.2f})')
if video:
    def dur(stream):
        r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', stream, '-show_entries', 'stream=duration', '-of', 'csv=p=0', video], capture_output=True, text=True)
        return float(r.stdout.strip() or 0)
    dv, da = dur('v:0'), dur('a:0')
    if abs(dv - da) > .1: fails.append(f'SYNC: final file video {dv:.2f}s vs audio {da:.2f}s')
    notes.append(f'final file: video {dv:.2f}s, audio {da:.2f}s')

# ---------- 2. place consistency ----------
# a) ORB + RANSAC: is it the same place and camera at all?  (same room 120-400 inliers, another place ~15)
# b) furniture zones: after aligning the frame to the master, compare edge maps inside zones where the furniture is
#    (zones in master pixels at 960x540, set per group). Redrawn furniture scores < .5, an edit of the master ~.65-.8.
#    A frame with 2+ low zones must be looked at; if it is fine, add it to the group's "approved" list.
orb = cv2.ORB_create(4000)
def load(name): return cv2.resize(cv2.imread(os.path.join(base, name + '.jpg'), cv2.IMREAD_GRAYSCALE), (960, 540))
def edges(im): return cv2.dilate(cv2.Canny(cv2.GaussianBlur(im, (5, 5), 0), 50, 150), None, iterations=2) > 0
MIN_INLIERS, ZONE_OK = 60, .5
verdict = {}
for g, d in groups.items():
    Mi = load(d['master']); Mk, Md = orb.detectAndCompute(Mi, None); Me = edges(Mi)
    zones = d.get('zones', {})
    for f in d['frames']:
        if f == d['master']: continue
        im = load(f); k, de = orb.detectAndCompute(im, None)
        m = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(Md, de) if de is not None else []
        inl, zs = 0, {}
        if len(m) >= 12:
            p1 = np.float32([Mk[x.queryIdx].pt for x in m]); p2 = np.float32([k[x.trainIdx].pt for x in m])
            H, mask = cv2.findHomography(p2, p1, cv2.RANSAC, 6.0)
            if H is not None:
                inl = int(mask.sum()); We = edges(cv2.warpPerspective(im, H, (960, 540)))
                for zn, (x0, y0, x1, y1) in zones.items():
                    a, b = Me[y0:y1, x0:x1], We[y0:y1, x0:x1]; zs[zn] = round(float((a & b).sum() / max(1, (a | b).sum())), 2)
        low = [zn for zn, v in zs.items() if v < ZONE_OK]
        ok = inl >= MIN_INLIERS and (len(low) < 2 or f in d.get('approved', []))
        verdict[(g, f)] = (ok, inl, zs)
        if inl < MIN_INLIERS: fails.append(f'PLACE: [{g}] {f} is a different place/camera than {d["master"]} (inliers {inl})')
        elif not ok: fails.append(f'PLACE: [{g}] {f} furniture differs from {d["master"]} in {low} {zs} - look at it; if fine add to "approved"')

# ---------- 3. sheets ----------
def sheet(tiles, path, c=4, w=480, h=270):
    r = (len(tiles) + c - 1) // c; S = Image.new('RGB', (w * c, h * r), 'white'); d = ImageDraw.Draw(S)
    for k, (img, label, col) in enumerate(tiles):
        x, y = (k % c) * w, (k // c) * h
        S.paste(Image.open(os.path.join(base, img + '.jpg')).convert('RGB').resize((w, h)), (x, y))
        d.rectangle((x, y, x + 8 + 7 * len(label), y + 16), fill=col); d.text((x + 4, y + 3), label, fill='white')
        if col == 'red': d.rectangle((x + 2, y + 2, x + w - 3, y + h - 3), outline='red', width=4)
    S.save(path, quality=88)
for g, d in groups.items():
    tiles = [(d['master'], 'MASTER ' + d['master'], 'black')]
    for f in d['frames']:
        if f == d['master']: continue
        ok, inl, zs = verdict[(g, f)]
        tiles.append((f, f'{f} {"OK" if ok else "CHECK"} ' + ' '.join(f'{v:.2f}' for v in zs.values()), 'darkgreen' if ok else 'red'))
    for i in range(0, len(tiles), 16): sheet(tiles[i:i + 16], os.path.join(out, f'place_{g}_{i // 16}.jpg'))
seq = []
for s in spec['shots']:
    if not seq or seq[-1][0] != s['img']: seq.append((s['img'], s['t0']))
tiles = [(i, f'{n + 1} {i} {int(t // 60)}:{int(t % 60):02d}', 'black') for n, (i, t) in enumerate(seq)]
for i in range(0, len(tiles), 20): sheet(tiles[i:i + 20], os.path.join(out, f'order_{i // 20}.jpg'))
ts = sorted({round(x['t0'] + .7, 2) for x in spec.get('texts', []) if x['style'] in ('note', 'card', 'big', 'strike', 'cap')})
tool = os.path.join(HERE, 'build_whatif.py')
subprocess.run([sys.executable, tool, tl_path, os.path.join(out, 'text')], env={**os.environ, 'STILLS': ','.join(map(str, ts))}, check=True)

# ---------- report ----------
rep = ['QC ' + os.path.basename(tl_path), f'shots {len(spec["shots"])}, unique frames {len(seq)}, lines {len(vo)}, {spec["duration"]:.1f}s'] + notes
rep += ['FAIL ' + f for f in fails] or ['all automatic checks passed']
rep += ['', 'Now look at the sheets in ' + out + ' at full size:', ' place_*.jpg  - same furniture/window/camera as MASTER; red tiles first',
        ' order_*.jpg  - in story order: who is in the frame and is it logical at that moment (hero in bed on sick days, clothes, day/night)',
        ' text_*.jpg   - every caption/arrow: points at the right thing, covers no face, no typos',
        ' everywhere   - extra arms/hands/legs, anachronisms (domes, lamps, chimneys), readable fake text']
open(os.path.join(out, 'report.txt'), 'w').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
sys.exit(1 if fails else 0)
