# QA report: Why_Its_So_Hard_To_Be_A_Construction_Worker.mp4

Duration 472.8s, 236 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 472.77s audio 472.80s |
| all voice blocks present | PASS | 30/30 |
| narration fits the cut (no clipped ending) | PASS | planned 435.1s, final 472.8s |
| srt cue count == blocks | PASS | 30 cues / 30 blocks |
| srt inside video duration | PASS | last cue ends 473.1s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 3 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 236 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 129 |
| hand-written labels inside safe area | PASS | 78 labels ok |
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
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
