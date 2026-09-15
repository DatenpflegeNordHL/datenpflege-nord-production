from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_public_release.py"

EXPECTED_PACKAGE_TOP_LEVEL = {"webroot", "RELEASE-MANIFEST.sha256"}

EXPECTED_WEBROOT_TOP_LEVEL = {
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
}

FORBIDDEN_WEBROOT_TOP_LEVEL = {
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
    "RELEASE-MANIFEST.sha256",
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
            package = Path(tmp) / "release-package"
            subprocess.run(
                [sys.executable, str(BUILDER), "--output", str(package)],
                cwd=ROOT,
                check=True,
            )

            self.assertEqual(EXPECTED_PACKAGE_TOP_LEVEL, {p.name for p in package.iterdir()})

            webroot = package / "webroot"
            webroot_top_level = {p.name for p in webroot.iterdir()}
            self.assertEqual(EXPECTED_WEBROOT_TOP_LEVEL, webroot_top_level)
            self.assertFalse(webroot_top_level & FORBIDDEN_WEBROOT_TOP_LEVEL)

            manifest_path = package / "RELEASE-MANIFEST.sha256"
            manifest_rows = {}
            for line in manifest_path.read_text(encoding="utf-8").splitlines():
                hash_value, relative = line.split("  ", 1)
                self.assertNotIn(relative, manifest_rows)
                manifest_rows[relative] = hash_value

            release_files = {
                p.relative_to(webroot).as_posix(): p
                for p in webroot.rglob("*")
                if p.is_file()
            }
            self.assertEqual(set(release_files), set(manifest_rows))

            for relative, path in release_files.items():
                self.assertEqual(digest(path), manifest_rows[relative], relative)

            for path in webroot.rglob("*"):
                self.assertFalse(path.is_symlink(), path)
                if path.is_file():
                    self.assertFalse(path.name.startswith(".env"), path)
                    self.assertNotIn(path.suffix.lower(), {".pem", ".key", ".p12", ".pfx"})


if __name__ == "__main__":
    unittest.main()
