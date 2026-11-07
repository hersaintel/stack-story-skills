import importlib.util
import pathlib
import tempfile
import unittest
import wave
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/generate_demo_music.py'

class AudioTags(HTMLParser):
    def __init__(self):
        super().__init__(); self.tracks = {}
    def handle_starttag(self, tag, attrs):
        if tag == 'audio':
            values = dict(attrs); self.tracks[values.get('id')] = values

class AudioTests(unittest.TestCase):
    def test_original_music_is_reproducible_stereo_pcm(self):
        self.assertTrue(SCRIPT.is_file(), 'missing original music generator')
        spec = importlib.util.spec_from_file_location('demo_music', SCRIPT)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            a, b = pathlib.Path(tmp)/'a.wav', pathlib.Path(tmp)/'b.wav'
            mod.generate(a, duration=1, sample_rate=8000)
            mod.generate(b, duration=1, sample_rate=8000)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with wave.open(str(a)) as audio:
                self.assertEqual((audio.getnchannels(), audio.getsampwidth(), audio.getframerate(), audio.getnframes()), (2, 2, 8000, 8000))
                self.assertNotEqual(set(audio.readframes(8000)), {0})

    def test_music_rejects_invalid_configuration(self):
        self.assertTrue(SCRIPT.is_file(), 'missing original music generator')
        spec = importlib.util.spec_from_file_location('demo_music_invalid', SCRIPT)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp)/'bad.wav'
            for duration in [0, -1, float('nan'), float('inf'), 1000, True]:
                with self.subTest(duration=duration), self.assertRaises(ValueError):
                    mod.generate(output, duration=duration)
            for rate in [0, 7999, 48001, 24000.5, True]:
                with self.subTest(rate=rate), self.assertRaises(ValueError):
                    mod.generate(output, sample_rate=rate)
            self.assertFalse(output.exists())

    def test_demo_has_voice_and_carved_music(self):
        directory = ROOT / 'examples/demo/composition'
        tags = AudioTags(); tags.feed((directory/'index.html').read_text())
        self.assertEqual(set(tags.tracks), {'narration', 'music-bed'})
        for name, attrs in tags.tracks.items():
            self.assertEqual(float(attrs['data-duration']), 30)
            self.assertTrue((directory/attrs['src']).is_file(), name+' asset missing')
        self.assertIn('data-fx-carve', tags.tracks['music-bed'])
        self.assertIn('data-fx-chain', tags.tracks['music-bed'])
        self.assertIn('data-automation', tags.tracks['music-bed'])
        self.assertNotIn('data-fx-carve', tags.tracks['narration'])

if __name__ == '__main__': unittest.main()
