# pdf-cos — PDF / Rust

Pinned release: `0.39.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf-cos/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf_cos
python3 parsarium.py run pdf rust pdf_cos controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf_cos CORPUS_DIR runs/pdf-pdf_cos-replay
python3 parsarium.py afl build pdf rust pdf_cos
python3 parsarium.py afl prepare pdf rust pdf_cos runs/pdf-pdf_cos-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
