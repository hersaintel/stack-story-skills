# Verification

## Source and offline checks

`python3 -m unittest discover -s tests -v`: **14 tests passed** at the current preview checkpoint. Configuration covers defaults, all override fields, project/override precedence, input non-mutation, invalid types/keys, non-finite/out-of-range durations, missing/malformed files, relative music paths and paths with spaces. Installer covers individual/both installation, collision preservation, symlink refusal, interrupted-copy cleanup and CLI errors. Diagram tests cover resource presence, inlining and unresolved-token failure. Sample tests cover embedded fonts, seek-safe motion and silent 1920×1080/30-second root metadata.

The first diagram tests failed because the vendored implementation/resources were absent. The five config and five installer tests also failed before their implementations existed. A later installer-test interruption stub incorrectly rejected shutil's recursive positional arguments; the test stub was corrected, not the production installer. A sample regression failed on unsupported host fallback fonts before the composition font stack and CSS transition were corrected.

These tests do not establish cloud rendering, a universal automated video renderer, crash-safe installation or concurrent-writer isolation.

## Installed skills

Both `stack-diagram` and `stack-video` were installed into the active default profile after a disposable-directory smoke install. Both names loaded successfully through the native `skill_view` tool, with their linked resources visible. Installed file hashes matched source, excluding Python caches. Before/after hashing confirmed **all 288 files in the existing brag skill were unchanged**. The installer does not install render dependencies.

## Diagram runtime

```text
python3 skills/stack-diagram/scripts/build.py examples/demo/diagram/draft.html .runtime/icons examples/demo/diagram/stack.html --fonts skills/stack-diagram/assets/fonts
<isolated-python> skills/stack-diagram/scripts/render_png.py examples/demo/diagram/stack.html examples/demo/diagram/stack.png --scale 2
```

Both PNGs rendered at 2000×720 and were opened with the vision tool. Browser, Python API, local SQLite, HTTPS and reads/writes labels were legible in both themes, with no clipping or arrow-through-label defect observed. The illustrative diagram uses bundled generic pictograms only. The diagram's built HTML embeds fonts and icons.

The system Playwright Python import succeeded but its driver was broken (missing system cli.js). An isolated project-local Python environment with Playwright 1.64.1 launched Chromium successfully and performed the PNG exports. No system package was replaced.

## Video preview acceptance

Engine: HyperFrames CLI **0.9.19**, local Chromium, Node **26.7.0**. Composition: `examples/demo/composition/index.html`; associated `index.motion.json` declares appearance/order/in-frame assertions.

```text
npx --yes hyperframes check examples/demo/composition --snapshots --json
```

Latest check: **ok: true**. Zero lint errors, runtime errors, layout errors, motion errors or contrast errors. Nine layout samples; 300 motion samples; all 69 contrast checks passed. There are six maintainability lint warnings (five nested header scenes and one dense timeline track), plus one intentional-silence craft warning. These are not hidden or described as strict-mode success. Roles and labels were enlarged after the first check; unsupported font fallbacks and browser-clock CSS transitions were removed from the video derivative, not upstream resources.

Two representative browser snapshots (API introduction and full final architecture) were visually inspected. The preview server returned HTTP 200 and opened the actual Studio project in the desktop preview pane. The composition reuses the built diagram DOM and adds deterministic reveal, measured-length edge tracing, packet overlays and headings. The measured-length trace pattern follows the local registry's svg-stroke-trace example. The pinned GSAP CDN script is resolved at initial composition compilation.

**Final preview approval received; MP4 rendered and FFprobe acceptance passed.** The run is intentionally landscape, dark, 30 seconds, no music, no voice.

Source snapshot: `0f4f3af` (executable composition unchanged from reviewed `0e91d40`). After preview approval, the parent ran:

```text
npx --yes hyperframes@0.9.19 render examples/demo/composition --quality delivery --workers 1 --fps 30 --output examples/demo/stack.mp4
ffprobe -v error -show_format -show_streams -of json examples/demo/stack.mp4
```

Actual result: **H.264, 1920×1080, 30/1 fps, 900 frames, 30.000000 seconds, zero audio streams, 1,363,927 bytes**. SHA-256: `df71dfd69b0105b2fc2b612fe210bf856b9014185ef2542465bb3f1f2d298e4b`. Render summary: **beginframe capture, hardware GPU**, one worker, approximately 99.3 seconds. Duration matches exactly, within the one-frame acceptance tolerance. File metadata contains renderer/encoder versions and container brands, not personal paths.

A contact sheet extracted from the encoded MP4 at 2/8/14/20/26 seconds was visually inspected: distinct headings, progressive node introduction and flow tracing were present, with no clipping or corruption observed. `poster.jpg` is the inspected full-architecture frame extracted at 28.3 seconds, not a mockup or a blank entrance frame. The final MP4 and poster are included under `examples/demo/`.

## Behavioral evaluation

Fresh no-guidance controls were recorded separately for both skills. The diagram control chose SVG as visual source rather than the upstream HTML contract; the video control already handled evidence and unavailable narration correctly but lacked the concrete engine/config/preview contract. Fresh post-skill application-contract evaluation passed all five diagram and all seven video contract elements. It was read-only: no helper execution or rendering by that evaluator. No safety improvement is claimed where the control already passed. See `docs/evaluation/`.

## Not exercised end to end

Requested narration/provider setup, music mixing, vertical/square reflow, alternate tones/themes/durations as encoded media, live brand-logo downloads, cloud rendering, gallery sharing and TSX conversion. Configuration validation covers their relevant option fields, not every render outcome. No private project topology, source or audio was uploaded.

## Independent review and publication

Independent source review found no Critical/Important issue and one deferred minor: an extremely large integer duration can raise OverflowError before the range check, resulting in a traceback instead of a friendly validation error. The parent reproduced it. See `docs/review.md` for snapshot, evidence, dispositions and limitations. The encoded-video acceptance above is parent verification of the unchanged reviewed composition; it is not attributed to the source reviewer. Public GitHub branch/commit/tree/README verification is performed separately at handoff, not inferred from installation or push success.
