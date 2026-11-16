# pdfsink-rs — PDF / Rust

Pinned release: `0.2.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfsink-rs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfsink_rs
python3 parsarium.py run pdf rust pdfsink_rs controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfsink_rs CORPUS_DIR runs/pdf-pdfsink_rs-replay
python3 parsarium.py afl build pdf rust pdfsink_rs
python3 parsarium.py afl prepare pdf rust pdfsink_rs runs/pdf-pdfsink_rs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
