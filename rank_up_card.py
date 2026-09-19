import math
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

WIDTH = 1200
HEIGHT = 480

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


def has_star_motif(rank_name: str) -> bool:
    return rank_name.casefold() == "cafe star"


def draw_filled_star(
    draw: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    outer_radius: int,
    fill,
) -> None:
    inner_radius = int(outer_radius * 0.45)
    points = []

    for index in range(10):
        angle = math.radians(-90 + (index * 36))

        if index % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius

        x = center_x + int(math.cos(angle) * radius)
        y = center_y + int(math.sin(angle) * radius)
        points.append((x, y))

    draw.polygon(
        points,
        fill=fill,
    )


def create_rank_up_card(
    rank_name: str,
    rank_level: int,
) -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )

    draw = ImageDraw.Draw(image)

    title_bar_font = load_font(22, bold=True)
    address_font = load_font(18)
    heading_font = load_font(58, bold=True)
    body_font = load_font(22)
    rank_font = load_font(44, bold=True)
    level_font = load_font(20, bold=True)

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
        width=4,
    )

    # Browser header
    header_left = banner_left + 8
    header_top = banner_top + 8
    header_right = banner_right - 8

    title_bar_bottom = header_top + 42

    draw.rectangle(
        (
            header_left,
            header_top,
            header_right,
            title_bar_bottom,
        ),
        fill=SLATE_BLUE,
        outline=MIDNIGHT_VIOLET,
        width=3,
    )

    # Window controls
    button_size = 24
    button_gap = 5
    button_total_width = (button_size * 3) + (button_gap * 2)

    button_start_x = (
        header_right
        - 12
        - button_total_width
    )

    button_y = (
        header_top
        + ((title_bar_bottom - header_top) - button_size) // 2
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
            width=2,
        )

    first_button_x = button_start_x
    second_button_x = (
        button_start_x
        + button_size
        + button_gap
    )
    third_button_x = (
        button_start_x
        + (button_size + button_gap) * 2
    )

    # Minimise
    draw.line(
        (
            first_button_x + 6,
            button_y + 17,
            first_button_x + 18,
            button_y + 17,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    # Maximise
    draw.rectangle(
        (
            second_button_x + 6,
            button_y + 6,
            second_button_x + 18,
            button_y + 18,
        ),
        outline=MIDNIGHT_VIOLET,
        width=2,
    )

    # Close
    draw.line(
        (
            third_button_x + 6,
            button_y + 6,
            third_button_x + 18,
            button_y + 18,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    draw.line(
        (
            third_button_x + 18,
            button_y + 6,
            third_button_x + 6,
            button_y + 18,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    # Title-bar text
    title_text = "webcafe.exe"

    title_bbox = draw.textbbox(
        (0, 0),
        title_text,
        font=title_bar_font,
    )

    title_height = title_bbox[3] - title_bbox[1]

    title_x = header_left + 14
    title_y = (
        header_top
        + ((title_bar_bottom - header_top) - title_height) // 2
        - title_bbox[1]
    )

    draw.text(
        (title_x, title_y),
        title_text,
        fill=LINEN,
        font=title_bar_font,
    )

    # Browser toolbar
    toolbar_top = title_bar_bottom + 3
    toolbar_bottom = toolbar_top + 48

    draw.rectangle(
        (
            header_left,
            toolbar_top,
            header_right,
            toolbar_bottom,
        ),
        fill=PALE_SLATE,
        outline=MIDNIGHT_VIOLET,
        width=3,
    )

    # Address bar
    address_left = header_left + 110
    address_top = toolbar_top + 9
    address_right = header_right - 18
    address_bottom = toolbar_bottom - 9

    draw.rectangle(
        (
            address_left,
            address_top,
            address_right,
            address_bottom,
        ),
        fill=LINEN,
        outline=MIDNIGHT_VIOLET,
        width=2,
    )

    # Navigation controls
    nav_center_y = (toolbar_top + toolbar_bottom) // 2

    back_x = header_left + 24

    draw.line(
        (
            back_x + 8,
            nav_center_y - 7,
            back_x,
            nav_center_y,
            back_x + 8,
            nav_center_y + 7,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    forward_x = header_left + 54

    draw.line(
        (
            forward_x,
            nav_center_y - 7,
            forward_x + 8,
            nav_center_y,
            forward_x,
            nav_center_y + 7,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    home_x = header_left + 83
    home_y = nav_center_y

    draw.line(
        (
            home_x - 9,
            home_y,
            home_x,
            home_y - 8,
            home_x + 9,
            home_y,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    draw.rectangle(
        (
            home_x - 6,
            home_y,
            home_x + 6,
            home_y + 8,
        ),
        outline=MIDNIGHT_VIOLET,
        width=2,
    )

    # Address-bar text
    address_text = "https://webcafe.exe/rank-up"

    address_bbox = draw.textbbox(
        (0, 0),
        address_text,
        font=address_font,
    )

    address_height = address_bbox[3] - address_bbox[1]

    address_text_x = address_left + 12
    address_text_y = (
        address_top
        + ((address_bottom - address_top) - address_height) // 2
        - address_bbox[1]
    )

    draw.text(
        (address_text_x, address_text_y),
        address_text,
        fill=MIDNIGHT_VIOLET,
        font=address_font,
    )

    # Achievement content
    content_left = banner_left + 70
    content_top = toolbar_bottom + 38

    heading_text = "RANK UP"
    subheading_text = "you ranked up to"
    rank_text = rank_name.upper()
    level_text = f"LEVEL {rank_level}"

    draw.text(
        (content_left, content_top),
        heading_text,
        fill=LINEN,
        font=heading_font,
    )

    draw.text(
        (content_left, content_top + 76),
        subheading_text,
        fill=SOFT_PERIWINKLE,
        font=body_font,
    )

    draw.text(
        (content_left, content_top + 112),
        rank_text,
        fill=LINEN,
        font=rank_font,
    )

    level_bbox = draw.textbbox(
        (0, 0),
        level_text,
        font=level_font,
    )

    level_width = level_bbox[2] - level_bbox[0]
    level_height = level_bbox[3] - level_bbox[1]

    level_x = content_left
    level_y = content_top + 172

    badge_padding_x = 10
    badge_padding_y = 5

    draw.rectangle(
        (
            level_x,
            level_y,
            level_x + level_width + (badge_padding_x * 2),
            level_y + level_height + (badge_padding_y * 2),
        ),
        fill=SLATE_BLUE,
    )

    draw.text(
        (
            level_x + badge_padding_x,
            level_y + badge_padding_y - level_bbox[1],
        ),
        level_text,
        fill=LINEN,
        font=level_font,
    )

    # Rank motif
    if has_star_motif(rank_name):
        star_center_x = banner_right - 260
        star_center_y = toolbar_bottom + 155

        draw_filled_star(
            draw,
            star_center_x,
            star_center_y,
            62,
            LINEN,
        )

        draw_filled_star(
            draw,
            star_center_x + 96,
            star_center_y + 66,
            24,
            SOFT_PERIWINKLE,
        )

        draw_filled_star(
            draw,
            star_center_x - 92,
            star_center_y + 78,
            18,
            SLATE_BLUE,
        )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_rank_up_card("Cafe Star", 70)