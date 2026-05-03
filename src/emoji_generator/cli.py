"""Emoji Generator — generates emoji-style PNG images."""

import cyclopts

from .omya import generate_omya
from .stamp import generate_stamp

app = cyclopts.App(
    name="emoji-generator",
    help="Generate emoji-style PNG images.",
)


@app.command
def stamp(
    text: str,
    *,
    rotation: float = 12,
    color: str = "#FF2828",
    noise: float = 0.3,
    output: str = "stamp.png",
):
    """Generate a rubber stamp PNG.

    Parameters
    ----------
    text
        Stamp text. Use ';' to separate lines.
    rotation
        Rotation angle in degrees (positive = counter-clockwise).
    color
        Stamp ink color in hex format (e.g. #FF2828).
    noise
        Wear intensity from 0.0 (clean) to 1.0 (heavy wear).
    output
        Output PNG file path.
    """
    generate_stamp(text, rotation=rotation, color=color, noise=noise, output=output)


@app.command
def omya(
    logo: str,
    *,
    logo_height: int | None = None,
    logo_width: int | None = None,
    padding: int = 0,
    output: str = "omya.png",
    no_white_filter: bool = False,
):
    """Generate an "old man yells at" image with a logo.

    Composes three layers: sky background, the logo pasted near the top-left,
    and Grandpa Simpson on top — so the logo visually appears behind the
    character.

    Parameters
    ----------
    logo
        URL (http/https) or local path to a logo image.
    logo_height
        Logo height in pixels (width scales to preserve aspect ratio).
        Default 80 if neither --logo-height nor --logo-width is set.
    logo_width
        Logo width in pixels (height scales to preserve aspect ratio).
    padding
        Pixels of padding from the top and left edges.
    output
        Output PNG file path.
    no_white_filter
        Keep white pixels instead of making them transparent.
    """
    generate_omya(
        logo,
        logo_height=logo_height,
        logo_width=logo_width,
        padding=padding,
        output=output,
        no_white_filter=no_white_filter,
    )


def main():
    app()
