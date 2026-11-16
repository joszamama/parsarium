# postsvg — SVG / JavaScript

Pinned release: `2.2.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/postsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript postsvg
python3 parsarium.py run svg javascript postsvg controls/svg/red-green.svg
python3 parsarium.py replay svg javascript postsvg CORPUS_DIR runs/svg-postsvg-replay
python3 parsarium.py afl build svg javascript postsvg
python3 parsarium.py afl prepare svg javascript postsvg runs/svg-postsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
