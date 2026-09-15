#!/usr/bin/env python3
"""Additional deterministic graph, indexability and service-entity checks.

Run alongside site_audit.py. These checks prove repository properties, not
business truth, rich-result eligibility, hosted CI or production behavior.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_audit

ALLOWED_CANONICALS = {
    "https://datenpflege-nord.de/",
    "https://datenpflege-nord.de/en/",
    "https://datenpflege-nord.de/impressum/",
    "https://datenpflege-nord.de/datenschutz/",
    "https://datenpflege-nord.de/softwareentwicklung-luebeck/",
    "https://datenpflege-nord.de/webentwicklung-luebeck/",
    "https://datenpflege-nord.de/ki-automatisierung-luebeck/",
    "https://datenpflege-nord.de/wissen/individualsoftware-kosten/",
    "https://datenpflege-nord.de/wissen/website-relaunch-checkliste/",
}

AUTHORITY_OWNERS = {
    "https://datenpflege-nord.de/wissen/individualsoftware-kosten/":
        "https://datenpflege-nord.de/softwareentwicklung-luebeck/",
    "https://datenpflege-nord.de/wissen/website-relaunch-checkliste/":
        "https://datenpflege-nord.de/webentwicklung-luebeck/",
}


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings: list[int] = []
        self.images: list[dict] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append(int(tag[1]))
        if tag == "img":
            self.images.append(dict(attrs))


def link_graph(pages):
    """Only actual same-origin page links count, not sitemap membership."""
    graph = {p.canonical: set() for p in pages.values() if p.canonical}
    by_path = {path.resolve(): page.canonical for path, page in pages.items()}
    for path, page in pages.items():
        if page.canonical not in graph:
            continue
        for href in page.hrefs:
            target = site_audit.parse_internal_target(path, href)
            if target:
                dest = by_path.get(target[0].resolve())
                if dest in graph and dest != page.canonical:
                    graph[page.canonical].add(dest)
    return graph


def orphan_pages(graph, start):
    seen, pending = set(), [start]
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        pending.extend(graph.get(node, set()) - seen)
    return set(graph) - seen


def validate_canonical_scope(pages):
    """Allow only the reviewed core, legal and Phase-5 authority routes."""
    discovered = {page.canonical for page in pages.values() if page.canonical}
    errors = []
    for url in sorted(discovered - ALLOWED_CANONICALS):
        errors.append(f"Unexpected canonical route in Phase 1-3 scope: {url}")
    for url in sorted(ALLOWED_CANONICALS - discovered):
        errors.append(f"Missing canonical route in Phase 1-3 scope: {url}")
    return errors


def validate_structure(page, source):
    errors = []
    parser = StructureParser()
    parser.feed(source)
    previous = 0
    for level in parser.headings:
        if level > previous + 1:
            errors.append(f"{page.path}: skipped heading level h{previous} -> h{level}")
        previous = level
    for image in parser.images:
        for dimension in ("width", "height"):
            value = image.get(dimension, "") or ""
            if not value.isdigit() or int(value) <= 0:
                errors.append(f"{page.path}: missing positive image {dimension}: {image.get('src')}")
    for name in ("robots", "googlebot", "bingbot"):
        directives = page.metadata.get(name, "").lower().replace(",", " ").split()
        if {"noindex", "none"} & set(directives):
            errors.append(f"{page.path}: canonical page excluded from indexing by {name}")
    canonical = urlsplit(page.canonical or "")
    if (canonical.scheme, canonical.netloc) != ("https", "datenpflege-nord.de") or canonical.query or canonical.fragment:
        errors.append(f"{page.path}: canonical origin/query/fragment is invalid")
    return errors


def validate_homepage_proof(source):
    """Reject template proof and unlabelled static GitHub totals."""
    errors = []
    for marker in ('brand-belt', '/images/clients-logo/', 'mainframe-hero', 'mainframe-poster'):
        if marker in source:
            errors.append(f"Homepage contains unverified template proof: {marker}")
    if re.search(r'<strong\s+data-stat="[^"]+">\s*\d+\s*</strong>', source):
        errors.append("Homepage contains an unsupported static GitHub total")
    return errors


def validate_service_schema(page):
    errors, nodes = [], []
    for block in page.jsonld_blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            errors.append(f"{page.path}: invalid JSON-LD")
            continue
        if not isinstance(data, dict):
            errors.append(f"{page.path}: expected a schema object")
            continue
        nodes.extend(data.get("@graph", [data]))
    for kind in ("Organization", "WebPage", "Service", "BreadcrumbList"):
        if sum(isinstance(n, dict) and n.get("@type") == kind for n in nodes) != 1:
            errors.append(f"{page.path}: expected one {kind}")
    if errors:
        return errors
    types = {n["@type"]: n for n in nodes if isinstance(n, dict) and isinstance(n.get("@type"), str)}
    org, web, service, breadcrumb = (types[t] for t in ("Organization", "WebPage", "Service", "BreadcrumbList"))
    origin = site_audit.ORIGIN + "/"
    canonical = page.canonical
    expected_org = origin + "#organization"
    checks = {
        "legal organization identity": org.get("name") == "Green Vector Energo GmbH" and org.get("@id") == expected_org,
        "organization URL": org.get("url") == origin,
        "WebPage metadata parity": web.get("name") == page.title and web.get("description") == page.description,
        "WebPage identity": web.get("url") == canonical and web.get("@id") == canonical + "#webpage",
        "WebSite relationship": web.get("isPartOf") == {"@id": origin + "#website"},
        "breadcrumb relationship": web.get("breadcrumb") == {"@id": canonical + "#breadcrumb"},
        "service relationship": web.get("about") == {"@id": canonical + "#service"},
        "service identity": service.get("url") == canonical and service.get("@id") == canonical + "#service",
        "service provider": service.get("provider") == {"@id": expected_org},
        "verified service area": service.get("areaServed") == ["Lübeck", "Schleswig-Holstein"],
        "breadcrumb identity": breadcrumb.get("@id") == canonical + "#breadcrumb",
    }
    items = breadcrumb.get("itemListElement", [])
    checks["breadcrumb trail"] = isinstance(items, list) and len(items) == 2 and all(isinstance(x, dict) for x in items) and [x.get("position") for x in items] == [1, 2] and [x.get("item") for x in items] == [origin, canonical]
    for label, passed in checks.items():
        if not passed:
            errors.append(f"{page.path}: {label} mismatch")
    # Explicit expansion gates for this release; future changes need reviewed evidence.
    for node in nodes:
        if isinstance(node, dict) and (node.get("@type") in ("FAQPage", "LocalBusiness", "Review", "AggregateRating") or "aggregateRating" in node or "review" in node):
            errors.append(f"{page.path}: gated schema expansion")
    return errors


def validate_authority_schema(page):
    errors, nodes = [], []
    for block in page.jsonld_blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            return [f"{page.path}: invalid JSON-LD"]
        if not isinstance(data, dict):
            return [f"{page.path}: expected a schema object"]
        nodes.extend(data.get("@graph", [data]))
    for kind in ("Organization", "WebPage", "TechArticle", "BreadcrumbList"):
        if sum(isinstance(n, dict) and n.get("@type") == kind for n in nodes) != 1:
            errors.append(f"{page.path}: expected one {kind}")
    if errors:
        return errors
    types = {n["@type"]: n for n in nodes if isinstance(n, dict) and isinstance(n.get("@type"), str)}
    org, web, article, breadcrumb = (
        types[t] for t in ("Organization", "WebPage", "TechArticle", "BreadcrumbList")
    )
    canonical = page.canonical
    origin = site_audit.ORIGIN + "/"
    article_id = canonical + "#article"
    checks = {
        "legal organization identity": org.get("name") == "Green Vector Energo GmbH" and org.get("alternateName") == "DatenpflegeNord" and org.get("@id") == origin + "#organization",
        "WebPage metadata parity": web.get("name") == page.title and web.get("description") == page.description,
        "WebPage identity": web.get("url") == canonical and web.get("@id") == canonical + "#webpage",
        "article relationship": web.get("mainEntity") == {"@id": article_id},
        "article identity": article.get("@id") == article_id and article.get("mainEntityOfPage") == {"@id": canonical + "#webpage"},
        "article author": article.get("author") == {"@type": "Person", "name": "Dustin Zander", "url": origin + "#profil"},
        "article publisher": article.get("publisher") == {"@id": origin + "#organization"},
        "article language": article.get("inLanguage") == "de-DE",
        "breadcrumb relationship": web.get("breadcrumb") == {"@id": canonical + "#breadcrumb"},
        "breadcrumb identity": breadcrumb.get("@id") == canonical + "#breadcrumb",
    }
    items = breadcrumb.get("itemListElement", [])
    checks["breadcrumb trail"] = (
        isinstance(items, list)
        and len(items) == 2
        and [item.get("position") for item in items] == [1, 2]
        and [item.get("item") for item in items] == [origin, canonical]
    )
    for label, passed in checks.items():
        if not passed:
            errors.append(f"{page.path}: {label} mismatch")
    for node in nodes:
        if isinstance(node, dict) and (
            node.get("@type") in ("FAQPage", "LocalBusiness", "Review", "AggregateRating")
            or "aggregateRating" in node
            or "review" in node
        ):
            errors.append(f"{page.path}: gated schema expansion")
    return errors


def validate_authority_content(page, source):
    errors = []
    canonical = page.canonical or ""
    owner = AUTHORITY_OWNERS.get(canonical)
    if owner and owner.removeprefix(site_audit.ORIGIN) not in page.hrefs:
        errors.append(f"{page.path}: authority page does not link to its commercial owner")
    forbidden = ("NordWerk Digital GmbH", "FAQPage", "AggregateRating")
    for marker in forbidden:
        if marker in source:
            errors.append(f"{page.path}: gated authority claim/schema: {marker}")
    if canonical.endswith("/individualsoftware-kosten/"):
        if re.search(r"\b\d{2,}(?:[.,]\d+)?\s*(?:€|Euro)\b", source, re.I):
            errors.append(f"{page.path}: unsupported numeric price claim")
        for required in ("data-scope-check", "Make-or-Buy", "Keine Preisautomatik"):
            if required not in source:
                errors.append(f"{page.path}: missing decision feature: {required}")
    if canonical.endswith("/website-relaunch-checkliste/"):
        for required in ("data-relaunch-checklist", "KEEP", "REDIRECT", "Fortschritt nur lokal gespeichert"):
            if required not in source:
                errors.append(f"{page.path}: missing relaunch feature: {required}")
    return errors


def main():
    pages = site_audit.parse_pages()
    graph = link_graph(pages)
    errors = validate_canonical_scope(pages)
    errors.extend(f"Orphan canonical page: {url}" for url in sorted(orphan_pages(graph, site_audit.ORIGIN + "/")))
    for path, page in pages.items():
        source = path.read_text(encoding="utf-8")
        errors.extend(validate_structure(page, source))
        if page.canonical in {site_audit.ORIGIN + "/", site_audit.ORIGIN + "/en/"}:
            errors.extend(validate_homepage_proof(source))
        if path.parent.name in {"softwareentwicklung-luebeck", "webentwicklung-luebeck", "ki-automatisierung-luebeck"}:
            errors.extend(validate_service_schema(page))
        if page.canonical in AUTHORITY_OWNERS:
            errors.extend(validate_authority_schema(page))
            errors.extend(validate_authority_content(page, source))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Golden audit passed: {len(pages)} reachable canonical pages; structure/indexability, three service graphs and two authority graphs checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
