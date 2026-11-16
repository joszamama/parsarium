# svg2img — SVG / JavaScript

Pinned release: `1.0.0-beta.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/svg2img/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript svg2img
python3 parsarium.py run svg javascript svg2img controls/svg/red-green.svg
python3 parsarium.py replay svg javascript svg2img CORPUS_DIR runs/svg-svg2img-replay
python3 parsarium.py afl build svg javascript svg2img
python3 parsarium.py afl prepare svg javascript svg2img runs/svg-svg2img-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
