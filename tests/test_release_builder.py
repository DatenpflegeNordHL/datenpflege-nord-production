from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_public_release.py"

EXPECTED_TOP_LEVEL = {
    "index.html",
    "en",
    "softwareentwicklung-luebeck",
    "webentwicklung-luebeck",
    "ki-automatisierung-luebeck",
    "impressum",
    "datenschutz",
    "assets",
    "images",
    "apple-touch-icon.png",
    "favicon.svg",
    "og-datenpflege-nord.png",
    "robots.txt",
    "sitemap.xml",
    "RELEASE-MANIFEST.sha256",
}

FORBIDDEN_TOP_LEVEL = {
    ".git",
    ".github",
    "backend",
    "docs",
    "tests",
    "scripts",
    "MASTER-SITE-EVIDENCE.md",
    "KEYWORD-INTENT-MAP.md",
    "AUTHORITY-ENTITY-MAP.md",
    "AUTHORITY-OPPORTUNITY-QUEUE.md",
    "RELEASE-VERIFICATION.md",
    "THIRD_PARTY_NOTICES.md",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class ReleaseBuilderTest(unittest.TestCase):
    def test_release_is_allowlisted_and_manifest_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "webroot"
            subprocess.run(
                [sys.executable, str(BUILDER), "--output", str(output)],
                cwd=ROOT,
                check=True,
            )

            top_level = {p.name for p in output.iterdir()}
            self.assertEqual(EXPECTED_TOP_LEVEL, top_level)
            self.assertFalse(top_level & FORBIDDEN_TOP_LEVEL)

            manifest_path = output / "RELEASE-MANIFEST.sha256"
            manifest_rows = {}
            for line in manifest_path.read_text(encoding="utf-8").splitlines():
                hash_value, relative = line.split("  ", 1)
                self.assertNotIn(relative, manifest_rows)
                manifest_rows[relative] = hash_value

            release_files = {
                p.relative_to(output).as_posix(): p
                for p in output.rglob("*")
                if p.is_file() and p.name != "RELEASE-MANIFEST.sha256"
            }
            self.assertEqual(set(release_files), set(manifest_rows))

            for relative, path in release_files.items():
                self.assertEqual(digest(path), manifest_rows[relative], relative)

            for path in output.rglob("*"):
                self.assertFalse(path.is_symlink(), path)
                if path.is_file():
                    self.assertFalse(path.name.startswith(".env"), path)
                    self.assertNotIn(path.suffix.lower(), {".pem", ".key", ".p12", ".pfx"})


if __name__ == "__main__":
    unittest.main()
