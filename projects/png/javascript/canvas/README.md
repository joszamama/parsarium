# canvas — PNG / JavaScript

Pinned release: `3.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/canvas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript canvas
python3 parsarium.py run png javascript canvas controls/png/red-green.png
python3 parsarium.py replay png javascript canvas CORPUS_DIR runs/png-canvas-replay
python3 parsarium.py afl build png javascript canvas
python3 parsarium.py afl prepare png javascript canvas runs/png-canvas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
