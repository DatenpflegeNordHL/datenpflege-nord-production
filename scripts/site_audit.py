#!/usr/bin/env python3
"""Dependency-free static checks for the DatenpflegeNord production site.

The goal is to catch structural regressions before a pull request reaches main.
It intentionally avoids subjective SEO scoring and checks only deterministic facts.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ORIGIN = "https://datenpflege-nord.de"
ROOT = Path(__file__).resolve().parents[1]
SOCIAL_META_REQUIRED = {
    "og:title",
    "og:description",
    "og:type",
    "og:url",
    "og:image",
    "twitter:card",
    "twitter:title",
    "twitter:description",
    "twitter:image",
}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
EXPECTED_SCRIPTS = {
    Path("index.html"): "/assets/home-de.js",
    Path("en/index.html"): "/assets/home-en.js",
    Path("webentwicklung-luebeck/index.html"): "/assets/service.js",
    Path("softwareentwicklung-luebeck/index.html"): "/assets/service.js",
    Path("ki-automatisierung-luebeck/index.html"): "/assets/service.js",
    Path("wissen/individualsoftware-kosten/index.html"): "/assets/authority.js",
    Path("wissen/website-relaunch-checkliste/index.html"): "/assets/authority.js",
}


@dataclass
class Page:
    path: Path
    lang: str | None = None
    title: str = ""
    description: str | None = None
    description_count: int = 0
    canonical: str | None = None
    canonical_count: int = 0
    h1_count: int = 0
    ids: set[str] = field(default_factory=set)
    duplicate_ids: set[str] = field(default_factory=set)
    hrefs: list[str] = field(default_factory=list)
    resources: list[tuple[str, str]] = field(default_factory=list)
    jsonld_blocks: list[str] = field(default_factory=list)
    labels_for: set[str] = field(default_factory=set)
    controls: list[tuple[str, str, dict[str, str]]] = field(default_factory=list)
    images_missing_alt: list[str] = field(default_factory=list)
    unsafe_blank_links: list[str] = field(default_factory=list)
    alternates: dict[str, str] = field(default_factory=dict)
    duplicate_hreflangs: set[str] = field(default_factory=set)
    metadata: dict[str, str] = field(default_factory=dict)
    semantic_structure: list[tuple[str, str]] = field(default_factory=list)
    inline_script_count: int = 0
    inline_styles: list[str] = field(default_factory=list)
    event_handlers: list[str] = field(default_factory=list)


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

        if "style" in a:
            self.page.inline_styles.append(tag)
        for name in a:
            if name.startswith("on"):
                self.page.event_handlers.append(f"{tag}[{name}]")

        element_id = a.get("id")
        if element_id:
            if element_id in self.page.ids:
                self.page.duplicate_ids.add(element_id)
            self.page.ids.add(element_id)

        if tag in {"header", "nav", "main", "section", "form", "footer"}:
            self.page.semantic_structure.append((tag, a.get("id", "")))

        if tag == "html":
            self.page.lang = a.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.page.h1_count += 1
        elif tag == "meta":
            key = (a.get("property") or a.get("name") or "").strip().lower()
            content = a.get("content", "").strip()
            if key:
                self.page.metadata[key] = content
            if key == "description":
                self.page.description_count += 1
                self.page.description = content or None
        elif tag == "link":
            rel_tokens = {token.lower() for token in a.get("rel", "").split()}
            href = a.get("href", "").strip()
            if "canonical" in rel_tokens:
                self.page.canonical_count += 1
                self.page.canonical = href or None
            if "alternate" in rel_tokens and a.get("hreflang", "").strip():
                hreflang = a["hreflang"].strip().lower()
                if hreflang in self.page.alternates:
                    self.page.duplicate_hreflangs.add(hreflang)
                self.page.alternates[hreflang] = href
            if href and rel_tokens.intersection(
                {"stylesheet", "icon", "apple-touch-icon", "preload", "modulepreload"}
            ):
                self.page.resources.append(("link", href))
        elif tag == "a":
            href = a.get("href", "").strip()
            if href:
                self.page.hrefs.append(href)
            if a.get("target", "").lower() == "_blank":
                rel_tokens = {token.lower() for token in a.get("rel", "").split()}
                if "noopener" not in rel_tokens:
                    self.page.unsafe_blank_links.append(href or "<empty href>")
        elif tag == "img":
            src = a.get("src", "").strip()
            if "alt" not in a:
                self.page.images_missing_alt.append(src or "<unknown src>")
            if src:
                self.page.resources.append(("img", src))
            self._add_lazy_and_srcset_resources(tag, a)
        elif tag == "script":
            src = a.get("src", "").strip()
            if src:
                self.page.resources.append(("script", src))
            script_type = a.get("type", "").lower()
            if not src and script_type != "application/ld+json":
                self.page.inline_script_count += 1
            if script_type == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_parts = []
        elif tag == "source":
            src = a.get("src", "").strip()
            if src:
                self.page.resources.append(("source", src))
            self._add_lazy_and_srcset_resources(tag, a)
        elif tag == "video":
            poster = a.get("poster", "").strip()
            if poster:
                self.page.resources.append(("poster", poster))
        elif tag == "label":
            target = a.get("for", "").strip()
            if target:
                self.page.labels_for.add(target)
        elif tag in {"input", "select", "textarea"}:
            if tag == "input" and a.get("type", "text").lower() in {
                "hidden", "submit", "button", "reset", "image"
            }:
                return
            control_id = a.get("id", "").strip()
            self.page.controls.append((tag, control_id, a))

    def _add_lazy_and_srcset_resources(self, tag: str, attrs: dict[str, str]) -> None:
        data_src = attrs.get("data-src", "").strip()
        if data_src:
            self.page.resources.append((f"{tag} data-src", data_src))
        for attr in ("srcset", "data-srcset"):
            for candidate in attrs.get(attr, "").split(","):
                resource = candidate.strip().split(maxsplit=1)[0] if candidate.strip() else ""
                if resource:
                    self.page.resources.append((f"{tag} {attr}", resource))

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
    if href.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:")):
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


def stylesheet_texts(page: Page) -> list[tuple[Path, str]]:
    stylesheets: list[tuple[Path, str]] = []
    for kind, resource in page.resources:
        if kind != "link" or not urlparse(resource).path.lower().endswith(".css"):
            continue
        target_info = parse_internal_target(page.path, resource)
        if target_info is None:
            continue
        target, _ = target_info
        if target.is_file():
            stylesheets.append((target, target.read_text(encoding="utf-8")))
    return stylesheets


def display_target(target: Path) -> str:
    return str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target)


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
            errors.append(
                f"{prefix}: duplicate title also used by "
                f"{titles[page.title].relative_to(ROOT)}"
            )
        else:
            titles[page.title] = path

        if page.description_count != 1:
            errors.append(
                f"{prefix}: expected exactly one meta description, "
                f"found {page.description_count}"
            )
        elif not page.description:
            errors.append(f"{prefix}: meta description is empty")

        if page.h1_count != 1:
            errors.append(f"{prefix}: expected exactly one <h1>, found {page.h1_count}")
        if page.duplicate_ids:
            errors.append(f"{prefix}: duplicate id(s): {', '.join(sorted(page.duplicate_ids))}")
        if page.images_missing_alt:
            errors.append(
                f"{prefix}: image(s) missing alt attribute: "
                f"{', '.join(page.images_missing_alt)}"
            )
        if page.unsafe_blank_links:
            errors.append(
                f"{prefix}: target=_blank link(s) missing rel=noopener: "
                f"{', '.join(page.unsafe_blank_links)}"
            )
        if page.inline_script_count:
            errors.append(
                f"{prefix}: executable inline script(s) are forbidden by project CSP policy: "
                f"{page.inline_script_count}"
            )
        if page.inline_styles:
            errors.append(
                f"{prefix}: inline style attribute(s) are forbidden by project CSP policy: "
                f"{', '.join(page.inline_styles)}"
            )
        if page.event_handlers:
            errors.append(
                f"{prefix}: inline event handler(s) are forbidden: "
                f"{', '.join(page.event_handlers)}"
            )

        missing_social = sorted(
            key for key in SOCIAL_META_REQUIRED if not page.metadata.get(key, "").strip()
        )
        if missing_social:
            errors.append(f"{prefix}: missing social metadata: {', '.join(missing_social)}")

        if page.canonical_count != 1:
            errors.append(
                f"{prefix}: expected exactly one canonical link, "
                f"found {page.canonical_count}"
            )
        elif not page.canonical:
            errors.append(f"{prefix}: canonical link is empty")
        else:
            parsed = urlparse(page.canonical)
            if f"{parsed.scheme}://{parsed.netloc}" != ORIGIN:
                errors.append(f"{prefix}: canonical is not on {ORIGIN}: {page.canonical}")
            if page.canonical in canonicals:
                errors.append(
                    f"{prefix}: canonical duplicates "
                    f"{canonicals[page.canonical].relative_to(ROOT)}"
                )
            else:
                canonicals[page.canonical] = path
            if page.metadata.get("og:url") and page.metadata["og:url"] != page.canonical:
                errors.append(
                    f"{prefix}: og:url must equal canonical URL: {page.metadata['og:url']}"
                )

        if page.duplicate_hreflangs:
            errors.append(
                f"{prefix}: duplicate hreflang value(s): "
                f"{', '.join(sorted(page.duplicate_hreflangs))}"
            )
        if page.alternates and "x-default" not in page.alternates:
            errors.append(f"{prefix}: hreflang set is missing x-default")

        for tag, control_id, attrs in page.controls:
            aria_name = bool(attrs.get("aria-label", "").strip()) or bool(
                attrs.get("aria-labelledby", "").strip()
            )
            if not control_id and not aria_name:
                errors.append(
                    f"{prefix}: {tag} has no id and no explicit accessible name; "
                    "project policy requires an id+label or ARIA name"
                )
                continue
            has_name = aria_name or (control_id in page.labels_for)
            if not has_name:
                errors.append(
                    f"{prefix}: {tag}#{control_id} has no associated label "
                    "or accessible name"
                )

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
            if href.startswith("http://") or href.startswith("//"):
                errors.append(f"{prefix}: insecure URL in link: {href}")
            target_info = parse_internal_target(path, href)
            if target_info is None:
                continue
            target, fragment = target_info
            target = target.resolve()
            if not target.exists():
                errors.append(
                    f"{prefix}: broken internal link {href!r} -> {display_target(target)}"
                )
                continue
            if fragment and target.suffix.lower() == ".html":
                target_page = pages.get(target)
                if target_page is not None and fragment not in target_page.ids:
                    errors.append(
                        f"{prefix}: link {href!r} points to missing fragment #{fragment}"
                    )

        for kind, resource in page.resources:
            if resource.startswith("http://") or resource.startswith("//"):
                errors.append(f"{prefix}: insecure {kind} resource URL: {resource}")
            target_info = parse_internal_target(path, resource)
            if target_info is None:
                continue
            target, _ = target_info
            target = target.resolve()
            if not target.exists():
                errors.append(
                    f"{prefix}: missing local {kind} resource {resource!r} -> "
                    f"{display_target(target)}"
                )

        css_texts = stylesheet_texts(page)
        combined_css = "\n".join(text for _, text in css_texts)
        if re.search(r"\b(?:animation(?:-name)?|transition)\s*:", combined_css, re.I):
            if not re.search(
                r"prefers-reduced-motion\s*:\s*reduce", combined_css, re.IGNORECASE
            ):
                errors.append(
                    f"{prefix}: animated styles must define prefers-reduced-motion: reduce"
                )
        for css_path, css_text in css_texts:
            for match in CSS_URL.finditer(css_text):
                resource = match.group(2).strip()
                if not resource or resource.startswith(("data:", "#")):
                    continue
                if resource.startswith("http://") or resource.startswith("//"):
                    errors.append(
                        f"{prefix}: insecure CSS resource in {css_path.relative_to(ROOT)}: "
                        f"{resource}"
                    )
                    continue
                target_info = parse_internal_target(css_path, resource)
                if target_info is not None and not target_info[0].resolve().exists():
                    errors.append(
                        f"{prefix}: missing CSS resource {resource!r} referenced by "
                        f"{css_path.relative_to(ROOT)}"
                    )

        for key in ("og:image", "twitter:image"):
            resource = page.metadata.get(key, "")
            if resource:
                target_info = parse_internal_target(path, resource)
                if target_info is not None and not target_info[0].resolve().exists():
                    errors.append(f"{prefix}: {key} references missing resource: {resource}")

    hreflang_pages = [page for page in pages.values() if page.alternates]
    if hreflang_pages:
        reference = hreflang_pages[0].alternates
        for page in hreflang_pages:
            prefix = str(page.path.relative_to(ROOT))
            if page.alternates != reference:
                errors.append(f"{prefix}: hreflang mapping differs from the reciprocal set")
            for language, target_url in page.alternates.items():
                target_info = parse_internal_target(page.path, target_url)
                if target_info is None or target_info[0].resolve() not in pages:
                    errors.append(
                        f"{prefix}: hreflang {language!r} does not target a canonical page: "
                        f"{target_url}"
                    )

    by_canonical = {page.canonical: page for page in pages.values() if page.canonical}
    de_home = by_canonical.get(f"{ORIGIN}/")
    en_home = by_canonical.get(f"{ORIGIN}/en/")
    if de_home and en_home and de_home.semantic_structure != en_home.semantic_structure:
        errors.append("index.html and en/index.html: DE/EN semantic structure differs")

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


def validate_expected_scripts(pages: dict[Path, Page]) -> list[str]:
    errors: list[str] = []
    for relative_path, expected_script in EXPECTED_SCRIPTS.items():
        page = pages.get((ROOT / relative_path).resolve())
        if page is None:
            continue
        scripts = {urlparse(resource).path for kind, resource in page.resources if kind == "script"}
        if expected_script not in scripts:
            errors.append(
                f"{relative_path}: missing expected script {expected_script!r}"
            )
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

    errors: list[str] = []
    errors.extend(validate_pages(pages))
    errors.extend(validate_expected_scripts(pages))
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
