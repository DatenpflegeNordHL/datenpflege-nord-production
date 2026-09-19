import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "website-showcase" / "showcase-projects.json"
MANIFEST = ROOT / "docs" / "design-gallery" / "showcase-source-manifest.json"
CHECKSUMS = ROOT / "docs" / "design-gallery" / "showcase-public-media.sha256"
SOURCE_ORDER = ROOT / "docs" / "design-gallery" / "claude-directory-current-order.json"
PAGE = ROOT / "website-showcase" / "index.html"


class ShowcaseCatalogueTests(unittest.TestCase):
    def test_public_catalogue_contains_exact_current_directory_plus_owned_demos(self):
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        self.assertTrue(data["publicationPolicy"]["currentUpstreamDirectoryIsLegacyGate"])
        self.assertTrue(data["publicationPolicy"]["rightsMetadataIsInformational"])
        self.assertEqual(data["publicationPolicy"]["mediaOrigin"], "https://media.datenpflege-nord.de/gallery-media")
        self.assertEqual(data["summary"]["publicProjects"], 377)
        self.assertEqual(data["summary"]["publicLegacyProjects"], 371)
        self.assertEqual(data["summary"]["publicShowcaseEntries"], 377)
        self.assertEqual(data["summary"]["realVideos"], 371)
        self.assertEqual(data["summary"]["templateDemos"], 6)
        self.assertEqual(len(data["projects"]), 377)
        legacy = [project for project in data["projects"] if project["sourceType"] == "legacy"]
        owned = [project for project in data["projects"] if project["sourceType"] == "owned"]
        self.assertEqual(len(legacy), 371)
        self.assertEqual(len(owned), 6)
        for project in data["projects"]:
            self.assertTrue(project["active"])
            self.assertEqual(project["publicationStatus"], "active")
            self.assertEqual(project["poster"]["type"], "image")
            self.assertTrue(project["poster"]["src"])
            self.assertFalse(project["indexable"])
            if project["video"]:
                self.assertTrue(project["video"]["src"].startswith("https://media.datenpflege-nord.de/gallery-media/"))
                self.assertEqual(urlparse(project["video"]["src"]).hostname, "media.datenpflege-nord.de")
                self.assertEqual(project["sourceType"], "legacy")
                self.assertEqual(project["publicLabel"], "Video-Preview")
                self.assertIn("rightsStatus", project)
                self.assertIn("riskFlags", project)
            else:
                self.assertEqual(project["licenseStatus"], "owned")
                self.assertEqual(project["sourceType"], "owned")
                self.assertEqual(project["publicLabel"], "DatenpflegeNord Demo")
                self.assertTrue(project["demo"].startswith("/website-showcase/demo/"))

    def test_public_catalogue_uses_explicit_current_source_order(self):
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        source = json.loads(SOURCE_ORDER.read_text(encoding="utf-8"))
        projects = data["projects"]
        self.assertEqual([p["displayOrder"] for p in projects], list(range(1, 378)))
        self.assertEqual(data["summary"]["currentUpstreamProjects"], 546)
        self.assertEqual(data["summary"]["currentDirectoryProjects"], 371)
        self.assertEqual(data["summary"]["addedSinceSnapshot"], 0)
        self.assertEqual(data["summary"]["removedSinceSnapshot"], 0)
        self.assertEqual(source["source"]["currentCommit"], "f3d7e12f34bf7d90130dce3ec3b26cf69c29794e")
        self.assertEqual(source["summary"]["currentPublicDirectoryProjects"], 371)
        expected = [
            "hero-sections/fearless-vision-hero",
            "hero-sections/equilibrium-liquid-glass-hero",
            "hero-sections/designpro-video-hero",
            "hero-sections/datacore-video-hero",
            "hero-sections/cinematic-stream-hero",
            "hero-sections/aethera-cinematic-hero",
            "templates/premium/lexingtonthemes/carrington",
            "landing-pages/mentality-landing",
            "landing-pages/forma-video-landing",
            "templates/premium/lexingtonthemes/carriera",
            "landing-pages/dot-daily-calm-landing",
            "templates/premium/lexingtonthemes/carbon",
            "components-ui/aurora-sign-up",
            "animations-loaders/microvisuals-boomerang-hero",
            "templates/premium/lexingtonthemes/buio",
            "animations-loaders/mainframe-scrub-hero",
            "animations-loaders/dot-nokia-typing-hero",
            "templates/premium/lexingtonthemes/westend",
            "templates/premium/lexingtonthemes/brightlight",
            "landing-pages/pelmatech-health-companion",
        ]
        legacy = [project for project in projects if project["sourceType"] == "legacy"]
        self.assertEqual([p["source"]["path"] for p in legacy[:20]], expected)
        self.assertEqual([p["sourceOrder"] for p in legacy], list(range(1, 372)))
        self.assertTrue(all(p["sourceListedCurrent"] for p in legacy))

    def test_private_manifest_is_the_release_gate(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(data["summary"]["legacyFound"], 546)
        self.assertEqual(data["summary"]["totalProjects"], 552)
        self.assertEqual(data["summary"]["approved"], 30)
        self.assertEqual(data["summary"]["review"], 199)
        self.assertEqual(data["summary"]["unknown"], 323)
        self.assertEqual(data["summary"]["rejected"], 0)
        self.assertEqual(data["sourceArchive"]["pinnedCommit"], "9b5ad43b1450fe6b28a42a9cb8115498d5c56e2a")
        self.assertEqual(data["sourceArchive"]["currentCommit"], "f3d7e12f34bf7d90130dce3ec3b26cf69c29794e")
        self.assertEqual(data["media"]["publicRoot"], "/srv/nordwerk-gallery/media")
        self.assertEqual(data["media"]["privateRoot"], "/srv/nordwerk-gallery/media-private-20260918")
        self.assertEqual(sum(p["public"] for p in data["projects"]), 377)
        for project in data["projects"]:
            if project["sourceType"] == "legacy":
                self.assertEqual(project["public"], project["sourceListedCurrent"])
            else:
                self.assertTrue(project["public"])
            if project["public"] and project["video"]:
                self.assertEqual(len(project["poster"]["sha256"]), 64)
                self.assertEqual(len(project["video"]["sha256"]), 64)
                self.assertEqual(project["source"]["license"], "MIT")

    def test_current_upstream_top_projects_are_public_without_erasing_rights_metadata(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        order = json.loads(SOURCE_ORDER.read_text(encoding="utf-8"))
        by_path = {p["source"]["path"]: p for p in data["projects"] if p["source"]["repository"] == "pulkitxm/claude-directory"}
        public_paths = {p["source"]["path"] for p in catalogue["projects"] if p["source"]["repository"] == "pulkitxm/claude-directory"}
        top_paths = [p["sourcePath"] for p in sorted((p for p in order["projects"] if p["sourceListedCurrent"]), key=lambda p: p["sourceOrder"])[:12]]
        self.assertEqual(
            [by_path[path]["rightsStatus"] for path in top_paths],
            ["unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "review", "unknown", "unknown", "review", "unknown", "review"],
        )
        self.assertTrue(set(top_paths).issubset(public_paths))

    def test_public_media_checksum_set_is_complete(self):
        lines = [line for line in CHECKSUMS.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(lines), 754)
        legacy_media = [line for line in lines if "/srv/nordwerk-gallery/media/" in line]
        self.assertEqual(len(legacy_media), 742)

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
        self.assertEqual(page.count('class="showcase-card"'), 12)
        self.assertIn("Die ersten 12 Website-Beispiele sind direkt sichtbar.", page)
        self.assertIn('video.preload = "none"', source)
        self.assertIn("const LOAD_STEPS = [12, 24, 48]", source)
        self.assertIn("const LATE_BATCH_COUNT = 48", source)
        self.assertIn("let activeCardVideo = null", source)
        self.assertIn("new IntersectionObserver", source)
        self.assertIn("MOBILE_PREVIEW_RATIO = 0.55", source)
        self.assertIn("mobileCandidates", source)
        self.assertIn("sourceOrder", SOURCE_ORDER.read_text(encoding="utf-8"))
        self.assertIn("displayOrder", source)
        self.assertIn("reduceMotion.matches || saveData", source)
        self.assertIn("video.src = project.video.src", source)
        self.assertIn('video.removeAttribute("src")', source)
        self.assertIn('preload="none"', page)
        self.assertNotIn("autoplay", page)
        self.assertIn("Claude Directory / Fable 5", page)


if __name__ == "__main__":
    unittest.main()
