#!/usr/bin/env python3
"""Create a release-gated inventory from the legacy gallery catalogue.

The output is documentation only. It is intentionally excluded from the public
deployment allowlist and keeps all imported legacy records non-publishable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def record(entry: dict) -> dict:
    media = entry.get("media", {})
    return {
        "id": entry["id"],
        "name": entry.get("customerTitle", entry["id"]),
        "source": "pulkitxm/claude-directory",
        "sourcePath": entry.get("sourcePath"),
        "framework": "unknown",
        "preview": None,
        "poster": media.get("poster"),
        "demo": media.get("video"),
        "externalDomains": [],
        "externalAssets": [],
        "fonts": [],
        "scripts": [],
        "trackers": [],
        "forms": [],
        "foreignBranding": "unknown",
        "deadLinks": "not_checked",
        "buildRuntimeProblems": "not_checked",
        "duplicateSimilarity": "not_checked",
        "licenseStatus": "unknown",
        "commercialTemplateHint": "premium_template" in entry.get("riskFlags", []),
        "riskFlags": entry.get("riskFlags", []),
        "reviewStatus": entry.get("reviewStatus", "pending"),
        "mediaStatus": entry.get("mediaStatus", "pending_sync"),
        "status": "unknown",
        "approved": False,
        "publiclyUsable": False,
        # Retain the immutable prompt identity as audit evidence. It does not
        # change the release gate and is kept only in documentation.
        "sourceEvidence": entry.get("sourceEvidence", {}),
        "note": "Nicht veröffentlichen: Rechte-, Marken-, Asset- und Medienprüfung fehlen.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--legacy-commit", required=True)
    args = parser.parse_args()
    source = json.loads(args.catalogue.read_text(encoding="utf-8"))
    entries = [record(entry) for entry in source["entries"]]
    output = {
        "schemaVersion": 1,
        "source": {
            "repository": "DatenpflegeNordHL/website-final",
            "branch": "agent/nordwerk-design-gallery",
            "commit": args.legacy_commit,
            "upstreamRepository": source["source"]["upstreamRepository"],
            "upstreamCommit": source["source"]["upstreamCommit"],
        },
        "releaseGate": {
            "rule": "Only approved records may be public.",
            "approved": 0,
            "review": 0,
            "rejected": 0,
            "unknown": len(entries),
        },
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "entries": len(entries)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
