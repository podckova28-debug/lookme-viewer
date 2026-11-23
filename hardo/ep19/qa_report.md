# QA report: Jobs_Disappearing_Fastest.mp4

Duration 285.9s, 143 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 285.80s audio 285.90s |
| all voice blocks present | PASS | 27/27 |
| narration fits the cut (no clipped ending) | PASS | planned 285.8s, final 285.9s |
| srt cues cover every block (>= blocks; ep14+ splits paragraphs into short cues) | PASS | 93 cues / 27 blocks |
| srt inside video duration | PASS | last cue ends 285.53s, video 285.90s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 0 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 143 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 148 |
| hand-written labels inside safe area | PASS | 95 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script | PASS | all readable clocks match |
| no isolated black marks (baked-in arrows) | PASS | none |
| loudness around -16 LUFS | PASS | -16.4 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 3 thumbnails |
| mp4 faststart (moov first) | PASS |  |
