# pdf-syntax — PDF / Rust

Pinned release: `0.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf-syntax/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf_syntax
python3 parsarium.py run pdf rust pdf_syntax controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf_syntax CORPUS_DIR runs/pdf-pdf_syntax-replay
python3 parsarium.py afl build pdf rust pdf_syntax
python3 parsarium.py afl prepare pdf rust pdf_syntax runs/pdf-pdf_syntax-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
