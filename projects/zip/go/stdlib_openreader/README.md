# archive/zip.OpenReader(path); File.Open() — ZIP / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip go stdlib_openreader
python3 parsarium.py run zip go stdlib_openreader controls/zip/hello.zip
python3 parsarium.py replay zip go stdlib_openreader CORPUS_DIR runs/zip-stdlib_openreader-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip go stdlib_openreader
python3 parsarium.py afl prepare zip go stdlib_openreader runs/zip-stdlib_openreader-afl --fandango 100
python3 parsarium.py afl run runs/zip-stdlib_openreader-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
