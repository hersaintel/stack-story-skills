"""Generate the original, deterministic ambient score for the stack demo.

No external songs, samples, dependencies, random numbers or network calls.
The source and generated score are distributed under LICENSE-PACK (MIT).
"""
import argparse
import array
import math
import pathlib
import sys
import wave

CHORDS = ((50, 57, 61, 66), (47, 54, 57, 62), (43, 50, 54, 59),
          (45, 52, 59, 61), (50, 57, 62, 64), (50, 57, 61, 66))


def generate(output: pathlib.Path, duration=30, sample_rate=24000):
    """Write stereo 16-bit PCM: soft pads, gentle plucks and a low pulse."""
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not 0 < duration <= 120:
        raise ValueError('duration must be finite, positive and at most 120 seconds')
    if type(sample_rate) is not int or not 8000 <= sample_rate <= 48000:
        raise ValueError('sample_rate must be an integer from 8000 to 48000')
    samples = array.array('h')
    tau = math.tau
    hz = lambda midi: 440 * 2 ** ((midi - 69) / 12)
    frequencies = [tuple(hz(note) for note in chord) for chord in CHORDS]
    for index in range(round(duration * sample_rate)):
        t = index / sample_rate
        slot = int(t // 5) % len(CHORDS)
        local = t % 5
        crossfade = min(local / .55, 1)
        crossfade = crossfade * crossfade * (3 - 2 * crossfade)
        current, previous = frequencies[slot], frequencies[(slot - 1) % len(CHORDS)]
        fade = min(t / .8, 1) * min(max((duration - t) / 2, 0), 1)
        beat = t % .625  # 96 BPM; a pluck per beat, no sampled percussion
        note = current[int(t / .625) % 4] * 2
        bell = .045 * (1 - math.exp(-beat / .012)) * math.exp(-beat / .24) * math.sin(tau * note * beat)
        bass = .035 * (crossfade * math.sin(tau * current[0] * .5 * t)
                       + (1 - crossfade) * math.sin(tau * previous[0] * .5 * t))
        pulse = .012 * math.exp(-beat / .09) * math.sin(tau * 55 * beat)
        for channel in range(2):
            phase = .08 * channel
            new = sum(math.sin(tau * freq * t + phase * (j + 1)) for j, freq in enumerate(current)) / 4
            old = sum(math.sin(tau * freq * t + phase * (j + 1)) for j, freq in enumerate(previous)) / 4
            pad = .14 * (crossfade * new + (1 - crossfade) * old)
            value = fade * (pad + bell + bass + pulse)
            samples.append(round(max(-1, min(1, value)) * 32767))
    if sys.byteorder != 'little':
        samples.byteswap()
    output = pathlib.Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), 'wb') as audio:
        audio.setnchannels(2); audio.setsampwidth(2); audio.setframerate(sample_rate)
        audio.writeframes(samples.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=pathlib.Path)
    parser.add_argument('--duration', type=float, default=30)
    args = parser.parse_args()
    try:
        generate(args.output, duration=args.duration)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
