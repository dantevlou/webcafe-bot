from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from theme import (
    LINEN,
    MIDNIGHT_VIOLET,
    PALE_SLATE, 
    SLATE_BLUE,
    SOFT_PERIWINKLE,
)


OUTPUT_PATH = Path("rank_up_preview.png")

WIDTH = 450
HEIGHT = 250

JETBRAINS_MONO_PATH = Path(
    r"C:\Users\dante\AppData\Local\Microsoft\Windows\Fonts"
    r"\JetBrainsMono-VariableFont_wght.ttf"
)


def load_font(size: int, bold: bool = False):
    font = ImageFont.truetype(
        JETBRAINS_MONO_PATH,
        size=size,
    )

    if bold:
        font.set_variation_by_name("Bold")

    return font


def create_rank_up_card() -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )

    draw = ImageDraw.Draw(image)

    title_bar_font = load_font(17, bold=True)

    window_left = 20
    window_top = 20
    window_right = 430
    window_bottom = 230

    # Window shell
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

    # Title bar
    title_bar_top = window_top + 4
    title_bar_bottom = window_top + 35
    title_bar_height = title_bar_bottom - title_bar_top

    draw.rectangle(
        (
            window_left + 4,
            title_bar_top,
            window_right - 4,
            title_bar_bottom,
        ),
        fill=SLATE_BLUE,
        outline=MIDNIGHT_VIOLET,
        width = 2,
    )

    # Window buttons
    button_size = 18
    button_gap = 4
    button_total_width = (button_size * 3) + (button_gap * 2)

    button_start_x = (
        window_right
        - 12
        - button_total_width
    )

    button_y = (
        title_bar_top
        + (title_bar_height - button_size) // 2
    )

    for index in range(3):
        button_x = (
            button_start_x
            + index * (button_size + button_gap)
        )

        draw.rectangle(
            (
                button_x,
                button_y,
                button_x + button_size,
                button_y + button_size,
            ),
            fill=SOFT_PERIWINKLE,
            outline=MIDNIGHT_VIOLET,
            width=1,
        )

    first_button_x = button_start_x
    second_button_x = button_start_x + button_size + button_gap
    third_button_x = button_start_x + (button_size + button_gap) * 2

    # Minimise
    draw.line(
        (
            first_button_x + 5,
            button_y + 13,
            first_button_x + 13,
            button_y + 13,
        ),
        fill=MIDNIGHT_VIOLET,
        width=1
    )

    # Maximise
    draw.rectangle(
        (
            second_button_x + 5,
            button_y + 5,
            second_button_x + 13,
            button_y + 13,
        ),
        outline=MIDNIGHT_VIOLET,
        width=1
    )

    # Close
    draw.line(
        (
            third_button_x + 5,
            button_y + 5,
            third_button_x + 13,
            button_y + 13,
        ),
        fill=MIDNIGHT_VIOLET,
        width=1
    )

    draw.line(
        (
            third_button_x + 13,
            button_y + 5,
            third_button_x + 5,
            button_y + 13,
        ),
        fill=MIDNIGHT_VIOLET,
        width=1
    )

    # Title-bar text
    title_text = "webcafe.exe"

    title_bbox = draw.textbbox(
        (0, 0),
        title_text,
        font=title_bar_font,
    )

    title_height = title_bbox[3] - title_bbox[1]

    title_x = window_left + 12
    title_y = (
        title_bar_top
        + (title_bar_height - title_height) // 2
        - title_bbox[1]
    )

    draw.text(
        (title_x, title_y),
        title_text,
        fill=LINEN,
        font=title_bar_font,
    )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_rank_up_card()