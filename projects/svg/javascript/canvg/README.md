# canvg — SVG / JavaScript

Pinned release: `4.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/canvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript canvg
python3 parsarium.py run svg javascript canvg controls/svg/red-green.svg
python3 parsarium.py replay svg javascript canvg CORPUS_DIR runs/svg-canvg-replay
python3 parsarium.py afl build svg javascript canvg
python3 parsarium.py afl prepare svg javascript canvg runs/svg-canvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
