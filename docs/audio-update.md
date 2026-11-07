# Audio update — narration and original music

## Scope and approval

The user requested both narration and background music for the existing sample, and an update to the public GitHub repository. The user explicitly chose **free local Kokoro narration** after being offered local or cloud TTS. No HeyGen account, paid API call, cloned user voice or third-party song was used. Skill defaults remain opt-in; brag is not modified.

## Current status

- Source implementation and stems: complete.
- Offline suite: **17 tests pass**.
- HyperFrames 0.9.19 browser check: **ok true**, zero errors across lint/runtime/layout/motion/contrast/audio; six pre-existing maintainability lint warnings remain. The silent-film warning is gone.
- Final audio-preview approval: received; the user described the preview as perfect before rendering.
- Encoded MP4/audio acceptance: **passed**. The sample now contains narration and music in a stereo AAC track; exact results are below. Public push verification is performed at handoff.

## Narration

`examples/demo/narration.json` records the five exact lines and start times. Local Kokoro-82M, `af_heart`, English, speed 1.0; executed through HyperFrames 0.9.19 TTS with `kokoro-onnx` 0.6.1 in an isolated Python 3.12 environment. Model weights and dependencies are not committed.

| Line | Start | Measured speech duration | End |
|---|---:|---:|---:|
| browser | 0.6 | 3.498667 | 4.098667 |
| api | 6.5 | 4.693333 | 11.193333 |
| sqlite | 12.5 | 4.266667 | 16.766667 |
| flow | 18.5 | 3.818667 | 22.318667 |
| overview | 24.5 | 4.672000 | 29.172000 |

The utterances are placed at their specified times, padded to 30 seconds and loudness-normalized to a target -18 LUFS/-2 dBTP. The committed `composition/assets/narration.wav` is 24 kHz mono PCM, exactly 30 seconds; measured mean -19.8 dBFS and maximum -2.0 dBFS. Loudness targets and measured dBFS statistics are different units and are not conflated.

## Original music and mix

`scripts/generate_demo_music.py` synthesizes a deterministic 96-BPM ambient score from oscillators: soft chord pads, a restrained pluck and low pulse. No downloaded song, recording, loop or brag asset is used. Source and the original score are distributed under `LICENSE-PACK`; model weights are not redistributed. The generated narration is synthetic, not a recording of Cory.

```text
python3 scripts/generate_demo_music.py .runtime/original-score.wav
ffmpeg -i .runtime/original-score.wav -af loudnorm=I=-24:TP=-3:LRA=7,aresample=24000 -c:a pcm_s16le examples/demo/composition/assets/music.wav
```

The committed music stem is 24 kHz stereo PCM, exactly 30 seconds; measured mean -25.8 dBFS and maximum -14.7 dBFS. HyperFrames owns preview/render timing and mixing through two named audio elements, `narration` and `music-bed`. Music fades in/out through a volume automation lane.

The canonical HyperFrames audio carve was applied to the **music bed**, against `narration`, strength 0.8. Actual analysis: six speech-band dips, seven dynamic carve lanes with a 325-point level envelope, and one retained authored volume lane. This makes spectral and level room for narration rather than simply adding two full-volume sources. The written `data-fx-carve`, `data-fx-chain` and `data-automation` attributes are retained in the editable composition.

```text
npm install --prefix .runtime/audio-tools --no-save @hyperframes/core@0.9.19
node <hyperframes-audio-skill>/scripts/carve.mjs --comp examples/demo/composition/index.html --core .runtime/audio-tools --bed music-bed --voice narration --strength 0.8
npx --yes hyperframes@0.9.19 check examples/demo/composition --snapshots --json
```

No dependency install scripts were approved or bypassed. The core analysis worked with the package manager's esbuild install-script block retained.

## Configuration and reproduction

The demo opts into both through `examples/demo/stack-video.json`. The public `resolved-config.json` is a portable export: all resolved settings are retained, while the music path is relative to the demo directory rather than leaking a machine-local absolute path. Local exact resolver stdout stays in ignored runtime evidence. `examples/stack-video.json` and the skill's defaults remain unchanged (voice false/music off).

```text
python3 skills/stack-video/scripts/config.py --config examples/demo/stack-video.json
HYPERFRAMES_PYTHON="<audio-venv>/bin/python" npx --yes hyperframes@0.9.19 tts "<line from narration.json>" --voice af_heart --speed 1.0 --output <line.wav> --json
```

Keep the virtual-environment interpreter path intact: resolving its symlink to the base Python loses the venv's packages. A failed package lookup was traced to precisely that and corrected by preserving the venv path; no system Python packages were changed.

## Tests and acceptance limits

Three new regressions first failed on the missing generator/audio tracks. The suite now verifies deterministic stereo PCM, rejected invalid generation settings, real stem resources, correct named tracks, and a carve on the bed rather than the voice; existing sample tests now expect requested audio instead of enforcing silence. Browser checks reported 300 motion samples and 69/69 contrast passes, with zero audio findings.

The assistant can measure clipping, levels, durations and source wiring but does not claim to have listened. The user listened to and approved the final Studio preview before rendering. The actual output at `examples/demo/stack.mp4` was then probed and inspected:

- H.264 video, 1920×1080, 30/1 fps, 900 frames, **30.000000 seconds**.
- **One stereo AAC audio stream**, 48 kHz, **30.000000 seconds**; audio is decoded, non-silent and present through the five narration scenes and music-only gaps.
- Encoded mix measurement: **-15.43 LUFS integrated**, **-1.90 dBTP true peak**, **4.50 LU loudness range**. The loudnorm analysis's hypothetical output values were not mistaken for measurements of the actual file.
- File size **2,113,940 bytes**; SHA-256 `9646f53527fd1e5bf56953151a00e66de2862ff5c2d5ec422b7355b4ccaddd17`.
- Actual engine summary: **beginframe capture, hardware GPU**, one worker, about 112.7 seconds. No effect-chain parsing failure or dry fallback was reported.
- Encoded frames independently sought at 2/8/14/20/26 seconds were visually inspected. The five phases and architecture remain readable and unclipped. The representative 28.3-second poster was regenerated and is byte-identical to the initial visual poster.

The silent release remains available in Git history at `6d56b8b`; an ignored local backup was also retained before replacing the sample. The original silent release and its independent-review evidence remain historical in `docs/verification.md` and `docs/review.md`. Remote branch/commit/tree/media verification is performed separately at handoff.

## Independent audio-source review

A fresh read-only reviewer examined `6d56b8b..56a53f4`, ran the full suite (**17/17 passed**), independently reproduced the committed music PCM from the generator plus documented normalization, checked both stems, all five narration intervals, the carve targets and every automation lane, and screened the committed tree for private paths/model weights/credentials. **No Critical or Important findings.** The helper, audio assets and composition were not changed after that reviewed source snapshot; subsequent changes add the approved encode and its documentation.

One **deferred Minor** remains in `scripts/generate_demo_music.py`: a positive sub-sample duration such as `1e-9` rounds to zero frames and writes an empty WAV. The parent reproduced it. This does not affect the tested 30-second demo or its committed assets; a future helper fix should reject frame counts below one with a regression test. The older extreme-integer configuration error from the original review is also unchanged and remains disclosed in `docs/review.md`.

The reviewer did not claim to hear the narration/music or certify a new render. Listening approval belongs to the user, and encoded-output validation belongs to the measured parent checks above. The review's initial pending-approval/encoding status was accurate for its pinned snapshot; both gates have since passed.
