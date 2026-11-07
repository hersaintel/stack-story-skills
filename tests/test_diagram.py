import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'stack-diagram'

class DiagramTests(unittest.TestCase):
    def test_bundled_resources_and_hermes_delivery(self):
        self.assertTrue((SKILL / 'scripts/build.py').is_file(), 'missing vendored build script')
        text = (SKILL / 'SKILL.md').read_text()
        self.assertIn('MEDIA:', text)
        for name in ['Geist.woff2', 'JetBrainsMono.woff2', 'OFL-Geist.txt', 'OFL-JetBrainsMono.txt']:
            self.assertTrue((SKILL / 'assets/fonts' / name).is_file())

    def test_self_contained_build_and_unresolved_tokens(self):
        self.assertTrue((SKILL / 'scripts/build.py').is_file(), 'missing build implementation')
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            icons = base / 'icons'; icons.mkdir()
            (icons / 'server.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            draft = base / 'draft.html'; out = base / 'out.html'
            draft.write_text('<img src="%%ICON_server%%">%%FONT_DISPLAY%%')
            cmd = [sys.executable, str(SKILL / 'scripts/build.py'), str(draft), str(icons), str(out), '--fonts', str(SKILL / 'assets/fonts')]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('data:image/svg+xml;base64,', out.read_text())
            self.assertNotIn('%%', out.read_text())
            draft.write_text('%%ICON_missing%%')
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unresolved tokens', result.stderr)

if __name__ == '__main__':
    unittest.main()
