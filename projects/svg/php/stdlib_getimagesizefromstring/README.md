# getimagesizefromstring — SVG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/svg/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build svg php stdlib_getimagesizefromstring
python3 parsarium.py run svg php stdlib_getimagesizefromstring controls/svg/red-green.svg
python3 parsarium.py replay svg php stdlib_getimagesizefromstring CORPUS_DIR runs/svg-stdlib_getimagesizefromstring-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php stdlib_getimagesizefromstring
python3 parsarium.py afl prepare svg php stdlib_getimagesizefromstring runs/svg-stdlib_getimagesizefromstring-afl --fandango 100
python3 parsarium.py afl run runs/svg-stdlib_getimagesizefromstring-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
