# png-js — PNG / JavaScript

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/png-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript png_js
python3 parsarium.py run png javascript png_js controls/png/red-green.png
python3 parsarium.py replay png javascript png_js CORPUS_DIR runs/png-png_js-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png javascript png_js
python3 parsarium.py afl prepare png javascript png_js runs/png-png_js-afl --fandango 100
python3 parsarium.py afl run runs/png-png_js-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
