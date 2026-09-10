#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "release-webroot"

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


def validate_output(output: Path) -> None:
    top_level = {p.name for p in output.iterdir() if p.name != MANIFEST_NAME}
    forbidden = sorted(top_level & FORBIDDEN_OUTPUT_NAMES)
    if forbidden:
        raise RuntimeError(f"Forbidden top-level release entries present: {', '.join(forbidden)}")

    for path in output.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"Symlink present in built release: {path.relative_to(output)}")
        if path.is_file():
            if path.name.startswith(".env") or path.suffix.lower() in FORBIDDEN_SUFFIXES:
                raise RuntimeError(f"Sensitive-looking file present in release: {path.relative_to(output)}")


def write_manifest(output: Path) -> None:
    rows: list[str] = []
    for path in sorted(p for p in output.rglob("*") if p.is_file() and p.name != MANIFEST_NAME):
        rel = path.relative_to(output).as_posix()
        rows.append(f"{sha256(path)}  {rel}")
    (output / MANIFEST_NAME).write_text("\n".join(rows) + "\n", encoding="utf-8")


def build(output: Path) -> None:
    if output.resolve() == ROOT.resolve():
        raise RuntimeError("Output must not be the repository root")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    missing: list[str] = []
    for relative in PUBLIC_ENTRIES:
        source = ROOT / relative
        if not source.exists():
            missing.append(relative)
            continue
        copy_entry(source, output / relative)

    if missing:
        raise RuntimeError(f"Missing required public release entries: {', '.join(missing)}")

    validate_output(output)
    write_manifest(output)
    validate_output(output)

    file_count = sum(1 for p in output.rglob("*") if p.is_file() and p.name != MANIFEST_NAME)
    print(f"Built deterministic public release with {file_count} files at {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the allowlisted DatenpflegeNord public webroot.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
