import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "website-showcase" / "showcase-projects.json"
PAGE = ROOT / "website-showcase" / "index.html"
LEGACY_INVENTORY = ROOT / "docs" / "design-gallery" / "legacy-showcase-projects.json"


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

        directions = data["curatedLegacyDirections"]
        self.assertEqual(len(directions), 24)
        for direction in directions:
            self.assertTrue(required <= set(direction))
            self.assertTrue(direction["approved"])
            self.assertEqual(direction["status"], "approved")
            self.assertEqual(direction["approvalScope"], "editorial-inspiration-only")
            self.assertEqual(direction["licenseStatus"], "owned-editorial-direction")
            self.assertEqual(direction["poster"]["type"], "css")
            self.assertIsNone(direction["demo"])
            self.assertFalse(direction["indexable"])

    def test_showcase_never_references_legacy_media_origin(self):
        public_source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (PAGE, ROOT / "assets" / "showcase.css", ROOT / "assets" / "showcase.js", CATALOGUE)
        )
        self.assertNotIn("media.datenpflege-nord.de", public_source)
        self.assertNotIn("pending_sync", public_source)
        self.assertNotIn("<video", public_source)

    def test_legacy_inventory_is_complete_but_not_publishable(self):
        inventory = json.loads(LEGACY_INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(inventory["releaseGate"]["unknown"], 546)
        self.assertEqual(len(inventory["entries"]), 546)
        self.assertTrue(all(entry["status"] == "unknown" for entry in inventory["entries"]))
        self.assertTrue(all(not entry["publiclyUsable"] for entry in inventory["entries"]))
        self.assertEqual(sum(entry["sourceEvidence"].get("promptPresent", False) for entry in inventory["entries"]), 541)

    def test_curation_evidence_keeps_original_media_and_legacy_records_private(self):
        report = json.loads((ROOT / "docs" / "design-gallery" / "legacy-curation.json").read_text(encoding="utf-8"))
        self.assertEqual(report["selection"]["count"], 24)
        for direction in report["directions"]:
            reference = direction["legacyReference"]
            self.assertEqual(reference["legacyStatus"], "unknown")
            self.assertFalse(reference["screening"]["originalMediaPublished"])
            self.assertEqual(reference["legacyMedia"]["poster"]["status"], "not_used_pending_sync")
            self.assertEqual(reference["legacyMedia"]["video"]["status"], "not_used_pending_sync")


if __name__ == "__main__":
    unittest.main()
