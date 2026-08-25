from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "site_audit.py"
SPEC = importlib.util.spec_from_file_location("site_audit", MODULE_PATH)
assert SPEC and SPEC.loader
site_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = site_audit
SPEC.loader.exec_module(site_audit)


class SiteAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.old_root = site_audit.ROOT
        site_audit.ROOT = self.root
        (self.root / "assets").mkdir()
        (self.root / "assets/site.css").write_text("body { color: #111; }\n")
        (self.root / "og.png").write_bytes(b"png")

    def tearDown(self) -> None:
        site_audit.ROOT = self.old_root
        self.temp_dir.cleanup()

    def page_html(
        self,
        canonical: str,
        *,
        body: str = "<main><section><h1>Title</h1></section></main>",
        alternates: str = "",
    ) -> str:
        return f"""<!doctype html><html lang="de-DE"><head>
<title>{canonical}</title><meta name="description" content="Description">
<link rel="canonical" href="{canonical}">{alternates}
<link rel="stylesheet" href="/assets/site.css">
<meta property="og:title" content="Title"><meta property="og:description" content="Description">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://datenpflege-nord.de/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Title">
<meta name="twitter:description" content="Description">
<meta name="twitter:image" content="https://datenpflege-nord.de/og.png">
</head><body>{body}</body></html>"""

    def write_page(self, route: str, html: str) -> None:
        path = self.root / route / "index.html" if route else self.root / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)

    def errors(self) -> list[str]:
        return site_audit.validate_pages(site_audit.parse_pages())

    def test_positive_minimal_page(self) -> None:
        self.write_page("", self.page_html("https://datenpflege-nord.de/"))
        self.assertEqual([], self.errors())

    def test_detects_lazy_srcset_and_css_resources(self) -> None:
        (self.root / "assets/site.css").write_text(".x { background:url(missing.svg); }\n")
        body = """<main><section><h1>Title</h1>
<img alt="" src="/og.png" srcset="/og.png 1x, /missing-2x.png 2x">
<video poster="/og.png"><source data-src="/missing.mp4"></video>
</section></main>"""
        self.write_page("", self.page_html("https://datenpflege-nord.de/", body=body))
        errors = "\n".join(self.errors())
        self.assertIn("missing local img srcset resource", errors)
        self.assertIn("missing local source data-src resource", errors)
        self.assertIn("missing CSS resource", errors)

    def test_detects_csp_unsafe_html_and_reduced_motion_gap(self) -> None:
        (self.root / "assets/site.css").write_text("a { transition: color .2s; }\n")
        body = """<main><section><h1>Title</h1>
<p style="color:red" onclick="alert(1)">Unsafe</p><script>alert(1)</script>
</section></main>"""
        self.write_page("", self.page_html("https://datenpflege-nord.de/", body=body))
        errors = "\n".join(self.errors())
        self.assertIn("executable inline script", errors)
        self.assertIn("inline style attribute", errors)
        self.assertIn("inline event handler", errors)
        self.assertIn("prefers-reduced-motion", errors)

    def test_detects_hreflang_and_de_en_structure_drift(self) -> None:
        alternates = """
<link rel="alternate" hreflang="de-DE" href="https://datenpflege-nord.de/">
<link rel="alternate" hreflang="en" href="https://datenpflege-nord.de/en/">
<link rel="alternate" hreflang="x-default" href="https://datenpflege-nord.de/">"""
        self.write_page("", self.page_html("https://datenpflege-nord.de/", alternates=alternates))
        self.write_page(
            "en",
            self.page_html(
                "https://datenpflege-nord.de/en/",
                body="<main><section><h1>Title</h1></section><section></section></main>",
                alternates=alternates,
            ).replace('lang="de-DE"', 'lang="en"', 1),
        )
        self.assertIn("DE/EN semantic structure differs", "\n".join(self.errors()))

    def test_detects_missing_expected_script(self) -> None:
        self.write_page("", self.page_html("https://datenpflege-nord.de/"))
        errors = site_audit.validate_expected_scripts(site_audit.parse_pages())
        self.assertIn("missing expected script '/assets/home-de.js'", "\n".join(errors))

        html = self.page_html("https://datenpflege-nord.de/").replace(
            "</body>", '<script src="/assets/home-de.js" defer></script></body>'
        )
        self.write_page("", html)
        self.assertEqual(
            [], site_audit.validate_expected_scripts(site_audit.parse_pages())
        )


if __name__ == "__main__":
    unittest.main()
