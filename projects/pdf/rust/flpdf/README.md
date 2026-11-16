# flpdf — PDF / Rust

Pinned release: `0.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/flpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust flpdf
python3 parsarium.py run pdf rust flpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust flpdf CORPUS_DIR runs/pdf-flpdf-replay
python3 parsarium.py afl build pdf rust flpdf
python3 parsarium.py afl prepare pdf rust flpdf runs/pdf-flpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
