# PyQt6 — ASCII PNM / Python

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pyqt6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pyqt6
python3 parsarium.py run ascii_pnm python pyqt6 controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pyqt6 CORPUS_DIR runs/ascii_pnm-pyqt6-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_pnm python pyqt6
python3 parsarium.py afl prepare ascii_pnm python pyqt6 runs/ascii_pnm-pyqt6-afl --fandango 100
python3 parsarium.py afl run runs/ascii_pnm-pyqt6-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Feedback scope:** AFL++ observes edges in the pinned `libQt6Gui.so.6` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
