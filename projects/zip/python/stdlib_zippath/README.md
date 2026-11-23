# zipfile.Path — ZIP / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip python stdlib_zippath
python3 parsarium.py run zip python stdlib_zippath controls/zip/hello.zip
python3 parsarium.py replay zip python stdlib_zippath CORPUS_DIR runs/zip-stdlib_zippath-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip python stdlib_zippath
python3 parsarium.py afl prepare zip python stdlib_zippath runs/zip-stdlib_zippath-afl --fandango 100
python3 parsarium.py afl run runs/zip-stdlib_zippath-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
