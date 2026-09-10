#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path, PurePosixPath


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError(f"Malformed manifest line {line_number}") from exc

        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise RuntimeError(f"Invalid SHA-256 on manifest line {line_number}")

        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or relative.startswith("./") or "\\" in relative:
            raise RuntimeError(f"Unsafe manifest path on line {line_number}: {relative}")
        if relative in expected:
            raise RuntimeError(f"Duplicate manifest path on line {line_number}: {relative}")

        expected[relative] = digest

    if not expected:
        raise RuntimeError("Release manifest is empty")
    return expected


def verify(webroot: Path, manifest: Path) -> None:
    webroot = webroot.resolve()
    manifest = manifest.resolve()

    if not webroot.is_dir():
        raise RuntimeError(f"Webroot does not exist: {webroot}")
    if not manifest.is_file():
        raise RuntimeError(f"Manifest does not exist: {manifest}")

    expected = load_manifest(manifest)
    actual: dict[str, Path] = {}

    for path in webroot.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"Symlink present in deployed webroot: {path.relative_to(webroot)}")
        if path.is_file():
            actual[path.relative_to(webroot).as_posix()] = path

    expected_paths = set(expected)
    actual_paths = set(actual)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)

    if missing:
        raise RuntimeError("Missing deployed files: " + ", ".join(missing))
    if extra:
        raise RuntimeError("Unexpected deployed files: " + ", ".join(extra))

    mismatched: list[str] = []
    for relative, expected_digest in expected.items():
        if sha256(actual[relative]) != expected_digest:
            mismatched.append(relative)

    if mismatched:
        raise RuntimeError("Hash mismatch for deployed files: " + ", ".join(sorted(mismatched)))

    print(f"Release manifest verified: {len(expected)} files match exactly.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a deployed webroot against a release SHA-256 manifest.")
    parser.add_argument("--webroot", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    try:
        verify(args.webroot, args.manifest)
    except RuntimeError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
