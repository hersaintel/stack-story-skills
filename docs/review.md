# Independent source review

## Snapshot and scope

Fresh reviewer: base `ab85f78` through `0e91d4042c7a1a45ab29788226744358a3bb7dce`. Read-only review of the approved design/plan, both skills, helper scripts, tests, examples, README and notices. The reviewer ran the full unittest suite: **14 passed**. Later evaluation-document updates were outside that pinned snapshot; the parent owns those documentation claims.

## Verdict

No Critical or Important findings; source publication has no blocking issue from this review. One Minor finding remains deferred rather than silently waived.

### Deferred minor: oversized integer duration error

`skills/stack-video/scripts/config.py`, duration validation: `math.isfinite` precedes the range check. A valid JSON duration integer such as `10**309` raises `OverflowError: int too large to convert to float`. The CLI therefore fails closed but prints a traceback rather than the documented actionable duration error. Ordinary valid durations and common invalid types/non-finite/out-of-range values are covered and pass.

The parent reproduced this with the current helper. Recommended future fix: check the numeric range before float conversion and pin it with a failing regression. No skill/helper code was changed after the review. Do not claim the validator handles every possible invalid JSON numeric value without a traceback.

## Verified by the reviewer

- Installer collision preservation, symlink refusal, individual/both selection, paths with spaces and interrupted-copy cleanup are supported by source/tests. Crash atomicity and concurrent-writer protection are explicitly disclaimed.
- Workflows do not invoke or modify brag. Dependency-only findings are separated from evidence of runtime topology. Music-off and unavailable narration instructions are explicit.
- MIT/OFL notices are present. Embedded example font bytes match bundled WOFF2 files, and embedded SVG instances match bundled generic pictograms. Both PNGs are 2000×720 without text/EXIF metadata chunks.
- Complete tracked text screening found no apparent credentials or personal home paths; no tracked symlinks or brag subtree.

## Limits and parent dispositions

The reviewer did not independently certify remote upstream byte parity, prior installed-profile/brag hashes, browser/visual history, unexercised audio/aspect-ratio workflows or GitHub state. Parent evidence is kept separate: a direct comparison with the downloaded pinned upstream archive verified **19 unchanged files** (all vendored resources/scripts/notices plus root LICENSE, excluding intentionally adapted SKILL.md). Native skill loads, source/installed hash parity, all 288 brag files unchanged, and browser checks are recorded in `verification.md`. Unexercised audio/aspect-ratio workflows remain explicitly unverified; remote publication and final MP4 acceptance are still pending.
