# pdfplumber — PDF / Rust

Pinned release: `0.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfplumber/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfplumber
python3 parsarium.py run pdf rust pdfplumber controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfplumber CORPUS_DIR runs/pdf-pdfplumber-replay
python3 parsarium.py afl build pdf rust pdfplumber
python3 parsarium.py afl prepare pdf rust pdfplumber runs/pdf-pdfplumber-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
