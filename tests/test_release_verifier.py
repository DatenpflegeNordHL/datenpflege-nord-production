from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_public_release.py"
VERIFIER = ROOT / "scripts" / "verify_release_manifest.py"


class ReleaseVerifierTest(unittest.TestCase):
    def build_package(self, root: Path) -> Path:
        package = root / "release-package"
        subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(package)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return package

    def verify(self, package: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(VERIFIER),
                "--webroot",
                str(package / "webroot"),
                "--manifest",
                str(package / "RELEASE-MANIFEST.sha256"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_exact_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = self.build_package(Path(tmp))
            result = self.verify(package)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("files match exactly", result.stdout)

    def test_modified_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = self.build_package(Path(tmp))
            target = package / "webroot" / "robots.txt"
            target.write_text(target.read_text(encoding="utf-8") + "# tampered\n", encoding="utf-8")
            result = self.verify(package)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Hash mismatch", result.stderr)

    def test_missing_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = self.build_package(Path(tmp))
            (package / "webroot" / "favicon.svg").unlink()
            result = self.verify(package)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Missing deployed files", result.stderr)

    def test_extra_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = self.build_package(Path(tmp))
            extra = package / "webroot" / "unexpected.txt"
            extra.write_text("not part of the release\n", encoding="utf-8")
            result = self.verify(package)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Unexpected deployed files", result.stderr)

    def test_symlink_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = self.build_package(Path(tmp))
            source = package / "webroot" / "robots.txt"
            link = package / "webroot" / "robots-link.txt"
            link.symlink_to(source)
            result = self.verify(package)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Symlink present", result.stderr)


if __name__ == "__main__":
    unittest.main()
