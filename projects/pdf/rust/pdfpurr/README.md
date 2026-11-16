# pdfpurr — PDF / Rust

Pinned release: `0.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfpurr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfpurr
python3 parsarium.py run pdf rust pdfpurr controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfpurr CORPUS_DIR runs/pdf-pdfpurr-replay
python3 parsarium.py afl build pdf rust pdfpurr
python3 parsarium.py afl prepare pdf rust pdfpurr runs/pdf-pdfpurr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
