# jurosh/pdf-merge — PDF / PHP

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/jurosh-pdf-merge/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php jurosh_pdf_merge
python3 parsarium.py run pdf php jurosh_pdf_merge controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php jurosh_pdf_merge CORPUS_DIR runs/pdf-jurosh_pdf_merge-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf php jurosh_pdf_merge
python3 parsarium.py afl prepare pdf php jurosh_pdf_merge runs/pdf-jurosh_pdf_merge-afl --fandango 100
python3 parsarium.py afl run runs/pdf-jurosh_pdf_merge-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
