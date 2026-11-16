# pngjs-image — PNG / JavaScript

Pinned release: `0.11.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/pngjs-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript pngjs_image
python3 parsarium.py run png javascript pngjs_image controls/png/red-green.png
python3 parsarium.py replay png javascript pngjs_image CORPUS_DIR runs/png-pngjs_image-replay
python3 parsarium.py afl build png javascript pngjs_image
python3 parsarium.py afl prepare png javascript pngjs_image runs/png-pngjs_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
