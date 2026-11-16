# @resvg/resvg-js — SVG / JavaScript

Pinned release: `2.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/resvg-resvg-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript resvg_resvg_js
python3 parsarium.py run svg javascript resvg_resvg_js controls/svg/red-green.svg
python3 parsarium.py replay svg javascript resvg_resvg_js CORPUS_DIR runs/svg-resvg_resvg_js-replay
python3 parsarium.py afl build svg javascript resvg_resvg_js
python3 parsarium.py afl prepare svg javascript resvg_resvg_js runs/svg-resvg_resvg_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
