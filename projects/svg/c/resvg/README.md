# resvg — SVG / C

Pinned release: `0.50.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c resvg
python3 parsarium.py run svg c resvg controls/svg/red-green.svg
python3 parsarium.py replay svg c resvg CORPUS_DIR runs/svg-resvg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg c resvg
python3 parsarium.py afl prepare svg c resvg runs/svg-resvg-afl --fandango 100
python3 parsarium.py afl run runs/svg-resvg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** The AFL++ target uses one-shot /work/replay @@ because the selected C API parses a local file; parser-source feedback comes from usvg Rust code.
