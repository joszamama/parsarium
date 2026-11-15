# plutosvg — SVG / C++

Pinned release: `0.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/plutosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp plutosvg
python3 parsarium.py run svg cpp plutosvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp plutosvg CORPUS_DIR runs/svg-plutosvg-replay
python3 parsarium.py afl build svg cpp plutosvg
python3 parsarium.py afl prepare svg cpp plutosvg runs/svg-plutosvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
