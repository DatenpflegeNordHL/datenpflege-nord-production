import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PreviewArtifactTests(unittest.TestCase):
    def test_pages_artifact_is_allowlisted_nonindexable_and_path_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "artifact"
            subprocess.run(
                ["python3", "scripts/build_preview_artifact.py", "--root", ".", "--output", str(output), "--base-path", "/datenpflege-nord-production"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            showcase = (output / "website-showcase" / "index.html").read_text(encoding="utf-8")
            script = (output / "assets" / "showcase.js").read_text(encoding="utf-8")
            self.assertEqual(showcase.count('name="robots"'), 1)
            self.assertIn('content="noindex, nofollow, noarchive"', showcase)
            self.assertIn('href="/datenpflege-nord-production/assets/showcase.css', showcase)
            self.assertIn('"/datenpflege-nord-production/website-showcase/showcase-projects.json', script)
            self.assertEqual((output / "robots.txt").read_text(encoding="utf-8"), "User-agent: *\nDisallow: /\n")
            self.assertFalse((output / "docs").exists())
            self.assertFalse((output / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
