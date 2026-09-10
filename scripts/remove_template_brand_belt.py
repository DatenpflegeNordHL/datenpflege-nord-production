from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", ROOT / "en" / "index.html"]
CSS_FILE = ROOT / "assets" / "home.css"
LOGO_DIR = ROOT / "images" / "clients-logo"
LOGOS = [LOGO_DIR / f"logo-{i}.svg" for i in range(1, 6)]

SECTION_RE = re.compile(
    r"\n?\s*<section\b[^>]*class=[\"'][^\"']*\bbrand-belt-section\b[^\"']*[\"'][^>]*>.*?</section>\s*",
    re.IGNORECASE | re.DOTALL,
)

CSS_SELECTORS = [
    ".brand-belt-section",
    ".brand-belt",
    ".brand-belt-viewport",
    ".brand-belt-track",
    ".brand-belt:hover .brand-belt-track",
    ".brand-belt-group",
    ".brand-logo-slot",
    ".brand-logo-slot img",
    ".brand-belt-section + .section",
]


def remove_balanced_block(text: str, start: int) -> tuple[str, int]:
    brace = text.find("{", start)
    if brace == -1:
        raise RuntimeError(f"Missing opening brace near offset {start}")
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                end = pos + 1
                while end < len(text) and text[end] in " \t":
                    end += 1
                if end < len(text) and text[end] == "\n":
                    end += 1
                return text[:start] + text[end:], end - start
    raise RuntimeError(f"Unbalanced CSS block near offset {start}")


def remove_selector_blocks(text: str, selector: str) -> tuple[str, int]:
    removed = 0
    while True:
        match = re.search(rf"(?m)^\s*{re.escape(selector)}\s*\{{", text)
        if not match:
            return text, removed
        text, _ = remove_balanced_block(text, match.start())
        removed += 1


def remove_keyframes(text: str) -> tuple[str, int]:
    removed = 0
    pattern = re.compile(r"(?m)^\s*@keyframes\s+brandBeltScroll\s*\{")
    while True:
        match = pattern.search(text)
        if not match:
            return text, removed
        text, _ = remove_balanced_block(text, match.start())
        removed += 1


def main() -> None:
    for path in HTML_FILES:
        original = path.read_text(encoding="utf-8")
        updated, count = SECTION_RE.subn("\n", original)
        if count != 1:
            raise RuntimeError(f"{path.relative_to(ROOT)}: expected one brand belt section, found {count}")
        path.write_text(updated, encoding="utf-8")

    css = CSS_FILE.read_text(encoding="utf-8")
    total_removed = 0
    # Longer selectors first so a shorter prefix cannot consume them.
    for selector in sorted(CSS_SELECTORS, key=len, reverse=True):
        css, count = remove_selector_blocks(css, selector)
        total_removed += count
    css, keyframes = remove_keyframes(css)
    total_removed += keyframes
    if total_removed < 10:
        raise RuntimeError(f"Expected at least 10 brand-belt CSS blocks, removed {total_removed}")

    # Remove now-empty dedicated reduced-motion blocks if present.
    css = re.sub(
        r"\n?\s*@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{\s*\}\s*",
        "\n",
        css,
        flags=re.IGNORECASE,
    )
    CSS_FILE.write_text(css, encoding="utf-8")

    missing = [str(path.relative_to(ROOT)) for path in LOGOS if not path.exists()]
    if missing:
        raise RuntimeError(f"Expected template logos are missing before cleanup: {missing}")
    for path in LOGOS:
        path.unlink()

    print("Removed template brand belt from DE/EN, related CSS, and five SVG assets.")


if __name__ == "__main__":
    main()
