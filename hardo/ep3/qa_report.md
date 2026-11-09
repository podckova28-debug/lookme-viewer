# QA report: Why_Its_So_Hard_To_Be_A_Teacher.mp4

Duration 386.4s, 193 sampled frames, 21 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 386.40s audio 386.40s |
| all voice blocks present | PASS | 30/30 |
| narration fits the cut (no clipped ending) | PASS | planned 387.1s, final 386.4s |
| srt cue count == blocks | PASS | 30 cues / 30 blocks |
| srt inside video duration | PASS | last cue ends 386.7s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 4 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 193 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 167 |
| hand-written labels inside safe area | PASS | 7 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 2 thumbnails |
| mp4 faststart (moov first) | PASS |  |
