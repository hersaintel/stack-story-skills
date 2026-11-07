# Technique evaluation: stack-diagram

## No-guidance control
A fresh agent was given only: Browser sends HTTPS to Python API; API reads/writes local SQLite. It was asked for an artifact/source-of-truth and validation/delivery contract without reading the new pack.

Its exact key choice: “I would deliver `architecture.svg` as the standalone, editable diagram and `architecture.png` as a convenient preview. The SVG would be the visual source of truth; any Python generator would also be delivered so the diagram can be regenerated.”

It correctly kept the topology narrow, did not invent services and proposed browser inspection. However, it selected SVG as the source of truth rather than the upstream HTML contract, and did not specify Hermes MEDIA delivery or both themes. These are reference-contract gaps, not evidence of unsafe behavior. No artifacts were generated in the control.

## Adaptation
The Hermes integration section establishes HTML as the single visual source, both-theme Chromium PNG export, tool-based inspection and native MEDIA delivery. Upstream code and geometry rules are retained. Programmatic build tests separately exercise embedding and unresolved-token failures.

## Post-skill evaluation
A fresh post-skill reader evaluated the same scenario after reading the source instructions. All five contract elements passed: HTML as sole visual source; both-theme Chromium PNGs; explicit vision inspection of both; actual-file MEDIA delivery; no invented topology. Exact key choice: “Build self-contained `out.html` as the sole visual source.” This was a read-only application-contract evaluation, not an executed render. Live render acceptance is recorded separately in docs/verification.md.
