from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "og-datenpflege-nord.png"

WIDTH, HEIGHT = 1200, 630
BG = "#F7F8FA"
NAVY = "#1A2E52"
TEXT = "#20242B"
MUTED = "#667085"
LINE = "#D9DCE2"
WHITE = "#FFFFFF"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def main() -> None:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)

    brand_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    title_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 58)
    subtitle_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 29)
    footer_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    monogram_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 27)

    draw.rounded_rectangle((72, 62, 176, 166), radius=24, fill=NAVY)
    draw.text((94, 96), "DPN", font=monogram_font, fill=WHITE)
    draw.text((208, 77), "DatenpflegeNord", font=brand_font, fill=NAVY)
    draw.text((208, 125), "Website-Checks · KI-Systeme · Schleswig-Holstein", font=subtitle_font, fill=MUTED)

    draw.line((72, 208, 1128, 208), fill=LINE, width=2)
    draw.text((72, 270), "Website-Checks & KI-Systeme", font=title_font, fill=TEXT)
    draw.text((72, 347), "für KMU", font=title_font, fill=TEXT)
    draw.text(
        (72, 448),
        "Technische Checks · digitale Pflichtstellen · KI-Automation",
        font=subtitle_font,
        fill=MUTED,
    )

    draw.rounded_rectangle((72, 536, 402, 585), radius=12, fill=NAVY)
    draw.text((96, 545), "datenpflege-nord.de", font=footer_font, fill=WHITE)
    draw.text((856, 548), "Lübeck", font=footer_font, fill=MUTED)

    canvas.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
