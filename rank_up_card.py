from pathlib import Path

from PIL import Image, ImageDraw

from theme import MIDNIGHT_VIOLET, PALE_SLATE, SOFT_PERIWINKLE


OUTPUT_PATH = Path("rank_up_preview.png")

WIDTH = 450
HEIGHT = 250


def create_rank_up_card() -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )

    draw = ImageDraw.Draw(image)

    window_left = 20
    window_top = 20
    window_right = 430
    window_bottom = 230

    shadow_offset = 5

    draw.rectangle(
        (
            window_left + shadow_offset,
            window_top + shadow_offset,
            window_right + shadow_offset,
            window_bottom + shadow_offset,
        ),
        fill=MIDNIGHT_VIOLET,
    )

    draw.rectangle(
        (
            window_left,
            window_top,
            window_right,
            window_bottom,
        ),
        fill=PALE_SLATE,
        outline=MIDNIGHT_VIOLET,
        width=3,
    )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_rank_up_card()