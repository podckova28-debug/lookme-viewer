# QA report: The_Weirdest_Jobs_In_The_World.mp4

Duration 427.5s, 214 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 427.43s audio 427.51s |
| all voice blocks present | PASS | 27/27 |
| narration fits the cut (no clipped ending) | PASS | planned 428.1s, final 427.5s |
| srt cue count == blocks | PASS | 27 cues / 27 blocks |
| srt inside video duration | PASS | last cue ends 427.7s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 4 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 214 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 122 |
| hand-written labels inside safe area | PASS | 93 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script (detector reading, verify by eye) | WARN | F402: clock reads 10:51, no time in this block |
| no isolated black marks (baked-in arrows) | PASS | none |
| loudness around -16 LUFS | PASS | -16.1 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
