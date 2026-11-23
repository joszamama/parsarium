# fop-core — SVG / Java

Pinned release: `2.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/fop-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java fop_core
python3 parsarium.py run svg java fop_core controls/svg/red-green.svg
python3 parsarium.py replay svg java fop_core CORPUS_DIR runs/svg-fop_core-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg java fop_core
python3 parsarium.py afl prepare svg java fop_core runs/svg-fop_core-afl --fandango 100
python3 parsarium.py afl run runs/svg-fop_core-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
