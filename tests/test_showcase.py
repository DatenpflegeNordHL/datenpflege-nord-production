import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "website-showcase" / "showcase-projects.json"
PAGE = ROOT / "website-showcase" / "index.html"


class ShowcaseCatalogueTests(unittest.TestCase):
    def test_public_catalogue_is_explicitly_rights_gated(self):
        data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        required = {
            "id", "slug", "name", "source", "licenseStatus", "status", "category",
            "style", "industries", "description", "poster", "demo", "technologies",
            "features", "indexable", "approved",
        }
        self.assertTrue(data["publicationPolicy"]["onlyApprovedProjectsArePublic"])
        self.assertGreater(len(data["projects"]), 0)
        for project in data["projects"]:
            self.assertTrue(required <= set(project))
            self.assertTrue(project["approved"])
            self.assertEqual(project["status"], "approved")
            self.assertEqual(project["licenseStatus"], "owned")
            self.assertIsNone(project["demo"])
            self.assertFalse(project["indexable"])

    def test_showcase_never_references_legacy_media_origin(self):
        public_source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (PAGE, ROOT / "assets" / "showcase.css", ROOT / "assets" / "showcase.js", CATALOGUE)
        )
        self.assertNotIn("media.datenpflege-nord.de", public_source)
        self.assertNotIn("pulkitxm", public_source)
        self.assertNotIn("<video", public_source)


if __name__ == "__main__":
    unittest.main()
