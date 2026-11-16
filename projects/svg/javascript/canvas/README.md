# canvas — SVG / JavaScript

Pinned release: `3.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript canvas
python3 parsarium.py run svg javascript canvas controls/svg/red-green.svg
python3 parsarium.py replay svg javascript canvas CORPUS_DIR runs/svg-canvas-replay
python3 parsarium.py afl build svg javascript canvas
python3 parsarium.py afl prepare svg javascript canvas runs/svg-canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
