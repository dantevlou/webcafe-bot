from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from theme import (
    LINEN,
    MIDNIGHT_VIOLET,
    PALE_SLATE,
    SLATE_BLUE,
    SOFT_PERIWINKLE,
)


OUTPUT_PATH = Path("welcome_preview.png")

WIDTH = 720
HEIGHT = 720

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


def text_size(font, text: str) -> tuple[int, int]:
    bbox = font.getbbox(text)
    return (
        bbox[2] - bbox[0],
        bbox[3] - bbox[1],
    )


def fit_text_with_ellipsis(font, text: str, max_width: int) -> str:
    ellipsis = "..."
    text_width, _ = text_size(font, text)

    if text_width <= max_width:
        return text

    trimmed_text = text

    while trimmed_text:
        candidate = trimmed_text + ellipsis
        candidate_width, _ = text_size(font, candidate)

        if candidate_width <= max_width:
            return candidate

        trimmed_text = trimmed_text[:-1]

    return ellipsis


def create_welcome_card(
    username: str,
    avatar: Image.Image | None = None,
) -> None:
    title_bar_font = load_font(28, bold=True)
    hero_font = load_font(38, bold=True)
    body_font = load_font(27)
    body_emphasis_font = load_font(27, bold=True)
    body_bold_font = load_font(29, bold=True)
    prompt_font = load_font(27)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        SOFT_PERIWINKLE,
    )
    draw = ImageDraw.Draw(image)

    window_left = 50
    window_top = 60
    window_right = 670
    window_bottom = 660

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
    title_bar_height = title_bar_bottom - title_bar_top

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

    # Window buttons
    button_size = 22
    button_gap = 5
    button_total_width = (button_size * 3) + (button_gap * 2)

    button_start_x = (
        window_right
        - 18
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
    title_text = "webcafe.exe"

    _, title_height = text_size(
        title_bar_font,
        title_text,
    )

    title_x = window_left + 18
    title_y = (
        title_bar_top
        + (title_bar_height - title_height) // 2
        - 3
    )

    draw.text(
        (title_x, title_y),
        title_text,
        fill=LINEN,
        font=title_bar_font,
    )

    # Terminal
    terminal_left = window_left + 18
    terminal_top = title_bar_bottom + 18
    terminal_right = window_right - 18
    terminal_bottom = window_bottom - 18

    draw.rectangle(
        (
            terminal_left,
            terminal_top,
            terminal_right,
            terminal_bottom,
        ),
        fill=MIDNIGHT_VIOLET,
        outline=SLATE_BLUE,
        width=3,
    )

    text_left = terminal_left + 34
    text_right = terminal_right - 34

    # Main title
    hero_text = "WELCOME TO WEBCAFE.EXE"

    _, hero_height = text_size(
        hero_font,
        hero_text,
    )

    hero_y = terminal_top + 38

    draw.text(
        (text_left, hero_y),
        hero_text,
        fill=LINEN,
        font=hero_font,
    )

    # Divider
    divider_y = hero_y + hero_height + 18

    draw.line(
        (
            text_left,
            divider_y,
            text_right,
            divider_y,
        ),
        fill=PALE_SLATE,
        width=2,
    )

    # Terminal information
    body_start_y = divider_y + 28
    line_step = 46

    # Avatar
    avatar_size = 124
    avatar_left = text_right - avatar_size
    avatar_top = body_start_y + 4
    avatar_border = 8

    if avatar is not None:
        draw.ellipse(
            (
                avatar_left - avatar_border,
                avatar_top - avatar_border,
                avatar_left + avatar_size + avatar_border,
                avatar_top + avatar_size + avatar_border,
             ),
             fill=LINEN,
        )

        avatar_image = ImageOps.fit(
            avatar,
            (avatar_size, avatar_size),
        )

        avatar_mask = Image.new(
            "L",
            (avatar_size, avatar_size),
            0,
        )
        avatar_mask_draw = ImageDraw.Draw(avatar_mask)
        avatar_mask_draw.ellipse(
            (0, 0, avatar_size, avatar_size),
            fill=255,
        )

        image.paste(
            avatar_image,
            (avatar_left, avatar_top),
            avatar_mask,
        )

    # Username
    welcome_prefix = ">> welcome, "

    normal_lines = [
        ">> session initialised",
        ">> status: guest",
    ]

    current_y = body_start_y

    draw.text(
        (text_left, current_y),
        welcome_prefix,
        fill=LINEN,
        font=body_font,
    )

    welcome_prefix_width, _ = text_size(
        body_font,
        welcome_prefix,
    )

    username_left = text_left + welcome_prefix_width
    username_right = avatar_left - 18
    username_max_width = username_right - username_left

    username_width, _ = text_size(
        body_emphasis_font,
        username,
    )

    username_fits_first_line = username_width <= username_max_width

    username_second_line = ""

    if not username_fits_first_line:
        second_line_max_width = avatar_left - 18 - text_left
        username_second_line = fit_text_with_ellipsis(
            body_emphasis_font,
            username,
            second_line_max_width,
        )

    if username_fits_first_line:
        draw.text(
            (username_left, current_y),
            username,
            fill=SOFT_PERIWINKLE,
            font=body_emphasis_font,
        )

        current_y += line_step
    else:
        current_y += line_step

        draw.text(
            (text_left, current_y),
            username_second_line,
            fill=SOFT_PERIWINKLE,
            font=body_emphasis_font,
        )

        current_y += line_step

    for line in normal_lines:
        draw.text(
            (text_left, current_y),
            line,
            fill=PALE_SLATE,
            font=body_font,
        )

        current_y += line_step

    # Important instruction
    draw.text(
        (text_left, current_y),
        ">> OPEN #USER-SETTINGS",
        fill=LINEN,
        font=body_bold_font,
    )

    current_y += line_step + 4

    draw.text(
        (text_left, current_y),
        ">> choose one colour.css",
        fill=PALE_SLATE,
        font=body_font,
    )

    # Terminal prompt
    prompt_text = "guest@webcafe:~$"
    prompt_y = current_y + 76

    draw.text(
        (text_left, prompt_y),
        prompt_text,
        fill=LINEN,
        font=prompt_font,
    )

    prompt_width, _ = text_size(
        prompt_font,
        prompt_text,
    )

    prompt_bbox = draw.textbbox(
        (text_left, prompt_y),
        prompt_text,
        font=prompt_font,
    )

    prompt_top = prompt_bbox[1]
    prompt_bottom = prompt_bbox[3]
    prompt_visual_height = prompt_bottom - prompt_top

    # Cursor
    cursor_width = 13
    cursor_height = 27

    cursor_x = (
        text_left
        + prompt_width
        + 12
    )

    cursor_y = (
        prompt_top
        + (prompt_visual_height - cursor_height) // 2
    )

    draw.rectangle(
        (
            cursor_x,
            cursor_y,
            cursor_x + cursor_width,
            cursor_y + cursor_height,
        ),
        fill=SOFT_PERIWINKLE,
    )

    image.save(OUTPUT_PATH)

    print(f"Saved preview to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_welcome_card("test_user")
