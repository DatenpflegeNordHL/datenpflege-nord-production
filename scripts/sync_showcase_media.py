#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MIRROR = Path("/srv/nordwerk-gallery/archive/claude-directory.git")
DEFAULT_ACTIVE_LINK = Path("/srv/nordwerk-gallery/media")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_tree_metadata(mirror: Path, commit: str, paths: list[str]) -> dict[str, dict]:
    command = ["git", f"--git-dir={mirror}", "ls-tree", "-rl", "--full-tree", commit, "--", *paths]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    metadata: dict[str, dict] = {}
    for line in result.stdout.splitlines():
        left, path = line.split("\t", 1)
        mode, kind, blob_sha, size = left.split()
        metadata[path] = {"mode": mode, "kind": kind, "gitBlobSha": blob_sha, "bytes": int(size)}
    return metadata


def looks_like_jpeg(path: Path) -> bool:
    with path.open("rb") as stream:
        return stream.read(3) == b"\xff\xd8\xff"


def looks_like_mp4(path: Path) -> bool:
    with path.open("rb") as stream:
        return b"ftyp" in stream.read(64)


def validate_release(release: Path, selected: list[dict], metadata: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    valid: list[dict] = []
    failures: list[dict] = []
    for project in selected:
        source_path = project["sourcePath"]
        poster_rel = f"{source_path}/poster.jpg"
        video_rel = f"{source_path}/demo.mp4"
        issues: list[str] = []
        files = {}
        for role, rel, signature_check in (
            ("poster", poster_rel, looks_like_jpeg),
            ("video", video_rel, looks_like_mp4),
        ):
            file_path = release / rel
            tree = metadata.get(rel)
            if tree is None:
                issues.append(f"{role}:missing-in-git-tree")
                continue
            if not file_path.is_file():
                issues.append(f"{role}:missing-after-extract")
                continue
            size = file_path.stat().st_size
            if size <= 0:
                issues.append(f"{role}:zero-byte")
            if size != tree["bytes"]:
                issues.append(f"{role}:size-mismatch:{size}!={tree['bytes']}")
            if not signature_check(file_path):
                issues.append(f"{role}:invalid-signature")
            files[role] = {
                "path": rel,
                "bytes": size,
                "gitBlobSha": tree["gitBlobSha"],
                "sha256": sha256(file_path),
            }
        record = {
            "sourcePath": source_path,
            "sourceOrder": project["sourceOrder"],
            "poster": files.get("poster"),
            "video": files.get("video"),
        }
        if issues:
            record["issues"] = issues
            failures.append(record)
        else:
            valid.append(record)
    return valid, failures


def activate_link(active_link: Path, release: Path) -> None:
    active_link.parent.mkdir(parents=True, exist_ok=True)
    temp_link = active_link.with_name(f".{active_link.name}.next-{os.getpid()}")
    if temp_link.exists() or temp_link.is_symlink():
        temp_link.unlink()
    temp_link.symlink_to(release)
    os.replace(temp_link, active_link)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish only currently listed Claude Directory showcase media.")
    parser.add_argument("--mirror", type=Path, default=DEFAULT_MIRROR)
    parser.add_argument("--active-link", type=Path, default=DEFAULT_ACTIVE_LINK)
    parser.add_argument("--release-root", type=Path)
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()

    source_order = load(ROOT / "docs/design-gallery/claude-directory-current-order.json")
    commit = source_order["source"]["currentCommit"]
    selected = sorted(
        (project for project in source_order["projects"] if project["sourceListedCurrent"]),
        key=lambda project: project["sourceOrder"],
    )
    if len(selected) != 371:
        raise SystemExit(f"Refusing sync: expected 371 currently listed projects, found {len(selected)}")
    if [project["sourceOrder"] for project in selected] != list(range(1, 372)):
        raise SystemExit("Refusing sync: public sourceOrder is not the exact contiguous 1..371 sequence")

    release_root = args.release_root or Path(f"/srv/nordwerk-gallery/public-media-current-{commit[:8]}")
    requested_paths = [
        rel
        for project in selected
        for rel in (f"{project['sourcePath']}/poster.jpg", f"{project['sourcePath']}/demo.mp4")
    ]
    metadata = git_tree_metadata(args.mirror, commit, requested_paths)
    missing_tree = sorted(set(requested_paths) - set(metadata))
    if missing_tree:
        print(json.dumps({"result": "FAIL", "reason": "missing-source-media", "paths": missing_tree}, ensure_ascii=False))
        return 2

    release_root.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{release_root.name}.staging-", dir=release_root.parent))
    try:
        archive = subprocess.Popen(
            ["git", f"--git-dir={args.mirror}", "archive", "--format=tar", commit, "--", *requested_paths],
            stdout=subprocess.PIPE,
        )
        assert archive.stdout is not None
        extract = subprocess.run(["tar", "-xf", "-", "-C", str(staging)], stdin=archive.stdout)
        archive.stdout.close()
        archive_rc = archive.wait()
        if archive_rc != 0 or extract.returncode != 0:
            raise RuntimeError(f"git archive/tar failed: archive={archive_rc}, tar={extract.returncode}")

        valid, failures = validate_release(staging, selected, metadata)
        if failures:
            print(json.dumps({"result": "FAIL", "validProjects": len(valid), "failedProjects": failures}, ensure_ascii=False, indent=2))
            return 3

        for directory in [staging, *[path for path in staging.rglob("*") if path.is_dir()]]:
            directory.chmod(0o755)
        for file_path in (path for path in staging.rglob("*") if path.is_file()):
            file_path.chmod(0o644)

        if release_root.exists():
            shutil.rmtree(release_root)
        os.replace(staging, release_root)
        staging = None
        if args.activate:
            activate_link(args.active_link, release_root)

        report = {
            "result": "PASS",
            "commit": commit,
            "projects": len(valid),
            "posters": len(valid),
            "videos": len(valid),
            "files": len(valid) * 2,
            "bytes": sum(row["poster"]["bytes"] + row["video"]["bytes"] for row in valid),
            "releaseRoot": str(release_root),
            "activeLink": str(args.active_link.resolve()) if args.activate else None,
            "failedProjects": [],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    finally:
        if staging is not None and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
