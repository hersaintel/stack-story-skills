# Stack Story Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Install and publicly publish independent stack-diagram and stack-video skills without modifying brag.

**Architecture:** Vendor only the pinned upstream skill directory with licenses and provenance. Add a separate stack-video workflow, a validated per-project JSON configuration helper, and a collision-safe pack installer. HyperFrames owns animation and rendering; no brag invocation or modification.

**Tech Stack:** Python 3.9+ standard-library helpers, unittest, Playwright/Chromium for diagram PNGs, HyperFrames with Node.js 22+ and FFmpeg for video.

**Spec:** `docs/superpowers/specs/2026-11-07-stack-story-design.md`

## Global Constraints
- Leave the installed brag skill and its behavior unchanged.
- Install both skills into the active Hermes profile without replacing existing skills silently.
- No automatic gallery submission or publication of future project diagrams.
- Preserve upstream MIT attribution, font OFL notices, and pinned source provenance.
- Configure format, duration, theme, tone, music, and opt-in narration per run.
- Explicit invocation overrides take precedence over project configuration, which takes precedence over documented defaults.
- Report unavailable audio assets/providers rather than substituting silently.
- Final preview approval precedes user-facing video rendering.

## Review Focus
- Invalid JSON, unknown keys, wrong types, and non-finite duration fail with actionable errors.
- Existing destinations, symlinks, and interrupted installs preserve installed skills.
- Paths with spaces work; helper paths do not depend on the current working directory.
- A dependency listed in a manifest is not evidence of a deployed service or data-flow edge.
- Audio disabled means no audio; voice enabled without a working provider is an explicit blocker.

## Task 1: Reproducible stack-diagram adaptation
**Files:** `skills/stack-diagram/**`, `UPSTREAM.md`, `LICENSE`, `tests/test_diagram.py`, `docs/evaluation/diagram.md`.
**Interfaces:** Consume upstream commit `1ed53e3e9525364ae5d82e0430f2bb3f7ef4c838`; produce the existing `build.py DRAFT ICONDIR OUT --fonts FONTSDIR` and `render_png.py IN.html OUT.png` interfaces with bundled resources intact.
- [ ] Run a baseline reference/application scenario with a fresh agent and record actual gaps before adding adaptation guidance.
- [ ] Write regression tests for unresolved icon/font tokens and self-contained build output; run and record the expected missing-resource or missing-adaptation failure.
- [ ] Fetch the pinned skill subtree and licenses only; record source SHA and any intentional adaptations. Preserve gallery consent requirements; do not invoke share.py.
- [ ] Adapt frontmatter/discovery and Hermes delivery instructions, addressing observed gaps rather than rewriting upstream design rules.
- [ ] Run build tests and the same post-skill application scenario; validate every linked resource.
- [ ] Commit with `feat(diagram): adapt pinned stack diagram skill` after reviewing the staged tree.

## Task 2: Independent stack-video workflow and configuration
**Files:** `skills/stack-video/SKILL.md`, `skills/stack-video/references/workflow.md`, `skills/stack-video/scripts/config.py`, `examples/stack-video.json`, `tests/test_config.py`, `docs/evaluation/video.md`.
**Interfaces:** `resolve_config(project: dict, overrides: dict) -> dict`; CLI `python config.py --config FILE [--format landscape|vertical|square] [--duration SECONDS] [--theme light|dark] [--tone TEXT] [--music FILE|off] [--voice|--no-voice]`. Returns normalized JSON; validation errors exit nonzero.
- [ ] Run a baseline architecture-video task without the new skill; record output-contract gaps.
- [ ] Write failing unittest cases for defaults, override precedence, all advertised fields, unknown keys, invalid types, non-finite/out-of-range duration, and missing config files.
- [ ] Implement defaults: landscape, 30 seconds, dark, explanatory tone, music off, voice false. Permit duration 10–120 seconds and require music to be off or an existing file. Resolve config-relative music paths against the config file's directory.
- [ ] Write the skill recipe: source evidence inventory → normalized config → architecture/edge manifest → storyboard → diagram reuse/generation → HyperFrames composition → check → preview approval → render → ffprobe and frame inspection. Reject unverified architecture claims and retain source citations in the plan.
- [ ] Document voice as opt-in; load the relevant media/TTS skill for actual narration. Never change brag or silently disable requested narration.
- [ ] Run the complete test suite and post-skill behavioral scenario, including audio-disabled and requested-but-unavailable narration cases.
- [ ] Commit with `feat(video): add independent stack walkthrough skill`.

## Task 3: Installation and real example acceptance
**Files:** `scripts/install.py`, `tests/test_install.py`, `examples/demo/**`, `docs/verification.md`, `README.md`, `.gitignore`.
**Interfaces:** `python scripts/install.py --skills-dir DIR [--skill stack-diagram|stack-video]`; default destination resolves the active HERMES_HOME skills directory. Refuse collisions and symlink destinations. Allow individual or both-skill installation.
- [ ] Write and run failing tests for install contents, individual installation, spaces in paths, collision refusal, symlinks, and rollback on an interrupted copy.
- [ ] Implement staging/validation before promotion and rollback on failure; never overwrite existing destinations.
- [ ] Run tests and exercise installation in a disposable directory before touching the active profile.
- [ ] Hash the brag tree, resolve active profile and inspect name collisions; install authorized skills and compare installed bytes with source. Verify exact-name loading in a fresh process if the current-session catalog is cached.
- [ ] Create a synthetic, explicitly illustrative architecture; render HTML and both PNG themes, inspect with vision tools, and fix layout defects.
- [ ] Build a short HyperFrames stack walkthrough; run check and open final preview. Obtain final preview approval before rendering the video. Probe the final file and inspect representative frames, recording exact commands and results.
- [ ] Verify brag tree hash unchanged. Write README installation, configuration, usage, dependencies, licensing, verified results and limitations; exclude runtime caches and fetched icon packages.
- [ ] Commit with `feat(pack): add installer and verified examples`.

## Task 4: Independent review and public publication
**Files:** `docs/review.md`, `docs/verification.md`, complete tracked tree.
**Interfaces:** Publish `hersaintel/stack-story-skills`, public, main default branch; remote SHA and tracked blob set must match the local source revision.
- [ ] Obtain fresh independent review; fix findings with failing regression tests and rerun the full suite.
- [ ] Scan all tracked text and staged content for secrets, personal paths, unintended dependencies and generated artifacts; verify notices and README claims.
- [ ] Commit final changes and rerun the suite against the committed tree; require a clean working tree.
- [ ] Create the public repository only after the publication gate passes; push main.
- [ ] Read remote visibility/default branch, resolve main SHA, compare complete tree/blob identities and README with local source.
- [ ] Journal completion only in the user's authorized Hermes Journal folder. Deliver repository link, installed names, verified evidence and any remaining blockers.

## Self-review
All approved features map to tasks above. Review-focus cases are assigned to configuration, installer, or behavioral tests. Pure tests do not substitute for the actual diagram/video render, independent review, active-profile installation, or remote verification. The final-preview approval is an explicit remaining human gate rather than implied by design approval.
