# svgson — SVG / JavaScript

Pinned release: `5.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/svgson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript svgson
python3 parsarium.py run svg javascript svgson controls/svg/red-green.svg
python3 parsarium.py replay svg javascript svgson CORPUS_DIR runs/svg-svgson-replay
python3 parsarium.py afl build svg javascript svgson
python3 parsarium.py afl prepare svg javascript svgson runs/svg-svgson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
