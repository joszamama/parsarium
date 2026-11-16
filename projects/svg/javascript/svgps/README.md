# svgps — SVG / JavaScript

Pinned release: `0.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/svgps/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript svgps
python3 parsarium.py run svg javascript svgps controls/svg/red-green.svg
python3 parsarium.py replay svg javascript svgps CORPUS_DIR runs/svg-svgps-replay
python3 parsarium.py afl build svg javascript svgps
python3 parsarium.py afl prepare svg javascript svgps runs/svg-svgps-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
