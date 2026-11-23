# PyQt6 — SVG / Python

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pyqt6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pyqt6
python3 parsarium.py run svg python pyqt6 controls/svg/red-green.svg
python3 parsarium.py replay svg python pyqt6 CORPUS_DIR runs/svg-pyqt6-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg python pyqt6
python3 parsarium.py afl prepare svg python pyqt6 runs/svg-pyqt6-afl --fandango 100
python3 parsarium.py afl run runs/svg-pyqt6-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
