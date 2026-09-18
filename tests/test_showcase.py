import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "website-showcase" / "showcase-projects.json"
MANIFEST = ROOT / "docs" / "design-gallery" / "showcase-source-manifest.json"
CHECKSUMS = ROOT / "docs" / "design-gallery" / "showcase-public-media.sha256"
PAGE = ROOT / "website-showcase" / "index.html"


class ShowcaseCatalogueTests(unittest.TestCase):
    def test_public_catalogue_contains_only_approved_projects(self):
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        self.assertTrue(data["publicationPolicy"]["onlyApprovedProjectsArePublic"])
        self.assertEqual(data["summary"]["publicProjects"], 30)
        self.assertEqual(data["summary"]["realVideos"], 24)
        self.assertEqual(data["summary"]["templateDemos"], 6)
        self.assertEqual(len(data["projects"]), 30)
        for project in data["projects"]:
            self.assertTrue(project["approved"])
            self.assertEqual(project["status"], "approved")
            self.assertEqual(project["poster"]["type"], "image")
            self.assertTrue(project["poster"]["src"])
            self.assertFalse(project["indexable"])
            if project["video"]:
                self.assertEqual(urlparse(project["video"]["src"]).hostname, "media.datenpflege-nord.de")
                self.assertEqual(project["licenseStatus"], "MIT-reviewed")
            else:
                self.assertEqual(project["licenseStatus"], "owned")
                self.assertTrue(project["demo"].startswith("/website-showcase/demo/"))

    def test_private_manifest_is_the_release_gate(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["summary"]["legacyFound"], 546)
        self.assertEqual(data["summary"]["totalProjects"], 552)
        self.assertEqual(data["summary"]["approved"], 30)
        self.assertEqual(data["summary"]["review"], 199)
        self.assertEqual(data["summary"]["unknown"], 323)
        self.assertEqual(data["summary"]["rejected"], 0)
        self.assertEqual(sum(p["public"] for p in data["projects"]), 30)
        for project in data["projects"]:
            self.assertEqual(project["public"], project["rightsStatus"] == "approved")
            if project["public"] and project["video"]:
                self.assertEqual(len(project["poster"]["sha256"]), 64)
                self.assertEqual(len(project["video"]["sha256"]), 64)
                self.assertEqual(project["source"]["license"], "MIT")
            if project["rightsStatus"] != "approved":
                self.assertIsNone(project["poster"]["sha256"])
                self.assertIsNone(project["video"]["sha256"])

    def test_public_media_checksum_set_is_complete(self):
        lines = [line for line in CHECKSUMS.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(lines), 60)

    def test_template_demos_are_noindex_follow_and_outside_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        demos = [project["demo"] for project in data["projects"] if project["demo"]]
        self.assertEqual(len(demos), 6)
        for route in demos:
            page = ROOT / route.lstrip("/") / "index.html"
            self.assertTrue(page.is_file(), route)
            source = page.read_text(encoding="utf-8")
            self.assertIn('content="noindex,follow,noarchive"', source)
            self.assertNotIn(route, sitemap)
            self.assertNotIn("http://", source)
            self.assertNotIn("https://", source)

    def test_video_lifecycle_is_interaction_only_and_single_active(self):
        source = (ROOT / "assets" / "showcase.js").read_text(encoding="utf-8")
        page = PAGE.read_text(encoding="utf-8")
        self.assertIn('video.preload = "none"', source)
        self.assertIn("let activeCardVideo = null", source)
        self.assertIn("video.src = project.video.src", source)
        self.assertIn('preload="none"', page)
        self.assertNotIn("autoplay", page)


if __name__ == "__main__":
    unittest.main()
