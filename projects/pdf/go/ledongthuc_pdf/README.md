# github.com/ledongthuc/pdf — PDF / Go

Pinned release: `v0.0.0-20261020125853-5e46805f718e`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-ledongthuc-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go ledongthuc_pdf
python3 parsarium.py run pdf go ledongthuc_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go ledongthuc_pdf CORPUS_DIR runs/pdf-ledongthuc_pdf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf go ledongthuc_pdf
python3 parsarium.py afl prepare pdf go ledongthuc_pdf runs/pdf-ledongthuc_pdf-afl --fandango 100
python3 parsarium.py afl run runs/pdf-ledongthuc_pdf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
