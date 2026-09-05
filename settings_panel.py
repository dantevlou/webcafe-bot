from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from theme import (
    LINEN,
    MIDNIGHT_VIOLET,
    PALE_SLATE,
    SLATE_BLUE,
    SOFT_PERIWINKLE,
)


OUTPUT_PATH = Path("settings_panel.png")

WIDTH = 920
HEIGHT = 620

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


def create_settings_panel() -> None:
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )
    draw = ImageDraw.Draw(image)

    window_left = 50
    window_top = 50
    window_right = 870
    window_bottom = 560

    # Window shadow
    draw.rectangle(
        (
            window_left + 12,
            window_top + 12,
            window_right + 12,
            window_bottom + 12,
        ),
        fill=MIDNIGHT_VIOLET,
    )

    # Main window
    draw.rectangle(
        (
            window_left,
            window_top,
            window_right,
            window_bottom,
        ),
        fill=PALE_SLATE,
        outline=MIDNIGHT_VIOLET,
        width=4,
    )

    # Title bar
    title_bar_top = window_top + 5
    title_bar_bottom = window_top + 56

    draw.rectangle(
        (
            window_left + 5,
            title_bar_top,
            window_right - 5,
            title_bar_bottom,
        ),
        fill=SLATE_BLUE,
        outline=MIDNIGHT_VIOLET,
        width=3,
    )

    title_bar_font = load_font(24, bold=True)

    # Window buttons
    button_size = 22
    button_gap = 5
    button_total_width = (button_size * 3) + (button_gap * 2)

    button_start_x = (
        window_right
        - 18
        - button_total_width
    )

    button_y = title_bar_top + 12

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
    second_button_x = button_start_x + button_size + button_gap
    third_button_x = button_start_x + (button_size + button_gap) * 2

    # Minimise
    draw.line(
        (
            first_button_x + 5,
            button_y + 15,
            first_button_x + 17,
            button_y + 15,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    # Maximise
    draw.rectangle(
        (
            second_button_x + 5,
            button_y + 5,
            second_button_x + 17,
            button_y + 17,
        ),
        outline=MIDNIGHT_VIOLET,
        width=2,
    )

    # Close
    draw.line(
        (
            third_button_x + 5,
            button_y + 5,
            third_button_x + 17,
            button_y + 17,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    draw.line(
        (
            third_button_x + 17,
            button_y + 5,
            third_button_x + 5,
            button_y + 17,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    # Title-bar text
    draw.text(
        (window_left + 18, title_bar_top + 10),
        "webcafe.exe // user settings",
        fill=LINEN,
        font=title_bar_font,
    )

    heading_font = load_font(32, bold=True)
    section_font = load_font(22, bold=True)
    body_font = load_font(17)

    # Settings heading
    draw.text(
        (window_left + 28, title_bar_bottom + 32),
        "USER SETTINGS",
        fill=MIDNIGHT_VIOLET,
        font=heading_font,
    )

    draw.text(
        (window_left + 28, title_bar_bottom + 72),
        "customise your webcafe profile",
        fill=SLATE_BLUE,
        font=body_font,
    )

    # Settings modules
    modules = [
        (
            "01 // colour.css",
            "choose your colour",
            "REQUIRED",
        ),
        (
            "02 // pronouns.ini",
            "choose your pronouns",
            "OPTIONAL",
        ),
        (
            "03 // region.sys",
            "choose your location",
            "OPTIONAL",
        ),
        (
            "04 // platforms.cfg",
            "select your gaming platforms",
            "OPTIONAL",
        ),
    ]

    content_left = window_left + 28
    content_right = window_right - 28

    column_gap = 16
    module_width = (
        content_right
        - content_left
        - column_gap
    ) // 2

    module_height = 82
    row_gap = 14
    module_start_y = title_bar_bottom + 118

    for index, (title, description, badge_text) in enumerate(modules):
        column = index % 2
        row = index // 2

        module_left = (
            content_left
            + column * (module_width + column_gap)
        )
        module_top = (
            module_start_y
            + row * (module_height + row_gap)
        )
        module_right = module_left + module_width
        module_bottom = module_top + module_height

        draw.rectangle(
            (
                module_left,
                module_top,
                module_right,
                module_bottom,
            ),
            fill=LINEN,
            outline=MIDNIGHT_VIOLET,
            width=3,
        )

        draw.text(
            (module_left + 14, module_top + 13),
            title,
            fill=MIDNIGHT_VIOLET,
            font=section_font,
        )

        draw.text(
            (module_left + 14, module_top + 48),
            description,
            fill=SLATE_BLUE,
            font=body_font,
        )

        badge_width = 88
        badge_height = 24
        badge_left = module_right - badge_width - 12
        badge_top = module_top + 12

        draw.rectangle(
            (
                badge_left,
                badge_top,
                badge_left + badge_width,
                badge_top + badge_height,
            ),
            fill=(
                SOFT_PERIWINKLE
                if badge_text == "REQUIRED"
                else PALE_SLATE
            ),
            outline=MIDNIGHT_VIOLET,
            width=2,
        )

        draw.text(
            (badge_left + 7, badge_top + 3),
            badge_text,
            fill=MIDNIGHT_VIOLET,
            font=body_font,
        )

    # Games module
    games_top = (
        module_start_y
        + 2 * (module_height + row_gap)
    )
    games_bottom = games_top + module_height

    draw.rectangle(
        (
            content_left,
            games_top,
            content_right,
            games_bottom,
        ),
        fill=LINEN,
        outline=MIDNIGHT_VIOLET,
        width=3,
    )

    draw.text(
        (content_left + 14, games_top + 13),
        "05 // games.lst",
        fill=MIDNIGHT_VIOLET,
        font=section_font,
    )

    draw.text(
        (content_left + 14, games_top + 48),
        "select the games you play",
        fill=SLATE_BLUE,
        font=body_font,
    )

    badge_width = 88
    badge_left = content_right - badge_width - 12
    badge_top = games_top + 12

    draw.rectangle(
        (
            badge_left,
            badge_top,
            badge_left + badge_width,
            badge_top + 24,
        ),
        fill=PALE_SLATE,
        outline=MIDNIGHT_VIOLET,
        width=2,
    )

    draw.text(
        (badge_left + 7, badge_top + 3),
        "OPTIONAL",
        fill=MIDNIGHT_VIOLET,
        font=body_font,
    )

    # Status bar
    status_top = window_bottom - 48

    draw.line(
        (
            window_left + 18,
            status_top,
            window_right - 18,
            status_top,
        ),
        fill=MIDNIGHT_VIOLET,
        width=2,
    )

    draw.text(
        (window_left + 28, status_top + 14),
        "changes save automatically",
        fill=SLATE_BLUE,
        font=body_font,
    )

    draw.text(
        (window_right - 228, status_top + 14),
        "controls below ↓",
        fill=MIDNIGHT_VIOLET,
        font=body_font,
    )

    image.save(OUTPUT_PATH)


if __name__ == "__main__":
    create_settings_panel()