# pngjs — PNG / JavaScript

Pinned release: `7.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/pngjs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript pngjs
python3 parsarium.py run png javascript pngjs controls/png/red-green.png
python3 parsarium.py replay png javascript pngjs CORPUS_DIR runs/png-pngjs-replay
python3 parsarium.py afl build png javascript pngjs
python3 parsarium.py afl prepare png javascript pngjs runs/png-pngjs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
