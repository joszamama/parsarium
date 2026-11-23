# load_image — PNG / Rust

Pinned release: `3.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/load-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust load_image
python3 parsarium.py run png rust load_image controls/png/red-green.png
python3 parsarium.py replay png rust load_image CORPUS_DIR runs/png-load_image-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png rust load_image
python3 parsarium.py afl prepare png rust load_image runs/png-load_image-afl --fandango 100
python3 parsarium.py afl run runs/png-load_image-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
