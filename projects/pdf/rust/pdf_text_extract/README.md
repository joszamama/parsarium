# pdf-text-extract — PDF / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf-text-extract/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf_text_extract
python3 parsarium.py run pdf rust pdf_text_extract controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf_text_extract CORPUS_DIR runs/pdf-pdf_text_extract-replay
python3 parsarium.py afl build pdf rust pdf_text_extract
python3 parsarium.py afl prepare pdf rust pdf_text_extract runs/pdf-pdf_text_extract-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
