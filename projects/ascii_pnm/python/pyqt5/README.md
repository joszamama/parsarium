# PyQt5 — ASCII PNM / Python

Pinned release: `5.15.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pyqt5/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pyqt5
python3 parsarium.py run ascii_pnm python pyqt5 controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pyqt5 CORPUS_DIR runs/ascii_pnm-pyqt5-replay
python3 parsarium.py afl build ascii_pnm python pyqt5
python3 parsarium.py afl prepare ascii_pnm python pyqt5 runs/ascii_pnm-pyqt5-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libQt5Gui.so.5` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
