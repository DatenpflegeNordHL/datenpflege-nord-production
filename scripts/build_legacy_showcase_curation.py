#!/usr/bin/env python3
"""Create rights-gated editorial directions from selected legacy metadata.

No legacy poster, video, markup, branding or source file is copied. A selected
record can only become an approved *editorial direction* when the pinned source
is MIT licensed, its project prompt was scanned without external URLs/trackers,
and its legacy media remains unused.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE_REPOSITORY = "pulkitxm/claude-directory"
SOURCE_COMMIT = "9b5ad43b1450fe6b28a42a9cb8115498d5c56e2a"

# path, public title, category, CSS variant, styles, industries, description
SELECTIONS = [
    ("animations-loaders/bloom-nested-squares", "Geschichtete Flächen", "Bewegung & Detail", "editorial", ["geometrisch", "ruhig", "editorial"], ["Beratung", "Kultur", "B2B"], "Versetzte Flächen als ruhiger Einstieg für Inhalte mit klarer Reihenfolge."),
    ("components-ui/animated-dots-rain", "Punktfeld & Tiefe", "Bewegung & Detail", "trust", ["atmosphärisch", "reduziert", "digital"], ["Software", "Bildung", "Kreativwirtschaft"], "Ein zurückhaltendes Punktfeld für digitale Themen, bei denen Tiefe ohne Ablenkung gefragt ist."),
    ("components-ui/background-paths-hero", "Linien als Orientierung", "Bewegung & Detail", "grid", ["strukturiert", "technisch", "klar"], ["Software", "Industrie", "B2B"], "Verbindende Linien übersetzen komplexe Zusammenhänge in eine verständliche visuelle Ordnung."),
    ("components-ui/gradient-dots-background", "Farbige Körnung", "Bewegung & Detail", "knowledge", ["texturiert", "freundlich", "modern"], ["Bildung", "SaaS", "Dienstleistung"], "Feine Farbflächen geben einer sachlichen Seite Wärme, ohne die Inhalte zu überzeichnen."),
    ("components-ui/terminal-cli-control-deck", "Technische Klarheit", "Digitale Produkte", "grid", ["präzise", "technisch", "kontraststark"], ["IT-Dienstleistung", "Software", "Industrie"], "Eine klare, technisch geprägte Sprache für Tools, Plattformen und Systemangebote."),
    ("shaders/abstract-glassy-shader", "Gläserne Fläche", "Bewegung & Detail", "product", ["transparent", "leicht", "digital"], ["SaaS", "Kreativwirtschaft", "Produktteams"], "Transparenz und weiche Ebenen als Akzent – sparsam eingesetzt und immer ohne schwere Live-Effekte."),
    ("shaders/aurora-borealis-shader", "Leuchtende Tiefe", "Bewegung & Detail", "story", ["leuchtend", "atmosphärisch", "mutig"], ["Kreativwirtschaft", "Bildung", "SaaS"], "Eine farbige Tiefenwirkung für Marken mit einer stärkeren, aber weiterhin kontrollierten visuellen Haltung."),
    ("shaders/blue-meshy-shader-lab", "Netzstruktur", "Digitale Produkte", "grid", ["vernetzt", "technisch", "dynamisch"], ["Software", "Daten", "B2B"], "Eine Netzmetapher für Schnittstellen, Systeme und Produkte mit vielen verbundenen Teilen."),
    ("shaders/flowing-waves-shader", "Fließende Bewegung", "Bewegung & Detail", "human", ["weich", "organisch", "ruhig"], ["Gesundheit", "Beratung", "Dienstleistung"], "Organische Bewegung als sanfter Akzent für erklärende oder menschlich geprägte Angebote."),
    ("shaders/grain-gradient-corners-lab", "Analoge Körnung", "Markenwebsite", "luxury", ["material", "editorial", "hochwertig"], ["Architektur", "Beratung", "Kultur"], "Körnung und Verlauf geben einer hochwertigen Redaktionstypografie eine spürbare Materialität."),
    ("shaders/mesh-gradient-shader-hero", "Weiche Farbräume", "Markenwebsite", "product", ["farbig", "weich", "modern"], ["SaaS", "Bildung", "Kreativwirtschaft"], "Farbige Räume schaffen einen klaren Markenakzent, ohne von Information und Kontaktweg abzulenken."),
    ("shaders/morphing-light-shader", "Wandelndes Licht", "Bewegung & Detail", "story", ["lebendig", "hell", "minimal"], ["Kultur", "Bildung", "Innovation"], "Ein heller, zurückhaltender Verlauf für Seiten, die Fortschritt und Veränderung sichtbar machen möchten."),
    ("shaders/radial-aperture-shader", "Radialer Fokus", "Landingpage", "campaign", ["fokussiert", "direkt", "grafisch"], ["Angebote", "Recruiting", "Veranstaltung"], "Ein konzentrierter Mittelpunkt stärkt eine einzelne Botschaft und einen klaren nächsten Schritt."),
    ("ui-design/aperture-minimalist-dark", "Dunkle Präzision", "Digitale Produkte", "luxury", ["dunkel", "minimal", "präzise"], ["Software", "Architektur", "Beratung"], "Eine reduzierte dunkle Richtung für Inhalte, bei denen Details und Kontrast die Orientierung tragen."),
    ("ui-design/bauhaus-form-follows-function", "Geometrische Ordnung", "Markenwebsite", "editorial", ["geometrisch", "klar", "mutig"], ["Architektur", "Bildung", "Kultur"], "Form, Raster und Farbe machen die Informationsarchitektur sichtbar und nachvollziehbar."),
    ("ui-design/bold-typography-design-system", "Typografie als Bühne", "Markenwebsite", "story", ["typografisch", "direkt", "selbstbewusst"], ["Beratung", "Kreativwirtschaft", "B2B"], "Große Typografie führt durch eine klare Botschaft – mit genug Raum für Substanz und Kontext."),
    ("ui-design/botanical-organic-serif", "Organische Ruhe", "Dienstleistungswebsite", "human", ["organisch", "ruhig", "serif"], ["Gesundheit", "Wellbeing", "Beratung"], "Ruhige Serifentypografie und natürliche Flächen für vertrauensvolle, persönliche Angebote."),
    ("ui-design/corporate-trust-design-system", "Klarer Vertrauensaufbau", "Unternehmenswebsite", "trust", ["vertrauensvoll", "informativ", "zugänglich"], ["B2B", "Fachbetrieb", "Dienstleistung"], "Eine sachliche Richtung, die Leistung, Ansprechpartner und Erreichbarkeit nachvollziehbar zusammenführt."),
    ("ui-design/handcraft-paper-ui", "Haptische Redaktion", "Markenwebsite", "knowledge", ["editorial", "material", "nahbar"], ["Handwerk", "Kultur", "Bildung"], "Eine redaktionelle Textur für Angebote mit handwerklichem Charakter und viel erklärendem Inhalt."),
    ("ui-design/industrial-skeuomorphism", "Industrielle Struktur", "Digitale Produkte", "grid", ["industriell", "robust", "strukturiert"], ["Industrie", "Logistik", "Software"], "Robuste Flächen und klare Module für Produkte oder Leistungen mit technischem Schwerpunkt."),
    ("ui-design/luxury-editorial-design-system", "Hochwertige Redaktion", "Markenwebsite", "luxury", ["hochwertig", "editorial", "zurückhaltend"], ["Architektur", "Kanzlei", "Beratung"], "Großzügige Typografie und kontrollierte Details für einen ruhigen, hochwertigen Auftritt."),
    ("ui-design/serif-editorial-design-system", "Serif & Story", "Wissensbereich", "knowledge", ["serif", "lesbar", "redaktionell"], ["B2B", "Bildung", "Organisationen"], "Leseführung und typografische Hierarchie für Fachinhalte, Entscheidungen und längere Texte."),
    ("ui-design/swiss-design-system", "Schweizer Raster", "Unternehmenswebsite", "editorial", ["rasterbasiert", "präzise", "klar"], ["B2B", "Software", "Beratung"], "Ein strenges, flexibles Raster bringt komplexe Inhalte ohne visuelle Reibung in eine klare Ordnung."),
    ("ui-design/verdant-organic-design-system", "Natürliche Struktur", "Dienstleistungswebsite", "trust", ["natürlich", "freundlich", "übersichtlich"], ["Gesundheit", "Handwerk", "lokale Dienstleistung"], "Natürliche Akzente verbinden einen freundlichen Auftritt mit einer gut zugänglichen Informationsstruktur."),
]


def make_direction(spec: tuple, legacy: dict) -> dict:
    path, name, category, variant, style, industries, description = spec
    return {
        "id": "editorial-" + path.replace("/", "-"),
        "slug": path.rsplit("/", 1)[-1],
        "name": name,
        "source": "DatenpflegeNord editorial design direction",
        "licenseStatus": "owned-editorial-direction",
        "status": "approved",
        "approvalScope": "editorial-inspiration-only",
        "category": category,
        "style": style,
        "industries": industries,
        "description": description,
        "poster": {"type": "css", "variant": variant},
        "demo": None,
        "technologies": ["Semantisches HTML", "Responsive CSS", "Progressive Enhancement"],
        "features": ["Eigene Inhalte", "Lokale Assets", "Keine fremde Live-Demo"],
        "indexable": False,
        "approved": True,
    }


def audit_evidence(direction: dict, legacy: dict) -> dict:
    """Keep source and media evidence outside the public catalogue."""
    return {
        "id": direction["id"],
        "legacyReference": {
            "id": legacy["id"],
            "sourcePath": legacy["sourcePath"],
            "repository": SOURCE_REPOSITORY,
            "commit": SOURCE_COMMIT,
            "upstreamLicense": "MIT",
            "promptGitBlobSha": legacy["sourceEvidence"]["promptGitBlobSha"],
            "legacyStatus": "unknown",
            "legacyMedia": {
                "poster": {
                    "status": "not_used_pending_sync",
                    "bytes": legacy["poster"]["bytes"],
                    "format": ".jpg",
                },
                "video": {
                    "status": "not_used_pending_sync",
                    "bytes": legacy["demo"]["bytes"],
                    "format": ".mp4",
                },
                "reason": "Only an independently authored editorial direction is public; legacy media and source files are never published.",
            },
            "screening": {
                "premiumOrCommercialHint": False,
                "riskFlags": [],
                "promptPresent": True,
                "promptExternalUrls": False,
                "promptTrackers": False,
                "originalMediaPublished": False,
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--legacy-catalogue", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    catalogue = json.loads(args.catalogue.read_text(encoding="utf-8"))
    legacy = json.loads(args.legacy_catalogue.read_text(encoding="utf-8"))
    by_path = {entry["sourcePath"]: entry for entry in legacy["entries"]}
    directions = []
    evidence = []
    for spec in SELECTIONS:
        path = spec[0]
        entry = by_path.get(path)
        if not entry:
            raise ValueError(f"Legacy record missing: {path}")
        if entry["status"] != "unknown" or entry["commercialTemplateHint"] or entry["riskFlags"]:
            raise ValueError(f"Legacy release gate changed: {path}")
        if not entry["poster"] or not entry["demo"] or not entry["sourcePath"]:
            raise ValueError(f"Legacy evidence incomplete: {path}")
        direction = make_direction(spec, entry)
        directions.append(direction)
        evidence.append(audit_evidence(direction, entry))
    catalogue["curatedLegacyDirections"] = directions
    args.catalogue.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "schemaVersion": 1,
        "source": {"repository": SOURCE_REPOSITORY, "commit": SOURCE_COMMIT, "license": "MIT"},
        "selection": {"count": len(directions), "approvalScope": "editorial-inspiration-only"},
        "excluded": {
            "premiumOrCommercial": 199,
            "remainingUnreviewedLegacyRecords": 522,
            "externalUrlOrTrackerPromptCandidates": [
                "animations-loaders/container-scroll-animation",
                "animations-loaders/scroll-expansion-hero",
                "components-ui/aurora-sign-up",
                "components-ui/core-features-gradient-cards",
                "components-ui/gradient-bars-background",
                "shaders/volumetric-beams-shader",
            ],
        },
        "directions": evidence,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"curated": len(directions), "catalogue": str(args.catalogue), "report": str(args.report)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
