# unpdf — PDF / Rust

Pinned release: `0.54.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/unpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust unpdf
python3 parsarium.py run pdf rust unpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust unpdf CORPUS_DIR runs/pdf-unpdf-replay
python3 parsarium.py afl build pdf rust unpdf
python3 parsarium.py afl prepare pdf rust unpdf runs/pdf-unpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
