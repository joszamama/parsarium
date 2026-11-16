# PySide6 — ASCII PNM / Python

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pyside6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pyside6
python3 parsarium.py run ascii_pnm python pyside6 controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pyside6 CORPUS_DIR runs/ascii_pnm-pyside6-replay
python3 parsarium.py afl build ascii_pnm python pyside6
python3 parsarium.py afl prepare ascii_pnm python pyside6 runs/ascii_pnm-pyside6-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libQt6Gui.so.6` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
