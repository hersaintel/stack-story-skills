import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/install.py'

class InstallTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.is_file(), 'missing installer')
        spec = importlib.util.spec_from_file_location('pack_installer', SCRIPT)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod

    def test_install_both_and_individual_with_spaces(self):
        mod = self.load()
        with tempfile.TemporaryDirectory(prefix='stack skills ') as tmp:
            target = pathlib.Path(tmp) / 'skills'
            mod.install(ROOT / 'skills', target, ['stack-diagram', 'stack-video'])
            for name in ['stack-diagram', 'stack-video']:
                self.assertEqual((target / name / 'SKILL.md').read_bytes(), (ROOT / 'skills' / name / 'SKILL.md').read_bytes())
            other = pathlib.Path(tmp) / 'other'
            mod.install(ROOT / 'skills', other, ['stack-video'])
            self.assertFalse((other / 'stack-diagram').exists())
            self.assertTrue((other / 'stack-video/scripts/config.py').exists())

    def test_collision_keeps_everything_unchanged(self):
        mod = self.load()
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            existing = target / 'stack-video'; existing.mkdir(); (existing / 'keep').write_text('user work')
            with self.assertRaises(FileExistsError):
                mod.install(ROOT / 'skills', target, ['stack-diagram', 'stack-video'])
            self.assertFalse((target / 'stack-diagram').exists())
            self.assertEqual((existing / 'keep').read_text(), 'user work')

    def test_symlink_refusal(self):
        mod = self.load()
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp); actual = root / 'actual'; actual.mkdir()
            target = root / 'link'; target.symlink_to(actual, target_is_directory=True)
            with self.assertRaises(ValueError):
                mod.install(ROOT / 'skills', target, ['stack-video'])
            self.assertEqual(list(actual.iterdir()), [])

    def test_copy_failure_rolls_back(self):
        mod = self.load()
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / 'skills'
            original = mod.shutil.copytree
            def failing(src, dst, *args, **kwargs):
                if pathlib.Path(src).name == 'stack-video':
                    raise OSError('synthetic interrupted copy')
                return original(src, dst, *args, **kwargs)
            with patch.object(mod.shutil, 'copytree', side_effect=failing):
                with self.assertRaises(OSError):
                    mod.install(ROOT / 'skills', target, ['stack-diagram', 'stack-video'])
            self.assertFalse((target / 'stack-diagram').exists())
            self.assertFalse((target / 'stack-video').exists())
            self.assertEqual(list(target.glob('.stack-story-*')), [])

    def test_cli_error_without_traceback(self):
        self.load()
        result = subprocess.run([sys.executable, str(SCRIPT), '--skill', 'nonexistent'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)

if __name__ == '__main__': unittest.main()
