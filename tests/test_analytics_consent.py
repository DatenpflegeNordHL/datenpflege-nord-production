from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

GA_PAGES = [
    "index.html",
    "en/index.html",
    "impressum/index.html",
    "datenschutz/index.html",
    "ki-automatisierung-luebeck/index.html",
    "softwareentwicklung-luebeck/index.html",
    "webentwicklung-luebeck/index.html",
    "website-showcase/index.html",
    "wissen/individualsoftware-kosten/index.html",
    "wissen/ki-prozessautomatisierung/index.html",
    "wissen/website-relaunch-checkliste/index.html",
]


class AnalyticsConsentTests(unittest.TestCase):
    def test_ga_pages_do_not_load_google_tag_directly(self):
        direct_loader = 'https://www.googletagmanager.com/gtag/js?id=G-NHB0PGPYTW'
        for relative in GA_PAGES:
            with self.subTest(page=relative):
                html = (ROOT / relative).read_text(encoding="utf-8")
                self.assertNotIn(direct_loader, html)
                self.assertIn("/assets/service.js?v=", html)

    def test_service_uses_basic_consent_gate(self):
        js = (ROOT / "assets/service.js").read_text(encoding="utf-8")
        required = [
            'const GA_ID = "G-NHB0PGPYTW"',
            'analytics_storage: "denied"',
            'ad_storage: "denied"',
            'ad_user_data: "denied"',
            'ad_personalization: "denied"',
            'window.gtag("consent", "default", denied)',
            'window.gtag("consent", "update", grantedAnalytics)',
            'dpn_consent_v1',
            'showModal()',
            'document.createElement("script")',
            'https://www.googletagmanager.com/gtag/js?id=',
            'cookie_expires: 180 * 24 * 60 * 60',
            'cookie_update: false',
            'allow_google_signals: false',
            'allow_ad_personalization_signals: false',
            'window.location.pathname.startsWith("/datenschutz")',
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_privacy_notice_matches_analytics_use(self):
        html = (ROOT / "datenschutz/index.html").read_text(encoding="utf-8")
        self.assertNotIn(
            "Diese Website setzt derzeit keine Analyse-, Marketing- oder Profiling-Dienste ein.",
            html,
        )
        self.assertIn("Google Analytics 4", html)
        self.assertIn("G-NHB0PGPYTW", html)
        self.assertIn("§ 25 Abs. 1 TDDDG", html)
        self.assertIn("dpn_consent_v1", html)
        self.assertIn("Datenschutz-Einstellungen", html)
        self.assertIn("180 Tage", html)
        self.assertIn("EU-US Data Privacy Framework", html)


if __name__ == "__main__":
    unittest.main()
