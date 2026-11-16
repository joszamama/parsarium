# oxidize-pdf — PDF / Rust

Pinned release: `5.5.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/oxidize-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust oxidize_pdf
python3 parsarium.py run pdf rust oxidize_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust oxidize_pdf CORPUS_DIR runs/pdf-oxidize_pdf-replay
python3 parsarium.py afl build pdf rust oxidize_pdf
python3 parsarium.py afl prepare pdf rust oxidize_pdf runs/pdf-oxidize_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
