# pypdf — PDF / Python

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pypdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pypdf
python3 parsarium.py run pdf python pypdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pypdf CORPUS_DIR runs/pdf-pypdf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf python pypdf
python3 parsarium.py afl prepare pdf python pypdf runs/pdf-pypdf-afl --fandango 100
python3 parsarium.py afl run runs/pdf-pypdf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
