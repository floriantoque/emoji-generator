"""Rubber stamp image generation."""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

STAMP_W, STAMP_H = 900, 560


def _find_font() -> str:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    print("No suitable font found.", file=sys.stderr)
    sys.exit(1)


def _parse_color(color: str) -> tuple[int, int, int, int]:
    """Parse hex color (#RRGGBB or #RGB) to RGBA tuple."""
    c = color.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6:
        print(f"Invalid color: {color}. Use hex like #FF2828", file=sys.stderr)
        sys.exit(1)
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (r, g, b, 255)


def _best_font(
    text: str, font_path: str, max_w: int, max_h: int, ratio: float = 0.92,
) -> tuple[ImageFont.FreeTypeFont, int]:
    """Find largest font size that fits text within max_w x max_h."""
    font_index = 1 if font_path.endswith(".ttc") else 0
    for fs in range(400, 40, -1):
        font = ImageFont.truetype(font_path, fs, index=font_index)
        bb = font.getbbox(text)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w <= max_w * ratio and h <= max_h:
            return font, h
    raise ValueError(f"Text too long to fit: {text!r}")


def _apply_wear(stamp: Image.Image, noise: float) -> Image.Image:
    """Apply ink-stain wear effect using seed-based clustering."""
    arr = np.array(stamp)
    rng = np.random.default_rng(42)

    ink_mask = arr[:, :, 3] > 0
    ink_pixels = np.argwhere(ink_mask)
    if len(ink_pixels) == 0:
        return stamp

    n_seeds = max(10, int(60 * noise))
    seed_indices = rng.choice(len(ink_pixels), min(n_seeds, len(ink_pixels)), replace=False)
    seeds = ink_pixels[seed_indices].astype(np.float32)

    coords = ink_pixels.astype(np.float32)
    chunk_size = 50_000
    min_dists = np.empty(len(coords), dtype=np.float32)

    for i in range(0, len(coords), chunk_size):
        chunk = coords[i : i + chunk_size]
        diffs = chunk[:, np.newaxis, :] - seeds[np.newaxis, :, :]
        dists = np.sqrt((diffs ** 2).sum(axis=2))
        min_dists[i : i + chunk_size] = dists.min(axis=1)

    radius = max(20.0, 80.0 * noise)
    prob = np.exp(-min_dists / radius)
    prob *= min(noise * 1.5, 1.0)

    remove = rng.random(len(prob)) < prob
    arr[ink_pixels[remove, 0], ink_pixels[remove, 1], 3] = 0

    return Image.fromarray(arr.astype("uint8"), "RGBA")


def generate_stamp(
    text: str,
    rotation: float = 12,
    color: str = "#FF2828",
    noise: float = 0.3,
    output: str = "stamp.png",
) -> None:
    """Generate a rubber stamp PNG."""
    lines = [line.strip() for line in text.split(";") if line.strip()]
    if not lines:
        print("No text provided.", file=sys.stderr)
        sys.exit(1)

    rgba = _parse_color(color)
    font_path = _find_font()

    stamp = Image.new("RGBA", (STAMP_W, STAMP_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stamp)

    margin_out, margin_in = 24, 44
    radius_out, radius_in = 48, 32
    border_out, border_in = 16, 8

    draw.rounded_rectangle(
        [margin_out, margin_out, STAMP_W - margin_out, STAMP_H - margin_out],
        radius=radius_out, outline=rgba, width=border_out,
    )
    draw.rounded_rectangle(
        [margin_in, margin_in, STAMP_W - margin_in, STAMP_H - margin_in],
        radius=radius_in, outline=rgba, width=border_in,
    )

    inner_x0 = margin_in + border_in + 10
    inner_x1 = STAMP_W - margin_in - border_in - 10
    inner_y0 = margin_in + border_in + 10
    inner_y1 = STAMP_H - margin_in - border_in - 10
    max_text_w = inner_x1 - inner_x0
    max_text_h = inner_y1 - inner_y0

    n_lines = len(lines)
    gap = max(10, 50 - (n_lines - 2) * 15) if n_lines > 1 else 0
    per_line_h = (max_text_h - gap * max(n_lines - 1, 0)) // n_lines

    fonts_and_heights = [_best_font(line, font_path, max_text_w, per_line_h) for line in lines]

    total_h = sum(h for _, h in fonts_and_heights) + gap * max(n_lines - 1, 0)
    y = inner_y0 + (max_text_h - total_h) / 2
    cx = STAMP_W // 2

    for line, (font, h) in zip(lines, fonts_and_heights):
        bb = font.getbbox(line)
        draw.text((cx - (bb[2] - bb[0]) // 2 - bb[0], y - bb[1]), line, font=font, fill=rgba)
        y += h + gap

    if noise > 0:
        stamp = _apply_wear(stamp, noise)

    rotated = stamp.rotate(rotation, expand=True, resample=Image.BICUBIC)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    rotated.save(output, "PNG")
    print(f"Saved → {output}  ({rotated.size[0]}×{rotated.size[1]}px)")
