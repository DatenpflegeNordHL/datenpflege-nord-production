"""Static acceptance checks for the bilingual promotional hero."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HeroPromoTests(unittest.TestCase):
    def test_bilingual_markup_and_required_order(self):
        cases = (
            ("index.html", "Aktuell: 75 % Neukundenrabatt", "Website-Inspirationen", "Designrichtungen ansehen"),
            ("en/index.html", "Current: 75% new customer discount", "Website Inspiration", "Explore design directions"),
        )
        for path, promo, title, subline in cases:
            with self.subTest(path=path):
                source = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn('<a href="/website-showcase/">Websites</a>', source)
                self.assertIn('<button', source[source.index('class="hero-promo"'):])
                self.assertNotIn('<a', source[source.index('class="hero-promo"'):source.index('class="hero-label"')])
                self.assertIn(promo, source)
                self.assertIn(title, source)
                self.assertIn(subline, source)
                positions = [
                    source.index('class="hero-promo"'),
                    source.index('class="hero-label"'),
                    source.index('id="hero-title"'),
                    source.index('class="hero-summary"'),
                    source.index('class="hero-entity"'),
                    source.index('class="hero-pills"'),
                    source.index('class="hero-showcase-card"'),
                ]
                self.assertEqual(positions, sorted(positions))

    def test_no_green_is_used_by_new_components(self):
        css = (ROOT / "assets/home.css").read_text(encoding="utf-8")
        start = css.index(".hero-promo")
        end = css.index(".stats-strip")
        component_css = css[start:end].lower()
        self.assertNotIn("#c8ff46", component_css)
        self.assertNotIn("var(--accent)", component_css)

    def test_frontend_uses_structured_promo_field(self):
        for path in ("assets/home-de.js", "assets/home-en.js"):
            source = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn('promo: "new_customer_75"', source)
            self.assertNotIn('message: `', source)


if __name__ == "__main__":
    unittest.main()
