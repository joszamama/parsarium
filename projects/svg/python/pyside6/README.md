# PySide6 — SVG / Python

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pyside6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pyside6
python3 parsarium.py run svg python pyside6 controls/svg/red-green.svg
python3 parsarium.py replay svg python pyside6 CORPUS_DIR runs/svg-pyside6-replay
python3 parsarium.py afl build svg python pyside6
python3 parsarium.py afl prepare svg python pyside6 runs/svg-pyside6-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
