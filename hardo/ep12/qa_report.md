# QA report: Jobs_That_Will_Appear_In_10_Years.mp4

Duration 508.0s, 254 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 507.97s audio 508.01s |
| all voice blocks present | PASS | 27/27 |
| narration fits the cut (no clipped ending) | PASS | planned 508.6s, final 508.0s |
| srt cue count == blocks | PASS | 27 cues / 27 blocks |
| srt inside video duration | PASS | last cue ends 507.90s, video 508.01s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 4 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 254 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 131 |
| hand-written labels inside safe area | PASS | 104 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (look at these clips frame by frame) | WARN | F206: objects multiply: components 4 -> 9 | F417: objects multiply: components 1 -> 5 |
| clocks agree with the script (detector reading, verify by eye) | WARN | F218: clock reads 8:35, no time in this block | F120: clock reads 1:46, no time in this block | F120: clock reads 4:08, no time in this block |
| no isolated black marks (baked-in arrows) | PASS | none |
| loudness around -16 LUFS | PASS | -16.3 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 3 thumbnails |
| mp4 faststart (moov first) | PASS |  |

## Blind checks
- Frames: two full blind passes (108 frames) + re-checks of every fixed frame; 20 frames fixed (third arms, ghost/orphan hands, cast lookalikes, logos, a duplicated character, melted map icons).
- Final video: 108 shots grabbed from the final file, checked by two independent reviewers at 2-4x crops, plus clips/subtitles/zoom review.
  Fixed after it: lineup F202/F227 hand recoloured (auditor's hand had the wrong skin tone), two-handled mug F224, robot halo F426,
  "#6" order on F11, arrow "robots need teachers" -> robot trainer on F25, "size of a bus" removed, last SRT cue inside the video,
  4% zoom on F202/F211/F222 (edge touches), F206 clip trimmed to 2.4 s.
