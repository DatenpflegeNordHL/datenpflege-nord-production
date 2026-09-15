"""Negative cases for release-relevant checks, not keyword/copy snapshots."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import golden_audit as audit
from site_audit import SiteHTMLParser


class GoldenAuditTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        path = self.root / "softwareentwicklung-luebeck/index.html"
        parser = SiteHTMLParser(path)
        self.source = path.read_text()
        parser.feed(self.source)
        self.page = parser.page

    def mutate_schema(self, kind, key, value):
        page = copy.deepcopy(self.page)
        graph = json.loads(page.jsonld_blocks[0])
        next(n for n in graph["@graph"] if n["@type"] == kind)[key] = value
        page.jsonld_blocks = [json.dumps(graph)]
        return audit.validate_service_schema(page)

    def test_disconnected_cycle_is_orphaned(self):
        graph = {"home": {"service"}, "service": {"home"}, "a": {"b"}, "b": {"a"}}
        self.assertEqual(audit.orphan_pages(graph, "home"), {"a", "b"})

    def test_phase_scope_rejects_added_or_missing_canonical(self):
        pages = audit.site_audit.parse_pages()
        self.assertEqual(audit.validate_canonical_scope(pages), [])

        extra = copy.deepcopy(self.page)
        extra.canonical = "https://datenpflege-nord.de/webdesign-luebeck/"
        pages[self.root / "webdesign-luebeck/index.html"] = extra
        self.assertTrue(any("Unexpected canonical" in e for e in audit.validate_canonical_scope(pages)))

        pages = {
            path: page
            for path, page in audit.site_audit.parse_pages().items()
            if page.canonical != "https://datenpflege-nord.de/en/"
        }
        self.assertTrue(any("Missing canonical" in e for e in audit.validate_canonical_scope(pages)))

    def test_current_service_graph_passes(self):
        self.assertEqual(audit.validate_service_schema(self.page), [])

    def test_metadata_drift_is_rejected(self):
        self.assertTrue(self.mutate_schema("WebPage", "description", "Unrelated service"))

    def test_wrong_provider_and_area_are_rejected(self):
        self.assertTrue(self.mutate_schema("Service", "provider", {"@id": "https://datenpflegenord.de/#organization"}))
        self.assertTrue(self.mutate_schema("Service", "areaServed", ["Hamburg"]))

    def test_unverified_legal_rename_is_rejected(self):
        self.assertTrue(self.mutate_schema("Organization", "name", "Unverified name"))

    def test_invalid_json_and_breadcrumb_are_rejected(self):
        self.assertTrue(self.mutate_schema("BreadcrumbList", "itemListElement", []))
        self.page.jsonld_blocks = ["{broken"]
        self.assertTrue(audit.validate_service_schema(self.page))

    def test_noindex_heading_skip_and_missing_dimensions(self):
        self.page.metadata["robots"] = "noindex,follow"
        errors = audit.validate_structure(self.page, '<h1>Page</h1><h3>Skip</h3><img src="x" alt="">')
        self.assertTrue(any("indexing" in e for e in errors))
        self.assertTrue(any("heading" in e for e in errors))
        self.assertTrue(any("width" in e for e in errors))
        self.assertTrue(any("height" in e for e in errors))

    def test_same_origin_links_only(self):
        home = self.root / "index.html"
        parser = SiteHTMLParser(home)
        parser.feed('<link rel="canonical" href="https://datenpflege-nord.de/"><a href="https://example.org/softwareentwicklung-luebeck/">External</a>')
        pages = {home: parser.page, self.page.path: self.page}
        self.assertEqual(audit.link_graph(pages)["https://datenpflege-nord.de/"], set())
        parser.page.hrefs.append("/softwareentwicklung-luebeck/#entscheidung")
        self.assertEqual(audit.link_graph(pages)["https://datenpflege-nord.de/"], {self.page.canonical})

    def test_homepage_proof_rejects_template_logos_and_static_totals(self):
        source = '<section class="brand-belt"><img src="/images/clients-logo/logo.svg"></section>'
        errors = audit.validate_homepage_proof(source)
        self.assertTrue(any("template proof" in error for error in errors))
        errors = audit.validate_homepage_proof('<strong data-stat="repos">17</strong>')
        self.assertTrue(any("static GitHub total" in error for error in errors))
        self.assertTrue(audit.validate_homepage_proof('<video src="/assets/hero/mainframe-hero.mp4">'))
        self.assertEqual(audit.validate_homepage_proof('<strong data-stat="repos">—</strong>'), [])

    def test_authority_pages_have_valid_schema_and_owner_links(self):
        for route in (
            "wissen/individualsoftware-kosten/index.html",
            "wissen/website-relaunch-checkliste/index.html",
        ):
            path = self.root / route
            parser = SiteHTMLParser(path)
            source = path.read_text()
            parser.feed(source)
            self.assertEqual([], audit.validate_authority_schema(parser.page))
            self.assertEqual([], audit.validate_authority_content(parser.page, source))

    def test_authority_schema_rejects_wrong_entity_and_author(self):
        path = self.root / "wissen/individualsoftware-kosten/index.html"
        parser = SiteHTMLParser(path)
        parser.feed(path.read_text())
        page = parser.page
        graph = json.loads(page.jsonld_blocks[0])
        next(node for node in graph["@graph"] if node["@type"] == "Organization")["name"] = "NordWerk Digital GmbH"
        next(node for node in graph["@graph"] if node["@type"] == "TechArticle")["author"]["name"] = "Certified Expert"
        page.jsonld_blocks = [json.dumps(graph)]
        errors = "\n".join(audit.validate_authority_schema(page))
        self.assertIn("legal organization identity", errors)
        self.assertIn("article author", errors)

    def test_authority_content_rejects_numeric_price_and_missing_owner(self):
        path = self.root / "wissen/individualsoftware-kosten/index.html"
        parser = SiteHTMLParser(path)
        source = '<div data-scope-check>Make-or-Buy Keine Preisautomatik 50.000 Euro</div>'
        parser.feed(source)
        parser.page.canonical = "https://datenpflege-nord.de/wissen/individualsoftware-kosten/"
        errors = "\n".join(audit.validate_authority_content(parser.page, source))
        self.assertIn("does not link", errors)
        self.assertIn("numeric price", errors)


if __name__ == "__main__":
    unittest.main()
