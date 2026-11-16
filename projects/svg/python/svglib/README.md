# svglib — SVG / Python

Pinned release: `2.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/svglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python svglib
python3 parsarium.py run svg python svglib controls/svg/red-green.svg
python3 parsarium.py replay svg python svglib CORPUS_DIR runs/svg-svglib-replay
python3 parsarium.py afl build svg python svglib
python3 parsarium.py afl prepare svg python svglib runs/svg-svglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
