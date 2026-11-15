# lopdf — PDF / Rust

Pinned release: `0.47.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/lopdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust lopdf
python3 parsarium.py run pdf rust lopdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust lopdf CORPUS_DIR runs/pdf-lopdf-replay
python3 parsarium.py afl build pdf rust lopdf
python3 parsarium.py afl prepare pdf rust lopdf runs/pdf-lopdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
