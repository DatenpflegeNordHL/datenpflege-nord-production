#!/usr/bin/env python3
"""Build a non-indexable GitHub Pages artifact from the release allowlist.

The production paths stay untouched. Root-relative references are rewritten only
in the generated artifact so the site also works below a project Pages path.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
from pathlib import Path


TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".txt", ".webmanifest", ".xml"}
ROOT_URL = re.compile(r"(?P<quote>[\"'])/(?!/)")
ROBOTS_META = re.compile(r"<meta\b(?=[^>]*\bname\s*=\s*[\"']robots[\"'])[^>]*>", re.I)


def load_public_files(root: Path):
    module_path = root / "ops" / "deploy" / "check_asset_versions.py"
    spec = importlib.util.spec_from_file_location("asset_versions", module_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load public allowlist from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.public_files(root)


def rewrite(content: str, base_path: str, suffix: str) -> str:
    content = ROOT_URL.sub(r"\g<quote>" + base_path + "/", content)
    if suffix == ".html":
        noindex = '<meta name="robots" content="noindex, nofollow, noarchive">'
        content, replacements = ROBOTS_META.subn(noindex, content, count=1)
        if not replacements:
            content = content.replace("</head>", f"  {noindex}\n</head>", 1)
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-path", required=True, help="Project Pages path, e.g. /owner-site")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    base_path = args.base_path.rstrip("/")
    if not re.fullmatch(r"/[A-Za-z0-9._-]+", base_path):
        raise ValueError("--base-path must be one simple absolute path segment")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite preview output: {output}")

    copied = []
    for source in load_public_files(root):
        target = output / source.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in TEXT_SUFFIXES:
            target.write_text(rewrite(source.read_text(encoding="utf-8"), base_path, source.suffix), encoding="utf-8")
        else:
            shutil.copy2(source, target)
        copied.append(target.relative_to(output).as_posix())

    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print(f"Built {len(copied)} allowlisted public files in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
