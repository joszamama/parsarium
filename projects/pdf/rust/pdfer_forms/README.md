# pdfer_forms — PDF / Rust

Pinned release: `0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/rust/pdfer-forms/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf rust pdfer_forms
python3 parsarium.py run pdf rust pdfer_forms controls/pdf/one-page.pdf
python3 parsarium.py replay pdf rust pdfer_forms CORPUS_DIR runs/pdf-pdfer_forms-replay
python3 parsarium.py afl build pdf rust pdfer_forms
python3 parsarium.py afl prepare pdf rust pdfer_forms runs/pdf-pdfer_forms-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
