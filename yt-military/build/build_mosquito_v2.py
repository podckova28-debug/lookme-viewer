#!/usr/bin/env python3
"""Mosquito episode, v2: captions, number callouts, dissolves, clip audio, loudness."""
import os, subprocess, sys, json, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR, AU, VI = f"{ROOT}/frames", f"{ROOT}/audio", f"{ROOT}/video"
OUT = f"{ROOT}/build/out2"; SEG = f"{OUT}/seg"; TXT = f"{OUT}/txt"
for d in (SEG, TXT): os.makedirs(d, exist_ok=True)
FPS, W, H = 25, 1920, 1080
LEAD, TAIL, XF = 0.5, 3.0, 0.45          # lead-in, tail, dissolve length
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FONT2): FONT2 = FONT

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).decode().strip())

sec_files = sorted(f for f in os.listdir(AU) if f.startswith("sec"))
sec_dur = [dur(f"{AU}/{f}") for f in sec_files]

# shot: (kind, file, overlay or None, clip_trim or None)
# overlay: ("cap", text) lower-third caption | ("num", big, small) number callout | ("quote", text, attribution) | ("end",)
def S(n, ov=None): return ("still", f"{FR}/{n}", ov, None)
def V(n, ov=None, trim=None): return ("clip", f"{VI}/{n}", ov, trim)

plan = [
    [S("f16_hands_plane.png"), S("f17_nose_closeup.png"), V("v11s_channel_dawn.mp4"),
     S("f18_lancaster_crew.png"), S("f19_goering_mic.png"),
     S("ref1_mosquito_ground.png", ("cap", "de Havilland DH.98 Mosquito, 1942"))],
    [S("f20_ministry_room.png", ("cap", "Air Ministry, London, 1938")), S("f22_tail_gunner.png"),
     S("f23_bf110_night.png", ("num", "200 mph  vs  300+ mph", "bomber cruise  /  fighter attack speed")),
     S("f24_armour_plate.png"), S("f25_de_havilland.png", ("cap", "Geoffrey de Havilland")), S("f26_drafting_table.png")],
    [S("f27_dh88_comet.png", ("cap", "DH.88 Comet, 1934")), S("f78_air_ministry_facade.png"), S("f28_whitehall_corridor.png"),
     S("f29_folder_rejected.png"), S("f79_freeman_window.png", ("cap", "Air Chief Marshal Sir Wilfrid Freeman")),
     S("f30_freeman_desk.png", ("num", "“Freeman’s Folly”", "the nickname inside the Ministry")),
     S("f31_london_1940.png", ("cap", "London, summer 1940")), S("f80_hatfield_factory_1940.png"),
     S("f33_spitfire_factory.png"), S("f32_barn_night_prototype.png")],
    [S("f34_manor_moat_mist.png", ("cap", "Salisbury Hall, Hertfordshire, 1940")), S("f13_salisbury_hall.png"),
     S("f12_factory_moulds.png"), S("f35_balsa_sandwich.png", ("num", "birch  •  balsa  •  birch", "the sandwich skin")),
     S("f37_wiring_inside.png"), S("f36_fuselage_halves_join.png"), S("f38_one_piece_wing.png"), S("f39_piano_factory.png"),
     V("v40_prototype_takeoff.mp4", ("cap", "25 November 1940 — first flight"), 3.4), S("f41_outruns_spitfire.png")],
    [S("f42_merlin_engine.png", ("cap", "Rolls-Royce Merlin × 2")), V("v43_contrails.mp4", ("num", "≈ 400 mph", "with a bomb load and fuel for Berlin")),
     S("f44_nightfighter_cockpit.png"), S("f45_bomber_falling.png", ("num", "1 in 20", "heavy bomber losses per sortie, worst months")),
     S("f46_ops_room.png"), S("f47_crew_walk_dusk.png"),
     S("f48_squadron_lineup.png", ("num", "fewer than 1 in 100", "Mosquito losses per sortie"))],
    [S("f49_berlin_morning.png", ("cap", "Berlin, 30 January 1943")), S("f76_navigator_map.png"), S("f50_daylight_formation.png"),
     S("f51_radio_studio.png", ("cap", "11:00 — Göring’s broadcast is delayed")), S("f52_berlin_sirens.png"),
     S("f19_goering_mic.png", ("quote", "“I turn green and yellow with envy.”", "Hermann Göring, 1943")),
     S("f53_ta154_hangar.png", ("cap", "Focke-Wulf Ta 154 “Moskito”")), S("f54_glue_factory_ruins.png"), S("f55_german_spar_failed.png")],
    [S("f56_pr_blue_high.png"), S("f57_amiens_prison.png", ("cap", "Amiens, 18 February 1944 — Operation Jericho")),
     V("v15s_amiens_snow.mp4"), V("v58s_over_prison_wall.mp4"), S("f59_wall_breach_escape.png", ("num", "200+", "prisoners escaped")),
     S("f60_pickard_fighter_behind.png", ("cap", "Group Captain Percy Pickard, killed in action")),
     S("f61_cookie_bomb_loading.png", ("num", "4,000 lb", "the same bomb a Lancaster carried")),
     V("v62s_night_takeoff.mp4"), V("v14_berlin_night.mp4"), S("f63_cockpit_over_berlin.png")],
    [S("f64_burma_monsoon.png", ("cap", "Burma, 1944")), S("f65_skin_delaminating.png"), S("f66_broken_wing_india.png"),
     S("f67_investigators_tent.png"), S("f77_glue_pots.png", ("num", "casein  →  formaldehyde resin", "the glue that was changed")),
     S("f68_inspector_torch.png"), S("f43_high_altitude_contrails.png"),
     S("f69_me262_jet.png", ("cap", "Messerschmitt Me 262, 1944")), S("f70_cockpit_jet_contrail.png")],
    [S("f71_mosquito_vs_lancaster.png"), S("f72_smooth_skin_macro.png"),
     S("f73_canada_production_line.png", ("num", "7,781 built", "Britain, Canada and Australia")), S("f74_museum_today.png")],
    [V("v75_sunset.mp4"), S("frame2_thumbnail_ki84.png", ("end",))],
]

# --- timeline (true durations) ---------------------------------------------
timeline = []
for si, shots in enumerate(plan):
    total = sec_dur[si] + (LEAD if si == 0 else 0) + (TAIL if si == len(plan) - 1 else 0)
    clip_total = sum((t or 5.0417) for k, _, _, t in shots if k == "clip")
    nst = sum(1 for k, *_ in shots if k == "still")
    sd = (total - clip_total) / nst
    for k, p, ov, t in shots:
        timeline.append([k, p, ov, (t or 5.0417) if k == "clip" else sd])
N = len(timeline)
starts = []; acc = 0.0
for k, p, ov, d in timeline: starts.append(acc); acc += d
TOTAL = acc

# --- overlay filter builders ---------------------------------------------------
def esc(s): return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "%%")
def fade_alpha(t0, t1, f=0.5):
    return f"if(lt(t,{t0}),0,if(lt(t,{t0+f}),(t-{t0})/{f},if(lt(t,{t1-f}),1,if(lt(t,{t1}),({t1}-t)/{f},0))))"
def overlay_filter(ov, d, idx):
    if ov is None: return ""
    t0, t1 = 0.8, max(1.6, d - 0.6)
    a = fade_alpha(t0, t1)
    if ov[0] == "cap":
        tf = f"{TXT}/{idx}_cap.txt"; open(tf, "w").write(ov[1])
        return (f",drawbox=x=0:y=ih-150:w=iw:h=70:color=black@0.55:t=fill:enable='between(t,{t0},{t1})'"
                f",drawtext=fontfile={FONT2}:textfile={tf}:fontsize=38:fontcolor=white:x=80:y=h-150+18:alpha='{a}'")
    if ov[0] == "num":
        tf1 = f"{TXT}/{idx}_big.txt"; open(tf1, "w").write(ov[1])
        tf2 = f"{TXT}/{idx}_small.txt"; open(tf2, "w").write(ov[2])
        return (f",drawbox=x=80:y=ih-300:w=iw*0.62:h=200:color=black@0.5:t=fill:enable='between(t,{t0},{t1})'"
                f",drawtext=fontfile={FONT}:textfile={tf1}:fontsize=92:fontcolor=white:x=110:y=h-285:alpha='{a}'"
                f",drawtext=fontfile={FONT2}:textfile={tf2}:fontsize=36:fontcolor=0xDDDDDD:x=112:y=h-170:alpha='{a}'")
    if ov[0] == "quote":
        tf1 = f"{TXT}/{idx}_q.txt"; open(tf1, "w").write(ov[1])
        tf2 = f"{TXT}/{idx}_qa.txt"; open(tf2, "w").write("— " + ov[2])
        return (f",drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:enable='between(t,{t0},{t1})'"
                f",drawtext=fontfile={FONT}:textfile={tf1}:fontsize=78:fontcolor=white:x=(w-text_w)/2:y=h/2-90:alpha='{a}'"
                f",drawtext=fontfile={FONT2}:textfile={tf2}:fontsize=40:fontcolor=0xDDDDDD:x=(w-text_w)/2:y=h/2+40:alpha='{a}'")
    if ov[0] == "end":
        tf1 = f"{TXT}/{idx}_e1.txt"; open(tf1, "w").write("NEXT: the captured fighter the Americans couldn’t explain")
        tf2 = f"{TXT}/{idx}_e2.txt"; open(tf2, "w").write("SUBSCRIBE  ▶")
        a2 = fade_alpha(0.8, d - 0.2)
        return (f",drawbox=x=0:y=0:w=iw:h=130:color=black@0.6:t=fill:enable='gte(t,0.8)'"
                f",drawtext=fontfile={FONT2}:textfile={tf1}:fontsize=44:fontcolor=white:x=(w-text_w)/2:y=42:alpha='{a2}'"
                f",drawbox=x=iw/2-230:y=ih/2-48:w=460:h=96:color=red@0.9:t=fill:enable='gte(t,1.6)'"
                f",drawtext=fontfile={FONT2}:textfile={tf2}:fontsize=56:fontcolor=white:x=(w-text_w)/2:y=h/2-30:alpha='{fade_alpha(1.6, d-0.2)}'")
    return ""

# --- segment commands -------------------------------------------------------------
cmds = []
for i, (k, p, ov, d) in enumerate(timeline):
    out = f"{SEG}/{i:03d}.mp4"
    dr = d + (XF if i < N - 1 else 0)          # dissolve compensation
    if k == "still":
        n = int(round(dr * FPS))
        zin = (i % 2 == 0); pdir = 1 if (i // 2) % 2 == 0 else -1
        z = f"1+0.09*on/{n}" if zin else f"1.09-0.09*on/{n}"
        vf = (f"scale=2688:1512:flags=lanczos,zoompan=z='{z}':x='(iw-iw/zoom)/2+({pdir})*(on/{n}-0.5)*iw*0.025'"
              f":y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
        if i == 0:
            vf += (f",drawtext=fontfile={FONT}:text='THE BOMBER WITH NO GUNS':fontsize=72:fontcolor=white:borderw=3:"
                   f"bordercolor=black:x=(w-text_w)/2:y=h-200:alpha='{fade_alpha(0.6, 5.4, 0.6)}'")
        vf += overlay_filter(ov, dr, i)
        cmds.append(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", p, "-t", f"{dr:.3f}", "-vf", vf, "-r", str(FPS),
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-g", "50", "-an", out])
    else:
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration={XF+0.2},format=yuv420p" + overlay_filter(ov, dr, i))
        cmds.append(["ffmpeg", "-v", "error", "-y", "-i", p, "-t", f"{dr:.3f}", "-vf", vf, "-r", str(FPS),
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-g", "50", "-an", out])

json.dump([{"i": i, "kind": k, "src": os.path.basename(p), "start": round(starts[i], 2), "dur": round(d, 2),
            "overlay": ov} for i, (k, p, ov, d) in enumerate(timeline)], open(f"{OUT}/timeline.json", "w"), indent=1)
print(f"segments {N}, total {TOTAL:.1f}s, narration {sum(sec_dur):.1f}s")

if "--test" in sys.argv:
    want = {}
    for i, (k, p, ov, d) in enumerate(timeline):
        if ov and ov[0] not in want: want[ov[0]] = i
    for t, i in want.items():
        r = subprocess.run(cmds[i], capture_output=True, text=True)
        print(t, i, "ok" if r.returncode == 0 else r.stderr[-400:], flush=True)
    json.dump(want, open(f"{OUT}/test_idx.json", "w")); sys.exit(0)
if "--run" not in sys.argv: sys.exit(0)
t0 = time.time()
def run(ic):
    i, c = ic; r = subprocess.run(c, capture_output=True, text=True)
    print(f"seg {i} {'FAILED '+r.stderr[-400:] if r.returncode else 'ok'} ({time.time()-t0:.0f}s)", flush=True); return r.returncode
with ThreadPoolExecutor(4) as ex: rcs = list(ex.map(run, enumerate(cmds)))
if any(rcs): sys.exit(1)

# --- dissolve chain ---------------------------------------------------------------
inputs = []; fc = []
for i in range(N): inputs += ["-i", f"{SEG}/{i:03d}.mp4"]
prev = "[0:v]"; off = 0.0
for i in range(1, N):
    off += timeline[i-1][3]                     # true start of segment i
    lab = f"[x{i}]" if i < N - 1 else "[vout]"
    fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}")
    prev = lab
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-g", "50", "-an", f"{OUT}/video_only.mp4"], check=True)
print(f"dissolves done ({time.time()-t0:.0f}s)", flush=True)

# --- audio: narration + clip sound, loudness normalised ------------------------------
# input 0 = video, input 1 = narration, inputs 2.. = clips that carry sound
ain = ["-i", f"{AU}/full_narration_barrett.mp3"]; af = []; mix = ["[n]"]
af.append(f"[1:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad=pad_dur={TAIL}[n]")
k = 2
for i, (kind, p, ov, d) in enumerate(timeline):
    if kind == "clip" and subprocess.run(["ffprobe", "-v", "quiet", "-select_streams", "a", "-show_entries", "stream=codec_name",
                                          "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip():
        ain += ["-i", p]; ms = int(starts[i] * 1000)
        af.append(f"[{k}:a]atrim=0:{d:.3f},afade=t=in:d=0.4,afade=t=out:st={d-0.6:.3f}:d=0.6,volume=0.22,adelay={ms}|{ms}[c{k}]")
        mix.append(f"[c{k}]"); k += 1
af.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
vf = f"fade=t=in:st=0:d=1,fade=t=out:st={TOTAL-1.8:.2f}:d=1.8"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video_only.mp4", *ain, "-filter_complex",
                f"[0:v]{vf}[vout];" + ";".join(af),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{ROOT}/build/mosquito_v2.mp4"], check=True)
print(f"done in {time.time()-t0:.0f}s -> build/mosquito_v2.mp4")
