# printpdf — PDF / Rust

Pinned release: `0.12.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/printpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust printpdf
python3 parsarium.py run pdf rust printpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust printpdf CORPUS_DIR runs/pdf-printpdf-replay
python3 parsarium.py afl build pdf rust printpdf
python3 parsarium.py afl prepare pdf rust printpdf runs/pdf-printpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
