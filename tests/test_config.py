import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/stack-video/scripts/config.py'

class ConfigTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.exists(), 'missing configuration implementation')
        spec = importlib.util.spec_from_file_location('stack_video_config', SCRIPT)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod

    def test_defaults(self):
        self.assertEqual(self.load().resolve_config({}, {}), dict(format='landscape', duration=30, theme='dark', tone='explanatory', music='off', voice=False))

    def test_precedence_all_fields_and_no_mutation(self):
        mod = self.load()
        project = dict(format='vertical', duration=40, theme='light', tone='calm', music='off', voice=True)
        before = project.copy()
        result = mod.resolve_config(project, dict(format='square', duration=20, theme='dark', tone='technical', music='off', voice=False))
        self.assertEqual(result, dict(format='square', duration=20, theme='dark', tone='technical', music='off', voice=False))
        self.assertEqual(project, before)

    def test_invalid_values(self):
        mod = self.load()
        for data in [[], {'unknown': 1}, {'format': 'portrait'}, {'theme': 'blue'}, {'voice': 'yes'}, {'duration': True}, {'duration': 0}, {'duration': 121}, {'duration': float('nan')}, {'duration': float('inf')}, {'duration': '30'}, {'tone': ''}, {'music': True}, {'music': 'no-such-track.wav'}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                mod.resolve_config(data, {})
        with self.assertRaises(ValueError):
            mod.resolve_config({}, {'unknown': 1})

    def test_config_relative_music_and_spaces(self):
        self.load()
        with tempfile.TemporaryDirectory(prefix='stack config ') as tmp:
            base = pathlib.Path(tmp)
            track = base / 'my track.wav'; track.write_bytes(b'test-only-path-validation')
            config = base / 'config.json'; config.write_text(json.dumps({'music': track.name, 'voice': True}))
            result = subprocess.run([sys.executable, str(SCRIPT), '--config', str(config), '--no-voice', '--duration', '15'], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data['music'], str(track))
            self.assertEqual(data['duration'], 15)
            self.assertFalse(data['voice'])

    def test_cli_errors(self):
        self.load()
        with tempfile.TemporaryDirectory() as tmp:
            bad = pathlib.Path(tmp) / 'bad.json'; bad.write_text('{oops')
            for args in [['--config', str(bad)], ['--config', str(bad.parent / 'missing.json')], ['--duration', 'nan']]:
                result = subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('error:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

if __name__ == '__main__': unittest.main()
