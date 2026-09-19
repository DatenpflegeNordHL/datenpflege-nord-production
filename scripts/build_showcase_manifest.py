#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_REPO = "pulkitxm/claude-directory"
UPSTREAM_SNAPSHOT_COMMIT = "9b5ad43b1450fe6b28a42a9cb8115498d5c56e2a"
PUBLIC_MEDIA_BASE = "https://media.datenpflege-nord.de/gallery-media"
INITIAL_STATIC_COUNT = 12
INITIAL_STATIC_START = "<!-- showcase-initial:start -->"
INITIAL_STATIC_END = "<!-- showcase-initial:end -->"
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


def git_tree_metadata(mirror: Path, commit: str, paths: list[str]) -> dict[str, dict]:
    result = subprocess.run(
        ["git", f"--git-dir={mirror}", "ls-tree", "-rl", "--full-tree", commit, "--", *paths],
        check=True,
        text=True,
        capture_output=True,
    )
    metadata = {}
    for line in result.stdout.splitlines():
        left, path = line.split("\t", 1)
        _mode, _kind, blob_sha, size = left.split()
        metadata[path] = {"gitBlobSha": blob_sha, "bytes": int(size)}
    return metadata

def public_sort_key(project: dict):
    if project.get("sourceType") == "legacy":
        return (int(project["sourceOrder"]), 0, project["source"]["path"])
    owned_slot = project.get("ownedSlot", 371)
    return (owned_slot, 1, project["source"]["path"])


def legacy_name(source_path: str) -> str:
    words = source_path.rsplit("/", 1)[-1].replace("-", " ").split()
    acronyms = {
        "ai": "AI", "api": "API", "cli": "CLI", "cms": "CMS", "crm": "CRM",
        "glsl": "GLSL", "hls": "HLS", "nft": "NFT", "saas": "SaaS", "ui": "UI",
        "ux": "UX", "webgl": "WebGL", "3d": "3D",
    }
    return " ".join(acronyms.get(word.lower(), word.capitalize()) for word in words)


def valid_media(path: Path, kind: str, expected_bytes: int) -> bool:
    if not path.is_file() or path.stat().st_size <= 0:
        return False
    if expected_bytes and path.stat().st_size != expected_bytes:
        return False
    with path.open("rb") as stream:
        head = stream.read(64)
    return head.startswith(b"\xff\xd8\xff") if kind == "poster" else b"ftyp" in head


def update_static_initial_cards(page: Path, projects: list[dict]) -> None:
    source = page.read_text(encoding="utf-8")
    if INITIAL_STATIC_START not in source or INITIAL_STATIC_END not in source:
        raise RuntimeError("showcase initial-card markers are missing")
    cards = []
    for project in projects[:INITIAL_STATIC_COUNT]:
        poster = project["poster"]
        cards.append(
            '<article class="showcase-card" data-project-id="{id}">'
            '<span class="showcase-card__media">'
            '<img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async">'
            '</span>'
            '<span class="showcase-card__body">'
            '<span class="showcase-card__category">{label} · {category}</span>'
            '<span class="showcase-card__title">{name}</span>'
            '</span>'
            '</article>'.format(
                id=html.escape(str(project["id"]), quote=True),
                src=html.escape(str(poster["src"]), quote=True),
                alt=html.escape(str(poster.get("alt") or f'Website-Vorschau: {project["name"]}'), quote=True),
                width=int(poster.get("width") or 960),
                height=int(poster.get("height") or 600),
                label=html.escape(str(project["publicLabel"])),
                category=html.escape(str(project["category"])),
                name=html.escape(str(project["name"])),
            )
        )
    replacement = INITIAL_STATIC_START + "\n        " + "\n        ".join(cards) + "\n        " + INITIAL_STATIC_END
    before, rest = source.split(INITIAL_STATIC_START, 1)
    _, after = rest.split(INITIAL_STATIC_END, 1)
    page.write_text(before + replacement + after, encoding="utf-8")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--media-root", type=Path, default=Path("/srv/nordwerk-gallery/media"))
    p.add_argument("--mirror", type=Path, default=Path("/srv/nordwerk-gallery/archive/claude-directory.git"))
    p.add_argument("--manifest", type=Path, default=ROOT / "docs/design-gallery/showcase-source-manifest.json")
    p.add_argument("--catalogue", type=Path, default=ROOT / "website-showcase/showcase-projects.json")
    args = p.parse_args()

    legacy = load(ROOT / "docs/design-gallery/legacy-showcase-projects.json")
    curation = load(ROOT / "docs/design-gallery/legacy-curation.json")
    baseline = load(ROOT / "docs/design-gallery/showcase-editorial-baseline.json")
    source_order = load(ROOT / "docs/design-gallery/claude-directory-current-order.json")
    current_commit = source_order["source"]["currentCommit"]
    source_metadata = {x["sourcePath"]: x for x in source_order["projects"]}
    requested_media_paths = [
        rel
        for entry in legacy["entries"]
        for rel in (entry["poster"]["sourcePath"], entry["demo"]["sourcePath"])
    ]
    current_media_metadata = git_tree_metadata(args.mirror, current_commit, requested_media_paths)
    by_editorial_id = {x["id"]: x for x in baseline.get("curatedLegacyDirections", [])}
    by_owned_slug = {x["slug"]: x for x in baseline.get("projects", [])}
    approved_refs = {x["legacyReference"]["sourcePath"]: x for x in curation["directions"]}

    manifest_projects = []
    public_projects = []
    sha_lines = []

    listed_paths = {path for path, meta in source_metadata.items() if meta["sourceListedCurrent"]}
    legacy_public_count = 0
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
        poster_tree = current_media_metadata.get(entry["poster"]["sourcePath"], entry["poster"])
        video_tree = current_media_metadata.get(entry["demo"]["sourcePath"], entry["demo"])
        media_ok = (
            source_path in listed_paths
            and valid_media(poster_file, "poster", poster_tree["bytes"])
            and valid_media(video_file, "video", video_tree["bytes"])
        )
        poster_sha = sha256(poster_file) if media_ok else None
        video_sha = sha256(video_file) if media_ok else None
        if media_ok:
            sha_lines.extend([
                f"{poster_sha}  /srv/nordwerk-gallery/media/{entry['poster']['sourcePath']}",
                f"{video_sha}  /srv/nordwerk-gallery/media/{entry['demo']['sourcePath']}",
            ])

        record = {
            "projectId": entry["id"],
            "slug": entry["sourcePath"].replace("/", "--"),
            "sourceType": "legacy",
            "source": {"repository": UPSTREAM_REPO, "commit": current_commit, "path": source_path, "license": "MIT"},
            "sourceCommit": current_commit,
            "sourceOrder": source_meta["sourceOrder"],
            "sourceLastUpdated": source_meta["sourceLastUpdated"],
            "sourceListedCurrent": source_meta["sourceListedCurrent"],
            "poster": {"path": entry["poster"]["sourcePath"], "bytes": poster_tree["bytes"], "gitBlobSha": poster_tree["gitBlobSha"], "sha256": poster_sha},
            "video": {"path": entry["demo"]["sourcePath"], "bytes": video_tree["bytes"], "gitBlobSha": video_tree["gitBlobSha"], "sha256": video_sha},
            "templatePath": source_path if source_path.startswith("templates/") else None,
            "rightsStatus": rights,
            "licenseStatus": "MIT-source; media-rights-not-asserted",
            "public": media_ok,
            "riskFlags": entry.get("riskFlags", []),
            "promptPresent": bool(entry.get("sourceEvidence", {}).get("promptPresent")),
        }
        manifest_projects.append(record)

        if media_ok:
            legacy_public_count += 1
            editorial = by_editorial_id.get(curated["id"]) if curated else None
            category = editorial["category"] if editorial else CATEGORY_LABELS.get(source_path.split("/", 1)[0], "Website-Inspiration")
            name = editorial["name"] if editorial else legacy_name(source_path)
            description = editorial["description"] if editorial else f"Video-Preview aus dem öffentlichen Claude Directory im Bereich {category}."
            public_projects.append({
                "id": entry["id"],
                "slug": record["slug"],
                "name": name,
                "sourceType": "legacy",
                "publicLabel": "Video-Preview",
                "source": {"repository": UPSTREAM_REPO, "commit": current_commit, "path": source_path},
                "sourceCommit": current_commit,
                "sourceOrder": source_meta["sourceOrder"],
                "sourceLastUpdated": source_meta["sourceLastUpdated"],
                "sourceListedCurrent": source_meta["sourceListedCurrent"],
                "rightsStatus": rights,
                "licenseStatus": "MIT-source; media-rights-not-asserted",
                "riskFlags": entry.get("riskFlags", []),
                "publicationStatus": "active",
                "active": True,
                "category": category,
                "style": editorial.get("style", []) if editorial else [],
                "industries": editorial.get("industries", []) if editorial else [],
                "description": description,
                "poster": {"type": "image", "src": f"{PUBLIC_MEDIA_BASE}/{entry['poster']['sourcePath']}", "alt": f"Website-Vorschau: {name}", "width": 960, "height": 600, "sha256": poster_sha},
                "video": {"src": f"{PUBLIC_MEDIA_BASE}/{entry['demo']['sourcePath']}", "type": "video/mp4", "sha256": video_sha},
                "demo": None,
                "templateAvailable": False,
                "indexable": False,
            })

    owned_slots = [60, 120, 180, 240, 300, 360]
    for owned_index, (slug, (project_id, poster_name, demo)) in enumerate(OWNED_DEMOS.items()):
        source = by_owned_slug[slug]
        poster_path = ROOT / "assets/showcase-demos" / poster_name
        demo_file = ROOT / demo.lstrip("/") / "index.html"
        poster_hash = sha256(poster_path)
        demo_hash = sha256(demo_file)
        record = {
            "projectId": project_id,
            "slug": slug,
            "sourceType": "owned",
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
            "licenseStatus": "owned",
            "public": True,
            "riskFlags": [],
            "promptPresent": False,
        }
        manifest_projects.append(record)
        public_projects.append({
            "id": project_id,
            "slug": slug,
            "name": source["name"],
            "sourceType": "owned",
            "publicLabel": "DatenpflegeNord Demo",
            "ownedSlot": owned_slots[owned_index],
            "source": {"repository": "DatenpflegeNordHL/datenpflege-nord-production", "path": demo.lstrip("/")},
            "sourceCommit": "self",
            "sourceOrder": None,
            "sourceLastUpdated": None,
            "sourceListedCurrent": False,
            "licenseStatus": "owned",
            "rightsStatus": "approved",
            "riskFlags": [],
            "publicationStatus": "active",
            "active": True,
            "category": source["category"],
            "style": source.get("style", []),
            "industries": source.get("industries", []),
            "description": source["description"],
            "poster": {"type": "image", "src": f"/assets/showcase-demos/{poster_name}?v={poster_hash}", "alt": f"Website-Vorschau: {source['name']}", "width": 1600, "height": 1000, "sha256": poster_hash},
            "video": None,
            "demo": demo,
            "templateAvailable": True,
            "indexable": False,
        })
        sha_lines.extend([f"{poster_hash}  assets/showcase-demos/{poster_name}", f"{demo_hash}  {demo.lstrip('/')}index.html"])

    public_projects.sort(key=public_sort_key)
    for display_order, project in enumerate(public_projects, 1):
        project["displayOrder"] = display_order

    counts = {key: sum(1 for x in manifest_projects if x["rightsStatus"] == key) for key in ("approved", "review", "rejected", "unknown")}
    manifest = {
        "schemaVersion": 3,
        "generatedAt": "2026-09-19",
        "sourceArchive": {
            "gitMirror": "/srv/nordwerk-gallery/archive/claude-directory.git",
            "gitBundle": "/srv/nordwerk-gallery/archive/claude-directory.bundle",
            "pinnedCommit": UPSTREAM_SNAPSHOT_COMMIT,
            "currentCommit": current_commit,
            "publicDirectoryUrl": source_order["source"]["publicDirectoryUrl"],
        },
        "media": {
            "publicRoot": "/srv/nordwerk-gallery/media",
            "publicBase": PUBLIC_MEDIA_BASE,
            "privateRoot": "/srv/nordwerk-gallery/media-private-20260918",
            "nginxLoopback": "127.0.0.1:8090",
        },
        "rightsPolicy": {"metadataRetained": True, "rightsMetadataBlocksCurrentDirectorySync": False, "noPublicRightsAssurance": True},
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
            "publicLegacyProjects": legacy_public_count,
            "publicShowcaseEntries": len(public_projects),
            "realVideos": sum(1 for x in public_projects if x.get("video")),
            "templateDemos": sum(1 for x in public_projects if x.get("demo")),
        },
        "projects": manifest_projects,
    }
    catalogue = {
        "schemaVersion": 3,
        "updatedAt": "2026-09-19",
        "publicationPolicy": {"currentUpstreamDirectoryIsLegacyGate": True, "rightsMetadataIsInformational": True, "templateDemosAreNoindex": True, "mediaOrigin": PUBLIC_MEDIA_BASE},
        "summary": manifest["summary"],
        "projects": public_projects,
    }
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.catalogue.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_static_initial_cards(ROOT / "website-showcase" / "index.html", public_projects)
    checksum_path = args.manifest.with_name("showcase-public-media.sha256")
    checksum_path.write_text("\n".join(sorted(sha_lines)) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(args.manifest), "catalogue": str(args.catalogue), "checksums": str(checksum_path), "summary": manifest["summary"]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
