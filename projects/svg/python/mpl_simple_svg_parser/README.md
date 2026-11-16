# mpl-simple-svg-parser — SVG / Python

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/mpl-simple-svg-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python mpl_simple_svg_parser
python3 parsarium.py run svg python mpl_simple_svg_parser controls/svg/red-green.svg
python3 parsarium.py replay svg python mpl_simple_svg_parser CORPUS_DIR runs/svg-mpl_simple_svg_parser-replay
python3 parsarium.py afl build svg python mpl_simple_svg_parser
python3 parsarium.py afl prepare svg python mpl_simple_svg_parser runs/svg-mpl_simple_svg_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
