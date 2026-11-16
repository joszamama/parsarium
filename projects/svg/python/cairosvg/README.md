# CairoSVG — SVG / Python

Pinned release: `2.9.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/cairosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python cairosvg
python3 parsarium.py run svg python cairosvg controls/svg/red-green.svg
python3 parsarium.py replay svg python cairosvg CORPUS_DIR runs/svg-cairosvg-replay
python3 parsarium.py afl build svg python cairosvg
python3 parsarium.py afl prepare svg python cairosvg runs/svg-cairosvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
