from __future__ import annotations

from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "assets" / "branding" / "datenpflegenord-logo.svg"
OUTPUT = ROOT / "og-datenpflege-nord-2026.png"

WIDTH, HEIGHT = 1200, 630
BG = "#F6F7F9"
NAVY = "#1B3154"
TEXT = "#20242B"
MUTED = "#5E6673"
LINE = "#D9DCE2"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def main() -> None:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)

    # Slim brand rail so the preview still reads as DatenpflegeNord when cropped.
    draw.rectangle((0, 0, 18, HEIGHT), fill=NAVY)

    logo_png = cairosvg.svg2png(
        url=str(LOGO),
        output_width=610,
        output_height=121,
    )
    logo = Image.open(BytesIO(logo_png)).convert("RGBA")
    canvas.paste(logo, (78, 68), logo)

    draw.line((78, 224, 1122, 224), fill=LINE, width=2)

    title_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
    subtitle_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 31)
    footer_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

    draw.text((78, 278), "Website-Checks & KI-Systeme", font=title_font, fill=TEXT)
    draw.text((78, 347), "für KMU", font=title_font, fill=TEXT)

    draw.text(
        (78, 445),
        "Technische Website-Checks · digitale Pflichtstellen · KI-Büroautomation",
        font=subtitle_font,
        fill=MUTED,
    )

    draw.rounded_rectangle((78, 533, 470, 584), radius=10, fill=NAVY)
    draw.text((101, 544), "datenpflege-nord.de", font=footer_font, fill="#FFFFFF")
    draw.text((830, 548), "Lübeck · Schleswig-Holstein", font=footer_font, fill=MUTED)

    canvas.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
