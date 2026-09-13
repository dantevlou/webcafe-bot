from pathlib import Path

from PIL import Image, ImageDraw

from theme import (
    MIDNIGHT_VIOLET,
    PALE_SLATE,
    SOFT_PERIWINKLE,
)


OUTPUT_PATH = Path("rank_up_preview.png")

WIDTH = 1200
HEIGHT = 480


def create_rank_up_card() -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )

    draw = ImageDraw.Draw(image)

    banner_left = 35
    banner_top = 35
    banner_right = 1165
    banner_bottom = 445

    # Banner shell
    shadow_offset = 8

    draw.rectangle(
        (
            banner_left + shadow_offset,
            banner_top + shadow_offset,
            banner_right + shadow_offset,
            banner_bottom + shadow_offset,
        ),
        fill=MIDNIGHT_VIOLET,
    )

    draw.rectangle(
        (
            banner_left,
            banner_top,
            banner_right,
            banner_bottom,
        ),
        fill=MIDNIGHT_VIOLET,
        outline=PALE_SLATE,
        width=4
    )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_rank_up_card()