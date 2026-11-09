#!/usr/bin/env python3
"""Assemble the Mosquito episode: stills with slow camera moves, clips, narration."""
import os, subprocess, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR, AU, VI = f"{ROOT}/frames", f"{ROOT}/audio", f"{ROOT}/video"
OUT = f"{ROOT}/build/out"
SEG = f"{OUT}/seg"
os.makedirs(SEG, exist_ok=True)
FPS = 25
W, H = 1920, 1080
LEAD = 0.5      # silence before narration
TAIL = 2.0      # picture after narration ends
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def dur(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())

sections = [f"{AU}/sec{i:02d}_" for i in range(1, 11)]
sec_files = sorted(f for f in os.listdir(AU) if f.startswith("sec"))
sec_dur = [dur(f"{AU}/{f}") for f in sec_files]
CLIP = 5.0417

def S(name): return ("still", f"{FR}/{name}")
def V(name): return ("clip", f"{VI}/{name}")

# shot plan per narration section (order matters)
plan = [
    [S("f16_hands_plane.png"), S("f17_nose_closeup.png"), V("v11_channel_dawn.mp4"),
     S("f18_lancaster_crew.png"), S("f19_goering_mic.png"), S("ref1_mosquito_ground.png")],
    [S("f20_ministry_room.png"), S("f22_tail_gunner.png"), S("f23_bf110_night.png"),
     S("f24_armour_plate.png"), S("f25_de_havilland.png"), S("f26_drafting_table.png")],
    [S("f27_dh88_comet.png"), S("f28_whitehall_corridor.png"), S("f29_folder_rejected.png"),
     S("f30_freeman_desk.png"), S("f20_ministry_room.png"), S("f31_london_1940.png"),
     S("f33_spitfire_factory.png"), S("f32_barn_night_prototype.png")],
    [S("f34_manor_moat_mist.png"), S("f13_salisbury_hall.png"), S("f12_factory_moulds.png"),
     S("f35_balsa_sandwich.png"), S("f37_wiring_inside.png"), S("f36_fuselage_halves_join.png"),
     S("f38_one_piece_wing.png"), S("f39_piano_factory.png"), V("v40_prototype_takeoff.mp4"),
     S("f41_outruns_spitfire.png")],
    [S("f42_merlin_engine.png"), V("v43_contrails.mp4"), S("f44_nightfighter_cockpit.png"),
     S("f45_bomber_falling.png"), S("f46_ops_room.png"), S("f47_crew_walk_dusk.png"),
     S("f48_squadron_lineup.png")],
    [S("f49_berlin_morning.png"), S("f76_navigator_map.png"), S("f50_daylight_formation.png"),
     S("f51_radio_studio.png"), S("f52_berlin_sirens.png"), S("f19_goering_mic.png"),
     S("f53_ta154_hangar.png"), S("f54_glue_factory_ruins.png"), S("f55_german_spar_failed.png")],
    [S("f56_pr_blue_high.png"), S("f57_amiens_prison.png"), V("v15_amiens_snow.mp4"),
     V("v58_over_prison_wall.mp4"), S("f59_wall_breach_escape.png"), S("f60_pickard_fighter_behind.png"),
     S("f61_cookie_bomb_loading.png"), V("v62_night_takeoff.mp4"), V("v14_berlin_night.mp4"),
     S("f63_cockpit_over_berlin.png")],
    [S("f64_burma_monsoon.png"), S("f65_skin_delaminating.png"), S("f66_broken_wing_india.png"),
     S("f67_investigators_tent.png"), S("f77_glue_pots.png"), S("f68_inspector_torch.png"),
     S("f43_high_altitude_contrails.png"), S("f69_me262_jet.png"), S("f70_cockpit_jet_contrail.png")],
    [S("f71_mosquito_vs_lancaster.png"), S("f72_smooth_skin_macro.png"),
     S("f73_canada_production_line.png"), S("f74_museum_today.png")],
    [V("v75_sunset.mp4"), S("frame2_thumbnail_ki84.png")],
]

# --- timeline -------------------------------------------------------------
timeline = []  # (kind, path, duration)
for si, shots in enumerate(plan):
    total = sec_dur[si]
    if si == 0: total += LEAD
    if si == len(plan) - 1: total += TAIL
    nclips = sum(1 for k, _ in shots if k == "clip")
    nstills = len(shots) - nclips
    still_d = (total - nclips * CLIP) / nstills
    for k, p in shots:
        timeline.append((k, p, CLIP if k == "clip" else still_d))

# --- per-segment ffmpeg commands ---------------------------------------------
cmds, concat = [], []
for i, (kind, path, d) in enumerate(timeline):
    out = f"{SEG}/{i:03d}.mp4"
    concat.append(out)
    if kind == "still":
        n = int(round(d * FPS))
        zin = (i % 2 == 0)
        pdir = 1 if (i // 2) % 2 == 0 else -1
        z = f"1+0.09*on/{n}" if zin else f"1.09-0.09*on/{n}"
        x = f"(iw-iw/zoom)/2+({pdir})*(on/{n}-0.5)*iw*0.025"
        y = f"(ih-ih/zoom)/2"
        vf = (f"scale=2688:1512:flags=lanczos,"
              f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p")
        if i == 0:
            vf += (f",drawtext=fontfile={FONT}:text='THE BOMBER WITH NO GUNS':fontsize=72:"
                   f"fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-200:"
                   f"alpha='if(lt(t,0.6),t/0.6,if(lt(t,4.4),1,max(0,(5-t)/0.6)))':enable='lt(t,5)'")
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", path, "-t", f"{d:.3f}",
               "-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
               "-g", "50", "-an", out]
    else:
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop={W}:{H},fps={FPS},format=yuv420p")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", path, "-t", f"{d:.3f}", "-vf", vf,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-g", "50", "-an", out]
    cmds.append(cmd)

with open(f"{OUT}/segments.json", "w") as f:
    json.dump([{"i": i, "kind": k, "src": os.path.basename(p), "dur": round(d, 3)}
               for i, (k, p, d) in enumerate(timeline)], f, indent=1)
with open(f"{OUT}/concat.txt", "w") as f:
    for p in concat: f.write(f"file '{p}'\n")
with open(f"{OUT}/cmds.sh", "w") as f:
    for c in cmds:
        f.write(" ".join(f"'{a}'" if (" " in a or "'" in a or "(" in a) else a for a in c) + "\n")

total = sum(d for _, _, d in timeline)
print(f"segments: {len(timeline)}  video length: {total:.1f}s  narration: {sum(sec_dur):.1f}s")

# --- run --------------------------------------------------------------------
if "--run" in sys.argv:
    from concurrent.futures import ThreadPoolExecutor
    import time
    t0 = time.time()
    only = [int(a) for a in sys.argv if a.isdigit()]
    todo = [(i, c) for i, c in enumerate(cmds) if not only or i in only]
    def run(ic):
        i, c = ic
        r = subprocess.run(c, capture_output=True, text=True)
        if r.returncode: print(f"segment {i} FAILED: {r.stderr[-300:]}", flush=True)
        else: print(f"segment {i} ok ({time.time()-t0:.0f}s)", flush=True)
        return r.returncode
    with ThreadPoolExecutor(4) as ex:
        rcs = list(ex.map(run, todo))
    if only or any(rcs): sys.exit(1 if any(rcs) else 0)
    # concat video
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/concat.txt",
                    "-c", "copy", f"{OUT}/video_only.mp4"], check=True)
    # mux narration: lead-in silence, fade out at the end
    afilter = f"adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad=pad_dur={TAIL},afade=t=out:st={LEAD+sum(sec_dur)-0.3}:d=1.2,volume=1.0"
    vfilter = f"fade=t=in:st=0:d=1,fade=t=out:st={total-1.5}:d=1.5"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video_only.mp4", "-i", f"{AU}/full_narration_barrett.mp3",
                    "-filter_complex", f"[0:v]{vfilter}[v];[1:a]{afilter}[a]", "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", f"{ROOT}/build/mosquito_draft_v1.mp4"], check=True)
    print(f"done in {time.time()-t0:.0f}s -> build/mosquito_draft_v1.mp4")
