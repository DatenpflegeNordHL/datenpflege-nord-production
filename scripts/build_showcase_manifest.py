#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_REPO = "pulkitxm/claude-directory"
UPSTREAM_SNAPSHOT_COMMIT = "9b5ad43b1450fe6b28a42a9cb8115498d5c56e2a"
PUBLIC_MEDIA_BASE = "https://media.datenpflege-nord.de/gallery-media"
OWNED_DEMOS = {
    "nordic-editorial": ("dpn-editorial-nordic-editorial", "nordic-hero.svg", "/website-showcase/demo/nordic-editorial/"),
    "human-service": ("dpn-editorial-human-service", "service-hero.svg", "/website-showcase/demo/human-service/"),
    "growth-story": ("dpn-editorial-growth-story", "story-hero.svg", "/website-showcase/demo/growth-story/"),
    "local-trust": ("dpn-editorial-local-trust", "regional-hero.svg", "/website-showcase/demo/regional-trust/"),
    "product-led": ("dpn-editorial-product-led", "product-hero.svg", "/website-showcase/demo/product-led/"),
    "quiet-luxury": ("dpn-editorial-quiet-luxury", "luxury-hero.svg", "/website-showcase/demo/quiet-luxury/"),
}
CATEGORY_LABELS = {
    "3d-games": "3D & Interaktiv",
    "animations-loaders": "Animation & Interaktion",
    "components-ui": "UI & Komponenten",
    "hero-sections": "Hero & Einstieg",
    "landing-pages": "Landingpages",
    "portfolios": "Portfolios",
    "shaders": "Visuelle Effekte",
    "templates": "Website-Templates",
    "ui-design": "UI-Design",
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def public_sort_key(project: dict):
    if project.get("sourceOrder") is not None:
        return (0, int(project["sourceOrder"]), 0, project["source"]["path"])
    if project.get("sourceLastUpdated"):
        timestamp = datetime.fromisoformat(project["sourceLastUpdated"]).timestamp()
        return (1, 0, -timestamp, project["source"]["path"])
    if project["source"]["repository"] == UPSTREAM_REPO:
        return (1, 1, 0, project["source"]["path"])
    return (2, 0, 0, project["source"]["path"])

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--media-root", type=Path, default=Path("/srv/nordwerk-gallery/media"))
    p.add_argument("--manifest", type=Path, default=ROOT / "docs/design-gallery/showcase-source-manifest.json")
    p.add_argument("--catalogue", type=Path, default=ROOT / "website-showcase/showcase-projects.json")
    args = p.parse_args()

    legacy = load(ROOT / "docs/design-gallery/legacy-showcase-projects.json")
    curation = load(ROOT / "docs/design-gallery/legacy-curation.json")
    baseline = load(ROOT / "docs/design-gallery/showcase-editorial-baseline.json")
    source_order = load(ROOT / "docs/design-gallery/claude-directory-current-order.json")
    current_commit = source_order["source"]["currentCommit"]
    source_metadata = {x["sourcePath"]: x for x in source_order["projects"]}
    by_editorial_id = {x["id"]: x for x in baseline.get("curatedLegacyDirections", [])}
    by_owned_slug = {x["slug"]: x for x in baseline.get("projects", [])}
    approved_refs = {x["legacyReference"]["sourcePath"]: x for x in curation["directions"]}

    manifest_projects = []
    public_projects = []
    sha_lines = []

    for entry in legacy["entries"]:
        source_path = entry["sourcePath"]
        source_meta = source_metadata[source_path]
        curated = approved_refs.get(source_path)
        if curated:
            rights = "approved"
        elif entry.get("commercialTemplateHint") or entry.get("riskFlags"):
            rights = "review"
        else:
            rights = "unknown"

        poster_file = args.media_root / entry["poster"]["sourcePath"]
        video_file = args.media_root / entry["demo"]["sourcePath"]
        poster_sha = sha256(poster_file) if rights == "approved" else None
        video_sha = sha256(video_file) if rights == "approved" else None
        if rights == "approved":
            sha_lines.extend([
                f"{poster_sha}  /srv/nordwerk-gallery/media/{entry['poster']['sourcePath']}",
                f"{video_sha}  /srv/nordwerk-gallery/media/{entry['demo']['sourcePath']}",
            ])

        record = {
            "projectId": entry["id"],
            "slug": entry["sourcePath"].replace("/", "--"),
            "source": {"repository": UPSTREAM_REPO, "commit": UPSTREAM_SNAPSHOT_COMMIT, "path": source_path, "license": "MIT"},
            "sourceCommit": current_commit,
            "sourceOrder": source_meta["sourceOrder"],
            "sourceLastUpdated": source_meta["sourceLastUpdated"],
            "sourceListedCurrent": source_meta["sourceListedCurrent"],
            "poster": {"path": entry["poster"]["sourcePath"], "bytes": entry["poster"]["bytes"], "gitBlobSha": entry["poster"]["gitBlobSha"], "sha256": poster_sha},
            "video": {"path": entry["demo"]["sourcePath"], "bytes": entry["demo"]["bytes"], "gitBlobSha": entry["demo"]["gitBlobSha"], "sha256": video_sha},
            "templatePath": source_path if source_path.startswith("templates/") else None,
            "rightsStatus": rights,
            "public": rights == "approved",
            "riskFlags": entry.get("riskFlags", []),
            "promptPresent": bool(entry.get("sourceEvidence", {}).get("promptPresent")),
        }
        manifest_projects.append(record)

        if rights == "approved":
            editorial = by_editorial_id[curated["id"]]
            public_projects.append({
                "id": entry["id"],
                "slug": record["slug"],
                "name": editorial["name"],
                "source": {"repository": UPSTREAM_REPO, "commit": UPSTREAM_SNAPSHOT_COMMIT, "path": source_path},
                "sourceCommit": current_commit,
                "sourceOrder": source_meta["sourceOrder"],
                "sourceLastUpdated": source_meta["sourceLastUpdated"],
                "sourceListedCurrent": source_meta["sourceListedCurrent"],
                "licenseStatus": "MIT-reviewed",
                "status": "approved",
                "category": editorial["category"],
                "style": editorial.get("style", []),
                "industries": editorial.get("industries", []),
                "description": editorial["description"],
                "poster": {"type": "image", "src": f"{PUBLIC_MEDIA_BASE}/{entry['poster']['sourcePath']}", "alt": f"Website-Vorschau: {editorial['name']}", "width": 960, "height": 600, "sha256": poster_sha},
                "video": {"src": f"{PUBLIC_MEDIA_BASE}/{entry['demo']['sourcePath']}", "type": "video/mp4", "sha256": video_sha},
                "demo": None,
                "templateAvailable": False,
                "indexable": False,
                "approved": True,
            })

    for slug, (project_id, poster_name, demo) in OWNED_DEMOS.items():
        source = by_owned_slug[slug]
        poster_path = ROOT / "assets/showcase-demos" / poster_name
        demo_file = ROOT / demo.lstrip("/") / "index.html"
        poster_hash = sha256(poster_path)
        demo_hash = sha256(demo_file)
        record = {
            "projectId": project_id,
            "slug": slug,
            "source": {
                "repository": "DatenpflegeNordHL/datenpflege-nord-production",
                "commit": "self",
                "commitSemantics": "same Git commit that contains this manifest",
                "path": demo.lstrip("/"),
                "license": "owned",
            },
            "sourceCommit": "self",
            "sourceOrder": None,
            "sourceLastUpdated": None,
            "sourceListedCurrent": False,
            "poster": {"path": f"assets/showcase-demos/{poster_name}", "bytes": poster_path.stat().st_size, "sha256": poster_hash},
            "video": None,
            "templatePath": demo,
            "templateSha256": demo_hash,
            "rightsStatus": "approved",
            "public": True,
            "riskFlags": [],
            "promptPresent": False,
        }
        manifest_projects.append(record)
        public_projects.append({
            "id": project_id,
            "slug": slug,
            "name": source["name"],
            "source": {"repository": "DatenpflegeNordHL/datenpflege-nord-production", "path": demo.lstrip("/")},
            "sourceCommit": "self",
            "sourceOrder": None,
            "sourceLastUpdated": None,
            "sourceListedCurrent": False,
            "licenseStatus": "owned",
            "status": "approved",
            "category": source["category"],
            "style": source.get("style", []),
            "industries": source.get("industries", []),
            "description": source["description"],
            "poster": {"type": "image", "src": f"/assets/showcase-demos/{poster_name}?v={poster_hash}", "alt": f"Website-Vorschau: {source['name']}", "width": 1600, "height": 1000, "sha256": poster_hash},
            "video": None,
            "demo": demo,
            "templateAvailable": True,
            "indexable": False,
            "approved": True,
        })
        sha_lines.extend([f"{poster_hash}  assets/showcase-demos/{poster_name}", f"{demo_hash}  {demo.lstrip('/')}index.html"])

    public_projects.sort(key=public_sort_key)
    for display_order, project in enumerate(public_projects, 1):
        project["displayOrder"] = display_order

    counts = {key: sum(1 for x in manifest_projects if x["rightsStatus"] == key) for key in ("approved", "review", "rejected", "unknown")}
    manifest = {
        "schemaVersion": 3,
        "generatedAt": "2026-09-18",
        "sourceArchive": {
            "gitMirror": "/srv/nordwerk-gallery/archive/claude-directory.git",
            "gitBundle": "/srv/nordwerk-gallery/archive/claude-directory.bundle",
            "pinnedCommit": UPSTREAM_SNAPSHOT_COMMIT,
            "currentCommit": current_commit,
            "publicDirectoryUrl": source_order["source"]["publicDirectoryUrl"],
        },
        "media": {"privateRoot": "/srv/nordwerk-gallery/media", "publicBase": PUBLIC_MEDIA_BASE, "nginxLoopback": "127.0.0.1:8090"},
        "rightsPolicy": {"approvedPublic": True, "reviewPublic": False, "rejectedPublic": False, "unknownPublic": False},
        "summary": {
            "legacyFound": len(legacy["entries"]),
            "currentUpstreamProjects": source_order["summary"]["currentInventoryProjects"],
            "currentDirectoryProjects": source_order["summary"]["currentPublicDirectoryProjects"],
            "addedSinceSnapshot": source_order["summary"]["addedSinceSnapshot"],
            "removedSinceSnapshot": source_order["summary"]["removedSinceSnapshot"],
            "ownedProjects": len(OWNED_DEMOS),
            "totalProjects": len(manifest_projects),
            **counts,
            "publicProjects": sum(1 for x in manifest_projects if x["public"]),
            "realVideos": sum(1 for x in public_projects if x.get("video")),
            "templateDemos": sum(1 for x in public_projects if x.get("demo")),
        },
        "projects": manifest_projects,
    }
    catalogue = {
        "schemaVersion": 3,
        "updatedAt": "2026-09-18",
        "publicationPolicy": {"onlyApprovedProjectsArePublic": True, "templateDemosAreNoindex": True, "mediaOrigin": PUBLIC_MEDIA_BASE},
        "summary": manifest["summary"],
        "projects": public_projects,
    }
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.catalogue.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksum_path = args.manifest.with_name("showcase-public-media.sha256")
    checksum_path.write_text("\n".join(sorted(sha_lines)) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(args.manifest), "catalogue": str(args.catalogue), "checksums": str(checksum_path), "summary": manifest["summary"]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
