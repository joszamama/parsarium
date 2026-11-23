# spatie/pdf-to-text — PDF / PHP

Pinned release: `1.55.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/spatie-pdf-to-text/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php spatie_pdf_to_text
python3 parsarium.py run pdf php spatie_pdf_to_text controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php spatie_pdf_to_text CORPUS_DIR runs/pdf-spatie_pdf_to_text-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf php spatie_pdf_to_text
python3 parsarium.py afl prepare pdf php spatie_pdf_to_text runs/pdf-spatie_pdf_to_text-afl --fandango 100
python3 parsarium.py afl run runs/pdf-spatie_pdf_to_text-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
