# pdfrum — PDF / Rust

Pinned release: `0.5.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfrum/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfrum
python3 parsarium.py run pdf rust pdfrum controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfrum CORPUS_DIR runs/pdf-pdfrum-replay
python3 parsarium.py afl build pdf rust pdfrum
python3 parsarium.py afl prepare pdf rust pdfrum runs/pdf-pdfrum-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
