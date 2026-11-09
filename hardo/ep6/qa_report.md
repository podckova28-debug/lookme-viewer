# QA report: Why_Its_So_Hard_To_Be_A_Flight_Attendant.mp4

Duration 550.8s, 275 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 550.70s audio 550.80s |
| all voice blocks present | PASS | 30/30 |
| narration fits the cut (no clipped ending) | PASS | planned 484.3s, final 550.8s |
| srt cue count == blocks | PASS | 30 cues / 30 blocks |
| srt inside video duration | PASS | last cue ends 550.5s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 0 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 275 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 144 |
| hand-written labels inside safe area | PASS | 6 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script | PASS | all readable clocks match |
| isolated black marks (possible baked-in arrows/symbols) | WARN | F106: 1 at [(np.float64(0.32), np.float64(0.03), np.float64(0.67), np.float64(0.17))] | F107: 3 at [(np.float64(0.0), np.float64(0.5), np.float64(0.03), np.float64(0.7)), (np.float64(0.86), np.float64(0.5), np.float64(0.95), np.float64(0.59)), (np.float64(0.0), np.float64(0.71), np.float64(0.13), np.float64(0.88))] | F109: 1 at [(np.float64(0.44), np.float64(0.19), np.float64(0.49), np.float64(0.66))] | F122: 2 at [(np.float64(0.58), np.float64(0.03), np.float64(0.81), np.float64(0.04)), (np.float64(0.86), np.float64(0.49), np.float64(0.87), np.float64(1.0))] | F123: 1 at [(np.float64(0.23), np.float64(0.15), np.float64(0.43), np.float64(0.19))] | F29: 3 at [(np.float64(0.64), np.float64(0.06), np.float64(0.64), np.float64(0.93)), (np.float64(0.43), np.float64(0.33), np.float64(0.43), np.float64(0.79)), (np.float64(0.45), np.float64(0.93), np.float64(0.64), np.float64(0.93))] |
| loudness around -16 LUFS | PASS | -16.2 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
