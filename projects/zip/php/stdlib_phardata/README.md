# php-phardata — ZIP / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip php stdlib_phardata
python3 parsarium.py run zip php stdlib_phardata controls/zip/hello.zip
python3 parsarium.py replay zip php stdlib_phardata CORPUS_DIR runs/zip-stdlib_phardata-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip php stdlib_phardata
python3 parsarium.py afl prepare zip php stdlib_phardata runs/zip-stdlib_phardata-afl --fandango 100
python3 parsarium.py afl run runs/zip-stdlib_phardata-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
