# zpdf-document — PDF / Rust

Pinned release: `0.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/zpdf-document/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust zpdf_document
python3 parsarium.py run pdf rust zpdf_document controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust zpdf_document CORPUS_DIR runs/pdf-zpdf_document-replay
python3 parsarium.py afl build pdf rust zpdf_document
python3 parsarium.py afl prepare pdf rust zpdf_document runs/pdf-zpdf_document-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
