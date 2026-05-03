# emoji-generator

Generate emoji-style PNG images from the command line.

## Features

This tool provides multiple commands to create fun, customizable PNG images:

- **stamp** — Generate rubber stamp images with text, rotation, and wear effects
- **old man yells at** (omya) — Create "old man yells at cloud" style images with custom logos

New features will be added based on user requests.

## Install & run

### Option 1: Quick run with uvx (no installation)

```bash
# Stamp
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator stamp 'HELLO;WORLD'

# Old man yells at
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator omya 'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'
```

### Option 2: Local development with uv sync

```bash
git clone https://github.com/floriantoque/emoji-generator
cd emoji-generator
uv sync

# Then use commands directly
uv run emoji-generator stamp 'APPROVED' --color '#1E90FF'
uv run emoji-generator omya './mylogo.png'
```

### What you can create

<div align="center">
  <img src="examples/stamp_solved.png" width="250" alt="Stamp example" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="examples/omya.png" width="180" alt="Old man yells at example" />
</div>

## Stamp

Generate rubber stamp PNG images with customizable text, rotation, and wear effects.

```bash
emoji-generator stamp 'LINE 1;LINE 2' [OPTIONS]
```

### Example output

![Stamp example](examples/stamp_solved.png)

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--rotation` | `12` | Angle in degrees |
| `--color` | `#FF2828` | Hex color of the stamp ink |
| `--noise` | `0.3` | Wear intensity: 0.0 (clean) to 1.0 (heavy) |
| `--output` | `stamp.png` | Output PNG file path |

### Examples

```bash
# Red stamp, default settings
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator stamp 'SAFETY;SOLVED !'

# Blue stamp, more rotation, heavy wear
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator stamp 'DO NOT;OPEN' --rotation -15 --color '#0044CC' --noise 0.7

# Clean green stamp, no wear
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator stamp 'APPROVED' --color '#228B22' --noise 0 --output approved.png

# Two-line stamp
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator stamp 'STAMP;SOLVED'
```

## Old man yells at

Create "old man yells at" style images with a logo. The logo is composited into the scene while Grandpa Simpson stays on top, creating a layered effect.

```bash
emoji-generator omya <LOGO> [OPTIONS]
```

`<LOGO>` is either a URL (`http://` / `https://`) or a local file path — auto-detected.

### Example output

![Old man yells at example](examples/omya.png)

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--logo-height` | `80` | Logo height in pixels (width scales to preserve aspect ratio) |
| `--logo-width` | — | Logo width in pixels (height scales to preserve aspect ratio). Overrides `--logo-height` if both set. |
| `--padding` | `0` | Pixels of padding from top and left edges |
| `--no-white-filter` | — | Keep white pixels instead of making them transparent |
| `--output` | `omya.png` | Output PNG file path |

### Examples

```bash
# Logo from a URL, default size
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator omya 'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'

# Logo from a local file, custom output
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator omya './mylogo.png' --output yelled_at.png

# Constrain by height (width scales)
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator omya './mylogo.png' --logo-height 120 --padding 10

# Constrain by width (height scales)
uvx --from git+https://github.com/floriantoque/emoji-generator emoji-generator omya './mylogo.png' --logo-width 150
```

## License

MIT
