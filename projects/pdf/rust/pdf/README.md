# pdf — PDF / Rust

Pinned release: `0.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf
python3 parsarium.py run pdf rust pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf CORPUS_DIR runs/pdf-pdf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf rust pdf
python3 parsarium.py afl prepare pdf rust pdf runs/pdf-pdf-afl --fandango 100
python3 parsarium.py afl run runs/pdf-pdf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
