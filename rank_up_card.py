from pathlib import Path

from PIL import Image

from theme import SOFT_PERIWINKLE


OUTPUT_PATH = Path("rank_up_preview.png")

WIDTH = 450
HEIGHT = 250


def create_rank_up_card() -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_rank_up_card()