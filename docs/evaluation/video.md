# Technique evaluation: stack-video

## No-guidance control
A fresh agent was asked to specify a 30-second vertical dark stack walkthrough, music off, narration requested with no TTS installed. Runtime evidence confirms Browser → API → SQLite; Redis appears only as a dependency. No proposed skill was provided.

The control correctly separated Redis from runtime evidence, kept brag independent, respected music-off and marked narration unavailable. Exact key statement: “Because no TTS provider is installed, I would stop before producing a purportedly complete voiced video.” This baseline already passed those safety requirements; the new skill is not credited with improving them.

Reference gaps: no rendering engine, config schema/precedence, exact required artifact names, one-frame media tolerance, or final Studio-preview approval contract. It described generic evidence/storyboard/source artifacts but not executable helper behavior. No render was performed.

## Implementation
A concrete HyperFrames workflow, JSON helper and artifact table address the reference gaps. The configuration helper is exercised independently by unittest; it does not generate audio or render a video. This is reference/technique guidance, not a general discipline policy, so the evaluation uses an application scenario rather than claiming repeated pressure-test safety evidence.

## Post-skill evaluation
A fresh post-skill reader evaluated the same task after reading the skill and workflow reference. All seven contract elements passed: named artifacts, configuration precedence/schema, direct HyperFrames engine, Redis evidence separation, unavailable-narration blocker, final-preview approval gate, and one-frame duration tolerance. Exact key choice: “Record blocked: narration unavailable because no TTS/recording exists.” The reader made no edits, ran no helper and performed no rendering; this proves sampled reference/application behavior only. Evidence/no-TTS handling already passed in the control, so no safety improvement is claimed. Actual helper execution and sample runtime acceptance are recorded separately in docs/verification.md.
