# skia-canvas — SVG / JavaScript

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/skia-canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript skia_canvas
python3 parsarium.py run svg javascript skia_canvas controls/svg/red-green.svg
python3 parsarium.py replay svg javascript skia_canvas CORPUS_DIR runs/svg-skia_canvas-replay
python3 parsarium.py afl build svg javascript skia_canvas
python3 parsarium.py afl prepare svg javascript skia_canvas runs/svg-skia_canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
