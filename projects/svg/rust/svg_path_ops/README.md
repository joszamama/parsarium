# svg_path_ops — SVG / Rust

Pinned release: `0.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svg-path-ops/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svg_path_ops
python3 parsarium.py run svg rust svg_path_ops controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust svg_path_ops CORPUS_DIR runs/svg-svg_path_ops-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg rust svg_path_ops
python3 parsarium.py afl prepare svg rust svg_path_ops runs/svg-svg_path_ops-afl --fandango 100
python3 parsarium.py afl run runs/svg-svg_path_ops-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
