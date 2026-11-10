# QA report: Why_Its_So_Hard_To_Be_An_Underwater_Welder.mp4

Duration 422.3s, 211 sampled frames, 26 checks, 0 FAIL

| Check | Status | Detail |
|---|---|---|
| 1080p30 | PASS | 1920x1080 @ 30/1 |
| audio track present | PASS | aac |
| video/audio length match | PASS | video 422.20s audio 422.31s |
| all voice blocks present | PASS | 27/27 |
| narration fits the cut (no clipped ending) | PASS | planned 422.9s, final 422.3s |
| srt cue count == blocks | PASS | 27 cues / 27 blocks |
| srt inside video duration | PASS | last cue ends 422.01s, video 422.31s |
| srt no overlaps | PASS | 0 overlaps |
| srt text == script | PASS | 0 differ |
| animated clips present and long enough | PASS | 4 clips; ok |
| white-background rule (mean luminance >= 120 on all samples) | PASS | 0 dark samples of 211 |
| no frozen video (>=6s without any motion) | PASS | 0 frozen samples |
| no pure black frames | PASS | min luminance 137 |
| hand-written labels inside safe area | PASS | 96 labels ok |
| labels do not cover drawing (ink under text < 6%) | PASS | ok |
| arrows point at something (ink near tip) | PASS | ok |
| arrows start outside their text and are not stubs | PASS | ok |
| animated clips keep the scene (no morphing drift) | PASS | ok |
| first/last frame pairs are animatable (same composition) | PASS | 0 pairs ok |
| clip anomaly hints (look at these clips frame by frame) | WARN | F406: objects multiply: components 1 -> 6 | F207: objects multiply: components 1 -> 4 |
| clocks agree with the script (detector reading, verify by eye) | WARN | F424: clock reads 3:08, no time in this block |
| isolated black marks (possible baked-in arrows/symbols) | WARN | F123: 8 at [(0.34, 0.45, 0.35, 0.56), (0.39, 0.45, 0.39, 0.56), (0.43, 0.45, 0.44, 0.56), (0.48, 0.45, 0.48, 0.56), (0.52, 0.45, 0.53, 0.56), (0.56, 0.45, 0.57, 0.56), (0.61, 0.45, 0.62, 0.56), (0.66, 0.45, 0.66, 0.56)] |
| loudness around -16 LUFS | PASS | -16.1 LUFS |
| no silence gaps > 2.5s | PASS | 0 gaps |
| thumbnails 1280x720 jpg < 2MB | PASS | 3 thumbnails |
| mp4 faststart (moov first) | PASS |  |

## Blind checks
- Frames: two full blind passes (108 frames) + re-check of every fixed frame. No mutations found. Fixed: off-style phone screen (F116),
  umbilical ending on a wall + fins (F27), red sleeves on the helmet-cam (F112), lookalike red jacket + floating fork (F420), logos/pseudo-text
  (F02, F04, F221, F412, F414), tally marks (F123), no white fade (F426), chamber costume (F22), dark background (F419).
- Final video: 108 shots from the final file checked by two independent reviewers. No mutations. Fixed after it: 1-in-600 icon grid redrawn
  (was 1 in 200), bar chart labelled, bends silhouette label + head crop, back-facing helmet (F27), labels moved/removed where the picture
  did not show the named thing.
- Voice: ASR check of all 27 blocks; block 27 re-voiced ("weld" heard as "world").
