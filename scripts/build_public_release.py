#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "release-package"

# Explicit allowlist. Anything not listed here is deployment-internal by default.
PUBLIC_ENTRIES = (
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
)

FORBIDDEN_OUTPUT_NAMES = {
    ".git",
    ".github",
    ".env",
    "backend",
    "docs",
    "tests",
    "scripts",
}

FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
MANIFEST_NAME = "RELEASE-MANIFEST.sha256"
WEBROOT_NAME = "webroot"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_symlinks(path: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"Refusing symlink in public release source: {path.relative_to(ROOT)}")
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_symlink():
                raise RuntimeError(
                    f"Refusing symlink in public release source: {child.relative_to(ROOT)}"
                )


def copy_entry(source: Path, destination: Path) -> None:
    reject_symlinks(source)
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def validate_webroot(webroot: Path) -> None:
    top_level = {p.name for p in webroot.iterdir()}
    forbidden = sorted(top_level & FORBIDDEN_OUTPUT_NAMES)
    if forbidden:
        raise RuntimeError(f"Forbidden top-level release entries present: {', '.join(forbidden)}")

    for path in webroot.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"Symlink present in built release: {path.relative_to(webroot)}")
        if path.is_file():
            if path.name.startswith(".env") or path.suffix.lower() in FORBIDDEN_SUFFIXES:
                raise RuntimeError(f"Sensitive-looking file present in release: {path.relative_to(webroot)}")


def write_manifest(webroot: Path, manifest: Path) -> None:
    rows: list[str] = []
    for path in sorted(p for p in webroot.rglob("*") if p.is_file()):
        rel = path.relative_to(webroot).as_posix()
        rows.append(f"{sha256(path)}  {rel}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")


def build(output: Path) -> None:
    if output.resolve() == ROOT.resolve():
        raise RuntimeError("Output must not be the repository root")

    if output.exists():
        shutil.rmtree(output)

    webroot = output / WEBROOT_NAME
    webroot.mkdir(parents=True)

    missing: list[str] = []
    for relative in PUBLIC_ENTRIES:
        source = ROOT / relative
        if not source.exists():
            missing.append(relative)
            continue
        copy_entry(source, webroot / relative)

    if missing:
        raise RuntimeError(f"Missing required public release entries: {', '.join(missing)}")

    validate_webroot(webroot)
    write_manifest(webroot, output / MANIFEST_NAME)

    package_entries = {p.name for p in output.iterdir()}
    expected_package_entries = {WEBROOT_NAME, MANIFEST_NAME}
    if package_entries != expected_package_entries:
        raise RuntimeError(
            f"Unexpected release-package entries: {sorted(package_entries - expected_package_entries)}"
        )

    file_count = sum(1 for p in webroot.rglob("*") if p.is_file())
    print(f"Built deterministic public release with {file_count} webroot files at {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the allowlisted DatenpflegeNord release package.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
