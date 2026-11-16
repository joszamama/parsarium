# pdfplumber — PDF / Rust

- **Pinned release:** `0.4.1`
- **License:** Apache-2.0
- **Parsed scope:** PDF page model
- **Underlying family:** lopdf + pdfplumber-parse
- **Local input API:** `Pdf::open_path(path, None).page_count()`
- **Documentation:** [API reference](<https://docs.rs/pdfplumber/0.4.1/pdfplumber/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdfplumber/README.md)

```sh
python3 parsarium.py build pdf rust pdfplumber
python3 parsarium.py run pdf rust pdfplumber controls/pdf/one-page.pdf
```
