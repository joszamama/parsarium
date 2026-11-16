# get-svg-colors — SVG / JavaScript

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/get-svg-colors/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript get_svg_colors
python3 parsarium.py run svg javascript get_svg_colors controls/svg/red-green.svg
python3 parsarium.py replay svg javascript get_svg_colors CORPUS_DIR runs/svg-get_svg_colors-replay
python3 parsarium.py afl build svg javascript get_svg_colors
python3 parsarium.py afl prepare svg javascript get_svg_colors runs/svg-get_svg_colors-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
