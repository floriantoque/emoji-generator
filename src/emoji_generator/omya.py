"""Old man yells at image generation."""

import sys
from importlib.resources import files
from io import BytesIO
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image, UnidentifiedImageError


def _load_logo(source: str, filter_white: bool = True) -> Image.Image:
    """Load a logo from a URL or local path. Returns RGBA."""
    try:
        if source.startswith(("http://", "https://")):
            req = Request(source, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as resp:
                data = resp.read()
            img = Image.open(BytesIO(data))
        else:
            path = Path(source)
            if not path.exists():
                print(f"Logo file not found: {source}", file=sys.stderr)
                sys.exit(1)
            img = Image.open(path)
        img = img.convert("RGBA")
        if filter_white:
            arr = np.array(img)
            r, g, b, _ = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
            white = (r > 240) & (g > 240) & (b > 240)
            arr[white, 3] = 0
            return Image.fromarray(arr, "RGBA")
        return img
    except URLError as e:
        print(f"Could not fetch logo from {source}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Could not decode image: {source}", file=sys.stderr)
        sys.exit(1)


def generate_omya(
    logo: str,
    logo_height: int | None = None,
    logo_width: int | None = None,
    padding: int = 0,
    output: str = "omya.png",
    no_white_filter: bool = False,
) -> None:
    """Generate an old man yells at image with a logo."""
    if logo_height is None and logo_width is None:
        logo_height = 80

    logo_img = _load_logo(logo, filter_white=not no_white_filter)

    bbox = logo_img.getchannel("A").getbbox()
    if bbox is not None:
        logo_img = logo_img.crop(bbox)

    assets = files("emoji_generator.assets")
    with assets.joinpath("omya_sky.png").open("rb") as f:
        sky = Image.open(f).convert("RGBA")
    with assets.joinpath("omya_man.png").open("rb") as f:
        man = Image.open(f).convert("RGBA")

    if logo_height is not None:
        scale = logo_height / logo_img.height
        new_size = (max(1, round(logo_img.width * scale)), logo_height)
    else:
        scale = logo_width / logo_img.width
        new_size = (logo_width, max(1, round(logo_img.height * scale)))
    logo_img = logo_img.resize(new_size, Image.LANCZOS)

    base = sky.copy()
    base.paste(logo_img, (padding, padding), logo_img)
    base.alpha_composite(man)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    base.save(output, "PNG")
    print(f"Saved → {output}  ({base.size[0]}×{base.size[1]}px)")
