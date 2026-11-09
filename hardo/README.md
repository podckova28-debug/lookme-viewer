# Hardo — animated profession explainers (Dinzo-style)

Lightweight part of the production pipeline for the YouTube channel "Hardo"
("Why It's So Hard to Be a …"). Heavy renders (mp4, Wan clips, generated frames)
are not in git; the hub page links to them on CloudFront.

- `pipeline/assemble_ep.py` — builds an episode from `plan.json`, `blocks.json`, `voice/NN.mp3`, `frames/*.png`, `clips/*.mp4`
  (Ken Burns stills, hand-lettered labels with arrows that snap to the text edge, Wan clips, SRT, loudness-normalised mix).
- `pipeline/qa_check.py` — 22-point QA on the finished mp4 (container, sync, SRT, white background, labels on white,
  arrows on ink and not stubs, clip drift, loudness, thumbnails). Exit 1 on any FAIL.
- `ep3/`, `ep4/` — plan, narration blocks, script with sources, YouTube metadata, QA report, thumbnails.
- `hub/hardo.html` (+ `hub/files/`) — the project hub page with download links, channel assets and the Dinzo comparison.

Episodes 1–2 live in the hub only (links and reports); their sources were produced in earlier sessions.
