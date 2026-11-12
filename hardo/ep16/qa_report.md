# QA report: The_Loneliest_Jobs_On_Earth.mp4

Duration 431.5s, 216 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 431.47s audio 431.46s |
| all voice blocks present | PASS | 27/27 |
| narration fits the cut (no clipped ending) | PASS | planned 431.5s, final 431.5s |
| srt cues cover every block (>= blocks; ep14+ splits paragraphs into short cues) | PASS | 127 cues / 27 blocks |
| srt inside video duration | PASS | last cue ends 431.13s, video 431.47s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 0 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 216 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 140 |
| hand-written labels inside safe area | PASS | 100 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script | PASS | all readable clocks match |
| no isolated black marks (baked-in arrows) | PASS | none |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 3 thumbnails |
| mp4 faststart (moov first) | PASS |  |
