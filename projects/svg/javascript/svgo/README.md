# svgo — SVG / JavaScript

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/svgo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript svgo
python3 parsarium.py run svg javascript svgo controls/svg/red-green.svg
python3 parsarium.py replay svg javascript svgo CORPUS_DIR runs/svg-svgo-replay
python3 parsarium.py afl build svg javascript svgo
python3 parsarium.py afl prepare svg javascript svgo runs/svg-svgo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
