# svg-eslint-parser — SVG / JavaScript

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/svg-eslint-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript svg_eslint_parser
python3 parsarium.py run svg javascript svg_eslint_parser controls/svg/red-green.svg
python3 parsarium.py replay svg javascript svg_eslint_parser CORPUS_DIR runs/svg-svg_eslint_parser-replay
python3 parsarium.py afl build svg javascript svg_eslint_parser
python3 parsarium.py afl prepare svg javascript svg_eslint_parser runs/svg-svg_eslint_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
