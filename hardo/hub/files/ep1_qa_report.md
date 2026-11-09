# QA report: Why_Its_So_Hard_To_Be_A_Nurse.mp4

Duration 119.6s, 60 sampled frames, 21 checks, 2 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 119.60s audio 119.60s |
| all voice blocks present | PASS | 9/9 |
| narration fits the cut (no clipped ending) | PASS | planned 119.8s, final 119.6s |
| srt cue count == blocks | PASS | 9 cues / 9 blocks |
| srt inside video duration | PASS | last cue ends 119.4s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 1 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 60 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 170 |
| hand-written labels inside safe area | PASS | 5 labels ok |
| labels do not cover drawing (ink under text < 6%) | FAIL | F06:'every night.' 37% ink under text; F08:'dinner' 99% ink under text; F10:'never rings' 17% ink under text |
| arrows point at something (ink near tip) | FAIL | F02:'not even yours' arrow tip on white (0.0% ink); F10:'never rings' arrow tip on white (0.0% ink) |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 3 thumbnails |
| mp4 faststart (moov first) | PASS |  |
