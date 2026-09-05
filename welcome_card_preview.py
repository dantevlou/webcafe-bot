from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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


def create_welcome_card() -> None:
    title_bar_font = load_font(28, bold=True)
    hero_font = load_font(38, bold=True)
    body_font = load_font(27)
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

    normal_lines = [
        ">> welcome, new user",
        ">> session initailised",
        ">> status: guest",
    ]

    current_y = body_start_y

    for index, line in enumerate(normal_lines):
        draw.text(
            (text_left, current_y),
            line,
            fill=(
                LINEN
                if index == 0
                else PALE_SLATE
            ),
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
    create_welcome_card()
