# pdf-inspector — PDF / Rust

Pinned release: `1.25.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf-inspector/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf_inspector
python3 parsarium.py run pdf rust pdf_inspector controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf_inspector CORPUS_DIR runs/pdf-pdf_inspector-replay
python3 parsarium.py afl build pdf rust pdf_inspector
python3 parsarium.py afl prepare pdf rust pdf_inspector runs/pdf-pdf_inspector-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
