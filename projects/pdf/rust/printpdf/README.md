# printpdf — PDF / Rust

Pinned release: `0.12.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/printpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust printpdf
python3 parsarium.py run pdf rust printpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust printpdf CORPUS_DIR runs/pdf-printpdf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf rust printpdf
python3 parsarium.py afl prepare pdf rust printpdf runs/pdf-printpdf-afl --fandango 100
python3 parsarium.py afl run runs/pdf-printpdf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
