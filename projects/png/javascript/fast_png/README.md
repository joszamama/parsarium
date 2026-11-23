# fast-png — PNG / JavaScript

Pinned release: `8.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/fast-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript fast_png
python3 parsarium.py run png javascript fast_png controls/png/red-green.png
python3 parsarium.py replay png javascript fast_png CORPUS_DIR runs/png-fast_png-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png javascript fast_png
python3 parsarium.py afl prepare png javascript fast_png runs/png-fast_png-afl --fandango 100
python3 parsarium.py afl run runs/png-fast_png-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
