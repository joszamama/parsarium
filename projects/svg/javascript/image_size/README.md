# image-size — SVG / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/image-size/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript image_size
python3 parsarium.py run svg javascript image_size controls/svg/red-green.svg
python3 parsarium.py replay svg javascript image_size CORPUS_DIR runs/svg-image_size-replay
python3 parsarium.py afl build svg javascript image_size
python3 parsarium.py afl prepare svg javascript image_size runs/svg-image_size-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
