# pngjs-nozlib — PNG / JavaScript

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/pngjs-nozlib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript pngjs_nozlib
python3 parsarium.py run png javascript pngjs_nozlib controls/png/red-green.png
python3 parsarium.py replay png javascript pngjs_nozlib CORPUS_DIR runs/png-pngjs_nozlib-replay
python3 parsarium.py afl build png javascript pngjs_nozlib
python3 parsarium.py afl prepare png javascript pngjs_nozlib runs/png-pngjs_nozlib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
