# QA report: Why_Its_So_Hard_To_Be_A_Line_Cook.mp4

Duration 399.2s, 200 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 399.20s audio 399.20s |
| all voice blocks present | PASS | 30/30 |
| narration fits the cut (no clipped ending) | PASS | planned 399.9s, final 399.2s |
| srt cue count == blocks | PASS | 30 cues / 30 blocks |
| srt inside video duration | PASS | last cue ends 399.5s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 3 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 200 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 152 |
| hand-written labels inside safe area | PASS | 10 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 3 pairs ok |
| clip anomaly hints (morph / phantom / multiplication) | PASS | none |
| clocks agree with the script | PASS | all readable clocks match |
| isolated black marks (possible baked-in arrows/symbols) | WARN | F19: 1 at [(np.float64(0.21), np.float64(0.17), np.float64(0.29), np.float64(0.22))] |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
