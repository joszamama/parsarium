# zune-png — PNG / Rust

Pinned release: `0.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/zune-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust zune_png
python3 parsarium.py run png rust zune_png controls/png/red-green.png
python3 parsarium.py replay png rust zune_png CORPUS_DIR runs/png-zune_png-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png rust zune_png
python3 parsarium.py afl prepare png rust zune_png runs/png-zune_png-afl --fandango 100
python3 parsarium.py afl run runs/png-zune_png-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
