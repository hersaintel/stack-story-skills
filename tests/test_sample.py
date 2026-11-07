import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SampleTests(unittest.TestCase):
    def test_video_uses_embedded_fonts_and_seekable_motion(self):
        text = (ROOT / 'examples/demo/composition/index.html').read_text()
        for unavailable in ['Hiragino Sans', 'Yu Gothic UI', 'Noto Sans CJK JP']:
            self.assertNotIn(unavailable, text, 'sample must not depend on host-only fallback fonts')
        self.assertFalse(re.search(r'\btransition\s*:', text), 'CSS transitions run outside the seekable timeline')
        for family in ['Geist', 'JetBrains Mono']:
            self.assertRegex(text, r'@font-face\s*\{\s*font-family:\s*"' + family + '"')

    def test_sample_matches_config_and_no_audio(self):
        text = (ROOT / 'examples/demo/composition/index.html').read_text()
        for value in ['data-width="1920"', 'data-height="1080"', 'data-duration="30"']:
            self.assertIn(value, text)
        self.assertNotRegex(text, r'<(?:audio|video)\b')
        self.assertIn('window.__timelines["stack-walkthrough"]', text)
        self.assertIn('id="request-edge"', text)
        self.assertIn('id="storage-edge"', text)

if __name__ == '__main__': unittest.main()
