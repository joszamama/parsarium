# ottosmops/pdftotext — PDF / PHP

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/ottosmops-pdftotext/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php ottosmops_pdftotext
python3 parsarium.py run pdf php ottosmops_pdftotext controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php ottosmops_pdftotext CORPUS_DIR runs/pdf-ottosmops_pdftotext-replay
python3 parsarium.py afl build pdf php ottosmops_pdftotext
python3 parsarium.py afl prepare pdf php ottosmops_pdftotext runs/pdf-ottosmops_pdftotext-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
