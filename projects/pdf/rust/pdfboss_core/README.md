# pdfboss-core — PDF / Rust

Pinned release: `2.16.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfboss-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfboss_core
python3 parsarium.py run pdf rust pdfboss_core controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfboss_core CORPUS_DIR runs/pdf-pdfboss_core-replay
python3 parsarium.py afl build pdf rust pdfboss_core
python3 parsarium.py afl prepare pdf rust pdfboss_core runs/pdf-pdfboss_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
