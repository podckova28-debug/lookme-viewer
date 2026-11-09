# QA report: Why_Its_So_Hard_To_Be_A_Truck_Driver.mp4

Duration 343.2s, 172 sampled frames, 27 checks, 1 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 343.13s audio 343.20s |
| all voice blocks present | PASS | 30/30 |
| narration fits the cut (no clipped ending) | PASS | planned 316.3s, final 343.2s |
| srt cue count == blocks | PASS | 30 cues / 30 blocks |
| srt inside video duration | PASS | last cue ends 343.5s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 2 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | FAIL | 22 dark samples of 172, first at 56s |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 91 |
| hand-written labels inside safe area | PASS | 9 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 2 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script (detector reading, verify by eye) | WARN | F02: clock reads 7:07, script says ['4:50'] | F02: clock reads 7:08, script says ['4:50'] | F02: clock reads 7:08, script says ['4:50'] | F06: clock reads 9:00, script says ['5:00'] | F06: clock reads 9:00, script says ['5:00'] | F23: clock reads 10:23, no time in this block |
| isolated black marks (possible baked-in arrows/symbols) | WARN | F01: 3 at [(np.float64(0.07), np.float64(0.07), np.float64(0.12), np.float64(0.11)), (np.float64(0.89), np.float64(0.53), np.float64(1.0), np.float64(0.54)), (np.float64(0.89), np.float64(0.62), np.float64(0.96), np.float64(0.74))] | F02: 5 at [(np.float64(0.0), np.float64(0.0), np.float64(0.04), np.float64(0.54)), (np.float64(0.0), np.float64(0.0), np.float64(0.06), np.float64(0.58)), (np.float64(0.25), np.float64(0.69), np.float64(0.34), np.float64(0.79)), (np.float64(0.57), np.float64(0.69), np.float64(0.65), np.float64(0.79)), (np.float64(0.36), np.float64(0.94), np.float64(0.54), np.float64(1.0))] | F03: 2 at [(np.float64(0.0), np.float64(0.0), np.float64(1.0), np.float64(0.93)), (np.float64(0.0), np.float64(0.11), np.float64(0.04), np.float64(0.48))] | F10: 1 at [(np.float64(0.19), np.float64(0.15), np.float64(0.22), np.float64(0.28))] | F24: 1 at [(np.float64(0.56), np.float64(0.01), np.float64(0.73), np.float64(0.42))] | F34: 1 at [(np.float64(0.88), np.float64(0.77), np.float64(1.0), np.float64(1.0))] | F35: 2 at [(np.float64(0.98), np.float64(0.0), np.float64(1.0), np.float64(0.24)), (np.float64(0.7), np.float64(0.83), np.float64(1.0), np.float64(0.9))] | F37: 1 at [(np.float64(0.0), np.float64(0.98), np.float64(0.31), np.float64(0.98))] |
| hero appears once per frame (colour clusters) | WARN | F02: 2 hero-coloured figures | F03: 3 hero-coloured figures | F04: 3 hero-coloured figures | F06: 2 hero-coloured figures | F09: 3 hero-coloured figures | F11: 2 hero-coloured figures | F12: 3 hero-coloured figures | F14: 2 hero-coloured figures | F20: 2 hero-coloured figures | F22: 2 hero-coloured figures | F32: 5 hero-coloured figures | F33: 2 hero-coloured figures | F34: 3 hero-coloured figures | F35: 3 hero-coloured figures |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
