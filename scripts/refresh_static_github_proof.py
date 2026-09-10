from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    ROOT / "index.html": {
        "repo_fallback_old": '<strong data-stat="repos">2</strong>',
        "repo_fallback_new": '<strong data-stat="repos">—</strong>',
        "dates": {
            "https://github.com/open-jarvis/OpenJarvis/pull/708": "10.08.2026",
            "https://github.com/open-jarvis/OpenJarvis/pull/702": "06.08.2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/24": "07.08.2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/23": "07.08.2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/22": "06.08.2026",
        },
        "opened": 'data-i18n="prOpened">PR geöffnet</span>',
        "merged": 'data-i18n="prMerged">PR gemergt</span>',
    },
    ROOT / "en" / "index.html": {
        "repo_fallback_old": '<strong data-stat="repos">2</strong>',
        "repo_fallback_new": '<strong data-stat="repos">—</strong>',
        "dates": {
            "https://github.com/open-jarvis/OpenJarvis/pull/708": "10 Aug 2026",
            "https://github.com/open-jarvis/OpenJarvis/pull/702": "6 Aug 2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/24": "7 Aug 2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/23": "7 Aug 2026",
            "https://github.com/DatenpflegeNordHL/Codex-Looper/pull/22": "6 Aug 2026",
        },
        "opened": 'data-i18n="prOpened">PR opened</span>',
        "merged": 'data-i18n="prMerged">PR merged</span>',
    },
}

ANCHOR_RE_TEMPLATE = r'(<a\b[^>]*href="{href}"[^>]*>.*?</a>)'
DATE_RE = re.compile(r'<span\s+data-i18n="current">(?:aktuell|recent)</span>')


def update_anchor(text: str, href: str, date: str, *, fix_708: bool, opened: str, merged: str) -> str:
    pattern = re.compile(ANCHOR_RE_TEMPLATE.format(href=re.escape(href)), re.DOTALL)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Missing static feed anchor: {href}")
    block = match.group(1)

    date_matches = DATE_RE.findall(block)
    if len(date_matches) != 1:
        raise RuntimeError(f"Expected one static current/recent date in {href}, found {len(date_matches)}")
    block = DATE_RE.sub(f'<span>{date}</span>', block, count=1)

    if fix_708:
        if block.count(opened) != 1:
            raise RuntimeError(f"Expected one opened badge in {href}")
        block = block.replace(opened, merged, 1)

    return text[:match.start()] + block + text[match.end():]


def main() -> None:
    for path, cfg in FILES.items():
        text = path.read_text(encoding="utf-8")

        if text.count(cfg["repo_fallback_old"]) != 1:
            raise RuntimeError(f"{path.relative_to(ROOT)}: expected exactly one static public-repo fallback of 2")
        text = text.replace(cfg["repo_fallback_old"], cfg["repo_fallback_new"], 1)

        for href, date in cfg["dates"].items():
            text = update_anchor(
                text,
                href,
                date,
                fix_708=href.endswith("/708"),
                opened=cfg["opened"],
                merged=cfg["merged"],
            )

        if 'data-i18n="current">aktuell</span>' in text or 'data-i18n="current">recent</span>' in text:
            raise RuntimeError(f"{path.relative_to(ROOT)}: stale generic static date marker remains")

        path.write_text(text, encoding="utf-8")

    print("Refreshed static GitHub proof: neutral repo fallback, verified PR #708 state and exact dates.")


if __name__ == "__main__":
    main()
