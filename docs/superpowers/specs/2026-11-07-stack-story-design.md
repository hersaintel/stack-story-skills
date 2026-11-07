# Stack Story Skills — approved design

## Intent
Provide independently invokable static architecture diagrams and stack walkthrough videos. Leave the installed brag skill and its behavior unchanged.

## Goals
- Adapt caru-ini/stack-diagram with upstream MIT attribution, font OFL notices, and pinned source provenance.
- Add a separate stack-video skill using HyperFrames directly, not brag.
- Explain evidenced components and request/data flow, ending on the full architecture. Accept an existing diagram or generate one as needed.
- Configure format, duration, theme, tone, music, and opt-in narration per run; document precedence and reject invalid configuration.
- Install both skills into the active Hermes profile without replacing existing skills silently.
- Publish a public hersaintel/stack-story-skills repository with accurate instructions and verified examples.

## Non-goals and anti-goals
Do not modify brag, publish user project diagrams automatically, submit to the upstream gallery, bundle fetched vendor icon archives, or invent architecture from dependency lists. Public repository approval does not authorize public uploads of future project data.

## Approach
Chosen: two skills in one pack, sharing diagram artifacts when useful. stack-diagram remains usable without stack-video; stack-video does not require brag. Alternatives: extend brag (rejected because it must remain independent), or duplicate the diagram engine inside stack-video (rejected because it creates divergent sources of truth).

## Builder decisions
Use JSON project configuration plus explicit invocation overrides, with documented defaults. Preserve the upstream diagram implementation and supporting resources. Keep new helper scripts small, portable Python where practical. Use HyperFrames domain skills for deterministic animation, checking, preview, rendering, and media verification. Music and narration configuration describe intent; unavailable assets/providers must be reported, never silently substituted. Require final preview approval for user-facing renders.

## Verification
Test configuration defaults, precedence, invalid values, and collision-safe installation. Evaluate each skill with baseline/post-skill scenarios. Render and visually inspect a public synthetic example diagram and video, and probe the encoded media. Compare brag contents before/after. Independently review final source. Scan the complete public tree for secrets and local paths. Verify remote visibility, branch, exact commit, tree, and README.

## Constraints
All working files belong in the user's designated Hermes project area. No sensitive vault reads. Journal only in the allowed Hermes Journal folder after completion. Tests and documentation must distinguish source validation, behavioral evaluation, installation, and runtime results.

## Approval
The human approved this design in the conversation before implementation planning.
