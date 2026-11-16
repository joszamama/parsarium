# skia-canvas — PNG / JavaScript

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/skia-canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript skia_canvas
python3 parsarium.py run png javascript skia_canvas controls/png/red-green.png
python3 parsarium.py replay png javascript skia_canvas CORPUS_DIR runs/png-skia_canvas-replay
python3 parsarium.py afl build png javascript skia_canvas
python3 parsarium.py afl prepare png javascript skia_canvas runs/png-skia_canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
