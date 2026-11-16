# sharp — SVG / JavaScript

Pinned release: `0.35.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/sharp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript sharp
python3 parsarium.py run svg javascript sharp controls/svg/red-green.svg
python3 parsarium.py replay svg javascript sharp CORPUS_DIR runs/svg-sharp-replay
python3 parsarium.py afl build svg javascript sharp
python3 parsarium.py afl prepare svg javascript sharp runs/svg-sharp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
