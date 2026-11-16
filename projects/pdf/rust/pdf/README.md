# pdf — PDF / Rust

Pinned release: `0.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdf
python3 parsarium.py run pdf rust pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdf CORPUS_DIR runs/pdf-pdf-replay
python3 parsarium.py afl build pdf rust pdf
python3 parsarium.py afl prepare pdf rust pdf runs/pdf-pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
