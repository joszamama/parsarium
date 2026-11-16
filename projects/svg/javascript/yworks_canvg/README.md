# @yworks/canvg — SVG / JavaScript

Pinned release: `4.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/yworks-canvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript yworks_canvg
python3 parsarium.py run svg javascript yworks_canvg controls/svg/red-green.svg
python3 parsarium.py replay svg javascript yworks_canvg CORPUS_DIR runs/svg-yworks_canvg-replay
python3 parsarium.py afl build svg javascript yworks_canvg
python3 parsarium.py afl prepare svg javascript yworks_canvg runs/svg-yworks_canvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
