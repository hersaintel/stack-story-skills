# Architecture walkthrough contract

## Run directory and required artifacts

Create `stack-video-output/` under the requested project (or the user's designated output area). If it exists, create a new timestamped sibling; get the timestamp from the system, not memory. Never overwrite a previous run. Keep private manifests out of a repository unless explicitly approved for publication.

| Artifact | Required content |
|---|---|
| `evidence.md` | Source location/line or explicit user statement for each claim; confirmed facts, dependency-only findings, assumptions, unknowns |
| `architecture.json` | Nodes with stable ids/labels/roles/evidence references; edges with source/target/meaning/evidence references; uncertain edges explicitly marked |
| `resolved-config.json` | Validated format/duration/theme/tone/music/voice for this run |
| `storyboard.md` | Beat timings summing to duration, exact visible copy, source references, visual action, narration text when requested |
| `diagram/` | Reused or generated self-contained HTML plus browser-exported light/dark PNGs; source provenance |
| `composition/` | Editable HyperFrames project with local assets, deterministic registered timeline, root dimensions/duration matching config |
| `verification.md` | Check command/results, frame checks, audio probes, approval status, blockers; append encoded-media results after rendering |
| `stack.mp4`, `poster.jpg` | Final deliverables only after approval and successful verification |

## Evidence first

Inspect only the scoped project files, using `search_files` and `read_file`. Do not open `.env`, credentials, unrelated workspaces or sensitive notes to discover a stack. A manifest establishes a dependency; source usage/configuration can establish a runtime role; live deployment claims need actual deployment evidence. Do not invent protocol, provider, latency, throughput or security properties. If an existing diagram disagrees with the evidence, reconcile it rather than reproduce the error. State illustrative examples as illustrative.

For the supplied Browser → Python API → local SQLite example, valid facts are HTTPS on the browser edge and reads/writes on the database edge. SQLite is embedded/local, not a network database server. Redis in dependencies alone belongs in the unknown/dependency-only list, not the request path.

## Story shape

1. Orient: what system and question does the flow explain?
2. Introduce the runtime components and boundaries.
3. Trace one request or job through the actual edges, labeling protocol/operation only where known.
4. End with the full architecture and a concise takeaway.

Use the requested tone in wording and pacing; keep the technical claims unchanged. Hold labels long enough to read. The 30-second default is an architecture explanation, not brag's 15–25-second launch formula. Vertical layouts should stack nodes and use vertical safe margins; square layouts must be authored for square, not cropped after rendering.

## Audio decisions

- `music: "off"`: no music generation, download or track. Never add a brag soundtrack implicitly.
- Music file: probe with FFprobe, ensure it contains decodable audio, confirm reuse rights, copy to local composition assets and use the HyperFrames audio contract for placement/mixing.
- `voice: false`: no voice provider invocation.
- `voice: true`: read the installed media/TTS guidance, inspect available routes without printing secrets, and generate or accept narration. Missing TTS/recording is a blocker, not permission to output a silent final. Provider installation, paid calls and cloud uploads require their own scope/consent. Record timing, intelligibility and whether music masks narration.

## Composition and checks

Load HyperFrames domain contracts before authoring. Search the local registry by the intended motion before hand-building motion. Reuse meaningful primitives where available. Keep all runtime media/fonts local; one paused registered timeline; no wall-clock/random/network-dependent animation. Preserve source diagram proportions and logo colors. Narrate or label why the components connect, not just their names.

Run from `composition/` through `terminal`, inspecting installed `--help` before relying on flags:

```text
npx hyperframes check --snapshots
npx hyperframes preview --background
```

Read the returned preview URL and verify HTTP 200. Deliver the Studio URL with its project hash; keep it alive during review. Record **awaiting final preview approval** and stop. Do not treat passing checks or an approved plan as render consent.

After explicit final-preview approval:

```text
npx hyperframes render --quality delivery --workers 1 --output ../stack.mp4
ffprobe -v error -show_format -show_streams -of json ../stack.mp4
```

Use one worker on constrained machines, checking the worker's actual memory budget rather than just host RAM. Compare encoded duration within one frame, configured dimensions, fps and audio presence. Extract and visually inspect frames at the opening, each major flow beat and final settled architecture with `vision_analyze`. Choose a readable representative poster, not a blank entrance frame. If a renderer/browser fails, record the exact blocker and deliver the checked source; never fabricate a video or substitute a different renderer without agreement. Stop preview after review ends.

## Delivery

Use `MEDIA:` for local MP4, poster and a source archive if requested. Include only a short result summary: what was verified, requested options not exercised, and remaining blockers. Keep scripts/source and artifacts separate; the configuration helper validates intent, it does not implement a universal video renderer. Public pack approval does not authorize publication of a future project's topology or source.
