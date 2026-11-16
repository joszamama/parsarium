# pdf-extract — PDF / Rust

Pinned release: `0.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf-extract/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf_extract
python3 parsarium.py run pdf rust pdf_extract controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf_extract CORPUS_DIR runs/pdf-pdf_extract-replay
python3 parsarium.py afl build pdf rust pdf_extract
python3 parsarium.py afl prepare pdf rust pdf_extract runs/pdf-pdf_extract-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
