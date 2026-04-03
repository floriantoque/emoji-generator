# emoji-generator

Generate emoji-style PNG images from the command line.

## Install & run

```bash
# From GitHub (no install needed)
uvx --from git+https://github.com/floriantoque/stamp-generator emoji-generator stamp 'HELLO;WORLD'

# Or install locally
uv pip install git+https://github.com/floriantoque/stamp-generator
emoji-generator stamp 'APPROVED' --color '#1E90FF'
```

## Usage

```bash
emoji-generator stamp 'LINE 1;LINE 2' [OPTIONS]
```

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
uv run emoji-generator stamp 'SAFETY;SOLVED !'

# Blue stamp, more rotation, heavy wear
uv run emoji-generator stamp 'DO NOT;OPEN' --rotation -15 --color '#0044CC' --noise 0.7

# Clean green stamp, no wear
uv run emoji-generator stamp 'APPROVED' --color '#228B22' --noise 0 --output approved.png

# Two-line stamp
uv run emoji-generator stamp 'STAMP;SOLVED'
```

![STAMP SOLVED example](examples/stamp_solved.png)

### Local development

```bash
uv run emoji-generator stamp 'HELLO;WORLD'
uv run emoji-generator stamp 'APPROVED' --color '#228B22' --noise 0
```

## License

MIT
