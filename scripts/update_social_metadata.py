from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONED_IMAGE = "https://datenpflege-nord.de/og-datenpflege-nord.png?v=20260908-3"
OLD_IMAGE = "https://datenpflege-nord.de/og-datenpflege-nord.png"

ROOT_INDEX = ROOT / "index.html"


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected metadata fragment not found: {old}")
    return text.replace(old, new, 1)


def main() -> None:
    text = ROOT_INDEX.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '<meta property="og:title" content="DatenpflegeNord | Software, Web &amp; KI aus Lübeck">',
        '<meta property="og:title" content="DatenpflegeNord – Website-Checks und KI-Systeme für KMU">',
    )
    text = replace_once(
        text,
        '<meta property="og:description" content="Softwareentwicklung, Webentwicklung und KI-Automatisierung aus Lübeck. Von Webanwendungen und APIs bis zu n8n-Workflows und KI-Agenten.">',
        '<meta property="og:description" content="Technische Website-Checks, digitale Pflichtstellen und KI-gestützte Büroautomation für kleine Unternehmen in Schleswig-Holstein.">',
    )
    text = replace_once(
        text,
        '<meta name="twitter:title" content="DatenpflegeNord | Software, Web &amp; KI aus Lübeck">',
        '<meta name="twitter:title" content="DatenpflegeNord – Website-Checks und KI-Systeme für KMU">',
    )
    text = replace_once(
        text,
        '<meta name="twitter:description" content="Softwareentwicklung, Webentwicklung und KI-Automatisierung für Unternehmen in Lübeck und Schleswig-Holstein.">',
        '<meta name="twitter:description" content="Technische Website-Checks, digitale Pflichtstellen und KI-gestützte Büroautomation für kleine Unternehmen in Schleswig-Holstein.">',
    )
    ROOT_INDEX.write_text(text, encoding="utf-8")

    for html in ROOT.rglob("*.html"):
        page = html.read_text(encoding="utf-8")
        updated = page.replace(OLD_IMAGE, VERSIONED_IMAGE)
        if updated != page:
            html.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
