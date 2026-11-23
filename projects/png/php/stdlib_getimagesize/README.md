# php-getimagesize — PNG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png php stdlib_getimagesize
python3 parsarium.py run png php stdlib_getimagesize controls/png/red-green.png
python3 parsarium.py replay png php stdlib_getimagesize CORPUS_DIR runs/png-stdlib_getimagesize-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png php stdlib_getimagesize
python3 parsarium.py afl prepare png php stdlib_getimagesize runs/png-stdlib_getimagesize-afl --fandango 100
python3 parsarium.py afl run runs/png-stdlib_getimagesize-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
