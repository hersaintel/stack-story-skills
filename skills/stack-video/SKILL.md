---
name: stack-video
description: Use when an architecture walkthrough video is requested.
version: 0.1.0
author: Cory (hersaintel), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [architecture, stack, video, hyperframes, data-flow]
    related_skills: [stack-diagram]
---

# Stack Video

Create an evidence-grounded architecture walkthrough using HyperFrames directly. This is not a brag wrapper: do not invoke, edit, or require brag. The output is an explanation of components and request/data flow, not an app-launch advertisement.

## When to Use

- “Make a video about this stack,” “animate the architecture,” or “explain this request flow.”
- A repository, explicit technology/topology brief, or an existing diagram is available.
- For a still image only, use stack-diagram. For a product-launch video, use brag separately.

## Prerequisites

Load `hyperframes-core`, `hyperframes-cli`, `hyperframes-animation`, and `hyperframes-creative` plus their task-specific references before composition authoring. They must be installed separately; if absent, report the dependency instead of claiming this pack includes them. HyperFrames needs Node.js 22+, FFmpeg/FFprobe and its Chromium browser. Diagram PNG export also needs Python 3.9+ with working Playwright/Chromium. No paid service or API key is needed for silent local videos. Narration needs an explicitly available TTS route or supplied recording; music needs an existing local audio file with usage permission.

## Configuration

Resolve `<skill>` to this SKILL.md's directory. Use `read_file` for project `stack-video.json` if present and `terminal` to run the helper with explicit paths. Missing an explicitly selected file is an error; no file means defaults. Overrides > project JSON > defaults.

| Field | Accepted | Default |
|---|---|---|
| format | landscape (1920×1080), vertical (1080×1920), square (1080×1080) | landscape |
| duration | finite number, 10–120 seconds | 30 |
| theme | light, dark | dark |
| tone | non-empty direction string | explanatory |
| music | off or existing local audio file path | off |
| voice | JSON boolean; CLI --voice / --no-voice | false |

Canonical example through `terminal` (replace paths with resolved paths):

```text
python "<skill>/scripts/config.py" --config "<project>/stack-video.json" --format vertical --duration 30 --no-voice
```

Without a file, omit `--config`. Save stdout as `resolved-config.json` in a new run directory; do not invent unsupported renderer flags from these option names. Music paths in JSON resolve against that file; CLI music paths resolve against the current working directory. Unknown keys and invalid values fail. File existence is not an audio codec/license check: probe audio before composition.

## Procedure

Read [references/workflow.md](references/workflow.md) and complete its artifact contract in order:

1. Evidence and graph: record confirmed nodes/edges with source references; dependencies alone do not establish a runtime service. Explicit user topology counts as evidence. Separate assumptions and unknowns.
2. Normalize config and write storyboard/narration script. Each scene references evidence and fits the duration.
3. Reuse a supplied diagram only after checking it matches the graph; otherwise use stack-diagram. HTML is the diagram's visual source. Animate diagram elements or derived browser PNGs; keep claims consistent.
4. Build a seek-safe HyperFrames composition using the actual chosen dimensions and root duration. Music off means no music asset/track; voice false means no narration. With voice true and no functioning TTS/recording, mark **blocked: narration unavailable** and stop before final rendering. Offer setup, supplied recording, or a silent version only with approval; never silently disable voice.
5. Run `hyperframes check`, inspect representative snapshots and verify exact current command support via `--help`. Open the final Studio preview and **wait for explicit preview approval** before rendering. Design/storyboard approval alone is not video approval.
6. Render locally, probe duration/dimensions/fps/audio and inspect encoded frames. Deliver actual MP4, poster, editable source, and verification report via `MEDIA:/absolute/path/to/file`.

## Pitfalls

- A package dependency is not a deployed node; show Redis only when its runtime role is evidenced.
- A static diagram zoom is not a walkthrough: reveal components, trace a meaningful flow, then hold the full architecture long enough to read.
- Small diagram labels will not survive vertical framing; reflow/relabel rather than shrink a landscape canvas.
- Do not import brag music assets automatically or change any other skill's defaults.
- Never publish project artifacts, upload source, call cloud render, send feedback containing project data, or submit to a gallery without separate consent.

## Verification

All required artifacts exist; graph claims map to evidence; resolved options match the invocation; `check` passes with real browser samples; final preview approval is recorded; encoded media matches duration within one frame at the chosen fps, exact dimensions, and intended audio tracks. Report unverified options/providers separately. A checked composition without an encoded MP4 is a preview checkpoint, not a completed video.
