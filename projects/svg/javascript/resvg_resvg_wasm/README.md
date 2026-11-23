# @resvg/resvg-wasm — SVG / JavaScript

Pinned release: `2.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/javascript/resvg-resvg-wasm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg javascript resvg_resvg_wasm
python3 parsarium.py run svg javascript resvg_resvg_wasm controls/svg/red-green.svg
python3 parsarium.py replay svg javascript resvg_resvg_wasm CORPUS_DIR runs/svg-resvg_resvg_wasm-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg javascript resvg_resvg_wasm
python3 parsarium.py afl prepare svg javascript resvg_resvg_wasm runs/svg-resvg_resvg_wasm-afl --fandango 100
python3 parsarium.py afl run runs/svg-resvg_resvg_wasm-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
