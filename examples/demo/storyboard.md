# One request, three components

30-second landscape, dark explanatory walkthrough. Audio update: local Kokoro narration and quiet original music, explicitly requested by the user; voice timing/script are in `narration.json`, and the mix/provenance are in `docs/audio-update.md`. Source: evidence.md, illustrative brief E1.

| Seconds | Visible heading | Action | Evidence |
|---|---|---|---|
| 0–6 | Start at the browser. | Introduce browser | E1 |
| 6–12 | The API handles the request. | Reveal Python API and draw HTTPS edge | E1 |
| 12–18 | SQLite stays local. | Reveal SQLite, host boundary and reads/writes edge | E1 |
| 18–24 | Follow the data path. | Packets follow the two confirmed edges | E1 |
| 24–30 | One request. Three components. | Hold full architecture; no additional services implied | E1 |

The composition embeds the generated diagram DOM/styles/fonts/icons. Source geometries are retained; only reveal/trace/packet overlays and video-scale headers are added. Measured-length edge tracing follows the HyperFrames svg-stroke-trace registry primitive; no whole-composition camera move. GSAP 3.14.2 loads from the pinned CDN URL during compilation. Diagram media/fonts are embedded.

The initial silent version was approved and verified at 1920×1080, 30 fps, 900 frames, 30.000000 seconds. The subsequent narration/music preview was also explicitly approved, then rendered and verified with a 30-second stereo AAC track. Historical silent evidence is in docs/verification.md; current audio acceptance and source provenance are in docs/audio-update.md.
