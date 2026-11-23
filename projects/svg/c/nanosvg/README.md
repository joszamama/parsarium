# nanosvg — SVG / C

Pinned release: `2023-12-29`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/nanosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c nanosvg
python3 parsarium.py run svg c nanosvg controls/svg/red-green.svg
python3 parsarium.py replay svg c nanosvg CORPUS_DIR runs/svg-nanosvg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg c nanosvg
python3 parsarium.py afl prepare svg c nanosvg runs/svg-nanosvg-afl --fandango 100
python3 parsarium.py afl run runs/svg-nanosvg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
