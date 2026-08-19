#!/usr/bin/env python3
"""Dependency-free static checks for the DatenpflegeNord production site.

The goal is to catch structural regressions before a pull request reaches main.
It intentionally avoids subjective SEO scoring and checks only deterministic facts.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ORIGIN = "https://datenpflege-nord.de"
ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Page:
    path: Path
    lang: str | None = None
    title: str = ""
    description: str | None = None
    canonical: str | None = None
    h1_count: int = 0
    ids: set[str] = field(default_factory=set)
    duplicate_ids: set[str] = field(default_factory=set)
    hrefs: list[str] = field(default_factory=list)
    jsonld_blocks: list[str] = field(default_factory=list)
    labels_for: set[str] = field(default_factory=set)
    controls: list[tuple[str, str, dict[str, str]]] = field(default_factory=list)
    images_missing_alt: list[str] = field(default_factory=list)
    unsafe_blank_links: list[str] = field(default_factory=list)


class SiteHTMLParser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.page = Page(path=path)
        self._in_title = False
        self._title_parts: list[str] = []
        self._in_jsonld = False
        self._jsonld_parts: list[str] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k.lower(): (v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        a = self._attrs(attrs)

        element_id = a.get("id")
        if element_id:
            if element_id in self.page.ids:
                self.page.duplicate_ids.add(element_id)
            self.page.ids.add(element_id)

        if tag == "html":
            self.page.lang = a.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.page.h1_count += 1
        elif tag == "meta" and a.get("name", "").lower() == "description":
            self.page.description = a.get("content", "").strip() or None
        elif tag == "link":
            rel_tokens = {token.lower() for token in a.get("rel", "").split()}
            if "canonical" in rel_tokens:
                self.page.canonical = a.get("href", "").strip() or None
        elif tag == "a":
            href = a.get("href", "").strip()
            if href:
                self.page.hrefs.append(href)
            if a.get("target", "").lower() == "_blank":
                rel_tokens = {token.lower() for token in a.get("rel", "").split()}
                if "noopener" not in rel_tokens:
                    self.page.unsafe_blank_links.append(href or "<empty href>")
        elif tag == "img":
            if "alt" not in a:
                self.page.images_missing_alt.append(a.get("src", "<unknown src>"))
        elif tag == "label":
            target = a.get("for", "").strip()
            if target:
                self.page.labels_for.add(target)
        elif tag in {"input", "select", "textarea"}:
            if tag == "input" and a.get("type", "text").lower() in {"hidden", "submit", "button", "reset", "image"}:
                return
            control_id = a.get("id", "").strip()
            if control_id:
                self.page.controls.append((tag, control_id, a))
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            self.page.title = "".join(self._title_parts).strip()
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.page.jsonld_blocks.append("".join(self._jsonld_parts).strip())
            self._jsonld_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._in_jsonld:
            self._jsonld_parts.append(data)


def route_to_file(path: str) -> Path:
    if not path or path == "/":
        return ROOT / "index.html"
    clean = path.lstrip("/")
    if path.endswith("/"):
        return ROOT / clean / "index.html"
    return ROOT / clean


def parse_internal_target(current: Path, href: str) -> tuple[Path, str] | None:
    if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
            return None
        return route_to_file(parsed.path), parsed.fragment

    if parsed.scheme or parsed.netloc:
        return None

    if parsed.path.startswith("/"):
        return route_to_file(parsed.path), parsed.fragment

    if not parsed.path:
        return current, parsed.fragment

    target = (current.parent / parsed.path).resolve()
    if parsed.path.endswith("/"):
        target = target / "index.html"
    return target, parsed.fragment


def parse_pages() -> dict[Path, Page]:
    pages: dict[Path, Page] = {}
    for path in sorted(ROOT.rglob("index.html")):
        if ".git" in path.parts:
            continue
        parser = SiteHTMLParser(path)
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        pages[path.resolve()] = parser.page
    return pages


def validate_pages(pages: dict[Path, Page]) -> list[str]:
    errors: list[str] = []
    titles: dict[str, Path] = {}
    canonicals: dict[str, Path] = {}

    for path, page in pages.items():
        rel = path.relative_to(ROOT)
        prefix = str(rel)

        if not page.lang:
            errors.append(f"{prefix}: <html> has no lang attribute")
        if not page.title:
            errors.append(f"{prefix}: missing <title>")
        elif page.title in titles:
            errors.append(f"{prefix}: duplicate title also used by {titles[page.title].relative_to(ROOT)}")
        else:
            titles[page.title] = path
        if not page.description:
            errors.append(f"{prefix}: missing meta description")
        if page.h1_count != 1:
            errors.append(f"{prefix}: expected exactly one <h1>, found {page.h1_count}")
        if page.duplicate_ids:
            errors.append(f"{prefix}: duplicate id(s): {', '.join(sorted(page.duplicate_ids))}")
        if page.images_missing_alt:
            errors.append(f"{prefix}: image(s) missing alt attribute: {', '.join(page.images_missing_alt)}")
        if page.unsafe_blank_links:
            errors.append(f"{prefix}: target=_blank link(s) missing rel=noopener: {', '.join(page.unsafe_blank_links)}")

        if not page.canonical:
            errors.append(f"{prefix}: missing canonical link")
        else:
            parsed = urlparse(page.canonical)
            if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
                errors.append(f"{prefix}: canonical is not on {ORIGIN}: {page.canonical}")
            if page.canonical in canonicals:
                errors.append(f"{prefix}: canonical duplicates {canonicals[page.canonical].relative_to(ROOT)}")
            else:
                canonicals[page.canonical] = path

        for tag, control_id, attrs in page.controls:
            has_name = (
                control_id in page.labels_for
                or bool(attrs.get("aria-label", "").strip())
                or bool(attrs.get("aria-labelledby", "").strip())
            )
            if not has_name:
                errors.append(f"{prefix}: {tag}#{control_id} has no associated label or accessible name")

        for index, block in enumerate(page.jsonld_blocks, start=1):
            if not block:
                errors.append(f"{prefix}: empty JSON-LD block #{index}")
                continue
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{prefix}: invalid JSON-LD block #{index}: {exc}")

    for path, page in pages.items():
        prefix = str(path.relative_to(ROOT))
        for href in page.hrefs:
            target_info = parse_internal_target(path, href)
            if target_info is None:
                continue
            target, fragment = target_info
            target = target.resolve()
            if not target.exists():
                errors.append(f"{prefix}: broken internal link {href!r} -> {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_page = pages.get(target)
                if target_page is not None and fragment not in target_page.ids:
                    errors.append(f"{prefix}: link {href!r} points to missing fragment #{fragment}")

    return errors


def validate_sitemap(pages: dict[Path, Page]) -> list[str]:
    errors: list[str] = []
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return ["sitemap.xml: missing"]

    try:
        tree = ET.parse(sitemap)
    except ET.ParseError as exc:
        return [f"sitemap.xml: invalid XML: {exc}"]

    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [
        (node.text or "").strip()
        for node in tree.findall(".//sm:loc", ns)
        if (node.text or "").strip()
    ]
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml: duplicate <loc> entries")

    sitemap_set = set(locs)
    canonical_set = {page.canonical for page in pages.values() if page.canonical}

    missing = sorted(canonical_set - sitemap_set)
    extra = sorted(sitemap_set - canonical_set)
    for url in missing:
        errors.append(f"sitemap.xml: canonical page missing from sitemap: {url}")
    for url in extra:
        errors.append(f"sitemap.xml: URL has no matching canonical HTML page: {url}")

    for url in locs:
        parsed = urlparse(url)
        if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
            errors.append(f"sitemap.xml: external or unexpected origin: {url}")
            continue
        target = route_to_file(parsed.path)
        if not target.exists():
            errors.append(f"sitemap.xml: URL does not map to a repository file: {url}")

    return errors


def validate_robots() -> list[str]:
    robots = ROOT / "robots.txt"
    if not robots.exists():
        return ["robots.txt: missing"]
    text = robots.read_text(encoding="utf-8")
    expected = f"Sitemap: {ORIGIN}/sitemap.xml"
    if expected not in text:
        return [f"robots.txt: missing exact sitemap directive {expected!r}"]
    return []


def main() -> int:
    pages = parse_pages()
    if not pages:
        print("ERROR: no index.html files found", file=sys.stderr)
        return 1

    errors = []
    errors.extend(validate_pages(pages))
    errors.extend(validate_sitemap(pages))
    errors.extend(validate_robots())

    if errors:
        print(f"Static site audit failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Static site audit passed: {len(pages)} HTML pages checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
